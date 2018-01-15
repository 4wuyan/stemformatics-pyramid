from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

@view_config(route_name = 'route_name for /error/action')
def redirect_view_1(request):
    return HTTPFound(location = '/error/')

@view_config(route_name = 'route_name for /error/action/id')
def redirect_view_2(request):
    return HTTPFound(location = '/error/')

@view_config(route_name = 'route_name for /project_grandiose')
def redirect_view_3(request):
    return HTTPFound(location = '/projects/project_grandiose')

@view_config(route_name = 'route_name for /leukomics')
def redirect_view_4(request):
    return HTTPFound(location = '/projects/leukomics')

@view_config(route_name = 'route_name for /')
def redirect_view_5(request):
    return HTTPFound(location = '/contents/index')

@view_config(route_name = 'route_name for /hamlet/index')
def redirect_view_6(request):
    return HTTPFound(location = '/contents/removal_of_hamlet')

@view_config(route_name = 'route_name for /tests')
def redirect_view_7(request):
    return HTTPFound(location = '/main/tests')

@view_config(route_name = 'route_name for /genes')
def redirect_view_8(request):
    return HTTPFound(location = '/genes/search')

@view_config(route_name = 'route_name for /genes/')
def redirect_view_9(request):
    return HTTPFound(location = '/genes/search')

@view_config(route_name = 'route_name for /genes/summary')
def redirect_view_10(request):
    return HTTPFound(location = '/expressions/yugene_graph')

@view_config(route_name = 'route_name for /workbench/gene_set_index')
def redirect_view_11(request):
    return HTTPFound(location = '/genes/gene_set_index')

@view_config(route_name = 'route_name for /workbench/public_gene_set_index')
def redirect_view_12(request):
    return HTTPFound(location = '/genes/public_gene_set_index')

@view_config(route_name = 'route_name for /workbench/gene_set_view/id')
def redirect_view_13(request):
    return HTTPFound(location = '/genes/gene_set_view')

@view_config(route_name = 'route_name for /workbench/gene_set_bulk_import_manager')
def redirect_view_14(request):
    return HTTPFound(location = '/genes/gene_set_bulk_import_manager')

@view_config(route_name = 'route_name for /workbench/merge_gene_sets')
def redirect_view_15(request):
    return HTTPFound(location = '/genes/merge_gene_sets')

@view_config(route_name = 'route_name for /admin/check_redis_consistency_for_datasets')
def redirect_view_16(request):
    return HTTPFound(location = '/api/check_redis_consistency_for_datasets')

@view_config(route_name = 'route_name for /workbench/histogram_wizard')
def redirect_view_17(request):
    return HTTPFound(location = '/expressions/histogram_wizard')

@view_config(route_name = 'route_name for /expressions')
def redirect_view_18(request):
    return HTTPFound(location = '/contents/index')

@view_config(route_name = 'route_name for /expressions/')
def redirect_view_19(request):
    return HTTPFound(location = '/contents/index')

@view_config(route_name = 'route_name for /datasets')
def redirect_view_20(request):
    return HTTPFound(location = '/datasets/search')

@view_config(route_name = 'route_name for /datasets/')
def redirect_view_21(request):
    return HTTPFound(location = '/datasets/search')
