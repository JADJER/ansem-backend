import hmac

from ansem.models import User


def authentication(email, password):
    user = User.query.filter_by(email=email).first()
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)
