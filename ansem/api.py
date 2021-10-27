from flask import Blueprint, request, jsonify, make_response
from .resources import *
from .models import KeyModel


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.before_app_request
def check_api_key():
    if 'x-api-key' not in request.headers:
        return make_response(jsonify({
            "description": "Api key is missing",
            "error": "x_api_key is missing",
            "status_code": 401
        }), 401)

    x_api_key = request.headers['x-api-key']

    api_key: KeyModel = KeyModel.query.filter_by(key=x_api_key).first()
    if not api_key:
        return make_response(jsonify({
            "description": "Api key invalid",
            "error": "x_api_key invalid",
            "status_code": 401
        }), 401)

    if api_key.revoked:
        return make_response(jsonify({
            "description": "Api key is revoked",
            "error": "x_api_key is revoked",
            "status_code": 401
        }), 401)


api_bp.register_blueprint(requests_bp)
api_bp.register_blueprint(sessions_bp)
api_bp.register_blueprint(troops_bp)
api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(profile_bp)
