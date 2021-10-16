from flask import jsonify, Blueprint, request, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import SessionModel, db

sessions_bp = Blueprint('sessions', __name__, url_prefix='/sessions')

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


@sessions_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_sessions():
    if not current_identity.is_admin:
        return make_response({'error', 'Auth error'}, 400)

    requests = SessionModel.query.all()
    return jsonify(requests)


@sessions_bp.route('', methods=['GET'])
@sessions_bp.route('/active', methods=['GET'])
def get_active_sessions():
    requests = SessionModel.query.filter_by(is_active=True).all()
    return jsonify(requests)


@sessions_bp.route('', methods=['POST'])
@jwt_required()
def create_session():
    if not current_identity.is_admin:
        return make_response({'error', 'Auth error'}, 400)

    if not request.is_json:
        return make_response({'error': 'Request data type wrong'}, 400)

    request_data = request.get_json(silent=True)
    if not request_data:
        return make_response({'error', "Request data error", 400})

    error = {}

    for field in fields:
        if field not in request_data:
            error[field] = error_messages.get(field)

    if error:
        return make_response({'error': error}, 400)

    session_object = SessionModel(
        name=request_data['name'],
        description=request_data['description'],
        date_start=request_data['date_start'],
        date_end=request_data['date_end'],
        is_active=request_data['is_active']
    )

    db.session.add(session_object)
    db.session.commit()

    return jsonify(session_object.as_json())


@sessions_bp.route('/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    session_object = SessionModel.query.get(session_id)
    if not session_object:
        return make_response({'error': 'Session not found'}, 400)

    if session_object.is_active:
        jsonify(session_object.as_json())

    if not current_identity.is_admin:
        return make_response({'error', 'Auth error'}, 400)

    return jsonify(session_object.as_json())


@sessions_bp.route('/<int:session_id>', methods=['PUT'])
@jwt_required()
def update_session(session_id):
    if not current_identity.is_admin:
        return make_response({'error', 'Auth error'}, 400)

    if not request.is_json:
        return make_response({'error': 'Request data type wrong'}, 400)

    request_data = request.get_json(silent=True)
    if not request_data:
        return make_response({'error', "Request data error", 400})

    error = {}

    for field in fields:
        if field not in request_data:
            error[field] = error_messages.get(field)

    if error:
        return make_response({'error': error}, 400)

    session_object = SessionModel.query.get(session_id)
    if not session_object:
        return make_response({'error': 'Session not found'}, 400)

    session_object.name = request_data['name']
    session_object.description = request_data['description']
    session_object.date_start = request_data['date_start']
    session_object.date_end = request_data['date_end']
    session_object.is_active = request_data['is_active']

    db.session.add(session_object)
    db.session.commit()

    return jsonify(session_object.as_json())


@sessions_bp.route('/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_request(session_id):
    if not current_identity.is_admin:
        return make_response({'error', 'Auth error'}, 400)

    session_object = SessionModel.query.get(session_id)
    if not session_object:
        return make_response({'error': 'Session not found'}, 400)

    db.session.delete(session_object)
    db.session.commit()

    return make_response({'result': 'OK'}, 200)
