from flask import jsonify, Blueprint, request, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import *

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')


@requests_bp.route('', methods=['GET'])
@jwt_required()
def get_all_requests():
    requests = RequestModel.query.filter_by(user_id=current_identity.id).all()
    return jsonify(requests)


@requests_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    request_object = RequestModel.query.filter_by(id=request_id, user_id=current_identity.id).first()
    if not request_object:
        return make_response({'error': 'Request not found'}, 400)

    return jsonify(request_object)


@requests_bp.route('', methods=['POST'])
@jwt_required()
def create_request():
    request_query = RequestModel(
        country=request.json['country'],
        city=request.json['city'],
        address=request.json['address'],
        school=request.json['school'],
        score=request.json['score'],
        index=request.json['index'],
    )

    db.session.add(request_query)
    db.session.commit()

    return jsonify(request_query)


# @jwt_required()
# def put():
#     pass
#
#
# @jwt_required()
# def delete():
#     pass
