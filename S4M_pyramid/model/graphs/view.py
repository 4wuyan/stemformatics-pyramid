import json
class View(object):
    def __init__(self,preview):
        self.title = preview.title
        self.title_dataset = preview.title_dataset
        self.title_grouped = preview.title_grouped
        self.title_id = preview.title_id
        self.ensembl_id = preview.ensembl_id
        self.ds_id = preview.graph.graph_data.ds_id 
        self.db_id = preview.graph.graph_data.db_id
        self.chip_type = preview.graph.graph_data.chip_type
        self.sort_by = preview.graph.sort_by
        self.ref_type = preview.graph.graph_data.ref_type
        self.ref_id = preview.graph.graph_data.ref_id
        self.cells_samples_assayed = preview.graph.graph_data.ds_md['cellsSamplesAssayed']
        self.handle = preview.graph.graph_data.handle
        self.symbol = preview.symbol
        self.graph_type = preview.graph.graph_type
        self.line_graph_available = preview.line_graph_available
        self.large = False
        self.header = preview.graph.graph_data.header
        if hasattr(preview.graph, 'plot_data_sd'):
            self.plot_data_sd = preview.graph.plot_data_sd
        try:
            self.plot_data = preview.graph.plot_data
            self.number_of_samples = len(preview.graph.graph_data.sample_labels)
            self.median_dataset_expression = preview.graph.graph_data.ds_md['medianDatasetExpression']
            self.detection_threshold = preview.graph.graph_data.ds_md['detectionThreshold']
            self.min_y_axis = 0
            self.log_2 = preview.graph.graph_data.log_2
            self.y_axis_label = preview.graph.graph_data.y_axis_label
            self.raw_probe_list = preview.graph.graph_data.raw_probe_list
            self.display_probe_list = preview.graph.graph_data.raw_probe_list
            self.probe_list = preview.graph.graph_data.probe_list
            self.species = preview.graph.graph_data.species
            self.xaxis_labels = preview.graph.xaxis_labels
            self.markings = preview.graph.markings
            self.limit_sort_by = preview.graph.graph_data.ds_md['limitSortBy']
            self.sample_type_display_order = preview.graph.graph_data.ds_md['sampleTypeDisplayOrder'].split(",")
            self.min_x_axis = preview.graph.min_x_axis
            self.max_x_axis = preview.graph.max_x_axis
            self.x_axis_ticks = preview.graph.x_axis_ticks
            self.probe_information = preview.probe_information
        except:
            self.plot_data = {}
            self.sample_type_display_order = []
            self.limit_sort_by = "Sample Type"

        try:
            self.probe_color_dict = preview.graph.probe_color_dict
        except:
            self.probe_color_dict = {}

        #self.json_data = json.dumps(self.plot_data)

class Preview(object):
    def __init__(self,graph,line_graph_available):
        self.graph = graph
        self.line_graph_available = line_graph_available

        self._set_titles() 
        title = self.title

        self.probe_information = self.graph.graph_data.probe_information
        self.view_data = View(self)

    def get_json_data(self):
        return json.dumps(self.view_data.__dict__)


    def _set_titles(self):   
        graph = self.graph

        self.title_dataset =self.graph.graph_data.ds_md['Title'] 
        if self.graph.sort_by != 'LineGraphGroup':
            self.title_grouped = " grouped by " + self.graph.sort_by 
        else:
            self.title_grouped = ""

        if graph.graph_data.ref_type == 'ensemblID':
            self.symbol = self.graph.graph_data.gene_data['symbol']
            self.ensembl_id = self.graph.graph_data.gene_data['ensemblID']
            self.title = "Title placeholder" # no longer used
            self.title_id=  " for Gene "+ self.symbol  
            


        if graph.graph_data.ref_type == 'probeID':
            self.symbol = graph.graph_data.ref_id
            self.ensembl_id = ""
            temp_name = self.graph.graph_data.probe_name 
            if temp_name[-1:] == 's':
                name = temp_name[0:-1]
            else:
                name = temp_name
            self.title = "Expression Graph"
            self.title_id= " for "+ name + " " + self.symbol  
            
        if graph.graph_data.ref_type == 'miRNA':
            self.ensembl_id = ""
            self.title = "Expression Graph"
            if len(graph.graph_data.mirna_data) ==1:
                self.symbol = graph.graph_data.mirna_data[0]['symbol']
                temp_name = self.graph.graph_data.probe_name 
                if temp_name[-1:] == 's':
                    name = temp_name[0:-1]
                else:
                    name = temp_name
                self.title_id= " for "+ name + " " + self.symbol  
            else:
                self.symbol = "multiple miRNA"
                self.title_id= " for multiple miRNA"


        if graph.graph_data.ref_type == 'gene_set_id':
            self.symbol = graph.graph_data.ref_id
            self.ensembl_id = ""
            gene_set_name = graph.graph_data.gene_set_name 
            self.title = "Multi Gene Expression Graph"
            self.title_id = " for " + gene_set_name

        
         

