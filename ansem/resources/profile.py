import hashlib

from flask import Blueprint, request, jsonify, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import UserModel, db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


def password_hash(password):
    encoded_password = password.encode('utf-8')
    hash_object = hashlib.sha512(encoded_password)
    hex_dig = hash_object.hexdigest()
    return hex_dig


@profile_bp.route('', methods=['POST'])
def create_profile():
    request_data = request.get_json()

    if not request_data:
        return make_response({'error': 'Request data error'}, 400)

    if 'email' not in request_data:
        return make_response({'error': 'Email is not set'}, 400)

    if 'password' not in request_data:
        return make_response({'error': 'Password is not set'}, 400)

    email = request_data['email']
    password = request_data['password']

    user = UserModel.query.filter_by(email=email).first()

    if not user:
        user = UserModel()
        user.email = email
        user.password = password_hash(password)

        if 'first_name' in request_data:
            user.first_name = request_data['first_name']

        if 'last_name' in request_data:
            user.last_name = request_data['last_name']

        db.session.add(user)
        db.session.commit()

    return jsonify(user)


@profile_bp.route('', methods=["GET"])
@jwt_required()
def get_profile():
    user = UserModel.query.get(current_identity.id)
    return jsonify(user)


@profile_bp.route('', methods=['PUT'])
@jwt_required()
def update_profile():
    request_data = request.get_json()

    if not request_data:
        return make_response({'error': 'Request data error'}, 400)

    if 'email' not in request_data:
        return make_response({'error': 'Email is not set'}, 400)

    if 'password' not in request_data:
        return make_response({'error': 'Password is not set'}, 400)

    user = UserModel.query.get(current_identity.id)
    user.email = request_data['email']
    user.password = password_hash(request_data['password'])

    if 'first_name' in request_data:
        user.first_name = request_data['first_name']

    if 'last_name' in request_data:
        user.last_name = request_data['last_name']

    db.session.add(user)
    db.session.commit()

    return jsonify(user)


@profile_bp.route('', methods=['DELETE'])
@jwt_required()
def delete_profile():
    user = UserModel.query.get(current_identity.id)
    db.session.delete(user)
    db.session.commit()

    return make_response({'result': 'OK'}, 200)
