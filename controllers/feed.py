from modules import *
from utilities import *


class FeedHandler(RequestHandler):

    @coroutine
    def get(self):

        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})

        if token_data:
            org_cursor = db.businesses.find()
            data = list()
            while (yield org_cursor.fetch_next):
                org_data = org_cursor.next_object()
                org_data['id'] = str(org_data['_id'])
                del org_data['_id']
                del org_data['password']
                del org_data['salt']
                
                products_cursor = db.products.find({'org_id': org_data['id']})
                while(yield products_cursor.fetch_next):
                    product = products_cursor.next_object()
                    product['id'] = str(product['_id'])
                    del product['_id']
                    product['org_data'] = org_data
                    data.append(product)

            if data:

                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Products exist'
                    },
                    'response': {
                        'data': data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 404,
                        'message': 'No products exist'
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
