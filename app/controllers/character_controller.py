from flask import Blueprint, request, jsonify
from app.services.character_service import CharacterService
from app.utils.auth import decode_token, token_required

char_bp = Blueprint('character', __name__, url_prefix='/api/characters')


@char_bp.route('/', methods=['GET'])
def get_all_characters():
    """캐릭터 목록 조회
    ---
    tags:
      - 캐릭터 (Characters)
    summary: 전체 캐릭터 목록 조회
    description: 모든 캐릭터의 기본 정보(이름, 타이틀, 해시태그 등)를 조회합니다.
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
                    example: "이준호"
                  title:
                    type: string
                    example: "까칠한 직장 상사"
                  hashtags:
                    type: string
                    example: "#츤데레 #워커홀릭"
                  profile_img_url:
                    type: string
                    example: "https://example.com/img/profile.jpg"
      500:
        description: 서버 에러
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
    description: |
      특정 캐릭터의 상세 정보를 조회합니다.
      로그인한 경우(쿠키 또는 헤더에 토큰 존재 시), 사용자의 진행 상황(호감도 등)도 함께 반환됩니다.
    parameters:
      - in: path
        name: char_id
        type: integer
        required: true
        description: 캐릭터 ID
    responses:
      200:
        description: 조회 성공
      404:
        description: 캐릭터 없음
    """
    try:
        user_id = None
        token = None

        # -----------------------------------------------------------
        # 1. 쿠키에서 토큰 찾기 (우선순위 1)
        # -----------------------------------------------------------
        if 'access_token' in request.cookies:
            token = request.cookies.get('access_token')

        # -----------------------------------------------------------
        # 2. 쿠키에 없으면 헤더에서 찾기 (우선순위 2 - 백업용)
        # -----------------------------------------------------------
        if not token and request.headers.get('Authorization'):
            auth_header = request.headers.get('Authorization')
            if "Bearer" in auth_header:
                token = auth_header.split(' ')[1]
            else:
                token = auth_header

        # -----------------------------------------------------------
        # 3. 토큰이 있으면 유저 ID 추출 시도 (에러나면 무시)
        # -----------------------------------------------------------
        if token:
            try:
                payload = decode_token(token)
                user_id = payload.get('user_id')
            except Exception:
                # 토큰이 만료되었거나 잘못된 경우 -> 그냥 비로그인 유저로 취급
                pass

        # 4. 서비스 호출 (user_id가 있으면 진행상황 포함, 없으면 기본 정보만)
        character = CharacterService.get_character_by_id(char_id, user_id)

        return jsonify({
            'success': True,
            'data': character
        }), 200

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': '서버 오류가 발생했습니다.'}), 500


@char_bp.route('/ending', methods=['POST'])
@token_required
def get_ending(current_user):
    """엔딩 결과 조회 및 게임 종료
    ---
    tags:
      - 캐릭터 (Characters)
    summary: 엔딩 결정 및 게임 종료 처리
    description: |
      호감도와 히든 선택 여부를 바탕으로 엔딩(성공/실패/히든)을 결정합니다.
      이 API가 호출되면 DB의 사용자 진행 상태(UserProgress)가 '종료(is_ended=True)'로 변경됩니다.
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - character_name
            - affinity
          properties:
            character_name:
              type: string
              example: "이준호"
              description: 캐릭터 이름
            affinity:
              type: integer
              example: 95
              description: 최종 호감도 점수
    """
    try:
        data = request.get_json()

        # 데이터 추출
        char_name = data.get('character_name')
        if not char_name:
            return jsonify({'success': False, 'message': '캐릭터 이름이 필요합니다.'}), 400

        user_id = current_user['user_id']

        # 서비스 호출
        result = CharacterService.get_ending(user_id, char_name)

        return jsonify({
            'success': True,
            'data': {
                'ending_type': result['ending_type'],
                'title': result['title'],
                'content': result['content'],
                'image_url': result['image_url']
            }
        }), 200

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except Exception as e:
        print(f"🔥 엔딩 에러: {str(e)}")
        return jsonify({'success': False, 'message': '엔딩 처리에 실패했습니다.'}), 500