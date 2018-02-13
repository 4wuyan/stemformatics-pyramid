from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from .controllers.workbench import WorkbenchController
from .controllers.contents import ContentsController
from .controllers.expressions import ExpressionsController
from .controllers.auth import AuthController
from .controllers.genes import GenesController
from .controllers.main import MainController
from .controllers.api import ApiController
from .controllers.datasets import DatasetsController

def main(global_config, **settings):
    setup_deprecated_pylons_globals(settings)
    setup_database_connection(settings)
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
    redirect_shortcut(config, '/project_grandiose', '/projects/project_grandiose')
    redirect_shortcut(config, '/leukomics', '/projects/leukomics')
    redirect_shortcut(config, '/', '/contents/index')
    redirect_shortcut(config, '/hamlet/index', '/contents/removal_of_hamlet')
    redirect_shortcut(config, '/tests', '/main/tests')
    redirect_shortcut(config, '/genes', '/genes/search')
    redirect_shortcut(config, '/genes/', '/genes/search')
    redirect_shortcut(config, '/genes/summary', '/expressions/yugene_graph')
    redirect_shortcut(config, '/workbench/gene_set_index', '/genes/gene_set_index')
    redirect_shortcut(config, '/workbench/public_gene_set_index', '/genes/public_gene_set_index')
    redirect_shortcut(config, '/workbench/gene_set_view/{id}', '/genes/gene_set_view/{id}')
    redirect_shortcut(config, '/workbench/gene_set_bulk_import_manager', '/genes/gene_set_bulk_import_manager')
    redirect_shortcut(config, '/workbench/merge_gene_sets', '/genes/merge_gene_sets')
    redirect_shortcut(config, '/admin/check_redis_consistency_for_datasets', '/api/check_redis_consistency_for_datasets')
    redirect_shortcut(config, '/workbench/histogram_wizard', '/expressions/histogram_wizard')
    redirect_shortcut(config, '/expressions', '/contents/index')
    redirect_shortcut(config, '/expressions/', '/contents/index')
    redirect_shortcut(config, '/datasets', '/datasets/search')
    redirect_shortcut(config, '/datasets/', '/datasets/search')

    # the following routing rules correspond to variable controller, i.e. '/{controller}*', in pylons.
    # You can't choose a view class via a routing variable in Pyramid.
    config.add_handler("auth with id", "/auth/{action}/{id}", handler=AuthController)
    config.add_handler("workbench","/workbench/{action}",handler=WorkbenchController)
    config.add_handler("workbench_withID","/workbench/{action}/{id}",handler=WorkbenchController)
    config.add_handler("contents","/contents/{action}",handler=ContentsController)
    config.add_handler("expressions","/expressions/{action}",handler=ExpressionsController)
    config.add_handler("auth","/auth/{action}",handler=AuthController)
    config.add_handler("genes","/genes/{action}",handler=GenesController)
    config.add_handler("main","/main/{action}",handler=MainController)
    config.add_handler("api","/api/{action}",handler=ApiController)
    config.add_handler("datasets","/datasets/{action}",handler=DatasetsController)
    return config.make_wsgi_app()

def setup_deprecated_pylons_globals(settings):
    from .lib.deprecated_pylons_globals import app_globals as g, config
    from .model.stemformatics import Stemformatics_Expression, Stemformatics_Admin

    # update deprecated pylons "config" global
    config.update(settings)
    Stemformatics_Admin.trigger_update_configs()

    # set up g
    g.all_sample_metadata = Stemformatics_Expression.setup_all_sample_metadata()

def setup_database_connection(settings):

    #-------------PostgreSQL----------------------

    from .model.stemformatics import db_deprecated_pylons_orm
    from sqlalchemy import engine_from_config
    engine = engine_from_config(settings, prefix='model.stemformatics.db.')

    # Defer the actual initialisation of the SQLSoup instance,
    # Because we don't have the engine info until this moment.
    db_deprecated_pylons_orm.lazy_init(engine)
    # For more info, see the source code at model/stemformatics/__init__.py

    #---------------------------------------------

    #-------------Redis---------------------------
    from .lib.deprecated_pylons_globals import config
    from .model import redis_interface_normal, redis_interface_for_pickle
    redis_interface_normal.lazy_init(unix_socket_path = config['redis_server'], decode_responses = True)
    redis_interface_for_pickle.lazy_init(unix_socket_path = config['redis_server'])
    #---------------------------------------------

def redirect_shortcut(config, old_path_pattern, new_path_pattern):
    def redirect_view(request):
        path = new_path_pattern.format(**request.matchdict)
        if request.query_string:
            path += '?' + request.query_string
        return HTTPFound(location = path)
    route_name = 'route_name for ' + old_path_pattern.format(controller='controller', action='action', id='id')
    config.add_route(route_name, old_path_pattern)
    config.add_view(redirect_view, route_name=route_name)

def config_static_views(config):
    config.add_static_view(name='static_views', path='public')
    config.add_static_view(name='css', path='public/css')
    config.add_static_view(name='images', path='public/images')
    config.add_static_view(name='js', path='public/js')
    config.add_static_view(name='themes', path='public/themes')
    config.add_static_view(name='img', path='public/img')
    config.add_static_view(name='help', path='public/help')
