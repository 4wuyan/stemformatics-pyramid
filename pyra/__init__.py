from pyramid.config import Configurator
from pyra.controllers.contents import ContentsController

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('pyramid_handlers')
    config.add_static_view(name='screen',path='public')
    config.add_handler('contact_us','/contact_us',handler=ContentsController,action='contact_us')
    config.scan()
    return config.make_wsgi_app()
