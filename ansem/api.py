from flask import Blueprint
from .resources import profile_bp, requests_bp

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api_bp.register_blueprint(profile_bp)
api_bp.register_blueprint(requests_bp)
