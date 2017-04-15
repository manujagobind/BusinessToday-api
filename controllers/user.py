from modules import *
from utilities import *


class RetrieveUserHandler(RequestHandler):

    @coroutine
    def get(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({"token": token})
        if token_data:
            user_data = yield db.businesses.find_one({'email_id': token_data['email_id'], 'type': 'business'})
            if user_data:
                del user_data['_id']
                del user_data['password']
                del user_data['salt']
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'User Exists'
                    },
                    'response': {
                        'token': token,
                        'data': user_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'User Does Not Exist'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))

class RetrieveProductsHandler(RequestHandler):

    @coroutine
    def get(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token})
        if token_data:
            products = yield db.products.find_one({'org_id': token_data['email_id']})   #TODO
            if products:
                del products['_id']
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'User Has Products'
                    },
                    'response': {
                        'token': token,
                        'data': products
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'User Has No Products'
                    },
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))


class AddProductsHandler(RequestHandler):

    @coroutine
    def post(self):
        token = self.get_argument('token')
        product_title = self.get_argument('product_title')
        product_desc = self.get_argument('product_desc')
        product_price = self.get_argument('product_price')

        token_data = yield db.tokens.find_one({"token": token})
        if token_data:
            org_id = token_data['email_id']
            productAdded = yield db.products.insert({
                'product_title': product_title,
                'product_desc': product_desc,
                'product_price': product_price,
                'org_id': org_id
            })
            if productAdded:
                ob = {
                    'status': 'true',
                    'code': 201,
                    'message': 'Product Added'
                }
            else:
                ob = {
                    'status': 'false',
                    'code': 500,
                    'message': 'Product Not Added'
                }
        else:
            ob = {
                'status': 'false',
                'code': 401,
                'message': 'Invalid token'
            }
        self.write(json_encode(ob))

#TODO add product id, get product by id, get user by id
