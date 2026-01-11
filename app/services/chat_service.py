from app.models import db, UserProgress, ChatLog, CharacterEvent, Character
from app.services.character_service import CharacterService
from app.utils.gemini import gemini_service
from app.utils.affinity import determine_ending, should_trigger_ending
from sqlalchemy import and_

class ChatService:
    @staticmethod
    def start_chat(user_id: int, char_id: int):
        """
        채팅방 생성/초기화 및 첫 인사말 설정 (DB에 저장된 고정 대사 사용)
        """
        # 1. 캐릭터 확인
        character = Character.query.get(char_id)
        if not character:
            raise ValueError("존재하지 않는 캐릭터입니다.")

        # 2. 진행 상황(UserProgress) 초기화
        progress = UserProgress.query.filter_by(user_id=user_id, char_name=character.name).first()

        if progress:
            # 기존 기록이 있다면 초기화 (재시작)
            progress.affinity = 0
            progress.current_step = 1
            progress.turn_count = 0
            progress.is_ended = False
            progress.is_chatting = True
        else:
            # 없으면 새로 생성
            progress = UserProgress(
                user_id=user_id,
                char_name=character.name,
                affinity=0,
                current_step=1,
                turn_count=0,
                is_ended=False,
                is_chatting=True
            )
            db.session.add(progress)

        # 3. 기존 대화 기록(ChatLog) 삭제 (새 게임을 위해 전면 삭제)
        ChatLog.query.filter_by(user_id=user_id, char_name=character.name).delete()

        # 4. 캐릭터의 첫 인사말 설정 (AI 생성 X -> DB 값 사용 O)
        # Character 모델에 'first_message' 컬럼이 존재해야 합니다.
        greeting_message = character.first_message

        # 만약 DB에 first_message가 비어있을 경우를 대비한 기본값 (선택 사항)
        if not greeting_message:
            greeting_message = f"안녕? 나는 {character.name}(이)야."

        # 5. 첫 인사말을 DB에 저장
        first_log = ChatLog(
            user_id=user_id,
            char_name=character.name,
            sender='ai',
            message=greeting_message
        )
        db.session.add(first_log)

        # 6. 변경사항 커밋
        db.session.commit()

        # 7. 프론트엔드에 필요한 정보 반환
        return {
            "character_id": character.id,
            "character_name": character.name,
            "greeting": greeting_message,
            "profile_img": character.profile_img_url,
            "affinity": 0,
            "current_step": 1
        }

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
        """채팅 기록 조회 (프로필 이미지 포함)"""

        # 1. 채팅 로그 조회
        logs = ChatLog.query.filter_by(
            user_id=user_id,
            char_name=char_name
        ).order_by(ChatLog.created_at.asc()).limit(limit).all()

        # 2. 캐릭터 정보 조회 (프로필 이미지를 얻기 위해)
        character = Character.query.filter_by(name=char_name).first()
        profile_img_url = character.profile_img_url if character else None

        # 3. 결과 리스트 구성
        result = []
        for log in logs:
            log_data = log.to_dict()

            # sender가 'ai'인 경우에만 캐릭터 프로필 이미지를 넣어줍니다.
            if log.sender == 'ai':
                log_data['profile_img_url'] = profile_img_url
            else:
                # 사용자(user)인 경우 None (또는 사용자 프사가 있다면 별도 로직 추가)
                log_data['profile_img_url'] = None

            result.append(log_data)

        return result

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
                # 모델에 updated_at이 없을 경우를 대비해 예외처리
                'updated_at': getattr(progress, 'updated_at', None).isoformat() if getattr(progress, 'updated_at',
                                                                                           None) else None
            }

            result.append(chat_item)

        # 최신 대화순 정렬
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
        prompt = gemini_service.build_character_prompt(character, message, progress.affinity, chat_history)
        ai_response_text = gemini_service.generate_response(prompt)

        # 3. AI 응답 저장
        ai_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='ai',
            message=ai_response_text
        )
        db.session.add(ai_log)

        # 4. 턴 수 증가 및 호감도 상승
        progress.turn_count += 1
        progress.affinity += 5

        # [중요] DB에 먼저 반영 (호감도 업데이트 확정)
        # flush를 하면 commit 전이라도 이후 로직에서 업데이트된 affinity 값을 보장받습니다.
        db.session.flush()

        # 5. 이벤트 트리거 로직 강화
        trigger_event = False

        if progress.affinity >= 60:
            print('이벤트 시작!')
            # 다음 이벤트 조회
            next_event = CharacterEvent.query.filter_by(
                char_id=character.id,
                event_order=progress.current_step
            ).first()

            if next_event:
                # 이벤트가 존재하면 트리거 발동
                progress.is_chatting = False
                trigger_event = True
                progress.turn_count = 0
            else:
                # [디버깅용] 조건은 만족했으나 DB에 해당 단계의 이벤트가 없는 경우
                print(f"⚠️ 알림: 호감도({progress.affinity}) 또는 턴 조건을 만족했으나, "
                      f"DB에 event_order={progress.current_step}인 이벤트가 없습니다.")
                # 만약 호감도가 60이 넘었는데 이벤트가 없다면? -> 엔딩일 수도 있음 (아래 로직 추가 가능)

        # 6. 변경사항 최종 저장
        db.session.commit()

        return {
            'type': 'chat',
            'response': ai_response_text,
            'trigger_event': trigger_event,
            'affinity': progress.affinity,
            'profile_img_url': character.profile_img_url
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
        choice_response = ""

        if choice_index == 1:
            score = event.choice_1_score
            choice_text = event.choice_1
            choice_response = event.choice_1_response
        elif choice_index == 2:
            score = event.choice_2_score
            choice_text = event.choice_2
            choice_response = event.choice_2_response
        elif choice_index == 3:
            score = event.choice_3_score
            choice_text = event.choice_3
            choice_response = event.choice_3_response
            progress.has_hidden = True
        else:
            raise ValueError("유효하지 않은 선택지입니다.")

        # 호감도 반영
        progress.affinity += score

        # 사용자 선택 로그 저장
        user_log = ChatLog(
            user_id=user_id,
            char_name=char_name,
            sender='user',
            message=choice_text,
        )
        db.session.add(user_log)

        if choice_response:
            ai_log = ChatLog(
                user_id=user_id,
                char_name=char_name,
                sender='ai',
                message=choice_response,  # [중요] 컬럼명을 message로 해야 에러가 안 남
            )
            db.session.add(ai_log)

        # 이벤트 후 처리 (다음 단계로 이동)
        progress.current_step += 1
        progress.turn_count = 0  # 턴 초기화

        # 엔딩 조건 체크 (호감도나 단계 기반)
        # 여기서 바로 엔딩 여부를 알려줄 수도 있고, 다음 턴에 체크할 수도 있음
        # 일단 DB 저장
        db.session.commit()

        # 선택에 대한 AI의 반응(Optional)을 생성해서 줄 수도 있음
        # 여기서는 간단히 성공 메시지만 반환
        return {
            'type': 'choice',
            'affinity': progress.affinity,
            'message': '선택이 반영되었습니다. 대화를 계속하세요.',
            'response': choice_response,
            'profile_img_url': character.profile_img_url
        }

    @staticmethod
    def get_current_event(user_id: int, char_name: str) -> dict:
        """현재 이벤트 및 선택지 조회"""
        # (기존 코드가 파일 뒷부분에 잘린 것 같아, 안전하게 다시 구현해 둡니다)
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
            # 이벤트가 없으면 엔딩일 수도 있고, 단순히 데이터가 없는 걸 수도 있음
            return {
                'is_ended': True,
                'event': None,
                'choices': [],
                'message': '다음 이벤트가 없습니다.'
            }

        return {
            'is_ended': False,
            'event': event.to_dict(),
            'choices': event.to_dict()['choices'],
            'profile_img_url': character.profile_img_url
        }