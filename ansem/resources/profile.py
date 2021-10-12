from flask import Blueprint, request, jsonify, make_response
from flask_jwt import jwt_required, current_identity
from ansem.models import UserModel, db
from ansem.utils import password_hash_generate

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

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


@profile_bp.route('', methods=['POST'])
def create_profile():
    request_data = request.get_json()

    if not request_data:
        return make_response({'error': 'Request data error'}, 400)

    for field in fields:
        if field not in request_data:
            return make_response(error_messages.get(field), 400)

    email = request_data['email']

    user = UserModel.query.filter_by(email=email).first()
    if user:
        return make_response({'error': 'User already exist with email'}, 400)

    mobile_no = request_data['mobile_no']

    user = UserModel.query.filter_by(mobile_no=mobile_no).first()
    if user:
        return make_response({'error': 'User already exist with mobile number'}, 400)

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

    for field in fields:
        if field not in request_data:
            return make_response(error_messages.get(field), 400)

    user = UserModel.query.get(current_identity.id)
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

    return jsonify(user)


@profile_bp.route('', methods=['DELETE'])
@jwt_required()
def delete_profile():
    user = UserModel.query.get(current_identity.id)
    db.session.delete(user)
    db.session.commit()

    return make_response({'result': 'OK'}, 200)
