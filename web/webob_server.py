from webob import Request
from jinja2 import Environment, FileSystemLoader


#WSGI middleware которое будет вставлять в HTML документ JavaScript и CSS файлы
class WsgiMiddleware(object):
    includes = [
    'app.js',
    'react.js',
    'leaflet.js',
    'D3.js',
    'moment.js',
    'math.js',
    'main.css',
    'bootstrap.css',
   'normalize.css',
   ]
    
    css = []
    js = []
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):            
        WsgiMiddleware.sort_includes()
        response = self.app(environ, start_response)
        yield response.render(styles = WsgiMiddleware.css, scripts = WsgiMiddleware.js).encode()  

    #разделим includes на две категории
    def sort_includes():
        for include in WsgiMiddleware.includes:
            if(include.split('.')[1] == 'js'):
                WsgiMiddleware.js.append(include)
            else:
                WsgiMiddleware.css.append(include)

#WSGI приложение которое отдает статикой файлы index.html и about.html
#(about.html доступно по ссылке из index.html)
def give_static(environ, start_response):
    path = 'index.html'
    response_code = '200 OK'
    response_type = ('Content-Type', 'text/HTML')
    start_response(response_code, [response_type])
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(path)
    return template

# Оборачиваем WSGI приложение в middleware
give_static = WsgiMiddleware(give_static)

req = Request.blank('\index.html')
print(req.get_response(give_static))
