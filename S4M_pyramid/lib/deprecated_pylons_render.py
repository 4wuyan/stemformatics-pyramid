from S4M_pyramid.lib.empty_class import EmptyClass as c
import S4M_pyramid.lib.helpers as h
from S4M_pyramid.lib.deprecated_pylons_globals import url
from pyramid.renderers import render_to_response

def render(template_path):
    full_path = "S4M_pyramid:templates/" + template_path
    context = {'c':c, 'h':h, 'url':url}
    return render_to_response(full_path, context)
