from modules import *

def passHash(password, salt = uuid.uuid4().hex):
    np = salt + password
    return pbkdf2_sha256.hash(np), salt
