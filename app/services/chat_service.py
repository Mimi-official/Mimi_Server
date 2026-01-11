from app.models import db, UserProgress, ChatLog, CharacterEvent, Character
from app.services.character_service import CharacterService
from app.utils.gemini import gemini_service
from app.utils.affinity import determine_ending, should_trigger_ending
from sqlalchemy import and_


class ChatService:
    @staticmethod
    def get_or_create_progress(user_id: int, char_name: str) -> UserProgress:
        """진행 상태 조회 또는 생성"""
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            char_name=char_name
        ).first()

        if not progress:
            progress = UserProgress(
                user_id=user_id,
                char_name=char_name,
                affinity=0,
                current_step=1,
                turn_count=0,
                is_ended=False,
                is_chatting=True
            )
            db.session.add(progress)
            db.session.commit()

        return progress

    @staticmethod
    def get_chat_history(user_id: int, char_name: str, limit: int = 10) -> list:
        """채팅 기록 조회"""
        logs = ChatLog.query.filter_by(
            user_id=user_id,
            char_name=char_name
        ).order_by(ChatLog.created_at.asc()).limit(limit).all()

        return [log.to_dict() for log in logs]

    @staticmethod
    def get_user_chat_list(user_id: int) -> list:
        """사용자의 대화 목록 조회 (캐릭터별 마지막 대화 포함)"""
        progresses = UserProgress.query.filter_by(user_id=user_id).all()

        result = []

        for progress in progresses:
            character = Character.query.filter_by(name=progress.char_name).first()

            if not character:
                continue

            last_chat = ChatLog.query.filter_by(
                user_id=user_id,
                char_name=progress.char_name
            ).order_by(ChatLog.created_at.desc()).first()

            chat_item = {
                'char_id': character.id,
                'char_name': character.name,
                'profile_img_url': character.profile_img_url,
                'affinity': progress.affinity,
                'is_ended': progress.is_ended,
                'last_message': last_chat.message if last_chat else None,
                'last_sender': last_chat.sender if last_chat else None,
                'last_chat_time': last_chat.created_at.isoformat() if last_chat else None,
                'updated_at': progress.updated_at.isoformat() if progress.updated_at else None
            }

            result.append(chat_item)

        result.sort(key=lambda x: x['updated_at'] if x['updated_at'] else '', reverse=True)

        return result

    @staticmethod
    def chat_with_character(user_id: int, char_name: str, message: str) -> dict:
        """자유 채팅 처리"""
        progress = ChatService.get_or_create_progress(user_id, char_name)
        character = CharacterService.get_character_by_name(char_name)

        # 1. 사용자 메시지 저장
        user_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='user',
            message=message
        )
        db.session.add(user_log)

        # 2. AI 응답 생성
        chat_history = ChatService.get_chat_history(user_id, char_name, limit=10)

        # 프롬프트 생성 (자유 채팅용)
        prompt = gemini_service.build_chat_prompt(character, message, progress.affinity, chat_history)
        ai_response_text = gemini_service.generate_response(prompt)

        # 3. AI 응답 저장
        ai_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='ai',
            message=ai_response_text
        )
        db.session.add(ai_log)

        # 4. 턴 수 증가 및 이벤트 트리거 체크
        progress.turn_count += 1

        trigger_event = False
        if progress.turn_count >= 3 and progress.is_chatting and not progress.is_ended:
            next_event = CharacterEvent.query.filter_by(
                char_id=character.id,
                event_order=progress.current_step
            ).first()

            if next_event:
                progress.is_chatting = False
                trigger_event = True
                progress.turn_count = 0

        db.session.commit()

        return {
            'type': 'chat',
            'response': ai_response_text,
            'trigger_event': trigger_event,
            'affinity': progress.affinity
        }

    @staticmethod
    def handle_choice(user_id: int, char_name: str, choice_index: int) -> dict:
        """선택지 처리"""
        progress = ChatService.get_or_create_progress(user_id, char_name)
        character = CharacterService.get_character_by_name(char_name)

        event = CharacterEvent.query.filter_by(
            char_id=character.id,
            event_order=progress.current_step
        ).first()

        if not event:
            raise ValueError("진행할 이벤트가 없습니다.")

        # 선택지에 따른 점수 계산
        score = 0
        choice_text = ""

        if choice_index == 1:
            score = event.choice_1_score
            choice_text = event.choice_1
        elif choice_index == 2:
            score = event.choice_2_score
            choice_text = event.choice_2
        elif choice_index == 3:
            score = event.choice_3_score
            choice_text = event.choice_3
        else:
            raise ValueError("유효하지 않은 선택지입니다.")

        # 호감도 반영
        progress.affinity += score

        # 사용자 선택 로그 저장
        user_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='user',
            message=f"[선택] {choice_text}"
        )
        db.session.add(user_log)

        # AI 리액션 생성
        chat_history = ChatService.get_chat_history(user_id, char_name, limit=5)
        prompt = gemini_service.build_character_prompt(character, choice_text, progress.affinity, chat_history)
        reaction = gemini_service.generate_response(prompt)

        ai_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='ai',
            message=reaction
        )
        db.session.add(ai_log)

        # 상태 업데이트
        progress.current_step += 1
        progress.is_chatting = True

        # 엔딩 체크
        has_hidden = score >= 30
        ending = determine_ending(progress.affinity, has_hidden)
        ending_data = None

        if progress.current_step > 3 or ending:
            if ending:
                ending_data = ChatService._generate_ending(character, ending, progress.affinity, user_id, char_name)
            progress.is_ended = True

        db.session.commit()

        return {
            'type': 'choice_result',
            'response': reaction,
            'affinity': progress.affinity,
            'affinity_change': score,
            'is_ended': progress.is_ended,
            'ending': ending_data
        }

    @staticmethod
    def _generate_ending(character, ending_type: str, affinity: int, user_id: int, char_name: str) -> dict:
        """엔딩 생성"""
        ending_map = {
            'success': {
                'title': character.success_end_title,
                'content': character.success_end_content,
                'img': character.success_end_img
            },
            'fail': {
                'title': character.fail_end_title,
                'content': character.fail_end_content,
                'img': character.fail_end_img
            },
            'hidden': {
                'title': character.hidden_end_title,
                'content': character.hidden_end_content,
                'img': character.hidden_end_img
            }
        }

        ending_info = ending_map.get(ending_type)

        if not ending_info:
            return None

        prompt = gemini_service.build_ending_prompt(character, ending_info['content'], affinity)
        ending_message = gemini_service.generate_response(prompt)

        ending_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='ai',
            message=f"[{ending_info['title']}]\n\n{ending_message}\n\n{ending_info['content']}"
        )
        db.session.add(ending_log)

        return {
            'type': ending_type,
            'title': ending_info['title'],
            'content': ending_info['content'],
            'message': ending_message,
            'img': ending_info['img']
        }

    @staticmethod
    def reset_progress(user_id: int, char_name: str) -> dict:
        """진행 상태 초기화"""
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            char_name=char_name
        ).first()

        if not progress:
            raise ValueError('진행 상태를 찾을 수 없습니다.')

        ChatLog.query.filter_by(
            user_id=user_id,
            char_name=char_name
        ).delete()

        progress.affinity = 0
        progress.current_step = 1
        progress.turn_count = 0
        progress.is_ended = False
        progress.is_chatting = True

        db.session.commit()

        return {'message': '진행 상태가 초기화되었습니다.'}

    @staticmethod
    def get_current_event(user_id: int, char_name: str) -> dict:
        """현재 이벤트 및 선택지 조회"""
        character = CharacterService.get_character_by_name(char_name)
        progress = ChatService.get_or_create_progress(user_id, char_name)

        if progress.is_ended:
            return {
                'is_ended': True,
                'event': None,
                'choices': []
            }

        event = CharacterEvent.query.filter_by(
            char_id=character.id,
            event_order=progress.current_step
        ).first()

        if not event:
            return {
                'is_ended': False,
                'event': None,
                'choices': [],
                'message': '다음 이벤트가 없습니다.'
            }

        return {
            'is_ended': False,
            'event': event.to_dict(),
            'choices': event.get_choices(),
            'current_step': progress.current_step,
            'affinity': progress.affinity
        }