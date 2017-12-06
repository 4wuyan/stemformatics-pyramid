from pyramid.view import view_config
from pyra.lib.carrier import EmpClass as c
from pyra.lib.helper import Helper as h

@view_config(route_name='home', renderer="templates/mytemplate.mako")
def my_view(request):
    return {'project': 'pyra'}

#@view_config(route_name='contact_us',renderer="templates/contact_us.mako")
def contact_us(request):
    #set up C
    info=c()
    info.site_name="S4M"
    info.feedback_email="S4M@unimelb.edu.au"
    info.title="S4M_title"
    info.production="true"
    info.debug=None
    info.header="S4M_header"
    info.user="James"
    info.uid=0
    info.full_name="jc w"
    info.notifycation="hello?"
    info.header_selected="expressions"
    #set up H
    helper= h()
    return {'c':info,'h':helper,'project_url':'/'}
