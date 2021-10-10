from flask import Blueprint, request, abort, jsonify
from flask_jwt import jwt_required, current_identity
from ansem.models import UserModel, db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('', methods=["GET"])
@jwt_required()
def get_profile():
    user = UserModel.query.get(current_identity.id)
    return jsonify(user)


@profile_bp.route('', methods=['POST'])
def create_profile():
    if not request.json:
        abort(400)

    email = request.json['email']
    password = request.json['password']

    user = UserModel.query.filter_by(email=email).first()

    if not user:
        user = UserModel(email=email, password=password)

        db.session.add(user)
        db.session.commit()

    return jsonify(user)
