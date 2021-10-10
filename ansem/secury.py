import hmac

from ansem.models import UserModel


def authentication(email, password):
    user = UserModel.query.filter_by(email=email).first()
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.query.get(user_id)
