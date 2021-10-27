from dataclasses import dataclass

from .database import db


@dataclass
class Key(db.Model):
    __tablename__ = 'keys'

    id: int = db.Column(db.Integer, primary_key=True)
    key: str = db.Column(db.String, unique=True)
    revoked: bool = db.Column(db.Boolean, default=False)
    description: str = db.Column(db.String)

    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

    def __repr__(self):
        return self.as_json()

    def __str__(self):
        return self.as_json()

    def as_json(self):
        return {
            'id': self.id,
            'key': self.key,
            'revoked': self.revoked,
            'description': self.description
        }
