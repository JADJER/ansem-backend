from flask import jsonify
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse

from ansem.models import User
from ansem.models import db

parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class Profile(Resource):

    @jwt_required()
    def get(self):
        # print('%s' % current_identity.password)
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()

        user = db.session.query(User).filter(User.email == args.email).first()

        if not user:
            user = User(email=args.email, password=args.password)

            db.session.add(user)
            db.session.commit()

        return jsonify(user)
