from flask_jwt import jwt_required
from flask_restful import Resource


class Profile(Resource):

    @jwt_required()
    def get(self):
        return {'hello': 'world'}
