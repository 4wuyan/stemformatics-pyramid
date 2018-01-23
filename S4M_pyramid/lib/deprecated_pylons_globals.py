# inspired by https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/pylons/index.html
# author: WU Yan
# original date: 5 Jan 2018
# last modified: 23 Jan 2018

import pyramid


class tmpl_context:
    pass

# https://docs.galaxyproject.org/en/master/_modules/routes/util.html
class url_generator:
    def __call__(self, *args, **kwargs):
        self.request = pyramid.threadlocal.get_current_request()
        is_qualified = kwargs.pop('qualified', False)
        controller_string = kwargs.pop('controller', None)
        action_string = kwargs.pop('action', None)

        url = ''

        if len(args) > 0:
            if args[0].startswith('http'):
                url = args[0]
            else:
                host = self.request.application_url
                if host[-1] != '/':
                    host += '/'
                url = host + args[0].lstrip('/')
        else:
            url = self.request.route_url(controller_string, action = action_string)
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


class deprecated_pylons_globals:
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

magic_globals = deprecated_pylons_globals()
url = url_generator()
