# inspired by https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/pylons/index.html
# author: WU Yan
# original date: 5 Jan 2018
# last modified: 11 Jan 2018

import pyramid
#from S4M_pyramid.lib.resolve_path_info import path_resolver


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

        has_path_string = len(args) > 0
        if has_path_string:
            host = self.request.application_url
            if host[-1] != '/':
                host += '/'
            url = host + args[0].lstrip('/')
        else:
            url = self.request.route_url(controller_string, action = action_string)
        return url
    #def set_environ(self, request = None):
    #    if not request:
    #        self.request = pyramid.threadlocal.get_current_request()
    #    else:
    #        self.request = request
    #    self.environ = request.environ
    #    resolver = path_resolver(self.request.path_info)
    #    resolver.resolve_path_info()
    #    self.environ['pylons.routes_dict'] = resolver.result
    def set_request(self, request):
        self.request = request


class deprecated_pylons_globals:
    def fetch(self):
        self.request = pyramid.threadlocal.get_current_request()
        self.response = self.request.response
        self.session = self.request.session

magic_globals = deprecated_pylons_globals()
url = url_generator()
