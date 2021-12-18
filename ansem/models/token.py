from dataclasses import dataclass

from .database import db


@dataclass
class Token(db.Model):
    __tablename__ = 'tokens'

    id: int = db.Column(db.Integer, primary_key=True)
    token: str = db.Column(db.String, unique=True, nullable=False)
    revoked: bool = db.Column(db.Boolean, default=False)
    description: str = db.Column(db.String, nullable=False)

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
