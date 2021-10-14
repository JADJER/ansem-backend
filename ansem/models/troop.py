from dataclasses import dataclass

from .database import db


@dataclass
class Troop(db.Model):
    __tablename__ = 'troops'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String)
    description: str = db.Column(db.String)
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)

    def __init__(self, **kwargs):
        super(Troop, self).__init__(**kwargs)

    def __repr__(self):
        return self.as_json()

    def __str__(self):
        return self.as_json()

    def as_json(self):
        return {
            'id': self.id,
            'name': self.email,
            'description': self.first_name,
            'date_start': self.last_name,
            'date_end': self.country
        }
