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
from asbool import asbool
import S4M_pyramid.lib.helpers as h

class GenesController(BaseController):

    def __init__(self,request): #CRITICAL-3

        super().__init__(request)
        c = self.request.c
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db


        self.default_human_dataset = int(config['default_human_dataset'])
        self.default_mouse_dataset = int(config['default_mouse_dataset'])
        self.useSqlSoup = True

        if 'useSqlSoup' in config:
            self.useSqlSoup = asbool(config['useSqlSoup'])

    def search(self):
        c = self.request.c
        request = self.request
        response = self.request.response
        db = self.db_deprecated_pylons_orm
        c.title = c.site_name+" - Gene Search - Search for your gene of interest"
        c.searchQuery = request.params.get("gene", None)
        if c.searchQuery is None:
            c.searchQuery = request.params.get("filter", None)

        db_id = request.params.get("db_id")
        selected_gene_id = request.params.get("ensembl_id",None)

        yugene_granularity_for_gene_search = config['yugene_granularity_for_gene_search']

        ### to remove later ###
        c.human_ds_id = self.default_human_dataset
        c.mouse_ds_id = self.default_mouse_dataset
        c.ucsc_links = Stemformatics_Auth.get_ucsc_links_for_uid(db,c.uid,db_id)
        c.yugene_graph_data = ""
        c.show_selections = False
        c.firstResult = None
        c.ensembl_id = None
        c.db_id = None

        genes_dict =  {}

        if c.searchQuery:
            c.searchQuery = str(c.searchQuery).encode('utf-8')
            c.title = c.site_name+" - Gene Search for %s" % c.searchQuery

        try:
            if selected_gene_id is not None:
                c.ensembl_id = selected_gene_id
                genes_dict = Stemformatics_Gene.get_genes(db,c.species_dict, selected_gene_id, db_id, False, None)
                c.results = genes_dict
                c.firstResult = genes_dict[c.ensembl_id]
                c.db_id = c.firstResult['db_id']
                c.ucsc_data = Stemformatics_Gene.get_ucsc_data_for_a_gene(db,c.db_id,c.ensembl_id)
                c.gene_set_results = Stemformatics_Gene_Set.get_numbers_for_gene_lists_for_gene(db,c.uid,c.ensembl_id)

            else:
                c.firstResult = None
                c.ensembl_id = ''
                c.db_id = None
                c.gene_set_results = None
                c.ucsc_data = None

        except Exception as e:
            c.firstResult = None
            c.ensembl_id = ''
            c.db_id = None
            c.ucsc_data = None
            c.gene_set_results = None



        export = request.params.get("export",None)
        if export is None:
            if selected_gene_id is not None:
                audit_dict = {'ref_type':'gene_id','ref_id':selected_gene_id,'uid':c.uid,'url':url,'request':request}
                result = Stemformatics_Audit.add_audit_log(audit_dict)
            else:
                # only get the search term if there was no ensembl id
                if c.searchQuery is not None:
                    audit_dict = {'ref_type':'search_term','ref_id':c.searchQuery,'uid':c.uid,'url':url,'request':request}
                    result = Stemformatics_Audit.add_audit_log(audit_dict)

            return render_to_response('S4M_pyramid:templates/genes/search.mako',self.deprecated_pylons_data_for_view,request=self.request)
        else:
            # Task #396 - error with ie8 downloading with these on SSL
            del response.headers['Cache-Control']
            del response.headers['Pragma']


            genes_dict = Stemformatics_Gene.get_genes(db,c.species_dict, c.searchQuery, db_id, False, None)


            response.headers['Content-type'] = 'text/tab-separated-values'
            stemformatics_version = config['stemformatics_version']
            response.headers['Content-Disposition'] = 'attachment;filename=export_stemformatics_'+stemformatics_version+'.tsv'
            response.charset= "utf8"
            data = self._convert_genes_dict_to_csv(selected_gene_id,genes_dict)
            return render_to_response('string',data,request=self.request)

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

    @action(renderer="string")
    def search_and_choose_genes_ajax(self):
        request = self.request
        c = self.request.c
        db = self.db_deprecated_pylons_orm
        temp_data = {}
        search_query = request.params.get("filter", None)
        db_id = request.params.get("db_id")

        max_number = 20
        temp_data = Stemformatics_Gene.search_and_choose_genes(db,c.species_dict,search_query,db_id,max_number)

        json_data = json.dumps(temp_data)

        audit_dict = {'ref_type':'search_term','ref_id':search_query,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return json_data