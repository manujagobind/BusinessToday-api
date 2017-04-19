from modules import *
from utilities import *

class RetrieveProductByIdHandler(RequestHandler):
    def get(self):
        product_id = self.request.headers['product_id']
        
        product_data = yield db.products.find_one({'_id': product_id})

        if product_data:
            ob = {
                'status': {
                    'success': 'true',
                    'code': 200,
                    'message': 'Product Exists',
                },
                'response': {
                    'product_id': product_id,
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
        self.write(json_encode(ob))
