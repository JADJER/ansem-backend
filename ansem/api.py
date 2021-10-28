from flask import Blueprint, request, jsonify, make_response
from .resources import *
from .models import KeyModel
from .utils import response_wrapper

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.before_app_request
def check_api_key():
    if 'x-api-key' not in request.headers:
        return response_wrapper(success=False, message="Api key is missing")

    x_api_key = request.headers['x-api-key']

    api_key: KeyModel = KeyModel.query.filter_by(key=x_api_key).first()
    if not api_key:
        return response_wrapper(success=False, message="Api key invalid")

    if api_key.revoked:
        return response_wrapper(success=False, message="Api key is revoked")


api_bp.register_blueprint(requests_bp)
api_bp.register_blueprint(sessions_bp)
api_bp.register_blueprint(troops_bp)
api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(profile_bp)
