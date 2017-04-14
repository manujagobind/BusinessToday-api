from modules import *
from utilities import *

class RegisterBusinessHandler(RequestHandler):

    @coroutine
    def post(self):
        email_id = self.get_argument('email_id')
        password = self.get_argument('password')
        org_name = self.get_argument('org_name')
        phone_no = self.get_argument('phone_no')
        addr = self.get_argument('addr')
        website_url = self.get_argument('website_url')

        isRegistered = yield db.businesses.find_one({'email_id': email_id})

        if not isRegistered:

            password, salt = passHash(password)
            yield db.businesses.insert({
                'email_id': email_id,
                'password': password,
                'org_name': org_name,
                'phone_no': phone_no,
                'addr': addr,
                'website_url': website_url,
                'salt': salt
            })

            now = datetime.now()
            time = now.strftime("%d-%m-%Y %I:%M %p")
            token = jwt.encode({"email_id" : email_id, "time" : time}, secret, algorithm = 'HS256')
            yield db.tokens.insert({
                'token': token,
                'email_id': email_id,
                'org_name': org_name,
            })

            ob = {
                'status': {
                    'success': 'true',
                    'code': 201,
                    'message': 'New Business Registered',
                },
                'response': {
                    'token' : token
                }
            }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 400,
                    'message': 'Business Already Registered',
                },
            }
        self.write(json_encode(ob))


class BusinessLoginHandler(RequestHandler):

    @coroutine
    def post(self):
        email_id = self.get_argument('email_id')
        password = self.get_argument('password')

        data = yield db.businesses.find_one({"email_id" : email_id})

        if data:

            if pbkdf2_sha256.verify(data['salt'] + password, data['password']):

                now = datetime.now()
                time = now.strftime("%d-%m-%Y %I:%M %p")

                token = get_token(email_id, time)
                yield db.tokens.insert({
                    'token': token,
                    'email_id': email_id,
                    'org_name': data['org_name'],
                })

                del data['_id']
                del data['password']
                del data['salt']

                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Login Successful',
                    },
                    'response': {
                        'token' : token,
                        'data' : data,
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 400,
                        'message': 'Invalid Password',
                    },
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 400,
                    'message': 'Invalid Email ID',
                },
            }
        self.write(json_encode(ob))


def AdminLoginHandler(RequestHandler):

    @coroutine
    def post(self):
        pass


def CheckTokenHandler(RequestHandler):

    @coroutine
    def post(self):
        pass
