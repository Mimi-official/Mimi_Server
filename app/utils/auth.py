import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps


# [중요] 순환 참조 방지를 위해 모델 import는 함수 안에서 하거나 필요한 경우에만 합니다.
# from app.models.token_blocklist import TokenBlocklist (필요시 주석 해제)

# ==========================================
#  헬퍼 함수들 (기존 유지)
# ==========================================

def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """비밀번호 검증"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_token(user_id: int, username: str) -> str:
    """JWT 토큰 생성"""
    expires_in_days = current_app.config.get('JWT_EXPIRES_IN_DAYS', 1)
    secret_key = current_app.config.get('JWT_SECRET', current_app.config.get('SECRET_KEY'))
    algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')

    payload = {
        'user_id': user_id,
        'username': username,
        'jti': str(uuid.uuid4()),
        'exp': datetime.utcnow() + timedelta(days=expires_in_days)
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def decode_token(token: str) -> dict:
    """JWT 토큰 디코드 (일반 함수용)"""
    secret_key = current_app.config.get('JWT_SECRET', current_app.config.get('SECRET_KEY'))
    algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('토큰이 만료되었습니다.')
    except jwt.InvalidTokenError:
        raise ValueError('유효하지 않은 토큰입니다.')


# ==========================================
#  [수정됨] 데코레이터
# ==========================================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200

        token = None

        # ---------------------------------------------------------
        # [수정 1] 쿠키에서 먼저 토큰을 찾습니다.
        # ---------------------------------------------------------
        if 'access_token' in request.cookies:
            token = request.cookies.get('access_token')
            print(f"👉 [DEBUG] 쿠키에서 토큰 발견: {token[:15]}...")  # 디버깅용 로그

        # ---------------------------------------------------------
        # [수정 2] 쿠키에 없으면 헤더에서 찾습니다.
        # ---------------------------------------------------------
        if not token and 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            print(f"👉 [DEBUG] 헤더에서 토큰 확인: {auth_header}")

            try:
                if " " in auth_header:
                    token = auth_header.split(' ')[1]
                else:
                    token = auth_header
            except IndexError:
                return jsonify({'success': False, 'message': '잘못된 토큰 형식입니다.'}), 401

        # ---------------------------------------------------------
        # 토큰이 둘 다 없으면 에러
        # ---------------------------------------------------------
        if not token:
            print("👉 [DEBUG] 토큰이 없음 (쿠키, 헤더 모두 없음)")
            return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401

        try:
            # 1. 시크릿 키 가져오기
            secret_key = current_app.config.get('JWT_SECRET', current_app.config.get('SECRET_KEY'))
            algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')

            # 2. 토큰 해독
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            print(f"👉 [DEBUG] 토큰 해독 성공: user_id={payload.get('user_id')}")

            # 3. 블랙리스트 확인 (순환 참조 방지를 위해 안에서 import)
            from app.models.token_blocklist import TokenBlocklist

            jti = payload.get('jti')
            if jti:
                blocked = TokenBlocklist.query.filter_by(jti=jti).first()
                if blocked:
                    print("👉 [DEBUG] 블랙리스트에 있는 토큰임 (로그아웃됨)")
                    return jsonify({'success': False, 'message': '로그아웃된 토큰입니다. 다시 로그인해주세요.'}), 401

            # 4. 사용자 정보 전달
            current_user = {
                'user_id': payload['user_id'],
                'username': payload['username']
            }

        except jwt.ExpiredSignatureError:
            print("👉 [DEBUG] 토큰 만료됨")
            return jsonify({'success': False, 'message': '토큰 유효기간이 만료되었습니다.'}), 401
        except jwt.InvalidTokenError as e:
            print(f"👉 [DEBUG] 유효하지 않은 토큰: {str(e)}")
            return jsonify({'success': False, 'message': '유효하지 않은 토큰입니다.'}), 401
        except Exception as e:
            print(f"👉 [DEBUG] 인증 알 수 없는 에러: {str(e)}")
            return jsonify({'success': False, 'message': '인증 처리 중 오류가 발생했습니다.'}), 401

        return f(current_user, *args, **kwargs)

    return decorated