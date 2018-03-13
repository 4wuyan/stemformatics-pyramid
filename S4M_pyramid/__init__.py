from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from .controllers.workbench import WorkbenchController
from .controllers.contents import ContentsController
from .controllers.expressions import ExpressionsController
from .controllers.auth import AuthController
from .controllers.tests import TestsController
from .controllers.statistics import StatisticsController
from .controllers.genes import GenesController
from .controllers.main import MainController
from .controllers.api import ApiController
from .controllers.admin import AdminController
from .controllers.datasets import DatasetsController
from .controllers.msc_signature import MscSignatureController
from .controllers.projects import ProjectsController
from .controllers.ensembl_upgrade import EnsemblUpgradeController
from .controllers.probes import ProbesController

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
    special_routing(config, '/project_grandiose', controller='projects', action='project_grandiose')
    special_routing(config, '/leukomics', controller='projects', action='leukomics')
    special_routing(config, '/', controller='contents', action='index')
    special_routing(config, '/hamlet/index', controller='contents', action='removal_of_hamlet')
    special_routing(config, '/tests', controller='main', action='tests')
    special_routing(config, '/genes', controller='genes', action='search')
    special_routing(config, '/genes/', controller='genes', action='search')
    special_routing(config, '/genes/summary', controller='expressions', action='yugene_graph')
    special_routing(config, '/workbench/gene_set_index', controller='genes', action='gene_set_index')
    special_routing(config, '/workbench/public_gene_set_index', controller='genes', action='public_gene_set_index')
    special_routing(config, '/workbench/gene_set_view/{id}', controller='genes', action='gene_set_view')
    special_routing(config, '/workbench/gene_set_bulk_import_manager', controller='genes', action='gene_set_bulk_import_manager')
    special_routing(config, '/workbench/merge_gene_sets', controller='genes', action='merge_gene_sets')
    special_routing(config, '/admin/check_redis_consistency_for_datasets', controller='api', action='check_redis_consistency_for_datasets')
    special_routing(config, '/workbench/histogram_wizard', controller='expressions', action='histogram_wizard')
    special_routing(config, '/expressions', controller='contents', action='index')
    special_routing(config, '/expressions/', controller='contents', action='index')
    special_routing(config, '/datasets', controller='datasets', action='search')
    special_routing(config, '/datasets/', controller='datasets', action='search')

    # the following routing rules correspond to variable controller, i.e. '/{controller}*', in pylons.
    # You can't choose a view class via a routing variable in Pyramid.
    config.add_handler("auth with id", "/auth/{action}/{id}", handler=AuthController)
    config.add_handler("workbench","/workbench/{action}",handler=WorkbenchController)
    config.add_handler("workbench_withID","/workbench/{action}/{id}",handler=WorkbenchController)
    config.add_handler("contents","/contents/{action}",handler=ContentsController)
    config.add_handler("expressions","/expressions/{action}",handler=ExpressionsController)
    config.add_handler("auth","/auth/{action}",handler=AuthController)
    config.add_handler("tests","/tests/{action}",handler=TestsController)
    config.add_handler("tests_withID","/tests/{action}/{id}",handler=TestsController)
    config.add_handler("statistics","/statistics/{action}",handler=StatisticsController)
    config.add_handler("genes","/genes/{action}",handler=GenesController)
    config.add_handler("genes_withID","/genes/{action}/{id}",handler=GenesController)
    config.add_handler("main","/main/{action}",handler=MainController)
    config.add_handler("api","/api/{action}",handler=ApiController)
    config.add_handler("datasets","/datasets/{action}",handler=DatasetsController)
    config.add_handler("msc_signature","/msc_signature/{action}",handler=MscSignatureController)
    config.add_handler("projects","/projects/{action}",handler=ProjectsController)
    config.add_handler("ensembl_upgrade","/ensembl_upgrade/{action}",handler=EnsemblUpgradeController)
    config.add_handler("ensembl_upgrade_withID","/ensembl_upgrade/{action}/{id}",handler=EnsemblUpgradeController)
    config.add_handler("admin", "/admin/{action}", handler=AdminController)
    config.add_handler("admin_withID", "/admin/{action}/{id}", handler=AdminController)
    config.add_handler("probes","/probes/{action}",handler=ProbesController)



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

from S4M_pyramid.lib.deprecated_pylons_globals import url
def special_routing(config, path, **kwargs):
    controller = kwargs.get('controller')
    action = kwargs.get('action')
    controller_pointer = eval(controller.capitalize() + 'Controller')

    route_name = 'route_name for ' + path.format(controller='controller', action='action', id='id')
    config.add_handler(route_name, path, handler=controller_pointer, action=action)

    '''
    The code below makes sure things like
    url.environ['pylons.routes_dict']['controller']
    url.environ['pylons.routes_dict']['action']
    get correct values
    '''
    url.special_rules[path] = kwargs

def config_static_views(config):
    config.add_static_view(name='static_views', path='public')
    config.add_static_view(name='css', path='public/css')
    config.add_static_view(name='images', path='public/images')
    config.add_static_view(name='js', path='public/js')
    config.add_static_view(name='themes', path='public/themes')
    config.add_static_view(name='img', path='public/img')
    config.add_static_view(name='help', path='public/help')

    # serve assets that need to be accessed from the root of your domain
    # https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/pylons/static.html
    config.include("pyramid_assetviews")
    filenames = ['robots.txt', 'favicon.ico', 'favicon.png']
    config.add_asset_views("S4M_pyramid:public", filenames=filenames)
