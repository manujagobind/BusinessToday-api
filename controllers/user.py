from modules import *
from utilities import *


class RetrieveCurrentUserHandler(RequestHandler):

    @coroutine
    def get(self):
        token = self.request.headers['token']
        user_type = self.request.headers['user_type'].lower()

        if user_type in ['admin', 'business']:
            token_data = yield db.tokens.find_one({'token': token, 'type': user_type})

            if token_data and user_type in ['business']:
                user_data = yield db.businesses.find_one({'_id': ObjectId(token_data['user_id'])})
            elif token_data and user_type in ['admin']:
                user_data = yield db.admins.find_one({'_id': ObjectId(token_data['user_id'])})

            if token_data and user_data:
                user_data['id'] = str(user_data['_id'])
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
                        'type': user_type,
                        'data': user_data
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
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid User Type'
                }
            }
        self.write(json_encode(ob))

class RetrieveAllProductsOfCurrentBusinessHandler(RequestHandler):

    @coroutine
    def get(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            cursor = db.products.find({'org_id': token_data['user_id']})
            products = list()
            while (yield cursor.fetch_next):
                product = cursor.next_object()
                product['id'] = str(product['_id'])
                del product['_id']
                products.append(product)
            if products:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'User Has Products'
                    },
                    'response': {
                        'token': token,
                        'data': products    #This is a list
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

        token_data = yield db.tokens.find_one({"token": token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            productAdded = yield db.products.insert({
                'product_title': product_title,
                'product_desc': product_desc,
                'product_price': product_price,
                'org_id': org_id,
            })
            if productAdded:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 201,
                        'message': 'Product Added'
                    }
                }
            else:
                ob = {
                    'status': {
                        'status': 'false',
                        'code': 500,
                        'message': 'Product Not Added'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid token'
                }
            }
        self.write(json_encode(ob))
