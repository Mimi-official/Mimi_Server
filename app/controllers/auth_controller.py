from flask import Blueprint, request, jsonify, make_response  # make_response 추가
from app.services.auth_service import AuthService
from app.utils.auth import token_required
import traceback

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ... (register 함수는 그대로 두셔도 됩니다) ...

@auth_bp.route('/login', methods=['POST'])
def login():
    """로그인 (쿠키 설정 추가됨)"""
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

        # 3. 쿠키 설정 (핵심!)
        response.set_cookie(
            'access_token',     # 쿠키 이름
            token,              # 토큰 값
            httponly=True,      # 자바스크립트 접근 불가 (보안)
            secure=False,       # 로컬(HTTP) 개발환경이면 False, 배포(HTTPS)는 True
            samesite='Lax',     # CSRF 보호용 (Lax 권장)
            max_age=60*60*24*14    # 1일 (24시간)
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
    """로그아웃 (쿠키 삭제 추가됨)"""
    try:
        # 쿠키 또는 헤더에서 토큰 추출 (블랙리스트 추가용)
        token = request.cookies.get('access_token')
        if not token:
             auth_header = request.headers.get('Authorization')
             if auth_header and ' ' in auth_header:
                 token = auth_header.split(' ')[1]

        # 서비스 로그아웃 처리 (토큰 블랙리스트 등)
        if token:
            AuthService.logout(token)

        # 1. 응답 객체 생성
        response = make_response(jsonify({
            'success': True,
            'message': '로그아웃되었습니다.'
        }))

        # 2. 쿠키 삭제 (만료시간을 과거로 설정하여 브라우저가 지우게 함)
        response.delete_cookie('access_token')

        return response, 200

    except Exception as e:
        print(f"\n\n🔥 로그아웃 에러 🔥\n{str(e)}")
        return jsonify({'success': False, 'message': '오류 발생'}), 500


@auth_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_account(current_user):
    """회원 탈퇴 (쿠키 삭제 추가됨)"""
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
        response.delete_cookie('access_token')

        return response, 200

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        print("\n\n🔥 회원 탈퇴 에러 🔥")
        traceback.print_exc()
        return jsonify({'success': False, 'message': '서버 오류'}), 500