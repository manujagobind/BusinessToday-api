from modules import *

def passHash(password, salt = uuid.uuid4().hex):
    np = salt + password
    return pbkdf2_sha256.hash(np), salt

def get_token(email_id, time):
    return jwt.encode({"email_id" : email_id, "time" : time}, secret, algorithm = 'HS256')
