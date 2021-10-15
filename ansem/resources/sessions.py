from flask import jsonify, Blueprint, request, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import RequestModel, db

sessions_bp = Blueprint('sessions', __name__, url_prefix='/sessions')

fields = [
    'email',
    'password',
    'first_name',
    'last_name',
    'country',
    'city',
    'address',
    'mobile_no'
]

error_messages = {
    'email': 'Email is not set',
    'password': 'Password is not set',
    'first_name': 'First name is not set',
    'last_name': 'Last name is not set',
    'country': 'Country is not set',
    'city': 'City is not set',
    'address': 'Address is not set',
    'mobile_no': 'Mobile number is not set'
}


@requests_bp.route('', methods=['GET'])
@jwt_required()
def get_all_sessions():
    requests = RequestModel.query.filter_by(user_id=current_identity.id).all()
    return jsonify(requests)


@requests_bp.route('', methods=['GET'])
def get_active_sessions():
    requests = RequestModel.query.filter_by(user_id=current_identity.id).all()
    return jsonify(requests)


@requests_bp.route('', methods=['POST'])
@jwt_required()
def create_request():
    if not request.is_json:
        return make_response({'error': 'Request data type wrong'}, 400)

    request_data = request.get_json(silent=True)
    if not request_data:
        return make_response({'error', "Request data error", 400})

    for field in fields:
        if field not in request_data:
            return make_response({'error': error_messages.get(field)}, 400)

    request_object = RequestModel(
        school=request_data['school'],
        class_no=request_data['class_no'],
        score=request_data['score'],
        index=request_data['index'],
        user_id=current_identity.id
    )

    db.session.add(request_object)
    db.session.commit()

    return jsonify(request_object.as_json())


@requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()
    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    return jsonify(request_object)


@requests_bp.route('/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_request(request_id):
    if not request.is_json:
        return make_response({'error': 'Request data type wrong'}, 400)

    request_data = request.get_json(silent=True)
    if not request_data:
        return make_response({'error', "Request data error", 400})

    request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()
    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    request_object.school = request_data['school']
    request_object.class_no = request_data['class_no']
    request_object.score = request_data['score']
    request_object.index = request_data['index']

    db.session.add(request_object)
    db.session.commit()

    return jsonify(request_object.as_json())


@requests_bp.route('/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_request(request_id):
    request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()
    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    db.session.delete(request_object)
    db.session.commit()

    return make_response({'result': 'OK'}, 200)
