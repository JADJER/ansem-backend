from flask_restful import Resource


class Request(Resource):
    def get(self, id):
        return {'hello': 'world'}
