from flask import Blueprint, request, jsonify, make_response  # make_response 추가
from app.services.auth_service import AuthService
from app.utils.auth import token_required
import traceback

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
        print("\n\n🔥 회원가입 에러 🔥")
        traceback.print_exc()
        print("🔥 ----------------------------- 🔥\n\n")

        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500

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

        # 1. 서비스 로직 수행
        result = AuthService.login(username, password)
        token = result['token'] # 토큰 분리

        # 2. 응답 객체 생성 (JSON 데이터 포함)
        response = make_response(jsonify({
            'success': True,
            'message': '로그인에 성공했습니다.',
            'data': result
        }))

        is_production = os.getenv('FLASK_ENV') == 'production'

        if is_production:
            # 배포 환경 (Vercel): HTTPS 필수, Cross-Site 허용
            cookie_secure = True
            cookie_samesite = 'None'
        else:
            # 로컬 환경: HTTP 허용, 같은 도메인(Lax)
            cookie_secure = False
            cookie_samesite = 'Lax'

        # 3. 쿠키 설정 (핵심!)
        response.set_cookie(
            'access_token',     # 쿠키 이름
            token,              # 토큰 값
            httponly=True,      # 자바스크립트 접근 불가 (보안)
            secure=cookie_secure,       # 로컬(HTTP) 개발환경이면 False, 배포(HTTPS)는 True
            samesite=cookie_samesite,     # CSRF 보호용 (Lax 권장)
            max_age=60*60*24*14  ,
            path='/',# 1일 (24시간)
        )

        return response, 200

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 401
    except Exception as e:
        print("\n\n🔥 로그인 에러 🔥")
        traceback.print_exc()
        return jsonify({'success': False, 'message': '서버 오류가 발생했습니다.'}), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """로그아웃
    ---
    tags:
      - 인증 (Auth)
    summary: 로그아웃
    description: |
      서버 측 토큰을 블랙리스트에 등록하고, 클라이언트의 쿠키를 만료시킵니다.
      (Cookie의 access_token 필요)
    security:
      - Bearer: []
    responses:
      200:
        description: 로그아웃 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: 로그아웃되었습니다.
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: 오류 발생
    """
    try:
        # 쿠키 또는 헤더에서 토큰 추출 (블랙리스트 추가용)
        token = request.cookies.get('access_token')

        # 서비스 로그아웃 처리 (토큰 블랙리스트 등)
        if token:
            AuthService.logout(token)

        # 1. 응답 객체 생성
        response = make_response(jsonify({
            'success': True,
            'message': '로그아웃되었습니다.'
        }))

        is_production = os.getenv('FLASK_ENV') == 'production'

        if is_production:
            # 배포 환경 (Vercel): HTTPS 필수, Cross-Site 허용
            cookie_secure = True
            cookie_samesite = 'None'
        else:
            # 로컬 환경: HTTP 허용, 같은 도메인(Lax)
            cookie_secure = False
            cookie_samesite = 'Lax'

        # 2. 쿠키 삭제 (만료시간을 과거로 설정하여 브라우저가 지우게 함)
        response.delete_cookie('access_token', path='/', samesite=cookie_samesite, secure=cookie_secure)

        return response, 200

    except Exception as e:
        print(f"\n\n🔥 로그아웃 에러 🔥\n{str(e)}")
        return jsonify({'success': False, 'message': '오류 발생'}), 500


@auth_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_account(current_user):
    """회원 탈퇴
    ---
    tags:
      - 인증 (Auth)
    summary: 회원 탈퇴
    description: |
      비밀번호 확인 후 계정을 영구 삭제하고 로그아웃 처리합니다.
      (Cookie의 access_token 필요)
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - password
          properties:
            password:
              type: string
              example: password123
              description: 본인 확인용 비밀번호
    responses:
      200:
        description: 탈퇴 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: 회원 탈퇴가 완료되었습니다.
      400:
        description: 비밀번호 불일치
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: 비밀번호가 일치하지 않습니다.
    """
    try:
        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({'success': False, 'message': '비밀번호를 입력해주세요.'}), 400

        user_id = current_user['user_id']
        result = AuthService.delete_account(user_id, password)

        # 회원 탈퇴 후에도 쿠키를 지워야 함
        response = make_response(jsonify({
            'success': True,
            'message': result['message']
        }))

        is_production = os.getenv('FLASK_ENV') == 'production'

        if is_production:
            # 배포 환경 (Vercel): HTTPS 필수, Cross-Site 허용
            cookie_secure = True
            cookie_samesite = 'None'
        else:
            # 로컬 환경: HTTP 허용, 같은 도메인(Lax)
            cookie_secure = False
            cookie_samesite = 'Lax'

        response.delete_cookie('access_token', path='/', samesite=cookie_samesite, secure=cookie_secure)

        return response, 200

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        print("\n\n🔥 회원 탈퇴 에러 🔥")
        traceback.print_exc()
        return jsonify({'success': False, 'message': '서버 오류'}), 500


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me(current_user):
    """내 정보 조회
    ---
    tags:
      - 인증 (Auth)
    summary: 현재 로그인한 사용자 정보 조회
    description: |
      Access Token을 기반으로 현재 사용자의 최신 프로필 정보를 반환합니다.
      (Cookie의 access_token 필요)
    security:
      - Bearer: []
    responses:
      200:
        description: 조회 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: 사용자 정보를 조회했습니다.
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
                created_at:
                  type: string
                  example: "2024-05-21T10:00:00"
      404:
        description: 사용자 없음 (탈퇴 등)
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: 사용자 정보를 찾을 수 없습니다.
    """
    try:
        # token_required에서 넘겨준 user_id 추출
        user_id = current_user['user_id']

        # 서비스 호출 (DB에서 최신 정보 조회)
        user_info = AuthService.get_current_user(user_id)

        return jsonify({
            'success': True,
            'message': '사용자 정보를 조회했습니다.',
            'data': user_info
        }), 200

    except ValueError as e:
        # 사용자가 DB에 없는 경우 (토큰은 유효하나 강제 탈퇴 당한 경우 등)
        return jsonify({'success': False, 'message': str(e)}), 404

    except Exception as e:
        print("\n\n🔥 내 정보 조회 에러 🔥")
        traceback.print_exc()
        return jsonify({'success': False, 'message': '서버 오류가 발생했습니다.'}), 500