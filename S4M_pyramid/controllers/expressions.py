from pyramid_handlers import action
# c is used to emulate the "from pylons import tmpl_context as c" functionality from Pylons
from S4M_pyramid.lib.empty_class import EmptyClass as c
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


FTS_SEARCH_EXPRESSION = fe.Regex(r"[^\'\"\`\$\\]*", not_empty=False, if_empty=None)
import pyramid.httpexceptions as e

class ExpressionsController(BaseController):
    # 'sca' is short for scatter.  Makes validity checking easier.
    _graphTypes = {'sca': 'scatter', 'bar': 'bar', 'box': 'box', 'default': 'line', 'lin': 'line'}

    def __init__(self,request):
        super().__init__(request)
        c.debug = "True"#turned on debug for result.mako
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        self.default_human_dataset = config['default_human_dataset']
        self.default_mouse_dataset = config['default_mouse_dataset']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db

    @action(renderer="templates/expressions/index.mako")
    def index(self):
        c.title = c.site_name + ' Graphs - Home'
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/expressions/gene_expression_graph.mako")
    def gene_expression_graph(self):
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/expressions/multi_view.mako")
    def multi_view(self):
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/expressions/yugene.mako")
    def yugene(self):
        return self.deprecated_pylons_data_for_view

    @action(renderer="templates/expressions/multi_gene_graph.mako")
    def multi_gene_graph(self):
        return self.deprecated_pylons_data_for_view

    '''This action(and its page) is longer in use'''
    #@action(renderer="templates/expressions/probe_expression_graph.mako")
    #def probe_expression_graph(self):
        # ds_id = 5012 is a valid entry for testing on the pyramid-1 VM
    #    c.ds_id = int(self.request.params.get('ds_id'))
    #    c.db_id = Stemformatics_Dataset.get_db_id(c.ds_id)
    #    c.chip_type = Stemformatics_Dataset.getChipType(c.ds_id)
    #    c.handle = Stemformatics_Dataset.getHandle(self.db_deprecated_pylons_orm,c.ds_id)
    #    return self.deprecated_pylons_data_for_view

    '''Note that this function doesn't use action decorator. because it has more than one possible
    renderer, therefore, render_to_response is used inside the function to respond using different
    renderer'''
    def result(self):
        """ These three functions set what is needed in self._type to be
        used in the graph object orientated code  """
        self._get_inputs_for_graph()  # This is in controllers/expressions.py
        self._check_dataset_status()  # This is in lib/base.py
        result = self._check_gene_status()  # This is in lib/base.py

        db = self.db_deprecated_pylons_orm #pyramid's way to setup orm db

        """ If not result, then there was an error and we want to render an option
        to select a proper gene. With the dataset, if there is no dataset, we
        simply choose a default to render the graph in the background before
        we allow the user to choose a proper dataset.  """
        if isinstance(result,e.HTTPFound):
            return result
        elif result != "1":
            return self._temp.render
        """ This sets the type of graph that will be available. So you can have options
        such as miRNA,gene_set_id  and probeID with an appropriate ref_id.  """
        self._temp.ref_type = 'ensemblID'
        self._temp.ref_id = self._temp.ensemblID

        # changes done for task 2527
        """ This is where the main graph object orientated code is called. """
        # self._temp.this_view = self._setup_graphs(self._temp) #This is in lib/base.py

        """ List of output variables required for setting up the template """
        # c.chip_type = self._temp.this_view.chip_type
        c.ensemblID = c.ref_id = self._temp.ref_id
        c.ref_type = self._temp.ref_type
        c.symbol = self._temp.symbol
        c.dataset_status = self._temp.dataset_status
        c.chip_type = Stemformatics_Dataset.getChipType(c.ds_id)
        c.db_id = self._temp.db_id  # c.db_id is not set in the pylons code,this line is added in pyramid
        # and it gives the error when calling for ucsc data in line 103.
        # still try to work out why the pylons code can get away with not setting up c.db_id

        c.probe_name = Stemformatics_Dataset.get_probe_name(c.ds_id)

        if self._temp.ref_type == 'ensemblID':
            c.ucsc_links = Stemformatics_Auth.get_ucsc_links_for_uid(db, c.uid, c.db_id)
            c.ucsc_data = Stemformatics_Gene.get_ucsc_data_for_a_gene(db, c.db_id, c.ref_id)
            c.data = Stemformatics_Gene.get_genes(db, c.species_dict, self._temp.geneSearch, c.db_id, True, None)
  
        show_limited = True
        if self._temp.ref_type == 'miRNA':
            c.datasets = Stemformatics_Dataset.getAllDatasetDetailsOfOneChipType(db, c.uid, show_limited,
                                                                                 self._temp.ref_type)
        else:
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db, c.uid, show_limited, c.db_id)
        """ This simply get the output of the graph oo code ready for the mako templates """
        # self._set_outputs_for_graph()

        audit_dict = {'ref_type': 'gene_id', 'ref_id': self._temp.ensemblID, 'uid': c.uid, 'url': url,
                      'request': self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type': 'ds_id', 'ref_id': self._temp.ds_id, 'uid': c.uid, 'url': url, 'request': self.request,
                      'extra_ref_type': 'gene_id', 'extra_ref_id': self._temp.ensemblID}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        return render_to_response("S4M_pyramid:templates/expressions/result.mako",self.deprecated_pylons_data_for_view,request=self.request)
    
    @action(renderer="json")
    def graph_data(self):
        # check the gene/ dataset validity
        # than get the data
        self._temp.ds_id = ds_id = int(self.request.params.get("ds_id"))
        self._temp.geneSearch = ref_id = str(self.request.params.get("ref_id"))
        ref_type = str(self.request.params.get("ref_type"))
        self._temp.db_id = db_id = int(self.request.params.get("db_id"))
        format_type = str(self.request.params.get("format_type"))
        graphType = str(self.request.params.get("graphType"))
        select_probes = str(self.request.params.get("select_probes"))
        self._temp.url = self.request.environ.get('PATH_INFO')
        if self.request.environ.get('QUERY_STRING'):
            self._temp.url += '?' + self.request.environ['QUERY_STRING']
        self._check_dataset_status()
        error_data = ""


        # now check the dataset status
        if self._temp.dataset_status != "Available":
            redirect(url(controller='contents', action='index'), code=404)
        if ref_type == "ensemblID":
            result = self._check_gene_status()  #This is in lib/base.py
            if result == "0":
                error_data = "You have not entered a gene that was found."
                return json.dumps({"data": None, "error": error_data})
            if result == "many":
                error_data = "list of genes found"
                return json.dumps({"data": None, "error": error_data})
            if result == "1":
                ref_id = self._temp.ensemblID
        ref_id = ref_id.split(" ")
        data = Stemformatics_Expression.get_expression_graph_data(ds_id,ref_id,ref_type,db_id)
        if data == [] :
            data = None
            error_data = "Data Not found for Selected Parameters. Please choose different Parameters."

        if format_type == "tsv":
            self._temp.formatted_data = Stemformatics_Expression.change_graph_data_format(data,"tsv")
        else:
            self._temp.formatted_data = Stemformatics_Expression.change_graph_data_format(data,"json")

        # add to audit
        if ref_type == 'gene_set_id':
            ref_type = 'gene_set_id'
            #we dont want ref_type 'gene_id' and ref_id 1993 (which is gene list) , cause than when building redis keys 1993 get picked as gene
            # everything else could be gene_id , even if miRNA because the level would be gene_id anyway and it need to be broken into probe level data. But for gene_Set_id level is one higher than gene_id and we wantto distinguish
        else:
            ref_type = 'gene_id'
        audit_dict = {'ref_type':ref_type,'ref_id':self._temp.geneSearch,'uid':c.uid,'url':url,'request': self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type':'ds_id','ref_id':self._temp.ds_id,'uid':c.uid,'url':url,'request': self.request, 'extra_ref_type':ref_type, 'extra_ref_id':self._temp.geneSearch}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return json.dumps({"data":self._temp.formatted_data, "error": error_data})
    @action(renderer="json")
    def dataset_metadata(self):
        self._temp.ds_id = ds_id = int(self.request.params.get("ds_id"))
        error_data =""
        self._check_dataset_status()
        # now check the dataset status
        if self._temp.dataset_status != "Available":
            error_data = self._temp.error_message
            return json.dumps({"data":None,"error":error_data})
        dataset_metadata = Stemformatics_Dataset.get_expression_dataset_metadata(ds_id)

        json_dataset_metadata = json.dumps(dataset_metadata)
        return json.dumps({"error":error_data,"data":json_dataset_metadata})
    
    def _get_inputs_for_graph(self):
        choose_dataset_immediately = False
        probeSearch = self.request.params.get('probe')
        #sets the variable to "" instead of None,if parameter is not provided.
        c.select_probes = select_probes = self.request.params.get('select_probes','')
        geneSearch = FTS_SEARCH_EXPRESSION.to_python(self.request.params.get('gene'))
        feature_type = self.request.params.get('feature_type')
        feature_id = self.request.params.get('feature_id')
        original_temp_datasets = self.request.params.get('datasets')
        force_choose = self.request.params.get('force_choose')
        c.graphType = str(self.request.params.get("graphType"))

        db = self.db_deprecated_pylons_orm

        try:
            db_id = int(self.request.params.get('db_id'))
        except:
            db_id = None

        try:
            first_check = self.request.params.get('ds_id')
            second_check = self.request.params.get('datasetID')
            if first_check is not None:
                ds_id = int(first_check)
            else:
                ds_id = int(second_check)
        except:
            ds_id = None

        if ds_id is None:
            choose_dataset_immediately = True

            if db_id == self.mouse_db:
                ds_id = int(self.default_mouse_dataset)
            else:
                ds_id = int(self.default_human_dataset)

        c.list_of_valid_graphs = Stemformatics_Dataset.list_of_valid_graphs_for_dataset(ds_id)

        graphType = Stemformatics_Dataset.check_graphType_for_dataset(db, ds_id, self.request.params.get('graphType'),
                                                                      c.list_of_valid_graphs)
        sortBy = self.request.params.get('sortBy','')

        # This was an error with T#2079 where the graphType was originally line, but was changed to box
        # but the sortBy was still LineGraphGroup and that caused an error later on
        if graphType != 'line' and sortBy == 'LineGraphGroup':
            sortBy = 'Sample Type'

        self._temp.feature_type = feature_type
        self._temp.feature_id = feature_id
        self._temp.select_probes = select_probes
        self._temp.probeSearch = probeSearch
        self._temp.geneSearch = geneSearch
        c.db_id = self._temp.db_id = db_id
        c.graph_type = self._temp.graphType = graphType
        c.sortBy = self._temp.sortBy = sortBy
        c.ds_id = self._temp.ds_id = ds_id
        c.choose_dataset_immediately = self._temp.choose_dataset_immediately = choose_dataset_immediately
        c.allow_genePattern_analysis = Stemformatics_Dataset.allow_genePattern_analysis(db, self._temp.ds_id)
        self._temp.url = self.request.environ.get('PATH_INFO')

        self._temp.original_temp_datasets = original_temp_datasets
        self._temp.force_choose = force_choose

        if self.request.environ.get('QUERY_STRING'):
            self._temp.url += '?' + self.request.environ['QUERY_STRING']
        self._temp.large = self.request.params.get('size') == "large"

        c.url = self._temp.url

    def probe_result(self):
        db=self.db_deprecated_pylons_orm
        self._get_inputs_for_graph()
        c.chip_type = Stemformatics_Dataset.getChipType(db,c.ds_id)
        self._check_dataset_status()
        c.dataset_status = self._temp.dataset_status
        c.ref_type = self._temp.ref_type = 'probeID'
        show_limited = True
        if self._temp.ref_type == 'miRNA':
            c.datasets = Stemformatics_Dataset.getAllDatasetDetailsOfOneChipType(db,c.uid,show_limited,self._temp.ref_type)
        else:
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited,c.db_id)
        c.symbol = c.ref_id = self._temp.ref_id = self._temp.probeSearch
        if self._temp.select_probes is None:
            self._temp.select_probes = self._temp.probeSearch

        c.probe_name = Stemformatics_Dataset.get_probe_name(c.ds_id)

        # self._temp.this_view = self._setup_graphs(self._temp)
        # self._set_outputs_for_graph()
        audit_dict = {'ref_type':'ds_id','ref_id':self._temp.ds_id,'uid':c.uid,'url':url,'request':self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        return render_to_response("S4M_pyramid:templates/expressions/result.mako",self.deprecated_pylons_data_for_view,request=self.request)

    
    @action(renderer="/expressions/choose_dataset.mako")
    def choose_dataset(self):
        graphType = self.request.params.get("graphType","")
        gene = self.request.params.get("gene","")
        db_id = self.request.params.get("db_id","")
        gene_set_id = self.request.params.get("gene_set_id","")
        c.db_id = int(db_id)
        db=self.db_deprecated_pylons_orm

        if gene_set_id is None:
            c.url = h.url('/expressions/result?graphType='+str(graphType)+'&gene='+str(gene)+'&db_id='+str(db_id))
            show_limited = True

        else:
            c.url = h.url('/workbench/histogram_wizard?gene_set_id='+str(gene_set_id)+'&gene='+str(gene)+'&db_id='+str(db_id))
        c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited,c.db_id)

        c.species = Stemformatics_Dataset.returnSpecies(c.db_id)

        return self.deprecated_pylons_data_for_view

    def histogram_wizard(self):  # CRITICAL-4

        c.analysis = 3
        c.title = c.site_name + ' Analyses  - MultiGene Expression Graph Wizard'
        db = self.db_deprecated_pylons_orm
        #try: #this block is not in use
        #    db_id = int(db_id)
        #except:
        #    db_id = None
        try:
            ds_id = datasetID = int(self.request.params.get('datasetID'),'')
        except:
            ds_id = datasetID = None

        try:
            gene_set_id = int(self.request.params.get('gene_set_id'))
        except:
            gene_set_id = None

        if gene_set_id is None:
            # call a gene list chooser for
            try:
                result = Stemformatics_Gene_Set.getGeneSets(db, c.uid)
            except:
                result = None
            c.result = result
            c.public_result = Stemformatics_Gene_Set.getGeneSets(db, 0)
            c.url = h.url('/workbench/histogram_wizard')
            if ds_id is not None:
                c.filter_by_db_id = Stemformatics_Dataset.get_db_id(db, ds_id)
                c.url += '?datasetID=' + str(ds_id) + '&graphType=default'

            c.breadcrumbs = [[h.url('/workbench/index'), 'Analyses'],
                             ['', 'MultiGene Expression Graph - Choose Gene List (Step 1 of 2)']]
            return render_to_response('S4M_pyramid:templates/workbench/choose_gene_set.mako',self.deprecated_pylons_data_for_view,request=self.request)

        else:
            gene_set_id = int(gene_set_id)
            # check if user has access to gene list
            status = Stemformatics_Gene_Set.check_gene_set_availability(gene_set_id, c.uid)
            if status == False:
                redirect(url(controller='contents', action='index'), code=404)
            species = Stemformatics_Gene_Set.get_species(db, c.uid, gene_set_id)
            c.gene_set_name = gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db, c.uid, gene_set_id)
            db_id = Stemformatics_Gene_Set.get_db_id(db, c.uid, gene_set_id)

        if datasetID is None:
            # now get the dataset ID
            c.species = species
            show_limited = False
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db, c.uid, show_limited, db_id)
            c.breadcrumb_title = 'Choose Dataset for MultiGene Expression Graph'
            c.url = h.url('/workbench/histogram_wizard?graphType=default&db_id=' + str(db_id) + '&gene_set_id=' + str(
                gene_set_id))
            c.breadcrumbs = [[h.url('/workbench/index'), 'Analyses'],
                             [h.url('/workbench/histogram_wizard'), 'MultiGene Expression Graph - Choose Gene List'], [
                                 h.url('/workbench/histogram_wizard?db_id=' + str(db_id) + '&gene_set_id=' + str(
                                     gene_set_id)), 'MultiGene Expression Graph - Choose Dataset (Step 2 of 2)']]

            return render_to_response('S4M_Pyramid:templates/workbench/choose_dataset.mako',self.deprecated_pylons_data_for_view,request=self.request)

        c.dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db, ds_id, c.uid)
        c.probe_name = Stemformatics_Dataset.get_probe_name(ds_id)
        if c.dataset_status != "Available":
            return redirect(url(controller='contents', action='index'), code=404)

        # want to check if dataset_id has more than a sample type "limit_sort_by" option
        comparison_type = self.request.params.get('sortBy')

        datasetMetadataResult = Stemformatics_Dataset.getExpressionDatasetMetadata(db, datasetID, c.uid)
        c.comparison_type = datasetMetadataResult['limit_sort_by'].split(',')

        if comparison_type is None or comparison_type not in c.comparison_type:

            if datasetMetadataResult is None:
                return redirect(url(controller='contents', action='index'), code=404)

            num_options = len(c.comparison_type)

            if num_options > 1:
                # have to now display an option for which type to choose

                c.purple_title = 'Choose Sort By Attribute'
                c.help_text = 'There are multiple viewing options to sort by for this dataset. Select the attribute you would like to use for this graph.'

                c.options = {}
                for comparison_type in c.comparison_type:
                    c.options[comparison_type] = comparison_type

                c.breadcrumbs = [[h.url('/workbench/index'), 'Analyses'], [h.url('/workbench/histogram_wizard'),
                                                                           'MultiGene Expression Graph - Choose Gene List'],
                                 [h.url('/workbench/histogram_wizard?db_id=' + str(db_id) + '&gene_set_id=' + str(
                                     gene_set_id)), 'MultiGene Expression Graph - Choose Dataset'],
                                 ['#', 'MultiGene Expression Graph - Choose Comparion Type (Step 3 of 3)']]

                c.url = h.url(
                    '/workbench/histogram_wizard?graphType=default&db_id=' + str(db_id) + '&gene_set_id=' + str(
                        gene_set_id) + '&datasetID=' + str(datasetID)) + '&sortBy='
                return render_to_response('S4M_pyramid:templates/workbench/generic_choose.mako',self.deprecated_pylons_data_for_view,request=self.request)
            else:
                comparison_type = c.comparison_type[0]

        c.comparison_type_chosen = comparison_type

        # Create a GeneQuery instance.
        if gene_set_id is None:
            # error_handling_for_invalid_search_string()
            return redirect(url(controller='contents', action='index'), code=404)

        gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db, c.uid, gene_set_id)

        if gene_set_name is None:
            return redirect(url(controller='contents', action='index'), code=404)

        c.ref_type = self._temp.ref_type = "gene_set_id"
        c.symbol = c.ref_id = self._temp.ref_id = gene_set_id
        self._temp.probeSearch = ""
        self._temp.geneSearch = ""
        c.select_probes = self._temp.select_probes = self.request.params.get('select_probes')
        c.db_id = self._temp.db_id = db_id
        c.list_of_valid_graphs = Stemformatics_Dataset.list_of_valid_graphs_for_dataset(ds_id)
        graphType = Stemformatics_Dataset.check_graphType_for_dataset(db, ds_id, self.request.params.get('graphType'),
                                                                      c.list_of_valid_graphs)
        c.graphType = self._temp.graphType = graphType
        c.sortBy = self._temp.sortBy = comparison_type
        c.ds_id = self._temp.ds_id = ds_id
        c.choose_dataset_immediately = self._temp.choose_dataset_immediately = False
        c.chip_type = Stemformatics_Dataset.getChipType(db, c.ds_id)
        gene_set_items = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db, c.uid, gene_set_id)
        self._temp.url = self.request.environ.get('PATH_INFO')

        self._temp.original_temp_datasets = None
        self._temp.force_choose = None

        if self.request.environ.get('QUERY_STRING'):
            self._temp.url += '?' + self.request.environ['QUERY_STRING']
        self._temp.large = self.request.params.get('size') == "large"

        c.url = self._temp.url
        self._check_dataset_status()
        c.dataset_status = self._temp.dataset_status

        show_limited = True
        if self._temp.ref_type == 'miRNA':
            c.datasets = Stemformatics_Dataset.getAllDatasetDetailsOfOneChipType(db, c.uid, show_limited,
                                                                                 self._temp.ref_type)
        else:
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db, c.uid, show_limited, c.db_id)
        # self._check_gene_status()

        # self._temp.this_view = self._setup_graphs(self._temp)
        # self._set_outputs_for_graph()
        c.breadcrumbs = [[h.url('/workbench/index'), 'Analyses'],
                         [h.url('/workbench/histogram_wizard'), 'MultiGene Expression Graph - Choose Gene List'],
                         [h.url('/workbench/histogram_wizard?db_id=' + str(db_id) + '&gene_set_id=' + str(gene_set_id)),
                          'MultiGene Expression Graph - Choose Dataset'], ['#', 'Show MultiGene Expression Graph']]
        audit_dict = {'ref_type': 'gene_set_id', 'ref_id': gene_set_id, 'uid': c.uid, 'url': url, 'request': self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type': 'ds_id', 'ref_id': ds_id, 'uid': c.uid, 'url': url, 'request': self.request,
                      'extra_ref_type': 'gene_set_id', 'extra_ref_id': str(gene_set_id)}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        # now add entry for gene set items for gene_set_id so that this can be used in building redis keys
        gene_names = []
        for gene in gene_set_items[1]:
            gene_names.append(gene.gene_id)
        audit_dict = {'ref_type': 'ds_id', 'ref_id': ds_id, 'uid': c.uid, 'url': url, 'request': self.request,
                      'extra_ref_type': 'gene_set_items', 'extra_ref_id': json.dumps(gene_names)}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return render_to_response('S4M_pyramid:templates/expressions/result.mako',self.deprecated_pylons_data_for_view,request=self.request)

    def multi_dataset_result(self):
        db = self.db_deprecated_pylons_orm
        if c.uid == 0 or c.uid == "":
            c.message = "You do not have access to this page. Please check you are logged in."
            c.title = c.site_name+" Multiview - No access"
            return render_to_response('S4M_pyramid:templates/workbench/error_message.mako',self.deprecated_pylons_data_for_view,request=self.request)

        self._temp._multiple = True
        self._get_inputs_for_graph()
        result = self._check_gene_status()
        if result != "1":
            return self._temp.render

        result = self._check_multiple_datasets_status()
        if not result:
            return self._temp.render
        c.ref_type= self._temp.ref_type = 'ensemblID'
        c.ref_id = self._temp.ref_id = self._temp.ensemblID
        c.ds_id = self._temp.ds_id
        c.db_id = self._temp.db_id
        c.multi_view_datasets = self._temp.datasets
        self._get_multiple_dataset_results()

        if self._temp.ref_type == 'ensemblID':
            c.ensemblID = self._temp.ensemblID
            c.ucsc_links = Stemformatics_Auth.get_ucsc_links_for_uid(db,c.uid,c.db_id)
            c.ucsc_data = Stemformatics_Gene.get_ucsc_data_for_a_gene(db,c.db_id,c.ensemblID)
            c.data = Stemformatics_Gene.get_genes(db,c.species_dict,self._temp.geneSearch,c.db_id,True,None)
            c.symbol = self._temp.symbol

        try:
            if self._temp._multiple:
                c.view_data = {}
                c.chip_type = {}
                for ds_id in self._temp.datasets:
                    c.view_data[ds_id] = self._temp.view_data[ds_id]
                    # get chip_type for all selected datasets
                    c.chip_type[ds_id] = Stemformatics_Dataset.getChipType(ds_id)
            else:
                c.view_data = self._temp.view_data[ds_id]
        except:
            c.view_data = self._temp.view_data[ds_id]


        # self._set_outputs_for_graph()
        c.url = self._temp.url
        c.dataset_status = self._temp.dataset_status
        show_limited = True

        if self._temp.ref_type == 'miRNA':
            c.datasets = Stemformatics_Dataset.getAllDatasetDetailsOfOneChipType(db,c.uid,show_limited,self._temp.ref_type)
        else:
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited,c.db_id)

        audit_dict = {'ref_type':'gene_id','ref_id':self._temp.ensemblID,'uid':c.uid,'url':url,'request':self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)


        for ds_id in self._temp.datasets:
            audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':self.request}
            result = Stemformatics_Audit.add_audit_log(audit_dict)

        return render_to_response('S4M_pyramid:templates/expressions/multi_dataset_result.mako',self.db_deprecated_pylons_orm,request=self.request)

    def _check_multiple_datasets_status(self):
        db=self.db_deprecated_pylons_orm
        graphType = self._temp.graphType
        db_id = self._temp.db_id
        original_temp_datasets = self._temp.original_temp_datasets
        ensemblID = self._temp.ensemblID
        force_choose = self._temp.force_choose
        sortBy = self._temp.sortBy
        symbol = self._temp.symbol

        if original_temp_datasets is not None:
            temp_datasets = original_temp_datasets.split(',')
            datasets = [int(i) for i in temp_datasets]

            # Will have to save this now
            Stemformatics_Auth.save_multi_datasets(db, c.uid, db_id, datasets)
        else:
            datasets = Stemformatics_Auth.get_multi_datasets(db, c.uid, db_id)
            # datasets = []

        c.base_url = h.url(
            '/expressions/multi_dataset_result?gene=' + str(ensemblID) + '&db_id=' + str(db_id) + '&graphType=' + str(
                graphType))

        if len(datasets) < 2 or force_choose == 'yes':
            c.species = Stemformatics_Gene.get_species_from_db_id(db, db_id)
            show_limited = True
            c.all_datasets = Stemformatics_Dataset.getChooseDatasetDetails(db, c.uid, show_limited, db_id)
            c.loaded_datasets = json.dumps(datasets)
            c.analysis = 1
            c.purple_title = "Multi Dataset Graph Selection"
            c.help_text = "Please choose the four datasets you would like to see in your multi-dataset graph."
            c.breadcrumbs = [[h.url('/genes/search'), 'Gene Search'],
                             [h.url('/genes/search?gene=' + str(symbol)), symbol],
                             [h.url('/genes/summary?gene=' + str(ensemblID) + '&db_id=' + str(db_id)),
                              symbol + ' Summary'], ['', 'Choose multiple datasets']]
            c.title = c.site_name + " - Choose Datasets for Multiview - Choose multiple datasets to view concurrently for gene " + symbol
            self._temp.render = render_to_response('S4M_pyramid:expressions/choose_multi_datasets.mako',self.deprecated_pylons_data_for_view,request=self.request)
            return False

        # this is always false for multiview graphs
        self._temp.choose_dataset_immediately = False

        self._temp.datasets = datasets

        return True

    def _get_multiple_dataset_results(self):
        ensemblID = self._temp.ensemblID
        datasets = self._temp.datasets
        result = {}
        dataset_status = {}
        self._temp.view_data = {}
        for ds_id in datasets:

            # check user has access first
            dataset_status[ds_id] = Stemformatics_Dataset.check_dataset_with_limitations(db, ds_id, c.uid)

            if dataset_status[ds_id] == "Unavailable":
                if c.uid == '' or c.uid == 0:
                    # got this code from decorator in model/stemformatics/stemformatics_auth.py
                    c.user = None
                    session = self.request.session
                    session['path_before_login'] = self.request.path_info + '?' + self.request.query_string
                    session.save()
                    return redirect(h.url('/auth/login'))
                else:
                    return redirect(self.request.url + '&force_choose=yes')

            # should be the same for all datasets
            self._temp.ref_type = 'ensemblID'
            self._temp.ref_id = ensemblID
            self._temp.ds_id = ds_id
            self._temp.view_data[ds_id] = {}
            self._temp.view_data[ds_id]['ensemblID'] = ensemblID
            self._temp.view_data[ds_id]['ref_type'] = 'ensemblID'
            self._temp.view_data[ds_id]['ds_id'] = ds_id
            self._temp.view_data[ds_id]['probeName'] = Stemformatics_Dataset.get_probe_name(ds_id)
            # self._temp.view_graph_dict[ds_id] = self._setup_graphs(self._temp)

        self._temp.dataset_status = dataset_status


    def yugene_graph(self):

        result = self._summary_get_inputs()
        if not result:
            return self._temp.render

        result = self._summary_get_gene_details()
        if isinstance(result,e.HTTPFound):
            return result
        if not result:
            return self._temp.render

        self._summary_get_yugene_data()
        self._summary_set_outputs()

        audit_dict = {'ref_type':'gene_id','ref_id':self._temp.ensemblID,'uid':c.uid,'url':url,'request':self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        return render_to_response('S4M_pyramid:templates/genes/summary.mako',self.deprecated_pylons_data_for_view,request=self.request)


    def _summary_get_inputs(self):
        request=self.request
        geneSearch = request.params.get("gene")
        self._temp.geneSearch = str(geneSearch)
        try:
            self._temp.db_id = int(request.params.get("db_id"))
        except:
            self._temp.db_id = None
        self._temp.yugene_granularity_for_gene_search = request.params.get('yugene_granularity_for_gene_search',False)
        self._temp.large = request.params.get('size') == "large"
        self._temp.param_view_by = request.params.get("choose_to_view_by")
        self._temp.param_show_lower = request.params.get("show_lower")

        if (geneSearch is None) or (len(geneSearch) < 1):
            #error_handling_for_invalid_search_string()
            c.title = "Invalid Gene Search"
            c.message = "You have not entered a proper gene. Please go back and enter in another gene."
            self._temp.render  = render_to_response('S4M_pyramid:templates/workbench/error_message.mako')
            return False

        return True


    def _summary_get_gene_details(self):
        geneSearch = self._temp.geneSearch
        db_id = self._temp.db_id
        db = self.db_deprecated_pylons_orm
        request = self.request


        select_all_ambiguous = True
        chip_type = 0
        gene_list = []
        gene_list.append(geneSearch)
        get_description = True
        result = Stemformatics_Gene.get_genes(db, c.species_dict, geneSearch, db_id, False, None)

        if len(result) ==1 :
            original = geneSearch
            temp_gene = result.itervalues().next()
            geneSearch = temp_gene['EnsemblID']

            self._temp.db_id = db_id = temp_gene['db_id']
        else:
            # get a list together with some more details
            # and then choose
            c.db_id = db_id
            c.analysis = None
            c.show_probes_in_dataset = False
            c.multiple_genes = result
            c.url = request.environ.get('PATH_INFO')
            c.url += '?use=true'

            c.url = re.sub('gene=[\w\-\@]{2,}&','',c.url)
            c.breadcrumbs = [[h.url('/genes/search'),'Gene Search']]
            self._temp.render =  render_to_response('S4M_pyramid:templates/workbench/choose_from_multiple_genes.mako')
            return False

        # Pass the validated search string to the GeneQuery instance. Search for gene explicitly (True)
        self._temp.returnData = returnData = Stemformatics_Gene.get_genes(db,c.species_dict,geneSearch,db_id,True,None)

        if returnData == {} or returnData == None:
            return redirect(url(controller='contents', action='index'), code=404)

        for symbol in returnData:
            self._temp.symbol = returnData[symbol]['symbol']
            self._temp.ensemblID = returnData[symbol]['EnsemblID']
            break

        return True

    def _summary_set_outputs(self):
        db = self.db_deprecated_pylons_orm
        c.ensemblID = self._temp.ensemblID
        c.symbol = self._temp.symbol
        c.db_id = db_id = self._temp.db_id
        c.ucsc_links = Stemformatics_Auth.get_ucsc_links_for_uid(db,c.uid,db_id)
        c.ucsc_data = Stemformatics_Gene.get_ucsc_data_for_a_gene(db,db_id,c.ensemblID)
        # check if human or mouse
        if db_id == int(self.mouse_db):
            default_ds_id = self.default_mouse_dataset
        else:
            default_ds_id = self.default_human_dataset

        c.data = self._temp.returnData
        c.large = self._temp.large
        c.title = "Yugene Graph Data - Gene Summary for " + c.symbol
        c.yugene_graph_data = self._temp.yugene_graph_data

    """
    This is called by expressions.py/yugene_graph to get the data cached in redis (return_yugene_graph_data)
    """
    def _summary_get_yugene_data(self):
        db_id = self._temp.db_id
        ensemblID = self._temp.ensemblID
        param_view_by = self._temp.param_view_by
        param_show_lower = self._temp.param_show_lower
        yugene_granularity_for_gene_search ='auto'
        self._temp.yugene_graph_data = Stemformatics_Expression.return_yugene_graph_data(db_id,c.uid,ensemblID,g.all_sample_metadata,c.role)
