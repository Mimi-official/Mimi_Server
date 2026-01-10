from . import db
from datetime import datetime


class ChatLog(db.Model):
    __tablename__ = 'chat_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    char_name = db.Column(db.String(50), nullable=False)
    sender = db.Column(db.Enum('user', 'ai', name='sender_type'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'char_name': self.char_name,
            'sender': self.sender,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }