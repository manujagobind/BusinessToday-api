from modules import *
from utilities import *


class FeedHandler(RequestHandler):

    @coroutine
    def get(self):

        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token})

        if token_data and token_data['type'].tolower() in ['business']:
            org_id = token_data['user_id']
            org_cursor = db.businesses.find({'_id': org_id})

            data = list()
            while (yield org_cursor.fetch_next):
                org_data = org_cursor.next_object()
                products_cursor = db.products.find({'org_id': org_id})
                data.append(dict({org_data['_id']}))
                while(yield products_cursor.fetch_next):
                    product_data = products_cursor.next_object()

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
