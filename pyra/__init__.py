from pyramid.config import Configurator
from pyra.controllers.contents import ContentsController

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('pyramid_handlers')
    #set the path for static views
    config_static_views(config)
    #this dynamically routes the url to the actions
    config.add_handler("contents","/contents/{action}",handler=ContentsController)
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