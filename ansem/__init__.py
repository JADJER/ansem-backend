import os

from flask import Flask
from flask_jwt import JWT
from flask_cors import CORS

from .api import api_bp
from .models import db, migrate
from .config import Config
from .secury import identity_handler, authentication_handler, auth_response_handler, error_handler
from .commands import *


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_object(Config)
    app.config.from_pyfile(os.path.join(app.instance_path, 'app.cfg'))

    CORS(app)
    jwt = JWT(app, authentication_handler, identity_handler)
    jwt.jwt_error_handler(error_handler)
    jwt.auth_response_handler(auth_response_handler)

    db.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(api_key_bp)
    app.register_blueprint(admin_bp)

    return app
