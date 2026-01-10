import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app
from functools import wraps
from flask import request, jsonify


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
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRES_IN_DAYS'])
    }
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )
    return token


def decode_token(token: str) -> dict:
    """JWT 토큰 디코드"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET'],
            algorithms=[current_app.config['JWT_ALGORITHM']]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('토큰이 만료되었습니다.')
    except jwt.InvalidTokenError:
        raise ValueError('유효하지 않은 토큰입니다.')


def token_required(f):
    """JWT 인증 데코레이터"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'success': False, 'message': '잘못된 토큰 형식입니다.'}), 401

        if not token:
            return jsonify({'success': False, 'message': '인증 토큰이 필요합니다.'}), 401

        try:
            payload = decode_token(token)
            request.current_user = payload
        except ValueError as e:
            return jsonify({'success': False, 'message': str(e)}), 401

        return f(*args, **kwargs)

    return decorated