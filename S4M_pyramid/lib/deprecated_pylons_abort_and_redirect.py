import pyramid.httpexceptions as e

def abort(code):
    return e.exception_response(code)

def redirect(url, **kwargs):
    '''
    Note that in Pyramid, 404 HTTPNotFound exception doesn't take a redirect location,
    and it seems you have to use 3xx exceptions to perform redirection.
    So here I just use the default 302 HTTPFound, which is also the default code
    in pylons.controllers.util.redirect
    '''
    return e.HTTPFound(url)
