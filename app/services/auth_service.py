from app.models import db, User
from app.models.token_blocklist import TokenBlocklist
from app.utils.auth import hash_password, verify_password, create_token, decode_token
from datetime import datetime


class AuthService:
    @staticmethod
    def register(username: str, nickname: str, password: str) -> dict:
        """회원가입"""

        # 1. 아이디 중복 체크 (여기서 SELECT 쿼리 발생)
        if User.query.filter_by(username=username).first():
            raise ValueError('이미 존재하는 아이디입니다.')

        # 2. 유효성 검사
        if len(username) < 3 or len(username) > 20:
            raise ValueError('아이디는 3자 이상 20자 이하로 입력해주세요.')

        if len(password) < 6:
            raise ValueError('비밀번호는 6자 이상 입력해주세요.')

        if not nickname or len(nickname) < 2:
            raise ValueError('닉네임은 2자 이상 입력해주세요.')

        # 3. 비밀번호 암호화 (이 함수가 없으면 500 에러 발생)
        hashed_password = hash_password(password)

        # 4. 사용자 모델 생성
        user = User(
            username=username,
            nickname=nickname,
            password=hashed_password
        )

        # 5. DB 저장
        db.session.add(user)
        db.session.commit()  # 여기서 INSERT 쿼리 발생

        return user.to_dict()

    @staticmethod
    def login(username: str, password: str) -> dict:
        """로그인"""
        user = User.query.filter_by(username=username).first()

        if not user:
            raise ValueError('아이디 또는 비밀번호가 일치하지 않습니다.')

        if not verify_password(password, user.password):
            raise ValueError('아이디 또는 비밀번호가 일치하지 않습니다.')

        token = create_token(user.id, user.username)

        return {
            'token': token,
            'user': user.to_dict()
        }

    @staticmethod
    def logout(token: str):
        """로그아웃 (토큰 블랙리스트 추가)"""
        try:
            payload = decode_token(token)
            jti = payload.get('jti')
            exp = payload.get('exp')
            user_id = payload.get('user_id')

            if not jti:
                # jti가 없는 구버전 토큰 등의 경우 그냥 무시
                return

            # 블랙리스트에 저장
            blocked_token = TokenBlocklist(
                jti=jti,
                user_id=user_id,
                expires_at=datetime.fromtimestamp(exp)
            )

            db.session.add(blocked_token)
            db.session.commit()

        except Exception:
            # 이미 만료되었거나 오류 발생 시에도 로그아웃 처리된 것으로 간주
            pass