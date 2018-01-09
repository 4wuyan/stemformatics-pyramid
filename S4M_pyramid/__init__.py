from pyramid.config import Configurator
from S4M_pyramid.controllers.contents import ContentsController
from S4M_pyramid.controllers.expressions import ExpressionsController
from S4M_pyramid.controllers.auth import AuthController

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('pyramid_handlers')
    config.include('pyramid_beaker')
    #set the path for static views
    config_static_views(config)
    #this dynamically routes the url to the actions
    config.add_handler("contents","/contents/{action}",handler=ContentsController)
    config.add_handler("expressions","/expressions/{action}",handler=ExpressionsController)
    config.add_handler("auth","/auth/{action}",handler=AuthController)
    config.add_handler("index","/",handler=ContentsController,action="index")
    config.scan()
    return config.make_wsgi_app()

def config_static_views(config):
    config.add_static_view(name='static_views', path='public')
    config.add_static_view(name='css', path='public/css')
    config.add_static_view(name='images', path='public/images')
    config.add_static_view(name='js', path='public/js')
    config.add_static_view(name='themes', path='public/themes')
    config.add_static_view(name='img', path='public/img')
    config.add_static_view(name='help', path='public/help')
