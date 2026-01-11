from app.models import db, User
from app.models.token_blocklist import TokenBlocklist
from app.utils.auth import hash_password, verify_password, create_token, decode_token
from datetime import datetime


class AuthService:
    @staticmethod
    def register(username: str, nickname: str, password: str) -> dict:
        """회원가입"""
        if User.query.filter_by(username=username).first():
            raise ValueError('이미 존재하는 아이디입니다.')

        if len(username) < 3 or len(username) > 20:
            raise ValueError('아이디는 3자 이상 20자 이하로 입력해주세요.')

        if len(password) < 6:
            raise ValueError('비밀번호는 6자 이상 입력해주세요.')

        if not nickname or len(nickname) < 2:
            raise ValueError('닉네임은 2자 이상 입력해주세요.')

        hashed_password = hash_password(password)

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
                return

            # 블랙리스트에 저장
            blocked_token = TokenBlocklist(
                jti=jti,
                user_id=user_id,
                expires_at=datetime.fromtimestamp(exp)
            )

            db.session.add(blocked_token)
            db.session.commit()

        except Exception as e:
            # 이미 만료되었거나 오류 발생 시 pass하지만 디버깅을 위해 출력
            print(f"Logout Warning: {str(e)}")
            pass

    # [추가됨] 회원 탈퇴 기능
    @staticmethod
    def delete_account(user_id: int, password: str) -> dict:
        """회원 탈퇴"""
        user = User.query.get(user_id)

        if not user:
            raise ValueError('사용자를 찾을 수 없습니다.')

        # 본인 확인을 위해 비밀번호 재검증
        if not verify_password(password, user.password):
            raise ValueError('비밀번호가 일치하지 않습니다.')

        try:
            # 관련된 데이터 삭제 (Cascade 설정이 안되어 있다면 수동 삭제 필요)
            # 1. 사용자가 가진 토큰 블랙리스트 데이터 삭제 (선택사항)
            TokenBlocklist.query.filter_by(user_id=user.id).delete()

            # 2. 사용자 삭제
            db.session.delete(user)
            db.session.commit()

            return {'success': True, 'message': '회원 탈퇴가 완료되었습니다.'}

        except Exception as e:
            db.session.rollback()
            raise Exception(f'탈퇴 처리 중 오류 발생: {str(e)}')

    @staticmethod
    def get_current_user(user_id: int) -> dict:
        """현재 사용자 정보 조회"""
        user = User.query.get(user_id)

        if not user:
            raise ValueError('사용자 정보를 찾을 수 없습니다.')

        return user.to_dict()