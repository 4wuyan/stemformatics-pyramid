import logging

log = logging.getLogger(__name__)

from S4M_pyramid.lib.deprecated_pylons_globals import url, config
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from S4M_pyramid.model.stemformatics import Stemformatics_Auth,Stemformatics_Dataset as db

class ProjectsController(BaseController):
    #---------------------NOT MIGRATED--------------------------------
    def mcri(self):
        # Just keep this under our hat for now - too early to show them and finalise 16/04/2015
        redirect(url(controller='contents', action='index'), code=404)
        c.title = c.site_name + " - Murdoch Children's Research Institute"
        c.header = 'mcri'

        gid = Stemformatics_Auth.get_gid_by_name('MCRI')
        if c.role != 'annotator' and c.role != 'admin':
            result = Stemformatics_Auth.check_uid_in_group(c.uid,gid,c.role)
            if not result:
                redirect(url(controller='contents', action='index'), code=404)

        return render (url('/projects/mcri.mako'))

    @action(renderer="templates/projects/leukomics.mako")
    def leukomics(self):
        c = self.request.c
        c.title = c.site_name+" - LEUKomics"
        c.header = 'leukomics'
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/leukomics_data.mako")
    def leukomics_data(self):
        c = self.request.c
        c.title = c.site_name+" - LEUKomics"
        c.header = 'leukomics'
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/leukomics.mako") 
    def leukomics_publications(self):
        c = self.request.c
        c.title = c.site_name+" - LEUKomics"
        c.header = 'leukomics'
        return self.deprecated_pylons_data_for_view
    
    @action(renderer="templates/projects/project_grandiose.mako") 
    def project_grandiose(self):
        c = self.request.c
        ds_id = 6368
        dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)

        try:
            chip_type =dataset[ds_id]['chip_type']
            c.samer_methylation_probe_name = c.assay_platform_dict[chip_type]['probe_name']
        except:
            c.samer_methylation_probe_name = 'TSS' # default

        ds_ids = [6197,6198,6131,6130,6128]
        c.citations = Stemformatics_Dataset.get_citations_for_dataset_list(ds_ids)

        c.title = c.site_name+" - Project Grandiose"
        c.header = 'grandiose'
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/project_grandiose.mako")
    def grandiose(self):
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/iiiformatics")
    def iii_main(self):
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/iiiformatics.mako")
    def iiiformatics(self):
        c = self.request.c
        c.title = "3IIIformatics"
        c.header = 'iii_main'
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/iiiformatics_wellcome.mako")
    def iii_wellcome(self):
        c = self.request.c
        c.title = "3IIIformatics"
        c.header = 'iii_wellcome'
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/iiiformatics_arthritis.mako")
    def iii_arthritis(self):
        c = self.request.c
        c.title = "3IIIformatics"
        c.header = 'iii_arthritis'
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/projects/iiiformatics_immunobiology.mako")
    def iii_immunobiology(self):
        c = self.request.c
        c.title = "3IIIformatics"
        c.header = 'iii_immunobiology'
        return self.deprecated_pylons_data_for_view
