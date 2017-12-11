from pyramid.config import Configurator
from pyra.controllers.controller import MyController

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('pyramid_handlers')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(name='screen',path='pyra:')
    config.add_handler('home','/home',handler=MyController,action='test')
    config.add_handler('contact_us','/contact_us',handler=MyController,action='contact_us')
    config.scan()
    return config.make_wsgi_app()
