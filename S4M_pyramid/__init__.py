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
    # set the path for static views
    config_static_views(config)

    # this dynamically routes the url to the actions
    # the routing order is consistent with the order in pylons project

    # Custom routes are placed first
    config.add_route('route_name for /error/action', '/error/{action}')
    config.add_route('route_name for /error/action/id', '/error/{action}/{id}')
    config.add_route('route_name for /project_grandiose', '/project_grandiose')
    config.add_route('route_name for /leukomics', '/leukomics')
    config.add_route('route_name for /', '/')
    config.add_route('route_name for /hamlet/index', '/hamlet/index')
    config.add_route('route_name for /tests', '/tests')
    config.add_route('route_name for /genes', '/genes')
    config.add_route('route_name for /genes/', '/genes/')
    config.add_route('route_name for /genes/summary', '/genes/summary')
    config.add_route('route_name for /workbench/gene_set_index', '/workbench/gene_set_index')
    config.add_route('route_name for /workbench/public_gene_set_index', '/workbench/public_gene_set_index')
    config.add_route('route_name for /workbench/gene_set_view/id', '/workbench/gene_set_view/{id}')
    config.add_route('route_name for /workbench/gene_set_bulk_import_manager', '/workbench/gene_set_bulk_import_manager')
    config.add_route('route_name for /workbench/merge_gene_sets', '/workbench/merge_gene_sets')
    config.add_route('route_name for /admin/check_redis_consistency_for_datasets', '/admin/check_redis_consistency_for_datasets')
    config.add_route('route_name for /workbench/histogram_wizard', '/workbench/histogram_wizard')
    config.add_route('route_name for /expressions', '/expressions')
    config.add_route('route_name for /expressions/', '/expressions/')
    config.add_route('route_name for /datasets', '/datasets')
    config.add_route('route_name for /datasets/', '/datasets/')
    config.scan('.controllers')

    # the following routing rules correspond to variable controller, i.e. '/{controller}*', in pylons.
    # You can't choose a view class via a routing variable in Pyramid.
    config.add_handler("contents","/contents/{action}",handler=ContentsController)
    config.add_handler("expressions","/expressions/{action}",handler=ExpressionsController)
    config.add_handler("auth","/auth/{action}",handler=AuthController)
    return config.make_wsgi_app()

def config_static_views(config):
    config.add_static_view(name='static_views', path='public')
    config.add_static_view(name='css', path='public/css')
    config.add_static_view(name='images', path='public/images')
    config.add_static_view(name='js', path='public/js')
    config.add_static_view(name='themes', path='public/themes')
    config.add_static_view(name='img', path='public/img')
    config.add_static_view(name='help', path='public/help')
