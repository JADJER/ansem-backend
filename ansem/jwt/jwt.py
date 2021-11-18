from .jwt_error import JWTError
from .jwt_implementation import JwtImplementation
from .jwt_config import CONFIG_DEFAULTS


class JWT(object):

    _jwt_implementation: JwtImplementation

    def __init__(self, app=None, jwt_implementation: JwtImplementation = None):
        if app is not None:
            self.init_app(app, jwt_implementation)

    def init_app(self, app, jwt_implementation: JwtImplementation = None):
        self._jwt_implementation = jwt_implementation

        if jwt_implementation is None:
            self._jwt_implementation = JwtImplementation()

        for k, v in CONFIG_DEFAULTS.items():
            app.config.setdefault(k, v)

        app.config.setdefault('JWT_SECRET_KEY', app.config['SECRET_KEY'])

        auth_url_rule = app.config.get('JWT_AUTH_URL_RULE', None)
        if auth_url_rule:
            auth_url_options = app.config.get('JWT_AUTH_URL_OPTIONS', {'methods': ['POST']})
            auth_url_options.setdefault('view_func', self._jwt_implementation.auth_request)
            app.add_url_rule(auth_url_rule, **auth_url_options)

        refresh_url_rule = app.config.get('JWT_REFRESH_URL_RULE', None)
        if refresh_url_rule:
            refresh_url_options = app.config.get('JWT_REFRESH_URL_OPTIONS', {'methods': ['POST']})
            refresh_url_options.setdefault('view_func', self._jwt_implementation.refresh_request)
            app.add_url_rule(refresh_url_rule, **refresh_url_options)

        app.errorhandler(JWTError)(self._jwt_implementation.jwt_error)

        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}

        app.extensions['jwt'] = self
