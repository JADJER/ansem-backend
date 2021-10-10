class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = "email"
    JWT_AUTH_PASSWORD_KEY = 'password'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'
