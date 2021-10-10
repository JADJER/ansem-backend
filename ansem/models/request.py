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
        return '<Request %r>' % self.id
