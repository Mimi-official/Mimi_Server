from flask import Blueprint, request, jsonify
from app.services.character_service import CharacterService
from app.utils.auth import decode_token

char_bp = Blueprint('character', __name__, url_prefix='/api/characters')


@char_bp.route('/', methods=['GET'])
def get_all_characters():
    """모든 캐릭터 조회"""
    try:
        characters = CharacterService.get_all_characters()

        return jsonify({
            'success': True,
            'data': characters
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500


@char_bp.route('/<int:char_id>', methods=['GET'])
def get_character(char_id):
    """캐릭터 상세 조회"""
    try:
        # 선택적 인증 - 토큰이 있으면 사용자 정보도 함께
        user_id = None
        token = request.headers.get('Authorization')

        if token:
            try:
                token = token.split(' ')[1]
                payload = decode_token(token)
                user_id = payload.get('user_id')
            except:
                pass  # 토큰이 유효하지 않아도 캐릭터 정보는 볼 수 있음

        character = CharacterService.get_character_by_id(char_id, user_id)

        return jsonify({
            'success': True,
            'data': character
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500