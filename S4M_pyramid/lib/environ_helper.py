from S4M_pyramid.lib.empty_class import EmptyClass

def generate_environ(current_url):
    url = EmptyClass()
    url_tokens = current_url.split("/")
    action = url_tokens[len(url_tokens)-1]
    controller = url_tokens[len(url_tokens)-2]
    url_var_map = {'action':action,'controller':controller}
    url.environ = {'pylons.routes_dict':url_var_map}
    return url
