from . import db


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    char_name = db.Column(db.String(50), nullable=False)

    affinity = db.Column(db.Integer, default=0)
    current_step = db.Column(db.Integer, default=0)  # 현재 도달한 이벤트 단계 (1, 2, 3...)
    turn_count = db.Column(db.Integer, default=0)  # 자유 채팅 횟수 (이벤트 트리거용)
    is_ended = db.Column(db.Boolean, default=False)

    # 마지막으로 이벤트를 완료한 상태인지 체크 (True면 자유채팅 중, False면 선택지 고르는 중)
    is_chatting = db.Column(db.Boolean, default=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'char_name', name='user_char_unique'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'char_name': self.char_name,
            'affinity': self.affinity,
            'current_step': self.current_step,
            'is_ended': self.is_ended,
            'turn_count': self.turn_count,
            'is_chatting': self.is_chatting
        }