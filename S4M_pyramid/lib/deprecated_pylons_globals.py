# inspired by https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/pylons/index.html

import pyramid

class tmpl_context:
    pass

# https://docs.galaxyproject.org/en/master/_modules/routes/util.html
class UrlGenerator(object):
    def __call__(self, *args, **kwargs):
        self.request = pyramid.threadlocal.get_current_request()
        is_qualified = kwargs.pop('qualified', False)
        controller_string = kwargs.pop('controller', None)
        action_string = kwargs.pop('action', None)

        url = ''

        if len(args) > 0:
            url = args[0]
            if url.startswith('http'):
                return url
        else:
            url = '/{}/{}'.format(controller_string, action_string)
        if is_qualified:
            host = self.request.application_url
            if host[-1] != '/':
                host += '/'
            url = host + url.lstrip('/')
        return url
    def set_environ(self, request = None):
        if not request:
            self.request = pyramid.threadlocal.get_current_request()
        else:
            self.request = request
        self.environ = request.environ
        controller = None
        action = None
        id_ = None
        path_info = self.request.path_info
        if path_info[0] == '/':
            path_info = path_info[1:]
        tokens = path_info.split('/')
        token_num = len(tokens)
        if token_num > 0:
            controller = tokens[0]
        if token_num > 1:
            action = tokens[1]
        if token_num > 2:
            id_ = tokens[2]
        self.environ['pylons.routes_dict'] = {'controller':controller, 'action':action, 'id':id_}
    def set_request(self, request):
        self.request = request


class MagicGlobalsFromRequest(object):
    '''
    In Pylons, we have
        from pylons import request, response, session
    In Pyramid, we don't have these magic globals any more, and we shouldn't have them.

    Now the presence of the global response and session exists in the request object,
    and in Pyramid you must explicitly tell where the request is.

    In controllers, the incoming request is passed as an argument into the constructor of BaseController,
    and can be later accessed via self.request.

    In models, we shouldn't directly access request in theory. But that occasionally happens.
    In that case, pyramid provides us with "threadlocal.get_current_request()" to get the current request.

    Once you get the request, you can access response and session via
        response = request.response
        session = request.session

    This class is used as a shortcut ONLY FOR MODELS that want to access stuff they're not supposed to see.
        (It should be fine if you really use it to get request/response/session in controllers, but there's
        a neat way as is mentioned above.)
    '''
    def fetch(self):
        self.request = pyramid.threadlocal.get_current_request()
        self.response = self.request.response
        self.session = self.request.session
        self.c = self.request.c

class AppGlobals(object):
    pass
    # """Globals acts as a container for objects available throughout the
    # life of the application

    # """

    # def __init__(self):
    #     """One instance of Globals is created during application
    #     initialization (ie. at server start-up) and is available during requests via the
    #     'app_globals' variable.

    #     In the controller, use:
    #             from pylons import app_globals
    #             print app_globals.someAttribute

    #             Note that this global variable is instantiated when server starts, and is shared amongst
    #             all connections to the server. Hence if a user changes such a variable from one browser,
    #             another will see that change from another browser.
    #     """

    #     from S4M_pyramid.model.stemformatics import Stemformatics_Expression
    #     # the file is created by calling http://<base url>/expressions/setup_all_sample_metadata
    #     # it also sets up the g. in memory as well
    #     self.all_sample_metadata = Stemformatics_Expression.setup_all_sample_metadata()

    #     # The script portal-admin in stemformatics/scripts/sysadmin and stemformatics/sysadmin scripts
    #     # that runs a sql statement that downloads the gene_mappings.raw and the probe_mappings.raw
    #     # This task uses the gene_mappings.raw to manufacture the in memory list for quick access.
    #     # Get the probe mappings and gene mappings setup for bulk import manager


    #     """
    #     This is the only place I could find that runs purely on startup once.
    #     config is updated inside the function.
    #     """
    #     #Stemformatics_Admin.trigger_update_configs()


magic_globals = MagicGlobalsFromRequest()
url = UrlGenerator()
app_globals = AppGlobals()
