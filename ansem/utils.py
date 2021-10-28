import hashlib
from typing import Dict, Any

from flask import Response, jsonify


def password_hash_generate(password):
    encoded_password = password.encode('utf-8')
    hash_object = hashlib.sha512(encoded_password)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def response_wrapper(success: bool, message: str, data: Dict[str, Any] = None) -> Response:
    if not data:
        return jsonify({"success": success, "message": message})

    return jsonify({"success": success, "message": message, "data": data})
