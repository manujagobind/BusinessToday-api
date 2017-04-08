from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import os

from routes import *

def main():
    app = Application(route.routing)
    server = HTTPServer(app)
    port = int(os.environ.get("PORT", 5000))
    server.listen(port)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
