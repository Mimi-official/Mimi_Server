import bcrypt
import jwt
import uuid  # [수정] 여기가 빠져 있어서 에러가 났습니다!
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps


def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    # encode()로 바이트로 변환 후 해싱
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """비밀번호 검증"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_token(user_id: int, username: str) -> str:
    """JWT 토큰 생성"""
    # config에서 값 가져오기 (없을 경우 기본값 설정으로 에러 방지)
    expires_in_days = current_app.config.get('JWT_EXPIRES_IN_DAYS', 1)
    secret_key = current_app.config.get('JWT_SECRET', current_app.config.get('SECRET_KEY'))
    algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')

    payload = {
        'user_id': user_id,
        'username': username,
        'jti': str(uuid.uuid4()),  # 고유 식별자
        'exp': datetime.utcnow() + timedelta(days=expires_in_days)
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def decode_token(token: str) -> dict:
    """JWT 토큰 디코드"""
    secret_key = current_app.config.get('JWT_SECRET', current_app.config.get('SECRET_KEY'))
    algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('토큰이 만료되었습니다.')
    except jwt.InvalidTokenError:
        raise ValueError('유효하지 않은 토큰입니다.')


# app/utils/auth.py

from functools import wraps
from flask import request, jsonify, current_app
import jwt

# [중요] 순환 참조 방지를 위해 함수 내부에서 import 하거나, 필요한 것만 가져옵니다.
from app.models.token_blocklist import TokenBlocklist


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 디버깅: 헤더가 들어오는지 확인
        print(f"👉 [DEBUG] 요청 헤더: {request.headers.get('Authorization')}")

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # "Bearer <토큰>" 형식인지 확인
                if " " in auth_header:
                    token = auth_header.split(' ')[1]
                else:
                    print("👉 [DEBUG] Bearer 형식이 아님")
                    token = auth_header  # 혹시 모르니 그냥 넣어봄
            except IndexError:
                print("👉 [DEBUG] 토큰 추출 실패 (IndexError)")
                return jsonify({'success': False, 'message': '잘못된 토큰 형식입니다.'}), 401

        if not token:
            print("👉 [DEBUG] 토큰이 없음")
            return jsonify({'success': False, 'message': '인증 토큰이 필요합니다.'}), 401

        try:
            # 토큰 해독 시도
            # decode_token 함수 내용을 여기에 직접 풀어서 디버깅 (순환 참조 방지 및 확인용)
            secret_key = current_app.config.get('JWT_SECRET', 'jwt-secret-key')
            algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')

            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            print(f"👉 [DEBUG] 토큰 해독 성공: {payload}")

            # 블랙리스트 확인
            jti = payload.get('jti')
            if jti:
                blocked = TokenBlocklist.query.filter_by(jti=jti).first()
                if blocked:
                    print("👉 [DEBUG] 블랙리스트에 있는 토큰임 (로그아웃됨)")
                    return jsonify({'success': False, 'message': '로그아웃된 토큰입니다.'}), 401

            # user_id를 current_user로 전달
            current_user = {'user_id': payload['user_id'], 'username': payload['username']}

        except jwt.ExpiredSignatureError:
            print("👉 [DEBUG] 토큰 만료됨")
            return jsonify({'success': False, 'message': '만료된 토큰입니다.'}), 401
        except jwt.InvalidTokenError as e:
            print(f"👉 [DEBUG] 유효하지 않은 토큰: {str(e)}")
            return jsonify({'success': False, 'message': '유효하지 않은 토큰입니다.'}), 401
        except Exception as e:
            print(f"👉 [DEBUG] 알 수 없는 에러: {str(e)}")
            return jsonify({'success': False, 'message': f'인증 오류: {str(e)}'}), 401

        return f(current_user, *args, **kwargs)

    return decorated