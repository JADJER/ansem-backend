import click
from flask import Blueprint

from ansem.models import db, UserModel


admin_bp = Blueprint('admin', __name__)


@admin_bp.cli.command('set')
@click.argument('user_id')
@click.argument('value')
def set_admin(user_id, value: bool):
    user = UserModel.query.get(user_id)
    if not user:
        print("User with id {} not found".format(user_id))
        return

    user.is_admin = value

    db.session.add(user)
    db.session.commit()

    print("User {} is admin: {}".format(user.username, value))
