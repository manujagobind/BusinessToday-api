from modules import *
from utilities import *

class RetrieveProductByIdHandler(RequestHandler):

    @coroutine
    def get(self):
        product_id = self.request.headers['product_id']
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})

        if token_data:
            product_data = yield db.products.find_one({'_id': ObjectId(product_id)})
            if product_data:
                product_data['id'] = str(product_data['_id'])
                del product_data['_id']
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Product Exists',
                    },
                    'response': {
                        'data': product_data,
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'Product Does Not Exist',
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token',
                }
            }
        self.write(json_encode(ob))
