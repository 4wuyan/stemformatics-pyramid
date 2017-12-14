from pyramid_handlers import action
from pyra.lib.empty_class import EmpClass as c
from pyra.lib.base import BaseController

class ContentsController(BaseController):

    __autoexpose__ = None

    @action(renderer="templates/contact_us.mako")
    def contact_us(self):
        # set up C
        c.title = "S4M_title"
        c.header = ""
        c.user = ""
        c.uid = 0
        c.full_name = ""
        c.notifycation = ""
        c.header_selected = "contents"

        return {'c': c, 'h': self.helper, 'project_url': '/'}