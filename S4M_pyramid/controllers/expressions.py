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
from S4M_pyramid.lib.deprecated_pylons_globals import url
import json
import formencode.validators as fe
from pyramid.renderers import render_to_response
FTS_SEARCH_EXPRESSION = fe.Regex(r"[^\'\"\`\$\\]*", not_empty=False, if_empty=None)


class ExpressionsController(BaseController):
    # 'sca' is short for scatter.  Makes validity checking easier.
    _graphTypes = {'sca': 'scatter', 'bar': 'bar', 'box': 'box', 'default': 'line', 'lin': 'line'}

    def __init__(self,request):
        super().__init__(request)

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
        if result != "1":
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

        audit_dict = {'ref_type': 'gene_id', 'ref_id': self._temp.ensemblID, 'uid': c.uid, 'url': self.url,
                      'request': self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type': 'ds_id', 'ref_id': self._temp.ds_id, 'uid': c.uid, 'url': self.url, 'request': self.request,
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
            pass
            #redirect(url(controller='contents', action='index'), code=404)
            #redirect is not yet implemented
        if ref_type == "ensemblID":
            result = self._check_gene_status()  #This is in lib/base.py
            print(result)
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
        audit_dict = {'ref_type':ref_type,'ref_id':self._temp.geneSearch,'uid':c.uid,'url':self.url,'request': self.request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type':'ds_id','ref_id':self._temp.ds_id,'uid':c.uid,'url':self.url,'request': self.request, 'extra_ref_type':ref_type, 'extra_ref_id':self._temp.geneSearch}
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
        c.select_probes = select_probes = self.request.params.get('select_probes')
        print(c.select_probes)
        if c.select_probes == None:
            c.select_probes = select_probes = ""
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
        sortBy = self.request.params.get('sortBy')

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
