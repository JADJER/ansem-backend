from flask import Blueprint
from flask_jwt import jwt_required, current_identity

from ansem.models import RequestModel
from ansem.utils import response_wrapper

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

fields = [
    'user_id',
    'school',
    'class',
    'score',
    'index',
    'type',
    'session_id',
    'troop_id'
]

error_messages = {
    'user_id': 'Session name is not set',
    'school': 'Description is not set',
    'class': 'Date start is not set',
    'score': 'Date end is not set',
    'index': 'Is active not set',
    'type': 'Is active not set',
    'session_id': 'Is active not set',
    'troop_id': 'Is active not set'
}


@requests_bp.route('', methods=['GET'])
@jwt_required()
def get_requests():
    if not current_identity.is_admin:
        return response_wrapper(success=False, message="Access denied")

    requests = RequestModel.query.all()

    return response_wrapper(success=True, message="Ok", data=requests)


@requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    if not current_identity.is_admin:
        return response_wrapper(success=False, message="Access denied")

    request_object = RequestModel.query.get(request_id)
    if not request_object:
        return response_wrapper(success=False, message="Request not found")

    return response_wrapper(success=True, message="Ok", data=request_object)
