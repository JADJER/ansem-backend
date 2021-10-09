from .database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # do custom initialization here

    def __repr__(self):
        return '<User %r>' % self.username
