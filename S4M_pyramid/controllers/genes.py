from pyramid_handlers import action
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Auth, Stemformatics_Dataset, Stemformatics_Gene, Stemformatics_Audit, Stemformatics_Expression, Stemformatics_Gene_Set, db_deprecated_pylons_orm as db
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, app_globals as g, config
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
            c.searchQuery = str(c.searchQuery)#encode('utf-8')#Not needed in python3
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
        temp_data = {}
        search_query = request.params.get("filter", None)
        db_id = request.params.get("db_id")

        max_number = 20
        temp_data = Stemformatics_Gene.search_and_choose_genes(db,c.species_dict,search_query,db_id,max_number)

        json_data = json.dumps(temp_data)

        audit_dict = {'ref_type':'search_term','ref_id':search_query,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return json_data

    @action(renderer="templates/genes/feature_search.mako")
    def feature_search(self):
        request = self.request
        c = self.request.c

        c.title = c.site_name+" - Feature Search - Search for your feature of interest"
        c.db_id = db_id = request.params.get("db_id")
        c.feature_type = feature_type = request.params.get("feature_type")
        c.feature_search_term = feature_search_term = request.params.get("feature_search_term")
        use_json = False
        c.extra_message = ""
        if feature_search_term is None or len(feature_search_term) == 0:
            feature_search_term = ""
            c.data = None
        else:
            c.data = Stemformatics_Gene.find_feature_search_items(feature_search_term,db_id,feature_type,use_json)
            if c.data == [] or c.data is None:
                c.data == []
                c.extra_message = "No features found. Please change your search term."
            elif len(c.data) > 100:
                c.data = c.data[0:100]
                c.extra_message = "Too many features found, showing first 100. Please add to your search term."
        return self.deprecated_pylons_data_for_view

    @action(renderer="string")
    def get_feature_search_autocomplete(self):

        request = self.request
        c = self.request.c

        c.feature_search_term = feature_search_term = request.params.get("term")
        c.db_id = db_id = request.params.get("db_id")
        c.feature_type = feature_type = request.params.get("feature_type")
        try:
            species = c.species_dict[int(c.db_id)]['sci_name']
        except:
            species = None

        c.data = Stemformatics_Gene.autocomplete_feature_search_items(feature_search_term,species,feature_type)
        if request.params.get("raise_error") == "true":
            #raise Error
            pass

        return c.data

    def _convert_genes_dict_to_csv(self,ensembl_id,genes_dict):
        csv_text = "Symbol	Aliases	Description	Species	Ensembl ID	Entrez ID	Chromosome Location\n"
        for gene in genes_dict:
            if ensembl_id is not None and ensembl_id != gene:
               continue
            temp = genes_dict[gene]
            direction ='+' if temp['Location']['direction'] != -1 else '-'
            location = 'chr'+str(temp['Location']['chr'])+':'+str(temp['Location']['start'])+'-'+str(temp['Location']['end'])+','+direction
            csv_text += temp['symbol']+"	"+temp['aliases']+"	"+temp['description'].replace('<br />','')+"	"+temp['species']+"	"+temp['EnsemblID']+"	"+temp['EntrezID']+"	"+location+"\n"

        return csv_text

    action(renderer="string")#This might need to change as download may need to be a .tsv file
    def download_yugene(self):
        request = self.request
        c = self.request.c
        response = self.request.response
        geneSearch = request.params.get("gene")
        geneSearch = str(geneSearch)
        c.ensemblID = geneSearch

        db_id = request.params.get("db_id")
        db_id = int(db_id)
        param_view_by = request.params.get("choose_to_view_by")
        if param_view_by is None:
            choose_to_view_by = 0 # cell type
        else:
            choose_to_view_by = int(param_view_by)
        c.choose_to_view_by = choose_to_view_by



        param_show_lower = request.params.get("show_lower")
        if param_show_lower is None:
            show_lower = 'Dataset' # cell type
        else:
            show_lower = param_show_lower

        datasets_dict = Stemformatics_Dataset.get_all_x_platform_datasets_for_user(db,c.uid,db_id)
        c.platform_title =  'None'
        yugene_granularity_for_gene_search = 'full'
        graph_values = Stemformatics_Expression.return_x_platform_matricks_data(db,db_id,datasets_dict,c.ensemblID,choose_to_view_by,show_lower,g.all_sample_metadata,yugene_granularity_for_gene_search)
        del response.headers['Cache-Control']
        del response.headers['Pragma']
        response.headers['Content-type'] = 'text/tab-separated-values'
        stemformatics_version = config['stemformatics_version']
        response.headers['Content-Disposition'] = 'attachment;filename=export_stemformatics_'+stemformatics_version+'.tsv'
        response.charset= "utf8"
        data = "dataset_id\tdataset_name\tsample_id\tprobe_id\tyugene_value\n"

        for row in graph_values['export']:
            data += row+"\n"

        return data

    @action(renderer="templates/workbench/gene_set_index.mako")
    def public_gene_set_index(self):
        request = self.request
        c = self.request.c
        ensembl_id  = request.params.get('ensembl_id')
        initial_filter  = request.params.get('filter')
        uid = 0
        result = Stemformatics_Gene_Set.getGeneSets(db,uid)

        if ensembl_id is not None:
            search_result_for_gene = Stemformatics_Gene_Set.get_numbers_for_gene_lists_for_gene(db,uid,ensembl_id)
            c.gene_sets_in_search = search_result_for_gene[2]
        else:
            c.gene_sets_in_search = None

        if initial_filter is not None:
            c.initial_filter = initial_filter
        else:
            c.initial_filter = ""

        c.message  = request.params.get('message')
        result = Stemformatics_Gene_Set.getGeneSets(db,uid)
        c.result = result
        c.title = c.site_name+' Analyses  - View Gene Lists'
        c.public = True
        c.publish_gene_set_email_address = "email" #Stemformatics_Auth.get_publish_gene_set_email_address()
        c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/gene_set_index'),'View Public Gene Lists']]
        return self.deprecated_pylons_data_for_view


    @action(renderer="templates/workbench/gene_set_index.mako")
    @Stemformatics_Auth.authorise(db)
    def gene_set_index(self):
        request = self.request
        c = self.request.c
        Stemformatics_Auth.set_smart_redirect(h.url('/workbench/gene_set_index'))
        ensembl_id  = request.params.get('ensembl_id')
        initial_filter  = request.params.get('filter')
        c.message  = request.params.get('message')
        if ensembl_id is None:
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
            c.gene_sets_in_search = None
        else:
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
            search_result_for_gene = Stemformatics_Gene_Set.get_numbers_for_gene_lists_for_gene(db,c.uid,ensembl_id)
            c.gene_sets_in_search = search_result_for_gene[2]

        if initial_filter is not None:
            c.initial_filter = initial_filter
        else:
            c.initial_filter = ""

        c.result = result
        c.public = False
        c.title = c.site_name+' Analyses  - View Gene Lists'
        c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/gene_set_index'),'Manage Gene Lists']]
        c.publish_gene_set_email_address = "email" #Stemformatics_Auth.get_publish_gene_set_email_address()
        return self.deprecated_pylons_data_for_view