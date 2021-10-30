import hmac

from ansem.models import UserModel
from ansem.utils import password_hash_generate, response_wrapper


def error_handler(error):
    print(error)
    return response_wrapper(success=False, message=str(error))


def identity_handler(payload):
    user_id = payload['identity']
    return UserModel.query.get(user_id)


def authentication_handler(username, password):
    user = UserModel.query.filter_by(username=username).first()
    password_hash = password_hash_generate(password)
    if user and hmac.compare_digest(user.password, password_hash):
        return user


def auth_response_handler(access_token, identity):
    data = {
        'access_token': access_token.decode('utf-8'),
        'user': identity.as_json()
    }
    return response_wrapper(success=True, message="Ok", data=data)
