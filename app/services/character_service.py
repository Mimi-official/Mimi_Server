from app.models import db, Character, UserProgress


class CharacterService:
    @staticmethod
    def get_all_characters() -> list:
        """모든 캐릭터 목록 조회"""
        characters = Character.query.all()
        return [char.to_dict() for char in characters]

    @staticmethod
    def get_character_by_id(char_id: int, user_id: int = None) -> dict:
        """캐릭터 상세 조회 (로그인 시 진행도 포함)"""
        character = Character.query.get(char_id)
        if not character:
            raise ValueError("캐릭터를 찾을 수 없습니다.")

        data = character.to_dict(include_full=True)

        # 로그인한 유저라면 진행 상황 추가
        if user_id:
            progress = UserProgress.query.filter_by(user_id=user_id, char_name=character.name).first()
            if progress:
                data['user_progress'] = progress.to_dict()
            else:
                data['user_progress'] = None

        return data

    @staticmethod
    def get_ending(user_id: int, char_name: str) -> dict:
        """엔딩 결정 및 DB 업데이트 로직 (DB 조회 방식)"""

        # 1. 진행 정보(UserProgress) 먼저 조회
        progress = UserProgress.query.filter_by(user_id=user_id, char_name=char_name).first()
        if not progress:
            raise ValueError("진행 중인 대화 정보를 찾을 수 없습니다.")

        # 2. DB에서 값 가져오기
        affinity = progress.affinity

        # [중요] UserProgress 모델에 'is_hidden' 컬럼이 있어야 합니다.
        # 만약 컬럼명이 has_hidden이라면 progress.has_hidden으로 변경하세요.
        has_hidden = getattr(progress, 'has_hidden', False)

        # 3. 캐릭터 조회
        character = Character.query.filter_by(name=char_name).first()
        if not character:
            raise ValueError("캐릭터를 찾을 수 없습니다.")

        # 4. 엔딩 분기 로직
        ending_type = 'normal'
        title = ""
        content = ""
        img_url = ""

        if has_hidden:
            ending_type = '히든'
            title = character.hidden_end_title
            content = character.hidden_end_content
            img_url = character.hidden_end_img
        elif affinity >= 90:
            ending_type = '성공'
            title = character.success_end_title
            content = character.success_end_content
            img_url = character.success_end_img
        elif affinity <= 20:
            ending_type = '실패'
            title = character.fail_end_title
            content = character.fail_end_content
            img_url = character.fail_end_img
        else:
            # 노말 (조건 미달 시)
            ending_type = 'normal'
            title = "이야기가 마무리되었습니다."
            content = "특별한 결말에는 도달하지 못했지만, 즐거운 대화였습니다."
            img_url = character.profile_img_url

        # 5. DB 업데이트 (게임 종료 확정 처리)
        # 이미 progress 객체를 1번 단계에서 가져왔으므로 바로 수정하면 됩니다.
        progress.is_ended = True
        # progress.affinity = affinity # 이미 DB값과 같으므로 굳이 업데이트 안 해도 됨

        db.session.commit()

        # 6. 결과 반환
        return {
            'ending_type': ending_type,
            'title': title,
            'content': content,
            'image_url': img_url,
            'progress': progress,
        }

    @staticmethod
    def get_character_by_name(name: str):
        """이름으로 캐릭터 조회"""
        character = Character.query.filter_by(name=name).first()

        if not character:
            raise ValueError(f"'{name}'라는 캐릭터를 찾을 수 없습니다.")

        return character