from dataclasses import dataclass

from .database import db


@dataclass
class Session(db.Model):
    __tablename__ = 'sessions'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)
    description: str = db.Column(db.String)
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date, nullable=False)
    is_active: bool = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(Session, self).__init__(**kwargs)

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
            'date_end': self.country,
            'is_active': self.is_active
        }
