from modules import *
from utilities import *


class FeedHandler(RequestHandler):

    @coroutine
    def get(self):

        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token})

        if token_data:
            org_id = token_data['email_id']
            org_data = yield db.businesses.find_one({'email_id': org_id})   #TODO
            products_data = yield db.products.find_one({'org_id': org_id})  #TODO
            if products_data:
                del products_data['_id']
                del org_data['_id']
                del org_data['password']
                del org_data['salt']
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'This Organization has listed products'
                    },
                    'response': {
                        'org_data': org_data,
                        'products_data': products_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'This Organization hasn not listed any products yet'
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
