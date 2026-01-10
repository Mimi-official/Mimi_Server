from . import db


class CharacterEvent(db.Model):
    __tablename__ = 'character_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), nullable=False)
    event_order = db.Column(db.Integer, nullable=False)
    event_text = db.Column(db.Text)

    # 선택지 1
    choice_1 = db.Column(db.String(255))
    choice_1_score = db.Column(db.Integer)

    # 선택지 2
    choice_2 = db.Column(db.String(255))
    choice_2_score = db.Column(db.Integer)

    # 선택지 3
    choice_3 = db.Column(db.String(255))
    choice_3_score = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'char_id': self.char_id,
            'event_order': self.event_order,
            'event_text': self.event_text,
            'choices': [
                {'text': self.choice_1, 'score': self.choice_1_score} if self.choice_1 else None,
                {'text': self.choice_2, 'score': self.choice_2_score} if self.choice_2 else None,
                {'text': self.choice_3, 'score': self.choice_3_score} if self.choice_3 else None,
            ]
        }

    def get_choices(self):
        """선택지만 반환"""
        choices = []
        if self.choice_1:
            choices.append({'text': self.choice_1, 'score': self.choice_1_score, 'index': 1})
        if self.choice_2:
            choices.append({'text': self.choice_2, 'score': self.choice_2_score, 'index': 2})
        if self.choice_3:
            choices.append({'text': self.choice_3, 'score': self.choice_3_score, 'index': 3})
        return choices