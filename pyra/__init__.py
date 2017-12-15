from pyramid.config import Configurator
from pyra.controllers.contents import ContentsController

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('pyramid_handlers')
    config.add_static_view(name='static_views',path='public')
    config.add_static_view(name='css',path='public/css')
    config.add_static_view(name='images', path='public/images')
    config.add_handler("contents","/contents/{action}",handler=ContentsController)

    config.scan()
    return config.make_wsgi_app()
