import jwt
import logging
import warnings

from datetime import datetime
from collections import OrderedDict
from flask import current_app, request, jsonify

from ansem.jwt import JWTError

logger = logging.getLogger(__name__)


class JwtImplementation(object):
    def jwt_headers(self, identity):
        return None

    def jwt_payload(self, identity):
        iat = datetime.utcnow()
        exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
        identity = getattr(identity, 'id') or identity['id']
        return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}

    def jwt_encode(self, identity):
        secret = current_app.config['JWT_SECRET_KEY']
        algorithm = current_app.config['JWT_ALGORITHM']
        required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

        payload = self.jwt_payload(identity)
        missing_claims = list(set(required_claims) - set(payload.keys()))

        if missing_claims:
            raise RuntimeError('Payload is missing required claims: %s' % ', '.join(missing_claims))

        headers = self.jwt_headers(identity)

        return jwt.encode(payload, secret, algorithm=algorithm, headers=headers)

    def jwt_decode(self, token):
        secret = current_app.config['JWT_SECRET_KEY']
        algorithm = current_app.config['JWT_ALGORITHM']
        leeway = current_app.config['JWT_LEEWAY']

        verify_claims = current_app.config['JWT_VERIFY_CLAIMS']
        required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

        options = {
            'verify_' + claim: True
            for claim in verify_claims
        }

        options.update({
            'require_' + claim: True
            for claim in required_claims
        })

        return jwt.decode(token, secret, options=options, algorithms=[algorithm], leeway=leeway)

    def request(self):
        auth_header_value = request.headers.get('Authorization', None)
        auth_header_prefix = current_app.config['JWT_AUTH_HEADER_PREFIX']

        if not auth_header_value:
            return

        parts = auth_header_value.split()

        if parts[0].lower() != auth_header_prefix.lower():
            raise JWTError('Invalid JWT header', 'Unsupported authorization type')
        elif len(parts) == 1:
            raise JWTError('Invalid JWT header', 'Token missing')
        elif len(parts) > 2:
            raise JWTError('Invalid JWT header', 'Token contains spaces')

        return parts[1]

    def auth_request(self):
        data = request.get_json()
        username = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
        password = data.get(current_app.config.get('JWT_AUTH_PASSWORD_KEY'), None)
        criterion = [username, password, len(data) == 2]

        if not all(criterion):
            raise JWTError('Bad Request', 'Invalid credentials')

        identity = self.authentication(username, password)

        if identity:
            access_token = self.jwt_encode(identity)
            return self.auth_response(access_token, identity)
        else:
            raise JWTError('Bad Request', 'Invalid credentials')

    def auth_response(self, access_token, identity):
        return jsonify({'access_token': access_token.decode('utf-8')})

    def refresh_request(self):
        pass

    def refresh_response(self, refresh_token):
        pass

    def jwt_error(self, error):
        logger.error(error)
        return jsonify(OrderedDict([
            ('status_code', error.status_code),
            ('error', error.error),
            ('description', error.description),
        ])), error.status_code, error.headers

    def identity(self, payload):
        # user_id = payload['identity']
        # return UserModel.query.get(user_id)
        pass

    def authentication(self, username, password):
        # user = UserModel.query.filter_by(username=username).first()
        # password_hash = password_hash_generate(password)
        # if user and hmac.compare_digest(user.password, password_hash):
        #     return user
        pass
