import tornado.web
import tornado.escape

class testHandler(tornado.web.RequestHandler):

    def get(self):
        ob = {
            'status': 'OK',
            'response': 'API Server Running'
        }
        self.write(tornado.escape.json_encode(ob))
