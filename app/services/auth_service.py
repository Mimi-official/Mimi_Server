from app.models import db, User
from app.utils.auth import hash_password, verify_password, create_token


class AuthService:
    @staticmethod
    def register(username: str, nickname: str, password: str) -> dict:
        """회원가입"""
        # 중복 체크
        if User.query.filter_by(username=username).first():
            raise ValueError('이미 존재하는 아이디입니다.')

        # 유효성 검사
        if len(username) < 3 or len(username) > 20:
            raise ValueError('아이디는 3자 이상 20자 이하로 입력해주세요.')

        if len(password) < 6:
            raise ValueError('비밀번호는 6자 이상 입력해주세요.')

        if not nickname or len(nickname) < 2:
            raise ValueError('닉네임은 2자 이상 입력해주세요.')

        # 비밀번호 해싱
        hashed_password = hash_password(password)

        # 사용자 생성
        user = User(
            username=username,
            nickname=nickname,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return user.to_dict()

    @staticmethod
    def login(username: str, password: str) -> dict:
        """로그인"""
        user = User.query.filter_by(username=username).first()

        if not user:
            raise ValueError('아이디 또는 비밀번호가 일치하지 않습니다.')

        if not verify_password(password, user.password):
            raise ValueError('아이디 또는 비밀번호가 일치하지 않습니다.')

        # JWT 토큰 생성
        token = create_token(user.id, user.username)

        return {
            'token': token,
            'user': user.to_dict()
        }