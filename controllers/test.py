from modules import *

class testHandler(RequestHandler):

    def get(self):
        ob = {
            'status': {
                'success': 'true',
                'code': 200,
                'message': 'API Server Running',
            }
        }
        self.write(json_encode(ob))
