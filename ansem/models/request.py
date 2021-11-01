from dataclasses import dataclass

from .database import db


@dataclass
class Request(db.Model):
    __tablename__ = 'requests'

    id: int = db.Column(db.Integer, primary_key=True)
    school: str = db.Column(db.String, nullable=False)
    class_no: str = db.Column(db.String, nullable=False)
    score: float = db.Column(db.Float, nullable=False)
    index: int = db.Column(db.Integer, nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id: int = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)

    def __init__(self, **kwargs):
        super(Request, self).__init__(**kwargs)

    def __repr__(self):
        return self.as_json()

    def __str__(self):
        return self.as_json()

    def as_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'school': self.school,
            'class': self.class_no,
            'score': self.score,
            'index': self.index,
            'session_id': self.session_id
        }
