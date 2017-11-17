from jinja2 import Environment, FileSystemLoader
from wsgiref.simple_server import make_server
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.view import (view_config, view_defaults)

env = Environment(loader=FileSystemLoader('templates'))

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

#разделим includes на две категории
def sort_includes():
    for include in includes:
        if(include.split('.')[1] == 'js'):
            js.append(include)
        else:
            css.append(include)

#обернуть страницу в шаблон и вернуть ее
def index(request):
     return Response(env.get_template('/index.html').render({'styles':css,'scripts':js}))

def aboutme(request):
    return Response(env.get_template('/about/aboutme.html').render({'styles':css,'scripts':js}))

def home(request):
     return Response(env.get_template('/index.html').render({'styles':css,'scripts':js}))

#вернуть файлы статикой
def give_static():
    with Configurator() as config:
        config.add_route('index', '/index')
        config.add_route('aboutme', '/aboutme')
        config.add_route('home', '/')
        config.add_view(index, route_name='index')
        config.add_view(aboutme,route_name='aboutme')
        config.add_view(home,route_name='home')
        return config.make_wsgi_app()

if __name__ == '__main__':
    sort_includes()
    app=give_static()
    server = make_server('localhost', 8000, app)
    server.serve_forever()
