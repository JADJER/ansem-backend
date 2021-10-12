from flask import jsonify, Blueprint, request, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import RequestModel, db

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')


@requests_bp.route('', methods=['GET'])
@jwt_required()
def get_all_requests():
    requests = RequestModel.query.filter_by(user_id=current_identity.id).all()
    return jsonify(requests)


@requests_bp.route('', methods=['POST'])
@jwt_required()
def create_request():
    if not request.json:
        return make_response({'error', "Request format error", 400})

    request_object = RequestModel(
        country=request.json['country'],
        city=request.json['city'],
        address=request.json['address'],
        school=request.json['school'],
        score=request.json['score'],
        index=request.json['index'],
        user_id=current_identity.id
    )

    db.session.add(request_object)
    db.session.commit()

    return jsonify(request_object)


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
    if not request.json:
        return make_response({'error', "Request format error", 400})

    request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()
    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    request_object.country = request.json['country']
    request_object.city = request.json['city']
    request_object.address = request.json['address']
    request_object.school = request.json['school']
    request_object.score = request.json['score']
    request_object.index = request.json['index']

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
