from pylons import request, response, session, url, tmpl_context as c
import json
import logging
log = logging.getLogger(__name__)

# Live querying
from guide.model.stemformatics import *
from guide.model.graphs import *
from pylons import config

def test():

    graph_data()

def graph():
    assert True == True 
    
def graph_data():
    ds_id = 2000
    ref_type = "ensemblID"
    ref_id = "ENSG00000077943"
    sortBy = "Disease State"
    db_id = 56
    list_of_samples_to_remove = []
    this_graph_data = Graph_Data(db,ds_id,ref_type,ref_id,db_id,list_of_samples_to_remove)
    this_graph = Bar_Graph(this_graph_data,sortBy) 

    this_view = View(this_graph)
    assert this_graph.news == "now" 
    pass

     
