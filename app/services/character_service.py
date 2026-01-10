from app.models import db, Character, UserProgress


class CharacterService:
    @staticmethod
    def get_all_characters() -> list:
        """모든 캐릭터 조회"""
        characters = Character.query.all()
        return [char.to_dict() for char in characters]

    @staticmethod
    def get_character_by_id(char_id: int, user_id: int = None) -> dict:
        """캐릭터 상세 조회"""
        character = Character.query.get(char_id)

        if not character:
            raise ValueError('캐릭터를 찾을 수 없습니다.')

        result = character.to_dict(include_full=True)

        # 사용자 진행 상태도 함께 반환
        if user_id:
            progress = UserProgress.query.filter_by(
                user_id=user_id,
                char_name=character.name
            ).first()

            result['user_progress'] = progress.to_dict() if progress else None

        return result

    @staticmethod
    def get_character_by_name(char_name: str) -> Character:
        """이름으로 캐릭터 조회"""
        character = Character.query.filter_by(name=char_name).first()

        if not character:
            raise ValueError(f'캐릭터 "{char_name}"를 찾을 수 없습니다.')

        return character