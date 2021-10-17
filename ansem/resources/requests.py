from flask import jsonify, Blueprint, make_response, request
from flask_jwt import jwt_required, current_identity

from ansem.models import db, RequestModel

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
def get_all_requests():
    if current_identity.is_admin:
        requests = RequestModel.query.all()
    else:
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

    error = {}

    for field in fields:
        if field not in request_data:
            error[field] = error_messages.get(field)

    if error:
        return make_response({'error': error}, 400)

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
    if current_identity.is_admin:
        request_object = RequestModel.query.get(request_id)
    else:
        request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()

    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    return jsonify(request_object)


@requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def update_request(request_id):
    if not request.is_json:
        return make_response({'error': 'Request data type wrong'}, 400)

    request_data = request.get_json(silent=True)
    if not request_data:
        return make_response({'error': 'Request data error'}, 400)

    error = {}

    for field in fields:
        if field not in request_data:
            error[field] = error_messages.get(field)

    if error:
        return make_response({'error': error}, 400)

    request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()
    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    # request_object.email = request_data['email']
    # request_object.mobile_no = request_data['mobile_no']
    # request_object.first_name = request_data['first_name']
    # request_object.last_name = request_data['last_name']
    # request_object.country = request_data['country']
    # request_object.city = request_data['city']
    # request_object.address = request_data['address']

    db.session.add(request_object)
    db.session.commit()

    return jsonify(request_object.as_json())


@requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def delete_request(request_id):
    request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()
    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    db.session.delete(request_object)
    db.session.commit()

    return make_response({'result': 'OK'}, 200)
