from . import db


class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100))
    hashtags = db.Column(db.String(255))
    description = db.Column(db.Text)
    info = db.Column(db.Text)
    personality = db.Column(db.Text)
    first_message = db.Column(db.Text)
    system_prompt = db.Column(db.Text)
    profile_img_url = db.Column(db.String(255))

    # 성공 엔딩
    success_end_title = db.Column(db.String(100))
    success_end_content = db.Column(db.Text)
    success_end_img = db.Column(db.String(255))

    # 실패 엔딩
    fail_end_title = db.Column(db.String(100))
    fail_end_content = db.Column(db.Text)
    fail_end_img = db.Column(db.String(255))

    # 히든 엔딩
    hidden_end_title = db.Column(db.String(100))
    hidden_end_content = db.Column(db.Text)
    hidden_end_img = db.Column(db.String(255))

    # 관계
    events = db.relationship('CharacterEvent', backref='character', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_full=False):
        data = {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'hashtags': self.hashtags,
            'profile_img_url': self.profile_img_url
        }

        if include_full:
            data.update({
                'description': self.description,
                'info': self.info,
                'personality': self.personality,
                'first_message': self.first_message,
                'system_prompt': self.system_prompt,
                'success_end_title': self.success_end_title,
                'success_end_content': self.success_end_content,
                'success_end_img': self.success_end_img,
                'fail_end_title': self.fail_end_title,
                'fail_end_content': self.fail_end_content,
                'fail_end_img': self.fail_end_img,
                'hidden_end_title': self.hidden_end_title,
                'hidden_end_content': self.hidden_end_content,
                'hidden_end_img': self.hidden_end_img
            })

        return data