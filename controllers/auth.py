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
                'salt': salt,
                'org_name': org_name,
                'phone_no': phone_no,
                'addr': addr,
                'website_url': website_url,
            })
            ob = {
                'status': {
                    'success': 'true',
                    'code': 201,
                    'message': 'New Business Registered',
                },
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
                    'user_id': str(data['_id']),
                    'name': data['org_name'],
                    'type': 'business'
                })

                data['id'] = str(data['_id'])
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

class AddNewAdminHandler(RequestHandler):

    @coroutine
    def post(self):
        email_id = self.get_argument('email_id')
        password = self.get_argument('password')
        disp_name = self.get_argument('disp_name')

        adminExists = yield db.admins.find_one({'email_id': email_id})

        if not adminExists:
            password, salt = passHash(password)

            yield db.admins.insert({
                    'email_id': email_id,
                    'disp_name': disp_name,
                    'password': password,
                    'salt': salt,
                }
            )
            ob = {
                'status': 'success',
                'code': 201,
                'message': 'New Admin Added'
            }
        else:
            ob = {
                'status': 'false',
                'code': 400,
                'message': 'Admin Already Exists'
            }
        self.write(json_encode(ob))


class AdminLoginHandler(RequestHandler):

    @coroutine
    def post(self):
        email_id = self.get_argument('email_id')
        password = self.get_argument('password')

        data = yield db.admins.find_one({"email_id" : email_id})

        if data:

            if pbkdf2_sha256.verify(data['salt'] + password, data['password']):

                now = datetime.now()
                time = now.strftime("%d-%m-%Y %I:%M %p")

                token = get_token(email_id, time)
                yield db.tokens.insert({
                    'token': token,
                    'user_id': str(data['_id']),
                    'name': data['disp_name'],
                    'type': 'admin'
                })

                data['id'] = str(data['_id'])
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


class LogoutHandler(RequestHandler):

    @coroutine
    def post(self):
        token = self.get_argument('token')
        loggedout = yield db.tokens.remove({'token': token})
        if loggedout:
            ob = {
                'status': {
                    'success': 'true',
                    'code': 200,
                    'message': 'Logout Successful'
                }
            }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 500,
                    'message': 'Logout Not Successful'
                }
            }
        self.write(json_encode(ob))
