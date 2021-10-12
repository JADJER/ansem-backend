from dataclasses import dataclass

from .database import db


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String, unique=True, nullable=False)
    password: str = db.Column(db.String, nullable=False)
    first_name: str = db.Column(db.String, nullable=False)
    last_name: str = db.Column(db.String, nullable=False)
    country: str = db.Column(db.String, nullable=False, default="Belarus")
    city: str = db.Column(db.String, nullable=False)
    address: str = db.Column(db.String, nullable=False)
    mobile_no: str = db.Column(db.String, unique=True, nullable=False)

    json = {
        'id': id,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'country': country,
        'city': city,
        'address': address,
        'mobile_no': mobile_no,
    }

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return self.json

    def __str__(self):
        return self.json
