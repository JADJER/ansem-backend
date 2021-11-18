from flask import Blueprint
from ansem.jwt import jwt_required, current_identity
from .users import create_user, get_user, update_user, delete_user
from .profile_requests import profile_requests_bp

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
profile_bp.register_blueprint(profile_requests_bp)


@profile_bp.route('', methods=['POST'])
def create_profile():
    return create_user()


@profile_bp.route('', methods=["GET"])
@jwt_required()
def get_profile():
    return get_user(current_identity.id)


@profile_bp.route('', methods=['PUT'])
@jwt_required()
def update_profile():
    return update_user(current_identity.id)


@profile_bp.route('', methods=['DELETE'])
@jwt_required()
def delete_profile():
    return delete_user(current_identity.id)
