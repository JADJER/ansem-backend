from flask import Blueprint, request, jsonify, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import UserModel, db
from ansem.utils import password_hash_generate

users_bp = Blueprint('users', __name__, url_prefix='/users')

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


@users_bp.route('', methods=["GET"])
@jwt_required()
def get_users():
    if not current_identity.is_admin:
        return make_response({
            "description": "Access denied",
            "error": "access_denied"
        }, 403)

    users = UserModel.query.all()
    return jsonify(users)


@users_bp.route('', methods=['POST'])
def create_user():
    if not request.is_json:
        return make_response({
            "description": "Request data type wrong",
            "error": "bad_request"
        }, 400)

    request_data = request.get_json(silent=True)
    if not request_data:
        return make_response({
            "description": "Request data error",
            "error": "bad_request"
        }, 400)

    error = {}

    for field in fields:
        if field not in request_data:
            error[field] = error_messages.get(field)

    if error:
        return make_response({'errors': error}, 400)

    email = request_data['email']

    user = UserModel.query.filter_by(email=email).first()
    if user:
        return make_response({
            "description": "User already exist with email",
            "error": "user_exist"
        }, 409)

    mobile_no = request_data['mobile_no']

    user = UserModel.query.filter_by(mobile_no=mobile_no).first()
    if user:
        return make_response({
            "description": "User already exist with mobile number",
            "error": "user_exist"
        }, 409)

    user = UserModel(
        email=email,
        mobile_no=mobile_no,
        password=password_hash_generate(request_data['password']),
        first_name=request_data['first_name'],
        last_name=request_data['last_name'],
        country=request_data['country'],
        city=request_data['city'],
        address=request_data['address']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.as_json())


@users_bp.route('/<int:user_id>', methods=["GET"])
@jwt_required()
def get_user(user_id):
    if not (current_identity.is_admin or user_id == current_identity.id):
        return make_response({
            "description": "Access denied",
            "error": "access_denied"
        }, 403)

    user = UserModel.query.get(user_id)
    if not user:
        return make_response({
            "description": "User not found",
            "error": "not_found"
        }, 400)

    return jsonify(user.as_json())


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    if not (current_identity.is_admin or user_id == current_identity.id):
        return make_response({
            "description": "Access denied",
            "error": "access_denied"
        }, 403)

    if not request.is_json:
        return make_response({
            "description": "Request data type wrong",
            "error": "bad_request"
        }, 400)

    request_data = request.get_json(silent=True)
    if not request_data:
        return make_response({
            "description": "Request data error",
            "error": "bad_request"
        }, 400)

    error = {}

    for field in fields:
        if field not in request_data:
            error[field] = error_messages.get(field)

    if error:
        return make_response({'errors': error}, 400)

    user = UserModel.query.get(user_id)
    if not user:
        return make_response({
            "description": "User not found",
            "error": "not_found"
        }, 400)

    user.email = request_data['email']
    user.mobile_no = request_data['mobile_no']
    user.password = password_hash_generate(request_data['password'])
    user.first_name = request_data['first_name']
    user.last_name = request_data['last_name']
    user.country = request_data['country']
    user.city = request_data['city']
    user.address = request_data['address']

    db.session.add(user)
    db.session.commit()

    return jsonify(user.as_json())


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if not (current_identity.is_admin or user_id == current_identity.id):
        return make_response({
            "description": "Access denied",
            "error": "access_denied"
        }, 403)

    user = UserModel.query.get(user_id)
    if not user:
        return make_response({
            "description": "User not found",
            "error": "not_found"
        }, 400)

    db.session.delete(user)
    db.session.commit()

    return make_response({'result': 'OK'}, 410)
