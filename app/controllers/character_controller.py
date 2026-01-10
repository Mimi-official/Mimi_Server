from flask import Blueprint, request, jsonify
from app.services.character_service import CharacterService
from app.utils.auth import decode_token

char_bp = Blueprint('character', __name__, url_prefix='/api/characters')


@char_bp.route('/', methods=['GET'])
def get_all_characters():
    """캐릭터 목록 조회
    ---
    tags:
      - 캐릭터 (Characters)
    summary: 전체 캐릭터 목록 조회
    description: 모든 캐릭터의 기본 정보를 조회합니다.
    responses:
      200:
        description: 조회 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: 조원빈
                  title:
                    type: string
                    example: 다정한 미소 뒤에 말(馬)에 대한 광기를 숨긴 200cm의 거구 덕후
                  hashtags:
                    type: string
                    example: "#연하녀 #말덕후 #오타쿠 #서브컬쳐"
                  profile_img_url:
                    type: string
                    example: null
    """
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
    """캐릭터 상세 조회
    ---
    tags:
      - 캐릭터 (Characters)
    summary: 캐릭터 상세 정보 조회
    description: 특정 캐릭터의 상세 정보를 조회합니다. 로그인한 경우 진행 상태도 함께 조회됩니다.
    parameters:
      - in: path
        name: char_id
        type: integer
        required: true
        description: 캐릭터 ID
        example: 1
      - in: header
        name: Authorization
        type: string
        required: false
        description: JWT 토큰 (선택사항)
        example: Bearer eyJhbGc...
    responses:
      200:
        description: 조회 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: 조원빈
                title:
                  type: string
                  example: 다정한 미소 뒤에 말(馬)에 대한 광기를 숨긴 200cm의 거구 덕후
                hashtags:
                  type: string
                  example: "#연하녀 #말덕후"
                description:
                  type: string
                  example: 트랙 위의 흙먼지 속에서...
                system_prompt:
                  type: string
                  example: 당신은 조원빈입니다...
                user_progress:
                  type: object
                  nullable: true
                  properties:
                    affinity:
                      type: integer
                      example: 40
                    current_step:
                      type: integer
                      example: 2
                    is_ended:
                      type: boolean
                      example: false
      404:
        description: 캐릭터를 찾을 수 없음
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: 캐릭터를 찾을 수 없습니다.
    """
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