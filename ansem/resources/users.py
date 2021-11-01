from flask import Blueprint, request
from flask_jwt import jwt_required, current_identity
from ansem.models import UserModel, RequestModel, db
from ansem.utils import password_hash_generate, response_wrapper

users_bp = Blueprint('users', __name__, url_prefix='/users')

user_fields = [
    'username',
    'password',
    'first_name',
    'last_name'
]

request_fields = [
    'user_id',
    'school',
    'class',
    'score',
    'index',
    'session_id'
]

error_messages = {
    'username': 'Username is not set',
    'password': 'Password is not set',
    'first_name': 'First name is not set',
    'second_name': 'Second name is not set',
    'last_name': 'Last name is not set',
    'country': 'Country is not set',
    'city': 'City is not set',
    'address': 'Address is not set',
    'mobile_no': 'Mobile number is not set',
    'user_id': 'User ID is not set',
    'school': 'School is not set',
    'class': 'Class is not set',
    'score': 'Score is not set',
    'index': 'Index is not set',
    'session_id': 'Session ID is not set'
}


@users_bp.route('', methods=["GET"])
@jwt_required()
def get_users():
    if not current_identity.is_admin:
        return response_wrapper(success=False, message="Access denied")

    users = UserModel.query.all()
    return response_wrapper(success=True, message="Ok", data=users)


@users_bp.route('', methods=['POST'])
def create_user():
    if not request.is_json:
        return response_wrapper(success=False, message="Request data type wrong")

    request_data = request.get_json(silent=True)
    if not request_data:
        return response_wrapper(success=False, message="Request data error")

    for field in user_fields:
        if field not in request_data:
            return response_wrapper(success=False, message=error_messages.get(field))

    username = request_data['username']

    user = UserModel.query.filter_by(username=username).first()
    if user:
        return response_wrapper(success=False, message="User already exist with email")

    user = UserModel(
        username=username,
        password=password_hash_generate(request_data['password']),
        first_name=request_data['first_name'],
        last_name=request_data['last_name']
    )

    if 'second_name' in request_data:
        user.second_name = request_data['second_name']

    if 'country' in request_data:
        user.country = request_data['country']

    if 'city' in request_data:
        user.city = request_data['city']

    if 'address' in request_data:
        user.address = request_data['address']

    if 'mobile_no' in request_data:
        user.mobile_no = request_data['mobile_no']

    db.session.add(user)
    db.session.commit()

    return response_wrapper(success=True, message="User created", data=user)


@users_bp.route('/<int:user_id>', methods=["GET"])
@jwt_required()
def get_user(user_id):
    if not (current_identity.is_admin or user_id == current_identity.id):
        return response_wrapper(success=False, message="Access denied")

    user = UserModel.query.get(user_id)
    if not user:
        return response_wrapper(success=False, message="User not found")

    return response_wrapper(success=True, message="Ok", data=user)


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    if not (current_identity.is_admin or user_id == current_identity.id):
        return response_wrapper(success=False, message="Access denied")

    if not request.is_json:
        return response_wrapper(success=False, message="Request data type wrong")

    request_data = request.get_json(silent=True)
    if not request_data:
        return response_wrapper(success=False, message="Request data error")

    user = UserModel.query.get(user_id)
    if not user:
        return response_wrapper(success=False, message="User not found")

    if 'password' in request_data:
        user.password = password_hash_generate(request_data['password'])

    if 'first_name' in request_data:
        user.first_name = request_data['first_name']

    if 'second_name' in request_data:
        user.second_name = request_data['second_name']

    if 'last_name' in request_data:
        user.last_name = request_data['last_name']

    if 'country' in request_data:
        user.country = request_data['country']

    if 'city' in request_data:
        user.city = request_data['city']

    if 'address' in request_data:
        user.address = request_data['address']

    if 'mobile_no' in request_data:
        user.mobile_no = request_data['mobile_no']

    db.session.add(user)
    db.session.commit()

    return response_wrapper(success=True, message="Ok", data=user)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if not (current_identity.is_admin or user_id == current_identity.id):
        return response_wrapper(success=False, message="Access denied")

    user = UserModel.query.get(user_id)
    if not user:
        return response_wrapper(success=False, message="User not found")

    db.session.delete(user)
    db.session.commit()

    return response_wrapper(success=True, message='OK')


@users_bp.route('/<int:user_id>/requests', methods=['GET'])
def get_user_requests(user_id):
    requests = RequestModel.query.filter_by(user_id=user_id).all()

    return response_wrapper(success=True, message="Ok", data=requests)


@users_bp.route('/<int:user_id>/requests', methods=['POST'])
def create_user_request(user_id):
    if not request.is_json:
        return response_wrapper(success=False, message="Request data type wrong")

    request_data = request.get_json(silent=True)
    if not request_data:
        return response_wrapper(success=False, message="Request data error")

    for field in request_fields:
        if field not in request_data:
            return response_wrapper(success=False, message=error_messages.get(field))

    request_object = RequestModel(
        school=request_data['school'],
        class_no=request_data['class_no'],
        score=request_data['score'],
        index=request_data['index'],
        user_id=user_id,
        session_id=request_data['session_id'],
    )

    db.session.add(request_object)
    db.session.commit()

    return response_wrapper(success=True, message="Ok", data=request_object)


@users_bp.route('/<int:user_id>/requests/<int:request_id>', methods=['GET'])
def get_user_request(user_id, request_id):
    request_object = RequestModel.query.filter_by(id=request_id, user_id=user_id).first()
    if not request_object:
        return response_wrapper(success=False, message="Request not found")

    return response_wrapper(success=True, message="Ok", data=request_object)


@users_bp.route('/<int:user_id>/requests/<int:request_id>', methods=['PUT'])
def update_user_request(user_id, request_id):
    if not request.is_json:
        return response_wrapper(success=False, message="Request data type wrong")

    request_data = request.get_json(silent=True)
    if not request_data:
        return response_wrapper(success=False, message="Request data error")

    for field in request_fields:
        if field not in request_data:
            return response_wrapper(success=False, message=error_messages.get(field))

    request_object = RequestModel.query.filter_by(id=request_id, user_id=user_id).first()
    if not request_object:
        return response_wrapper(success=False, message="Request not found")

    # TODO Update request

    # request_object.email = request_data['email']
    # request_object.mobile_no = request_data['mobile_no']
    # request_object.first_name = request_data['first_name']
    # request_object.last_name = request_data['last_name']
    # request_object.country = request_data['country']
    # request_object.city = request_data['city']
    # request_object.address = request_data['address']

    db.session.add(request_object)
    db.session.commit()

    return response_wrapper(success=True, message="Ok", data=request_object)


@users_bp.route('/<int:user_id>/requests/<int:request_id>', methods=['DELETE'])
def delete_user_request(user_id, request_id):
    request_object = RequestModel.query.filter_by(id=request_id, user_id=user_id).first()

    if not request_object:
        return response_wrapper(success=False, message="Request not found")

    db.session.delete(request_object)
    db.session.commit()

    return response_wrapper(success=True, message="Ok")
