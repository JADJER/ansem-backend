import hashlib


def password_hash_generate(password):
    encoded_password = password.encode('utf-8')
    hash_object = hashlib.sha512(encoded_password)
    hex_dig = hash_object.hexdigest()
    return hex_dig
