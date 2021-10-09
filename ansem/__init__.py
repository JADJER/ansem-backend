import os

from flask import Flask
from flask_jwt import JWT

from .api import api_v1
from .secury import identity, authentication
from .models import db
from .config import Config


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

    JWT(app, authentication, identity)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_v1)

    return app
