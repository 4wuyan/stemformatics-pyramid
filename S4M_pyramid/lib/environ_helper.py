from S4M_pyramid.lib.empty_class import EmptyClass

def generate_environ(current_url):
    url = EmptyClass()
    url_var_map = {'action':'contact_us','controller':'contents'}
    url.environ = {'pylons.routes_dict':url_var_map}
    return url