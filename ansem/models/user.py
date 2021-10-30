from dataclasses import dataclass

from .database import db


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String, unique=True, nullable=False)
    password: str = db.Column(db.String, nullable=False)
    first_name: str = db.Column(db.String, nullable=False)
    second_name: str = db.Column(db.String)
    last_name: str = db.Column(db.String, nullable=False)
    country: str = db.Column(db.String)
    city: str = db.Column(db.String)
    address: str = db.Column(db.String)
    mobile_no: str = db.Column(db.String)
    is_admin: bool = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return self.as_json()

    def __str__(self):
        return self.as_json()

    def as_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'last_name': self.last_name,
            'country': self.country,
            'city': self.city,
            'address': self.address,
            'mobile_no': self.mobile_no,
            'is_admin': self.is_admin
        }
