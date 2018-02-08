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
        if c.searchQuery is not None:
            c.searchQuery = c.searchQuery.replace('<script>','').replace('</script>','')

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

    def _convert_genes_dict_to_csv(self,ensembl_id,genes_dict):
        csv_text = "Symbol  Aliases Description Species Ensembl ID  Entrez ID   Chromosome Location\n"
        for gene in genes_dict:
            if ensembl_id is not None and ensembl_id != gene:
               continue
            temp = genes_dict[gene]
            direction ='+' if temp['Location']['direction'] != -1 else '-'
            location = 'chr'+str(temp['Location']['chr'])+':'+str(temp['Location']['start'])+'-'+str(temp['Location']['end'])+','+direction
            csv_text += temp['symbol']+"    "+temp['aliases']+" "+temp['description'].replace('<br />','')+"    "+temp['species']+" "+temp['EnsemblID']+"   "+temp['EntrezID']+"    "+location+"\n"

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
        c.publish_gene_set_email_address = Stemformatics_Auth.get_publish_gene_set_email_address()
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
        c.publish_gene_set_email_address = Stemformatics_Auth.get_publish_gene_set_email_address()
        return self.deprecated_pylons_data_for_view

    #---------------------NOT MIGRATED--------------------------------
    def gene_set_view(self,id):
        gene_set_id = int(id)

        updated_gene_set_description  = request.params.get('description')

        # update gene description if appropriate
        if updated_gene_set_description is not None:
            result = Stemformatics_Gene_Set.update_gene_set_description(db,c.uid,gene_set_id,updated_gene_set_description)

        updated_gene_set_name = request.params.get('gene_set_name')
        # update gene name if appropriate
        if updated_gene_set_name is not None:
            result = Stemformatics_Gene_Set.update_gene_set_name(db,c.uid,gene_set_id,updated_gene_set_name)

        c.publish_gene_set_email_address = Stemformatics_Auth.get_publish_gene_set_email_address()

        result = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
        resultGeneSet = result[0]
        resultGeneSetData = result[1]

        if resultGeneSet.uid == 0:
            c.public = True
            c.title = c.site_name+' Analyses  - View Public Gene List - ' + resultGeneSet.gene_set_name
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/public_gene_set_index'),'View Public Gene Lists'],[h.url('/workbench/gene_set_view'+str(gene_set_id)),'Public Gene List View']]
        else:
            c.public = False
            c.title = c.site_name+' Analyses  - View Gene List - ' + resultGeneSet.gene_set_name
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/gene_set_index'),'Manage Gene Lists'],[h.url('/workbench/gene_set_view'+str(gene_set_id)),'Gene List View']]


        c.result = resultGeneSetData
        c.gene_set = resultGeneSet
        c.db_id = resultGeneSet.db_id
        c.message = request.params.get('message')
        Stemformatics_Auth.set_smart_redirect(h.url('/workbench/gene_set_view/'+str(gene_set_id)))
        return render('workbench/gene_set_view.mako')

    @Stemformatics_Auth.authorise(db)
    def gene_set_bulk_import_manager(self): #CRITICAL-4
        request = self.request
        c = self.request.c
        gene_set_id  = request.params.get('gene_set_id')
        if gene_set_id is not None:
            try:
                gene_set_id = int(gene_set_id)
            except:
                gene_set_id = None
        c.gene_set_id = gene_set_id
        gene_set_name  = request.params.get('gene_set_name')
        gene_set_description = request.params.get('description')
        db_id = request.params.get('db_id')
        geneSetRaw = request.params.get('revalidateText')
        saveGeneSet = request.params.get('saveGeneSet')
        revalidateGeneSet = request.params.get('validate')

        search_type = request.params.get('search_type')

        select_all_ambiguous_raw = request.params.get('select_all_ambiguous')

        if select_all_ambiguous_raw == "1":
            select_all_ambiguous = True
        else:
            select_all_ambiguous = False

        c.select_all_ambiguous = select_all_ambiguous

        saveSet = []
        if saveGeneSet is not None:
            for list in request.POST:
                if list.startswith('ENS') :
                    saveSet.append(list)

            if gene_set_id is not None:
                change_name_result = Stemformatics_Gene_Set.update_gene_set_name(db,c.uid,gene_set_id,gene_set_name)
                change_description_result = Stemformatics_Gene_Set.update_gene_set_description(db,c.uid,gene_set_id,gene_set_description)
                replace_genes_result = Stemformatics_Gene_Set.replace_gene_set_items(db,c.uid,gene_set_id,saveSet)
                if replace_genes_result is None:
                    c.message = "Could not update the Gene List. "
                    c.title = c.site_name+" Analyses - Error saving Gene List"
                    return render_to_response('S4M_pyramid:templates/workbench/error_message.mako',self.deprecated_pylons_data_for_view,request=self.request)
                else:
                    # result should be the gene set id
                    # also change needs_attention to be False
                    result = Stemformatics_Gene_Set.set_needs_attention_to_false(db,c.uid,gene_set_id)
                    default_url =url('/workbench/gene_set_view/'+str(gene_set_id))
                    redirect_url = Stemformatics_Auth.get_smart_redirect(default_url)
                    # now delete redis keys for that gene list
                    Stemformatics_Gene_Set.delete_short_term_redis_keys_for_a_gene_list(gene_set_id)
                    return redirect(redirect_url)
            else:
                result = Stemformatics_Gene_Set.addGeneSet(db,c.uid,gene_set_name,gene_set_description,db_id,saveSet)
                if result is None:
                    c.message = "Could not save Gene List. Please check the Gene List name is unique."
                    c.title = c.site_name+" Analyses - Error saving Gene List"
                    return render_to_response('S4M_pyramid:templates/workbench/error_message.mako',self.deprecated_pylons_data_for_view,request=self.request)
                else:
                    # result should be the gene set id
                    return redirect(url('/workbench/gene_set_view/'+str(result)))

        # this is the entry for the copy
        c.hide_save = False
        if revalidateGeneSet is None and saveGeneSet is None:
            c.hide_save = True

        if geneSetRaw != None and search_type != 'probes_using_chromosomal_locations':
            m = re.findall('[\w\.\-\@]{1,}',geneSetRaw)
        else:
            if geneSetRaw != None and search_type == 'probes_using_chromosomal_locations':
                m = re.findall('[\w\.\-\@\+\:\,]{1,}',geneSetRaw)
            else:
                m = []


        # now input this list into a gene function that will return a dictionary
        # { 'ILMN_2174394' : { 'original' : 'ILMN_2174394', 'symbol' : 'STAT1', 'status' : 'OK' } }
        # If we make it a list of objects then we can sort, we cannot sort on a dictionary
        if m != []:

            if search_type is None:
                search_type = 'all'

            resultData = Stemformatics_Gene.get_unique_gene_fast(db,m,db_id,search_type,select_all_ambiguous)

            c.search_type = search_type
            c.gene_set_processed = resultData
        else:
            c.gene_set_processed = []
            c.search_type = 'all'

        c.gene_set_raw = geneSetRaw
        c.gene_set_raw_list = m

        c.db_id = db_id
        c.error_message = ""
        # return 'Successfully uploaded: %s, size: %i rows' % (myfile.filename, len(m))
        c.title = c.site_name+' Analyses  - New Gene List'
        c.breadcrumbs = [[h.url('/genes/search'),'Genes'],['','Bulk Import Manager']]

        if gene_set_id is not None:
            gene_set_result = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
            db_id = c.db_id = Stemformatics_Gene_Set.get_db_id(db,c.uid,gene_set_id)
            gene_set = gene_set_result[0]
            gene_set_items = gene_set_result[1]

        if c.gene_set_raw is None and gene_set_id is not None:
            c.gene_set_raw = ""
            for gene in gene_set_items:
                c.gene_set_raw += gene.gene_id+"\n"

        if c.gene_set_raw == '' or c.gene_set_raw is None:
            c.gene_set_raw = "Enter list here eg.\nSTAT1\nSTAT2"

        if gene_set_name == 'None' or gene_set_name == '' or gene_set_name is None:
            if gene_set_id is not None:
                gene_set_name = gene_set.gene_set_name
            else:
                gene_set_name = ''

        if gene_set_description == 'None'  or gene_set_description == '' or gene_set_description is None:
            if gene_set_id is not None :
                gene_set_description = gene_set.description
            else:
                gene_set_description = ''
        c.gene_set_name = gene_set_name
        c.description = gene_set_description
        #if revalidateGeneSet == 'Validate':
        #    raise Error
        return render_to_response('S4M_pyramid:templates/workbench/gene_set_manage_bulk_import.mako',self.deprecated_pylons_data_for_view,request=self.request)

    #---------------------NOT MIGRATED--------------------------------
    def merge_gene_sets(self): #CRITICAL-4

        c.analysis = 8

        position  = request.params.get('position')
        gene_set_id  = request.params.get('gene_set_id')
        gene_set_id1  = request.params.get('gene_set_id1')
        gene_set_id2  = request.params.get('gene_set_id2')

        if gene_set_id1 is None and position == '1':
            gene_set_id1 = gene_set_id
        if gene_set_id2 is None and position == '2':
            gene_set_id2 = gene_set_id

        c.title = c.site_name+' Analyses - Merge Gene Lists'
        if gene_set_id1 is None:
            # call a gene list chooser for
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)

            c.public_result = Stemformatics_Gene_Set.getGeneSets(db,0)

            c.result = result
            c.url = h.url('/workbench/merge_gene_sets?position=1')
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/merge_gene_sets'),'Merge Gene Lists - Choose first gene list (Step 1 of 3)']]
            return render('workbench/choose_gene_set.mako')

        else:
            gene_set_id1 = int(gene_set_id1)
            species = Stemformatics_Gene_Set.get_species(db,c.uid,gene_set_id1)
            gene_set_name1 = Stemformatics_Gene_Set.get_gene_set_name(db,c.uid,gene_set_id1)
            c.filter_out_gene_sets = [gene_set_id1]
            db_id = Stemformatics_Gene_Set.get_db_id(db,c.uid,gene_set_id1)

        if gene_set_id2 is None:
            # call a gene list chooser for
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)

            c.public_result = Stemformatics_Gene_Set.getGeneSets(db,0)
            c.filter_by_db_id = db_id
            c.result = result
            c.url = h.url('/workbench/merge_gene_sets?gene_set_id1='+str(gene_set_id1)+'&position=2')
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/merge_gene_sets'),'Merge Gene Lists - Choose second gene list (Step 2 of 3)']]
            return render('workbench/choose_gene_set.mako')

        else:
            gene_set_id2 = int(gene_set_id2)
            gene_set_name2 = Stemformatics_Gene_Set.get_gene_set_name(db,c.uid,gene_set_id2)

        save = request.params.get('save')
        c.gene_set_name = request.params.get('gene_set_name')
        c.description = request.params.get('description')

        if c.gene_set_name is None:
            # get the list of ensemblIDs and then save this against the user
            c.gene_set_name = "Merge Gene Lists "+strftime("%Y-%m-%d %H:%M", gmtime())
            c.description = "From gene lists " + gene_set_name1 + " and " + gene_set_name2 + " Created:"+strftime("%Y-%m-%d %H:%M", gmtime())


        c.url = h.url('/workbench/merge_gene_sets?gene_set_id1='+str(gene_set_id1)+'&gene_set_id2='+str(gene_set_id2))
        if save is None:
            c.db_id = db_id
            c.message = ""
            return render('workbench/choose_gene_set_name.mako')

        result1 = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db,c.uid,gene_set_id1)
        result2 = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db,c.uid,gene_set_id2)
        gene_set_items_raw1 = result1[1]
        gene_set_items_raw2 = result2[1]
        merged_list = []
        for row in gene_set_items_raw1:
            merged_list.append(row.gene_id)
        for row in gene_set_items_raw2:
            merged_list.append(row.gene_id)
        merged_list = list(set(merged_list))

        result = Stemformatics_Gene_Set.addGeneSet(db,c.uid,c.gene_set_name,c.description,db_id,merged_list)
        if result is None:
            c.message = "Could not save Gene List. Please check the Gene List name is unique."
            c.title = c.site_name+" Analyses - Error merging Gene List"
            return render('workbench/error_message.mako')
        else:
            # result should be the gene list id
            redirect(url('/workbench/gene_set_view/'+str(result)))

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
