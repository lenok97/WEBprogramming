from wsgiref import simple_server, validate
from jinja2 import Environment, FileSystemLoader

class TrivialWSGIServer(object)
    def __init__(self, app)
        self.app = app
        self.server = simple_server.WSGIServer(
            ('localhost', 8000),
            simple_server.WSGIRequestHandler,
        )
        self.server.set_app(validate.validator(self.app))

    def serve(self)
        self.server.serve_forever()

def runner(app)
    TrivialWSGIServer(app).serve()