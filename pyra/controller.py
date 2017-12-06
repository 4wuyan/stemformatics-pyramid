from pyramid_handlers import action
from pyramid.response import Response
from pyra.lib.carrier import EmpClass as c
from pyra.lib.helper import Helper as h
class MyController():
    def __init__(self,request):
        self.request=request
        self.response=request.response

    @action(renderer="templates/mytemplate.mako")
    def test(self):
        return {'project':'pyra'}

    @action(renderer="templates/contact_us.mako")
    def contact_us(self):
        # set up C
        info = c()
        info.site_name = "S4M"
        info.feedback_email = "S4M@unimelb.edu.au"
        info.title = "S4M_title"
        info.production = "true"
        info.debug = None
        info.header = "S4M_header"
        info.user = "James"
        info.uid = 0
        info.full_name = "jc w"
        info.notifycation = "hello?"
        info.header_selected = "expressions"
        # set up H
        helper = h()
        return {'c': info, 'h': helper, 'project_url': '/'}