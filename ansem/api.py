from flask import Blueprint
from flask_restful import Api
from .resources import *

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(api_v1)
api.add_resource(Profile, '/profile')
api.add_resource(Requests, '/requests')
api.add_resource(Request, '/requests/<id>')
