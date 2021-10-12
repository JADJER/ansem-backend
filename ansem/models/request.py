from dataclasses import dataclass

from .database import db


@dataclass
class Request(db.Model):
    __tablename__ = 'requests'

    id: int = db.Column(db.Integer, primary_key=True)
    school: str = db.Column(db.String, nullable=False)
    class_no: str = db.Column(db.String, nullable=False)
    score: float = db.Column(db.Float)
    index: int = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', foreign_keys=user_id)

    json = {
        'id': id,
        'user_id': user_id,
        'school': school,
        'class': class_no,
        'score': score,
        'index': index
    }

    def __init__(self, **kwargs):
        super(Request, self).__init__(**kwargs)

    def __repr__(self):
        return self.json

    def __str__(self):
        return self.json
