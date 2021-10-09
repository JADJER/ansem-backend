from dataclasses import dataclass

from .database import db


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password: str = db.Column(db.String(150), nullable=False)
    first_name: str = db.Column(db.String(150), nullable=True)
    last_name: str = db.Column(db.String(150), nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # do custom initialization here

    def __repr__(self):
        return '<User %r>' % self.email
