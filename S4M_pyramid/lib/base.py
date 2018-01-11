from S4M_pyramid.lib.empty_class import EmptyClass as c
from S4M_pyramid.lib.helper import Helper as h
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
from S4M_pyramid.lib.deprecated_pylons_globals import url
from S4M_pyramid.config import config
from S4M_pyramid.model.stemformatics.stemformatics_help import Stemformatics_Help
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
from S4M_pyramid.model.stemformatics.stemformatics_gene import Stemformatics_Gene
from S4M_pyramid.lib import environ_helper
from S4M_pyramid.templates.external_db import *
from S4M_pyramid.model import init_model
import json
import socket
from sqlalchemy import create_engine
import sqlsoup
import re
from pyramid.renderers import render_to_response


class tempData(object):
    pass


class BaseController():

    #this is invoked every time an action is called
    def __init__(self,request):
        self._temp = tempData()
        #set up DB var for ORM
        engine = create_engine(config['orm_conn_string'])
        self.db_deprecated_pylons_orm = sqlsoup.SQLSoup(engine)
        #set up the protocol
        self.request=request
        self.response=request.response

        #set up url.environ
        self.url = environ_helper.generate_environ(request.url)

        #set up c,those are directly retrieved fro the DB
        c.site_name = config['site_name']
        c.feedback_email = config['feedback_email']
        c.production = config['production']
        c.stemformatics_version = config['stemformatics_version']
        c.title = config['site_name']
        # c attributes those are not from the DB
        c.user = ""
        c.uid = 0
        c.full_name = ""
        c.notification = ""
        c.header_selected = self.url.environ['pylons.routes_dict']['controller']
        c.hostname = socket.gethostname()
        c.role="user"
        c.debug = None
        c.header = ""
        c.breadcrumbs = []
        c.notifications = 0
        c.species_dict = Stemformatics_Gene.get_species(self.db_deprecated_pylons_orm)
        #set tutorial page
        c.tutorials_for_page = Stemformatics_Help.get_help_for_page("contents/contact_us",request.params)
        c.json_tutorials_for_page =  json.dumps(c.tutorials_for_page)
        c.tutorials = Stemformatics_Help.get_tutorial_list()
        #set up external db
        single_gene_url = "http://www.innatedb.com/getGeneCard.do?id="
        multiple_gene_url = "http://www.innatedb.com/batchSearch.do"
        c.innate_db_object = innateDB(single_gene_url,multiple_gene_url)

        single_gene_url = "http://string-db.com/newstring_cgi/show_network_section.pl?identifier="
        c.string_db_object = stringDB(single_gene_url)
        # set up h
        # request.host_url returns the url through the host (e.g. https://www-pyramid2.stemformatics.org/)
        self.helper = h(self.request, self.request.host_url)

        # should be put at last, when self.helper and self.url have been declared
        self.deprecated_pylons_data_for_view = {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}

    def _check_dataset_status(self):
        db = self.db_deprecated_pylons_orm
        dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db, self._temp.ds_id, c.uid)

        # if no access and already logged in then error out
        # if no access and not already logged in then redirect
        if dataset_status == "Unavailable":
            if c.uid == '' or c.uid == 0:
                # got this code from decorator in model/stemformatics/stemformatics_auth.py
                c.user = None
                self.request.session['path_before_login'] = self.request.path_info + '?' + self.request.query_string
                self.request.session.save()
                redirect(self.helper.url('/auth/login'))
            else:
                redirect(url(controller='contents', action='index'), code=404)
                self._temp.error_message = "Dataset Not Found. Please Enter a Proper Dataset."
        self._temp.dataset_status = dataset_status


    def _check_gene_status(self):
        ds_id = self._temp.ds_id
        db_id = self._temp.db_id
        this_url = self._temp.url
        geneSearch = self._temp.geneSearch
        db = self.db_deprecated_pylons_orm

        if (geneSearch is None) or (len(geneSearch) < 1):
            #error_handling_for_invalid_search_string()
            c.title = "Invalid Gene Search"
            c.message = "You have not entered a proper gene. Please go back and enter in another gene."
            self._temp.render = render_to_response("S4M_pyramid:templates/workbench/error_message.mako",self.deprecated_pylons_data_for_view,request=self.request)
            return "0"
            # return render ('workbench/error_message.mako')
            #redirect(this_url(controller='contents', action='index'), code=404)

        select_all_ambiguous = True
        chip_type = Stemformatics_Dataset.getChipType(ds_id)
        gene_list = []
        gene_list.append(geneSearch)
        get_description = True

        result = Stemformatics_Gene.get_genes(db, c.species_dict, geneSearch, db_id, False, None)
        if result == None or len(result) == 0:
            c.title = "Invalid Gene Search"
            c.message = "You have not entered a gene that was found. Please press your browser's back button and enter another gene. |"+self.helper.url('/genes/search?gene='+str(geneSearch))+":Or click here to go to gene search"
            self._temp.render = render_to_response("S4M_pyramid:templates/workbench/error_message.mako",self.deprecated_pylons_data_for_view,request=self.request)
            return "0"

        if len(result) == 1 :
            temp_gene = next(iter(result.values()))
            ensemblID = temp_gene['EnsemblID']
            self._temp.db_id = db_id = temp_gene['db_id']

            # check if gene is an ensembl id or not
            if ensemblID not in this_url:
                this_url = re.sub('gene=[\w\-\@]{2,}&','',this_url)
                this_url = this_url+'&gene='+ensemblID+ '&db_id='+str(db_id)
                redirect(this_url)

        else:
            # get a list together with some more details
            # and then choose
            c.db_id = db_id
            c.analysis = None
            c.show_probes_in_dataset = False
            c.multiple_genes = result
            c.url = self.request.environ.get('PATH_INFO')
            if self.request.environ.get('QUERY_STRING'):
                c.url += '?' + self.request.environ['QUERY_STRING']
            else:
                c.url += '?use=true'

            c.url = re.sub('gene=[\w\-\@]{2,}&','',c.url)
            c.url = re.sub('&db_id=[0-9]{2}','',c.url)
            c.url = re.sub('&db_id=','',c.url)
            c.breadcrumbs = [[self.helper.url('/genes/search'),'Gene Search']]
            self._temp.render = render_to_response("S4M_pyramid:templates/workbench/choose_from_multiple_genes.mako",self.deprecated_pylons_data_for_view,request=self.request)
            return "many"

        self._temp.ensemblID = ensemblID
        self._temp.symbol = result[ensemblID]['symbol']
        return "1"

