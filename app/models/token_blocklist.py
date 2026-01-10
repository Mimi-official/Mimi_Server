from . import db
from datetime import datetime

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(36), nullable=False, index=True)  # JWT 고유 식별자
    token_type = db.Column(db.String(10), nullable=False, default='access')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'jti': self.jti,
            'revoked_at': self.revoked_at
        }