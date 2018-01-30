from pyramid_handlers import action
from pyramid.response import Response
from pyramid.renderers import render_to_response
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
import psycopg2
import psycopg2.extras
class ContentsController(BaseController):
    @action(renderer="templates/contents/index.mako")
    def index(self):
        c = self.request.c
        c.header_selected = ''
        c.speed_up_page = 'true'
        c.title = c.site_name + " - Find expression data from leading stem cell laboratories in a format that is easy to search, easy to visualise and easy to export"

        c.tweets = []

        c.number_of_public_samples = Stemformatics_Dataset.get_number_public_samples()
        c.number_of_public_datasets = Stemformatics_Dataset.get_number_of_datasets()['Public']
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/contact_us.mako")
    def contact_us(self):
        c = self.request.c
        # set up C
        c.title=c.site_name+" - Contact Us"
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/about_us.mako")
    def about_us(self):
        c = self.request.c
        # set up C
        c.title = c.site_name + " - About Us"
        return self.deprecated_pylons_data_for_view

    #faq page wouldn't work without the tutorial list
    @action(renderer="templates/contents/faq.mako")
    def faq(self):
        c = self.request.c
        # set up C
        c.title = c.site_name + " - FAQ"
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/our_data.mako")
    def our_data(self):
        c = self.request.c
        # set up C
        c.title = c.site_name + " - Our Data"
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/our_code.mako")
    def our_code(self):
        c = self.request.c
        c.title = c.site_name+" - Our Code"
        return self.deprecated_pylons_data_for_view

    #faq page wouldn't work without the data_publication
    @action(renderer="templates/contents/our_publications.mako")
    def our_publications(self):
        c = self.request.c
        # set up C
        c.title = c.site_name + " - Our Publications"
        c.data_publications = Stemformatics_Dataset.get_data_publications()
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/disclaimer.mako")
    def disclaimer(self):
        c = self.request.c
        # set up C
        c.title = c.site_name + " - Disclaimer"
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/privacy_policy.mako")
    def privacy_policy(self):
        c = self.request.c
        # set up C
        c.title = c.site_name + " - Privacy Policy"
        return self.deprecated_pylons_data_for_view

    @action(renderer='templates/workbench/error_message.mako')
    def registration_submitted(self):
        c = self.request.c
        c.message = "Thank you for registering! Please confirm your registration by following instructions in your confirmation email."
        c.title = "Registration submitted"
        return self.deprecated_pylons_data_for_view

