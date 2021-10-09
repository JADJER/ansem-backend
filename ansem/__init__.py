import os

from flask import Flask
from flask_jwt import JWT

from .api import api_v1
from .secury import identity, authentication
from .models import db

jwt = JWT(authentication_handler=authentication, identity_handler=identity)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=b'e02d3a100e849c3cf396',
        # DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
        SQLALCHEMY_DATABASE_URI='sqlite:////home/jadjer/database.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    # app.register_blueprint(auth)
    app.register_blueprint(api_v1)

    return app
