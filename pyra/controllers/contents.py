from pyramid_handlers import action
from pyra.lib.empty_class import EmpClass as c
from pyra.lib.base import BaseController

class ContentsController(BaseController):

    __autoexpose__ = None

    @action(renderer="templates/contents/contact_us.mako")
    def contact_us(self):
        # set up C
        c.title=c.site_name+" - Contact_us"
        return {'c': c, 'h': self.helper, 'project_url': '/'}

    @action(renderer="templates/contents/about_us.mako")
    def about_us(self):
        # set up C
        c.title = c.site_name + " - About_us"
        return {'c': c, 'h': self.helper, 'project_url': '/'}
    #faq page wouldn't work without the tutorial list
    @action(renderer="templates/contents/faq.mako")
    def faq(self):
        # set up C
        c.title = c.site_name + " - Faq"
        return {'c': c, 'h': self.helper, 'project_url': '/'}
