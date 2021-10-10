from dataclasses import dataclass

from .database import db


@dataclass
class Request(db.Model):
    __tablename__ = 'requests'

    id: int = db.Column(db.Integer, primary_key=True)
    country: str = db.Column(db.String, nullable=False, default="Belarus")
    city: str = db.Column(db.String, nullable=False)
    address: str = db.Column(db.String, nullable=False)
    school: str = db.Column(db.String, nullable=False)
    score: float = db.Column(db.Float)
    index: int = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, **kwargs):
        super(Request, self).__init__(**kwargs)

    def __repr__(self):
        return {
            'id': self.id,
            'country': self.email,
            'city': self.first_name,
            'address': self.last_name,
            'school': self.last_name,
            'score': self.last_name,
            'index': self.last_name,
            'user_id': self.last_name
        }

    def __str__(self):
        return {
            'id': self.id,
            'country': self.email,
            'city': self.first_name,
            'address': self.last_name,
            'school': self.last_name,
            'score': self.last_name,
            'index': self.last_name,
            'user_id': self.last_name
        }
