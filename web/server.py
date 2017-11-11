from webob import Request
from paste.httpserver import serve
import os

current_directory = os.getcwd()

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
    
    css = ""
    js = ""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):            
        WsgiMiddleware.sort_includes()
        try:
            response = self.app(environ, start_response).decode() 
            if response.find('<head>') >=0:
                data, headend = response.split('</head>')
                response = data + WsgiMiddleware.css + '</head>' + headend
            if response.find('<body>') >=0:
                data, htmlend = response.split('</body>')
                response = data + WsgiMiddleware.js +'</body>' + htmlend
            yield (response).encode()  
        except FileNotFoundError:
            response_code = '404 Not Found'
            response_type = ('Content-Type', 'text/HTML')
            start_response(response_code, [response_type])
            yield ("404 Not Found").encode()

    #разделим includes на две категории
    def sort_includes():
        for include in WsgiMiddleware.includes:
            if(include.split('.')[1] == 'js'):
                WsgiMiddleware.js += '<script src="/_static/' + include + '"></script>\n'
            else:
                WsgiMiddleware.css += '<link rel="stylesheet" href="/_static/' + include + '"/>\n'

#приложение которое отдает статикой файлы index.html и about.html
#(about.html доступно по ссылке из index.html)
def give_static(environ, start_response):
    path = '\index.html'
    file= open(current_directory+path, 'r')
    response_code = '200 OK'
    response_type = ('Content-Type', 'text/HTML')
    start_response(response_code, [response_type])
    data=file.read() # str to bytes
    return data.encode()

# Оборачиваем WSGI приложение в middleware
give_static = WsgiMiddleware(give_static)

# Запускаем сервер
serve(give_static, host='localhost', port=8000)
