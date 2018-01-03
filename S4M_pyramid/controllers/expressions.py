from pyramid_handlers import action

# c is used to emulate the "from pylons import tmpl_context as c" functionality from Pylons
from S4M_pyramid.lib.empty_class import EmptyClass as c
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.config import config
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
import psycopg2
import psycopg2.extras
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

    @action(renderer="expressions/probe_expression_graph.mako")
    def probe_expression_graph(self):
        c.ds_id = int(self.request.params.get('ds_id'))
        c.db_id = Stemformatics_Dataset.get_db_id(c.ds_id)
        c.chip_type = Stemformatics_Dataset.getChipType(c.ds_id)
        c.handle = Stemformatics_Dataset.getHandle(c.ds_id)
        return self.deprecated_pylons_data_for_view
