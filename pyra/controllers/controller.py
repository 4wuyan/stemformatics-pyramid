from pyramid_handlers import action
from pyra.lib.carrier import EmpClass as c
from pyra.lib.helper import Helper as h
from pyra.lib.base import BaseController

class MyController(BaseController):


    @action(renderer="templates/mytemplate.mako")
    def test(self):
        return {'project':'pyra'}

    @action(renderer="templates/contact_us.mako")
    def contact_us(self):
        # set up C
        c.title = "S4M_title"
        c.header = ""
        c.user = ""
        c.uid = 0
        c.full_name = ""
        c.notifycation = "hello?"
        c.header_selected = "contents"
        # set up H
        helper = h(self.request)

        return {'c': c, 'h': helper, 'project_url': '/'}