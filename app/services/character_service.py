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
    def get_ending(user_id: int, char_name: str, affinity: int, has_hidden: bool) -> dict:
        """엔딩 결정 및 DB 업데이트 로직"""

        # 1. 캐릭터 조회
        character = Character.query.filter_by(name=char_name).first()
        if not character:
            raise ValueError("캐릭터를 찾을 수 없습니다.")

        # 2. 엔딩 분기 로직
        ending_type = 'normal'
        title = ""
        content = ""
        img_url = ""

        if has_hidden:
            ending_type = 'hidden'
            title = character.hidden_end_title
            content = character.hidden_end_content
            img_url = character.hidden_end_img
        elif affinity >= 90:
            ending_type = 'success'
            title = character.success_end_title
            content = character.success_end_content
            img_url = character.success_end_img
        elif affinity <= 20:
            ending_type = 'fail'
            title = character.fail_end_title
            content = character.fail_end_content
            img_url = character.fail_end_img
        else:
            # 노말/기타 (실패 메시지 혹은 별도 노말 메시지 사용)
            ending_type = 'normal'
            title = "이야기가 마무리되었습니다."
            content = "특별한 결말에는 도달하지 못했지만, 즐거운 대화였습니다."
            img_url = character.profile_img_url

            # 3. DB 업데이트 (게임 종료 처리)
        progress = UserProgress.query.filter_by(user_id=user_id, char_name=char_name).first()
        if progress:
            progress.is_ended = True
            progress.affinity = affinity
            db.session.commit()

        # 4. 결과 반환
        return {
            'ending_type': ending_type,
            'title': title,
            'content': content,
            'image_url': img_url
        }