#-------Last synchronised with Pylons repo (master) on---------------#
#-------------------------5 Feb 2018---------------------------------#
#-------------------------by WU Yan----------------------------------#

import logging

log = logging.getLogger(__name__)

from pyramid_handlers import action
from pyramid.renderers import render_to_response
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Dataset, Stemformatics_Audit
from S4M_pyramid.lib.deprecated_pylons_globals import url
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import redirect
from S4M_pyramid.model.stemformatics import db_deprecated_pylons_orm as db
from S4M_pyramid.model import twitter
import psycopg2
import psycopg2.extras

class ContentsController(BaseController):

    @action()
    def homepage(self):
        return redirect(url('/contents/index'))

    @action(renderer="templates/contents/index.mako")
    def index(self):
        c = self.request.c
        c.header_selected = ''
        c.speed_up_page = 'true'
        c.title = c.site_name+" - Find expression data from leading stem cell laboratories in a format that is easy to search, easy to visualise and easy to export"
        try:
            number = 3
            force_refresh = False
            result= twitter.get_recent_tweets(number,force_refresh)
            c.tweets = result[0]
        except:
            c.tweets = []

        c.number_of_public_samples = Stemformatics_Dataset.get_number_public_samples()
        c.number_of_public_datasets = Stemformatics_Dataset.get_number_of_datasets()['Public']
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/about_us.mako")
    def about_us(self):
        c = self.request.c
        c.title = c.site_name+" - About Us"
        return self.deprecated_pylons_data_for_view

    #---------------------NOT MIGRATED--------------------------------
    def speed_test(self):
        c.title = c.site_name+" - Speed Test"
        return render ('/contents/speed_test.mako')

    @action(renderer="templates/contents/our_data.mako")
    def our_data(self):
        c = self.request.c
        c.title = c.site_name+" - Our Data"
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
        c.title = c.site_name+" - Our Publications"
        c.data_publications = Stemformatics_Dataset.get_data_publications()
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/browser_compatibility.mako")
    def browser_compatibility(self):
        c = self.request.c
        c.title = c.site_name+" - Browser Compatibility"
        return self.deprecated_pylons_data_for_view

    # Faq page wouldn't work without the tutorial list
    @action(renderer="templates/contents/faq.mako")
    def faq(self):
        c = self.request.c
        request = self.request

        c.title = c.site_name+" - FAQ"
        audit_dict = {'ref_id':'faq','ref_type':'help_faq','uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        return self.deprecated_pylons_data_for_view

    @action()
    def help(self):
        return redirect(url('/contents/faq'))

    @action(renderer="templates/contents/contact_us.mako")
    def contact_us(self):
        c = self.request.c
        c.title = c.site_name+" - Contact Us"
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/privacy_policy.mako")
    def privacy_policy(self):
        c = self.request.c
        c.title = c.site_name+" - Privacy Policy"
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/contents/disclaimer.mako")
    def disclaimer(self):
        c = self.request.c
        c.title = c.site_name+" - Disclaimer"
        return self.deprecated_pylons_data_for_view

    @action()
    def hamlet(self):
        return redirect(url('/contents/removal_of_hamlet'))

    @action(renderer="templates/contents/download_mappings.mako")
    def download_mappings(self):
        c = self.request.c
        c.title = c.site_name+" - Download Probe Mappings"
        c.results = Stemformatics_Dataset.get_assay_platform_list(db)
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/workbench/error_message.mako")
    def removal_of_hamlet(self):
        c = self.request.c
        c.message = "After some deliberation, we have decided to remove the Hamlet Interactive Hierarchical Clustering as of v5.0.3 due to stability issues.  We apologise for the inconvenience.  Hierarchical Clusters can still be produced via the Analyses tab."
        c.title = "Removal of Hamlet"
        return self.deprecated_pylons_data_for_view

    @action(renderer='templates/workbench/error_message.mako')
    def registration_submitted(self):
        c = self.request.c
        c.message = "Thank you for registering! Please confirm your registration by following instructions in your confirmation email."
        c.title = "Registration submitted"
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/workbench/error_message.mako")
    def removal_of_comparative_marker_selection(self):
        c = self.request.c
        #redirect(url('/workbench/removal_of_comparative_marker_selection'))

        c.message = "After some deliberation, we have decided to remove the Comparative Marker Selection as of v4.1.  The main reason was that this particular implementation was unstable due to a number of reasons.  We apologise for the inconvenience. "
        c.title = "Removal of Comparative Marker Selection"
        return self.deprecated_pylons_data_for_view
