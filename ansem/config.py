class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = "username"
    JWT_AUTH_PASSWORD_KEY = 'password'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'
    JWT_AUTH_URL_RULE = '/api/v1/auth'
