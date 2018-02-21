import logging

log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c, url
from pylons import config
from pylons.controllers.util import abort, redirect

from guide.lib.base import BaseController, render

from guide.model.stemformatics import *


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

    #---------------------NOT MIGRATED--------------------------------
    def leukomics(self):
        c.title = c.site_name+" - LEUKomics"
        c.header = 'leukomics'
        return render (url('/projects/leukomics.mako'))

    #---------------------NOT MIGRATED--------------------------------
    def leukomics_data(self):
        c.title = c.site_name+" - LEUKomics"
        c.header = 'leukomics'
        return render (url('/projects/leukomics_data.mako'))

    #---------------------NOT MIGRATED--------------------------------
    def leukomics_publications(self):
        c.title = c.site_name+" - LEUKomics"
        c.header = 'leukomics'
        return render (url('/projects/leukomics.mako'))

    #---------------------NOT MIGRATED--------------------------------
    def project_grandiose(self):

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
        return render (url('/projects/project_grandiose.mako'))

    #---------------------NOT MIGRATED--------------------------------
    def grandiose(self):
        return redirect(url('/projects/project_grandiose'))

    #---------------------NOT MIGRATED--------------------------------
    def iii_main(self):
        return redirect(url('/projects/iiiformatics'))

    #---------------------NOT MIGRATED--------------------------------
    def iiiformatics(self):
        c.title = "3IIIformatics"
        c.header = 'iii_main'
        return render (url('/projects/iiiformatics.mako'))

    #---------------------NOT MIGRATED--------------------------------
    def iii_wellcome(self):
        c.title = "3IIIformatics"
        c.header = 'iii_wellcome'
        return render (url('/projects/iiiformatics_wellcome.mako'))

    #---------------------NOT MIGRATED--------------------------------
    def iii_arthritis(self):
        c.title = "3IIIformatics"
        c.header = 'iii_arthritis'
        return render (url('/projects/iiiformatics_arthritis.mako'))

    #---------------------NOT MIGRATED--------------------------------
    def iii_immunobiology(self):
        c.title = "3IIIformatics"
        c.header = 'iii_immunobiology'
        return render (url('/projects/iiiformatics_immunobiology.mako'))
