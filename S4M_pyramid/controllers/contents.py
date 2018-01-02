from pyramid_handlers import action
from S4M_pyramid.lib.empty_class import EmptyClass as c
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
from S4M_pyramid.config import *
import psycopg2
import psycopg2.extras

class ContentsController(BaseController):

   

    @action(renderer="templates/contents/contact_us.mako")
    def contact_us(self):
        # set up C
        c.title=c.site_name+" - Contact_us"
        return {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}

    @action(renderer="templates/contents/about_us.mako")
    def about_us(self):
        # set up C
        c.title = c.site_name + " - About_us"
        return {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}
    #faq page wouldn't work without the tutorial list
    @action(renderer="templates/contents/faq.mako")
    def faq(self):
        # set up C
        c.title = c.site_name + " - Faq"
        return {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}

    @action(renderer="templates/contents/our_data.mako")
    def our_data(self):
        # set up C
        c.title = c.site_name + " - Our Data"
        return {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}
    #data_publication page wouldn't work without the data_publication
    @action(renderer="templates/contents/our_publications.mako")
    def our_publications(self):
        # set up C
        c.title = c.site_name + " - Our Publications"
        c.data_publications = Stemformatics_Dataset.get_data_publications()
        return {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}

    @action(renderer="templates/contents/disclaimer.mako")
    def disclaimer(self):
        # set up C
        c.title = c.site_name + " - Disclaimer"
        return {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}

    @action(renderer="templates/contents/privacy_policy.mako")
    def privacy_policy(self):
        # set up C
        c.title = c.site_name + " - Privacy Policy"
        return {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}
