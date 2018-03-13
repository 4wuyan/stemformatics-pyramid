#TODO-1
import logging
from pyramid_handlers import action

from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import redirect
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, app_globals as g, config
from S4M_pyramid.model.stemformatics import db_deprecated_pylons_orm as db, Stemformatics_Probe, Stemformatics_Gene
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Auth, Stemformatics_Dataset, Stemformatics_Expression


from paste.deploy.converters import asbool

import json

import logging
log = logging.getLogger(__name__)


class ProbesController(BaseController):
    __name__ = 'ProbesController'

    def __init__(self,request):
        super().__init__(request)
        c = self.request.c
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db


        self.default_human_dataset = int(config['default_human_dataset'])
        self.default_mouse_dataset = int(config['default_mouse_dataset'])


    # Removed all ajax calls for getting gene search. Still using ajax for getting graph data
    @action(renderer='templates/probes/multi_map_summary.mako')
    def multi_map_summary(self):
        c = self.request.c
        probe_id = self.request.params.get('probe_id')
        ds_id = self.request.params.get('ds_id')
        db_id = self.request.params.get('db_id')

        try:
            ds_id = int(ds_id)
        except:
            return redirect(url(controller='contents', action='index'), code=404)


        unique_genes = Stemformatics_Probe.get_genes_for_probe([probe_id],db_id,ds_id)

        if unique_genes is None or unique_genes == []:
            return redirect(url(controller='contents', action='index'), code=404)

        if len(unique_genes) > 1:
            c.message = "This probe maps to multiple Ensembl identifiers ("


            if int(db_id) == c.human_db:
                c.message = c.message + config['current_human_ensembl_version_text'] + ")"
            else:
                c.message = c.message + config['current_mouse_ensembl_version_text'] + ")"

        else:
            c.message = "This probe does not map to multiple Ensembl identifiers"

        geneList=""
        for gene in unique_genes:
            geneList = geneList + "|" + gene[1]

        geneList = geneList[1:]
        geneDetails = Stemformatics_Gene.get_genes(db,c.species_dict,geneList,db_id,False,None)

        c.geneDetails = geneDetails

        c.title = c.site_name+" - Probe Multi Mapping Summary for " + probe_id
        c.unique_genes = unique_genes
        c.db_id = db_id
        c.probe_id = probe_id

        return self.deprecated_pylons_data_for_view



