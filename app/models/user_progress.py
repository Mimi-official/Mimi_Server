from . import db


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    char_name = db.Column(db.String(50), nullable=False)
    affinity = db.Column(db.Integer, default=0)
    current_step = db.Column(db.Integer, default=1)
    is_ended = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'char_name', name='user_char_unique'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'char_name': self.char_name,
            'affinity': self.affinity,
            'current_step': self.current_step,
            'is_ended': self.is_ended
        }