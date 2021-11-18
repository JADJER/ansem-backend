from functools import wraps

from flask import current_app, _request_ctx_stack
from werkzeug.local import LocalProxy

import jwt

from .jwt import JWT
from .jwt_error import JWTError
from .jwt_implementation import JwtImplementation

_jwt = LocalProxy(lambda: current_app.extensions['jwt'])


def _jwt_required(realm):
    """Does the actual work of verifying the JWT data in the current request.
    This is done automatically for you by `jwt_required()` but you could call it manually.
    Doing so would be useful in the context of optional JWT access in your APIs.

    :param realm: an optional realm
    """
    token = _jwt.request_callback()

    if token is None:
        raise JWTError('Authorization Required', 'Request does not contain an access token',
                       headers={'WWW-Authenticate': 'JWT realm="%s"' % realm})

    try:
        payload = _jwt.jwt_decode_callback(token)
    except jwt.InvalidTokenError as e:
        raise JWTError('Invalid token', str(e))

    _request_ctx_stack.top.current_identity = identity = _jwt.identity_callback(payload)

    if identity is None:
        raise JWTError('Invalid JWT', 'User does not exist')


def jwt_required(realm=None):
    """View decorator that requires a valid JWT token to be present in the request

    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(realm or current_app.config['JWT_DEFAULT_REALM'])
            return fn(*args, **kwargs)
        return decorator
    return wrapper
