from pyramid_handlers import action
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.config import config
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
from S4M_pyramid.model.stemformatics.stemformatics_auth import Stemformatics_Auth
from S4M_pyramid.model.stemformatics.stemformatics_gene import Stemformatics_Gene
from S4M_pyramid.model.stemformatics.stemformatics_audit import Stemformatics_Audit
from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression
from S4M_pyramid.model.stemformatics.stemformatics_gene_set import Stemformatics_Gene_Set
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals,url
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
import json
import formencode.validators as fe
import re
from pyramid.renderers import render_to_response
import S4M_pyramid.lib.helpers as h

class GenesController(BaseController):
    @action(renderer="string")
    def get_autocomplete(self):
        c = self.request.c
        db = self.db_deprecated_pylons_orm
        request = self.request
        geneSearch = request.params.get("term")
        try:
            geneSearch = str(geneSearch).strip()
        except:
            return json.dumps([])

        db_id = request.params.get("db_id")

        max_number = 20
        returnData = Stemformatics_Gene.getAutoComplete(db, c.species_dict, geneSearch, db_id, True, max_number)

        return json.dumps(returnData)

