import hmac

from flask import jsonify

from ansem.models import UserModel
from ansem.utils import password_hash_generate


def authentication(email, password):
    user = UserModel.query.filter_by(email=email).first()
    password_hash = password_hash_generate(password)
    if user and hmac.compare_digest(user.password, password_hash):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.query.get(user_id)


def auth_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user': identity.as_json()
    })

