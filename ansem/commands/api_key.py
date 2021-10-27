import click
from flask import Blueprint
import secrets
from ansem.models import KeyModel, db

api_key_bp = Blueprint('api_key', __name__)


@api_key_bp.cli.command('generate')
@click.argument('description')
def generate_api_key(description):
    key = secrets.token_urlsafe()

    key_model = KeyModel(key, description)

    db.session.add(key_model)
    db.session.commit()

    print("{} -> {}".format(description, key))


@api_key_bp.cli.command('list')
def list_api_key():
    keys = KeyModel.query.all()

    for key in keys:
        print("{} -> {}".format(key.description, key.key))
