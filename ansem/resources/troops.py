from flask import jsonify, Blueprint, request, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import TroopModel, db
from ansem.utils import response_wrapper

troops_bp = Blueprint('troops', __name__, url_prefix='/troops')

fields = [
    'name',
    'description',
    'date_start',
    'date_end',
    'is_active'
]

error_messages = {
    'name': 'Session name is not set',
    'description': 'Description is not set',
    'date_start': 'Date start is not set',
    'date_end': 'Date end is not set',
    'is_active': 'Is active not set'
}


@troops_bp.route('', methods=['GET'])
@jwt_required()
def get_all_troops():
    if not current_identity.is_admin:
        return response_wrapper(success=False, message="Access denied")

    troops = TroopModel.query.all()
    return jsonify(troops)


@troops_bp.route('', methods=['GET'])
@troops_bp.route('/active', methods=['GET'])
def get_active_troops():
    troops = TroopModel.query.filter_by(is_active=True).all()
    return jsonify(troops)


@troops_bp.route('', methods=['POST'])
@jwt_required()
def create_troop():
    if not current_identity.is_admin:
        return response_wrapper(success=False, message="Access denied")

    if not request.is_json:
        return response_wrapper(success=False, message="Request data type wrong")

    request_data = request.get_json(silent=True)
    if not request_data:
        return response_wrapper(success=False, message="Request data error")

    for field in fields:
        if field not in request_data:
            return response_wrapper(success=False, message=error_messages.get(field))

    troop_object = TroopModel(
        name=request_data['name'],
        description=request_data['description'],
        date_start=request_data['date_start'],
        date_end=request_data['date_end'],
        is_active=request_data['is_active']
    )

    db.session.add(troop_object)
    db.session.commit()

    return jsonify(troop_object.as_json())


@troops_bp.route('/<int:troop_id>', methods=['GET'])
@jwt_required()
def get_request(troop_id):
    troop_object = TroopModel.query.get(troop_id)
    if not troop_object:
        return response_wrapper(success=False, message="Troop not found")

    return jsonify(troop_object.as_json())


@troops_bp.route('/<int:troop_id>', methods=['PUT'])
@jwt_required()
def update_troop(troop_id):
    if not current_identity.is_admin:
        return response_wrapper(success=False, message="Access denied")

    if not request.is_json:
        return response_wrapper(success=False, message="Request data type wrong")

    request_data = request.get_json(silent=True)
    if not request_data:
        return response_wrapper(success=False, message="Request data error")

    for field in fields:
        if field not in request_data:
            return response_wrapper(success=False, message=error_messages.get(field))

    troop_object = TroopModel.query.get(troop_id)
    if not troop_object:
        return response_wrapper(success=False, message="Troop not found")

    troop_object.name = request_data['name']
    troop_object.description = request_data['description']
    troop_object.date_start = request_data['date_start']
    troop_object.date_end = request_data['date_end']
    troop_object.is_active = request_data['is_active']

    db.session.add(troop_object)
    db.session.commit()

    return jsonify(troop_object.as_json())


@troops_bp.route('/<int:troop_id>', methods=['DELETE'])
@jwt_required()
def delete_troop(troop_id):
    if not current_identity.is_admin:
        return response_wrapper(success=False, message="Access denied")

    troop_object = TroopModel.query.get(troop_id)
    if not troop_object:
        return response_wrapper(success=False, message="Troop not found")

    db.session.delete(troop_object)
    db.session.commit()

    return response_wrapper(success=True, message="OK")
