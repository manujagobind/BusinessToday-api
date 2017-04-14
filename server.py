from controllers.modules import *
from routes import *

def main():
    app = Application(routing)
    server = HTTPServer(app)
    port = int(os.environ.get("PORT", 5000))
    server.listen(port)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
