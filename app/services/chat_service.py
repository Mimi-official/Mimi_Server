from app.models import db, UserProgress, ChatLog, CharacterEvent
from app.services.character_service import CharacterService
from app.utils.gemini import gemini_service
from app.utils.affinity import determine_ending, should_trigger_ending


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
                is_ended=False
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
    def send_choice(user_id: int, char_name: str, choice_index: int) -> dict:
        """선택지 전송 및 AI 응답 생성"""
        # 캐릭터 정보 가져오기
        character = CharacterService.get_character_by_name(char_name)

        # 진행 상태 가져오기
        progress = ChatService.get_or_create_progress(user_id, char_name)

        if progress.is_ended:
            raise ValueError('이미 완료된 스토리입니다.')

        # 현재 이벤트 가져오기
        event = CharacterEvent.query.filter_by(
            char_id=character.id,
            event_order=progress.current_step
        ).first()

        if not event:
            raise ValueError('이벤트를 찾을 수 없습니다.')

        # 선택지 검증 및 점수 가져오기
        choices = event.get_choices()
        selected_choice = next((c for c in choices if c['index'] == choice_index), None)

        if not selected_choice:
            raise ValueError('유효하지 않은 선택지입니다.')

        choice_text = selected_choice['text']
        score_change = selected_choice['score']

        # 호감도 업데이트
        new_affinity = progress.affinity + score_change

        # 사용자 선택 로그 저장
        user_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='user',
            message=choice_text
        )
        db.session.add(user_log)

        # 채팅 기록 가져오기
        chat_history = ChatService.get_chat_history(user_id, char_name, limit=5)

        # AI 응답 생성
        prompt = gemini_service.build_character_prompt(
            character,
            choice_text,
            new_affinity,
            chat_history
        )
        ai_response = gemini_service.generate_response(prompt)

        # AI 응답 로그 저장
        ai_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='ai',
            message=ai_response
        )
        db.session.add(ai_log)

        # 다음 단계로 진행
        progress.affinity = new_affinity
        progress.current_step += 1

        # 엔딩 체크
        ending_data = None
        has_hidden = score_change >= 30  # 히든 선택지는 점수가 30 이상

        if should_trigger_ending(new_affinity, progress.current_step):
            ending_type = determine_ending(new_affinity, has_hidden)

            if ending_type:
                ending_data = ChatService._generate_ending(
                    character,
                    ending_type,
                    new_affinity,
                    user_id,
                    char_name
                )
                progress.is_ended = True

        db.session.commit()

        return {
            'ai_response': ai_response,
            'affinity': new_affinity,
            'affinity_change': score_change,
            'current_step': progress.current_step,
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

        # AI 엔딩 메시지 생성
        prompt = gemini_service.build_ending_prompt(
            character,
            ending_info['content'],
            affinity
        )
        ending_message = gemini_service.generate_response(prompt)

        # 엔딩 로그 저장
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

        # 채팅 로그 삭제
        ChatLog.query.filter_by(
            user_id=user_id,
            char_name=char_name
        ).delete()

        # 진행 상태 초기화
        progress.affinity = 0
        progress.current_step = 1
        progress.is_ended = False

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


@staticmethod
def chat_with_character(user_id: int, char_name: str, message: str) -> dict:
    """자유 채팅 처리"""
    progress = ChatService.get_or_create_progress(user_id, char_name)
    character = CharacterService.get_character_by_name(char_name)

    # 1. 유저 메시지 저장
    user_log = ChatLog(user_id=user_id, char_name=char_name, sender='user', message=message)
    db.session.add(user_log)

    # 2. Gemini에게 응답 요청 (컨텍스트 포함)
    chat_history = ChatService.get_chat_history(user_id, char_name, limit=10)
    gemini = gemini_service()
    ai_response_text = gemini.generate_chat_response(character, chat_history, message)

    # 3. AI 응답 저장
    ai_log = ChatLog(user_id=user_id, char_name=char_name, sender='ai', message=ai_response_text)
    db.session.add(ai_log)

    # 4. 턴 수 증가 및 이벤트 트리거 체크
    progress.turn_count += 1

    # 예: 3턴마다 이벤트 발생 (또는 호감도 기반 로직 추가 가능)
    trigger_event = False
    if progress.turn_count >= 3 and progress.is_chatting and not progress.is_ended:
        # 다음 이벤트가 존재하는지 확인
        next_event = CharacterEvent.query.filter_by(
            char_id=character.id, event_order=progress.current_step
        ).first()

        if next_event:
            progress.is_chatting = False  # 채팅 중단, 선택지 모드 진입
            trigger_event = True
            progress.turn_count = 0  # 턴 리셋

    db.session.commit()

    return {
        'type': 'chat',
        'response': ai_response_text,
        'trigger_event': trigger_event,  # 프론트에서 이 값이 True면 /event API를 호출하여 선택지 렌더링
        'affinity': progress.affinity
    }


@staticmethod
def handle_choice(user_id: int, char_name: str, choice_index: int) -> dict:
    """선택지 처리"""
    progress = ChatService.get_or_create_progress(user_id, char_name)
    character = CharacterService.get_character_by_name(char_name)

    # 현재 이벤트 가져오기
    event = CharacterEvent.query.filter_by(
        char_id=character.id, event_order=progress.current_step
    ).first()

    if not event:
        raise ValueError("진행할 이벤트가 없습니다.")

    # 선택지에 따른 점수 계산 (1, 2, 3번 선택지)
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

    # 호감도 반영
    progress.affinity += score

    # 유저가 선택한 내용을 로그로 저장 (선택지도 대화의 일부로 취급)
    log = ChatLog(user_id=user_id, char_name=char_name, sender='user', message=f"[선택] {choice_text}")
    db.session.add(log)

    # Gemini에게 선택 결과에 대한 짧은 리액션 요청
    gemini = gemini_service()
    reaction = gemini.generate_reaction(character, choice_text, score)
    ai_log = ChatLog(user_id=user_id, char_name=char_name, sender='ai', message=reaction)
    db.session.add(ai_log)

    # 상태 업데이트
    progress.current_step += 1
    progress.is_chatting = True  # 다시 채팅 모드로 복귀

    # 엔딩 체크
    ending = determine_ending(progress.affinity, score >= 30)  # 히든 조건(30점 이상) 체크
    if progress.current_step > 3 or ending:  # 3번 이벤트 후 또는 엔딩 조건 충족 시
        progress.is_ended = True

    db.session.commit()

    return {
        'type': 'choice_result',
        'response': reaction,
        'affinity': progress.affinity,
        'is_ended': progress.is_ended,
        'ending': ending if progress.is_ended else None
    }