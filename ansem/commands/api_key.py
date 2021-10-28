import click
import secrets
from flask import Blueprint

from ansem.models import db, KeyModel


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
        if key.revoked:
            print("{} -> {} [ REVOKED ]".format(key.description, key.key))
        else:
            print("{} -> {}".format(key.description, key.key))


@api_key_bp.cli.command('revoke')
@click.argument('key')
def revoke_api_key(key_value):
    key = KeyModel.query.filter_by(key=key_value).first()
    if not key:
        print("Key {} not found".format(key_value))
        return

    key.revoked = True

    db.session.add(key)
    db.session.commit()

    print("{} key is revoked".format(key.description))


@api_key_bp.cli.command('remove')
@click.argument('key')
def remove_api_key(key_value):
    key = KeyModel.query.filter_by(key=key_value).first()
    if not key:
        print("Key {} not found".format(key_value))
        return

    db.session.delete(key)
    db.session.commit()

    print("{} key is removed".format(key.description))
