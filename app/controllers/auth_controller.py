from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.auth_service import AuthService
from app.utils.auth import token_required
import traceback # <-- 파일 맨 위에 추가

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입
    ---
    tags:
      - 인증 (Auth)
    summary: 회원가입
    description: 새로운 사용자를 등록합니다.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - nickname
            - password
          properties:
            username:
              type: string
              example: testuser
              description: 로그인 아이디 (3-20자)
            nickname:
              type: string
              example: 테스트유저
              description: 게임 내 닉네임 (2자 이상)
            password:
              type: string
              example: password123
              description: 비밀번호 (6자 이상)
    responses:
      201:
        description: 회원가입 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: 회원가입이 완료되었습니다.
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                username:
                  type: string
                  example: testuser
                nickname:
                  type: string
                  example: 테스트유저
      400:
        description: 유효성 검사 실패
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: 이미 존재하는 아이디입니다.
    """
    try:
        data = request.get_json()

        username = data.get('username')
        nickname = data.get('nickname')
        password = data.get('password')

        if not username or not nickname or not password:
            return jsonify({
                'success': False,
                'message': '모든 필드를 입력해주세요.'
            }), 400

        user = AuthService.register(username, nickname, password)

        return jsonify({
            'success': True,
            'message': '회원가입이 완료되었습니다.',
            'data': user
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

    except Exception as e:
        print("\n\n🔥 진짜 에러 내용은 아래와 같습니다 🔥")
        traceback.print_exc()  # <--- 에러의 상세 위치와 원인을 출력해줍니다.
        print("🔥 ----------------------------- 🔥\n\n")

        return jsonify({'message': '서버 에러'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """로그인
    ---
    tags:
      - 인증 (Auth)
    summary: 로그인
    description: 사용자 인증 후 JWT 토큰을 발급합니다.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: testuser
              description: 로그인 아이디
            password:
              type: string
              example: password123
              description: 비밀번호
    responses:
      200:
        description: 로그인 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: 로그인에 성공했습니다.
            data:
              type: object
              properties:
                token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                  description: JWT 인증 토큰
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    username:
                      type: string
                      example: testuser
                    nickname:
                      type: string
                      example: 테스트유저
      401:
        description: 인증 실패
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: 아이디 또는 비밀번호가 일치하지 않습니다.
    """
    try:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'success': False,
                'message': '아이디와 비밀번호를 입력해주세요.'
            }), 400

        result = AuthService.login(username, password)

        return jsonify({
            'success': True,
            'message': '로그인에 성공했습니다.',
            'data': result
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """로그아웃
    ---
    tags:
      - 인증 (Auth)
    summary: 로그아웃
    description: 현재 사용 중인 토큰을 블랙리스트에 등록하여 무효화합니다.
    security:
      - Bearer: []
    responses:
      200:
        description: 로그아웃 성공
    """
    token = request.headers.get('Authorization').split(' ')[1]
    AuthService.logout(token)

    return jsonify({
        'success': True,
        'message': '성공적으로 로그아웃되었습니다.'
    }), 200