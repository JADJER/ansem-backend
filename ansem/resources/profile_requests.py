from flask import Blueprint
from ansem.jwt import jwt_required, current_identity
from .users import get_user_request, get_user_requests, create_user_request, update_user_request, delete_user_request

profile_requests_bp = Blueprint('profile_requests', __name__, url_prefix='/requests')


@profile_requests_bp.route('', methods=['GET'])
@jwt_required()
def get_requests():
    return get_user_requests(current_identity.id)


@profile_requests_bp.route('', methods=['POST'])
@jwt_required()
def create_request():
    return create_user_request(current_identity.id)


@profile_requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    return get_user_request(current_identity.id, request_id)


@profile_requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def update_request(request_id):
    return update_user_request(current_identity.id, request_id)


@profile_requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def delete_request(request_id):
    return delete_user_request(current_identity.id, request_id)
