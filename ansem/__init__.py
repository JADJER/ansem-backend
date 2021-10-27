import os

from flask import Flask
from flask_jwt import JWT
from flask_cors import CORS

from .api import api_bp
from .models import db, migrate
from .config import Config
from .secury import identity, authentication, auth_response_handler


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_pyfile(os.path.join(app.instance_path, 'app.cfg'))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)
    jwt = JWT(app, authentication, identity)
    jwt.auth_response_handler(auth_response_handler)

    db.init_app(app)
    migrate.init_app(app)

    # with app.app_context():
    #     db.create_all()

    app.register_blueprint(api_bp)

    return app
