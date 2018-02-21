#TODO-1
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import url

from guide.lib.base import BaseController, render

from sqlalchemy import or_, and_, desc

from sqlalchemy.exceptions import *

from paste.deploy.converters import asbool

import json

#for result data only
import math

import logging
log = logging.getLogger(__name__)

# Live querying
from guide.model.stemformatics import *
import re


from pylons import config

connection = db.engine.connect()


class ProbesController(BaseController):
    __name__ = 'ProbesController'

    #---------------------NOT MIGRATED--------------------------------
    def __before__(self):

        super(ProbesController, self).__before__ ()
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db


        self.default_human_dataset = int(config['default_human_dataset'])
        self.default_mouse_dataset = int(config['default_mouse_dataset'])




    # Removed all ajax calls for getting gene search. Still using ajax for getting graph data
    #---------------------NOT MIGRATED--------------------------------
    def multi_map_summary(self):

        probe_id = request.params.get('probe_id')
        ds_id = request.params.get('ds_id')
        db_id = request.params.get('db_id')

        try:
            ds_id = int(ds_id)
        except:
            redirect(url(controller='contents', action='index'), code=404)


        unique_genes = Stemformatics_Probe.get_genes_for_probe([probe_id],db_id,ds_id)

        if unique_genes is None or unique_genes == []:
            redirect(url(controller='contents', action='index'), code=404)

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

        return render('probes/multi_map_summary.mako')



