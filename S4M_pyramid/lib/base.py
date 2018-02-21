#-------Last synchronised with Pylons repo (master) on---------------#
#------------------------21 Feb 2018---------------------------------#
#-------------------------by WU Yan----------------------------------#

import S4M_pyramid.lib.helpers as h
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
from S4M_pyramid.lib.deprecated_pylons_globals import url, config
from S4M_pyramid.model.stemformatics import db_deprecated_pylons_orm as db, Stemformatics_Notification, Stemformatics_Help, Stemformatics_Gene, Stemformatics_Auth, Stemformatics_Dataset
from S4M_pyramid.templates.external_db import externalDB, innateDB, stringDB
from S4M_pyramid.model.graphs import Preview,Graph_Data,Scatterplot_Graph,Box_Graph,Bar_Graph,Line_Graph
import json
import socket
import re
from pyramid.renderers import render_to_response



class tempData(object):
    pass

class BaseController():

    # This is invoked every time an action is called
    def __init__(self, request):
        self.request = request
        self.request.c = self.request.tmpl_context
        c = self.request.c

        # set up url.environ
        url.set_environ(request)

        self._setup_c_deprecated_pylons_global()

        self.deprecated_pylons_data_for_view = {'c': c, 'h': h, 'url':url, 'config':config}

        self.request.add_finished_callback(self._update_page_history)

    def _setup_c_deprecated_pylons_global(self):
        c = self.request.c
        request = self.request
        session = self.request.session

        #---------Originally in __before__-------------------------------------------------
        self._temp = tempData()

        c.site_name = config['site_name']
        c.production = config['production']
        c.header_selected = url.environ['pylons.routes_dict']['controller']
        c.external_base_url = url('/',qualified=True)

        c.feedback_email = config['feedback_email']
        c.debug = request.params.get('debug')

        #set tutorial page
        c.tutorials = Stemformatics_Help.get_tutorial_list()
        this_url = url.environ['pylons.routes_dict']['controller'] + '/' + url.environ['pylons.routes_dict']['action']
        c.tutorials_for_page = Stemformatics_Help.get_help_for_page(this_url,request.params)
        c.json_tutorials_for_page =  json.dumps(c.tutorials_for_page)

        self._user_related_setup_for_c_deprecated_pylons_global()

        if not 'page_history' in session:
            session['page_history'] = []
        c.page_history = session.get('page_history')

        c.stemformatics_version = config['stemformatics_version']
        c.header = Stemformatics_Notification.get_header(db, request, c.uid) ##########################################################
        print(c.header)
        print(self.request.path)
        #----------------------------------------------------------------------------------

        #----------Originally in __init__--------------------------------------------------
        c.species_dict = Stemformatics_Gene.get_species(db)

        #set up external db
        single_gene_url = "http://www.innatedb.com/getGeneCard.do?id="
        multiple_gene_url = "http://www.innatedb.com/batchSearch.do"
        # innateDB from templates/external_db.py
        c.innate_db_object = innateDB(single_gene_url,multiple_gene_url)

        single_gene_url = "http://string-db.com/newstring_cgi/show_network_section.pl?identifier="
        c.string_db_object = stringDB(single_gene_url)

        c.guest_username = config['guest_username']
        c.hostname = socket.gethostname()

        # Set 'baseurl' for templating (if available) from config. Allow "correct" embedded XHTML link
        # generation in proxied environments etc.
        # Ensure that 'message' and 'msg_css' template variables exist
        c.message = ""
        c.msg_css = ""

        action = url.environ['pylons.routes_dict']['action']
        controller = url.environ['pylons.routes_dict']['controller']
        change_name = {'expressions':'graphs','workbench':'analyses'}
        if controller in change_name:
            controller = change_name[controller]
        c.title = config['site_name'] + ' ' + controller.capitalize() + ' - ' + action.replace('_',' ').title()
        #----------------------------------------------------------------------------------
    def _user_related_setup_for_c_deprecated_pylons_global(self):
        c = self.request.c
        request = self.request
        session = self.request.session
        if 'user' in session:
            c.user = session.get('user')
            c.uid = session.get('uid')
            c.full_name = session.get('full_name')
            c.role = session.get('role')
            c.notifications = 1
        else:

            #check cookie
            username = request.cookies.get('stay_signed_in')
            user_and_pwd_md5 = request.cookies.get('stay_signed_in_md5')
            cookie_user = Stemformatics_Auth.check_stay_signed_in_md5(db,username,user_and_pwd_md5)


            if cookie_user is not None:

                #Mark user as logged in
                session['user'] = cookie_user.username
                session['uid'] = cookie_user.uid
                session['full_name'] = cookie_user.full_name
                session['role'] = Stemformatics_Auth.get_user_role(db,cookie_user.uid)
                session.save()


                c.user = session.get('user')
                c.uid = session.get('uid')
                c.full_name = session.get('full_name')
                c.role = session.get('role')
                c.notifications = 1

            else:
                c.user = ""
                c.uid = 0
                c.full_name = ""
                c.notifications = 0
                c.role = None

    def _update_page_history(self, _request):
        c = self.request.c
        request = self.request
        session = self.request.session

        title = c.title
        skip_history = True if ('error' in request.path_info
                                or 'auth' in request.path_info
                                or 'main' in request.path_info
                                or ('hamlet' in request.path_info and 'index' not in request.path_info)
                                or 'ajax' in request.path_info
                                or 'return_gene_search_graph' in request.path_info
                                or 'genes/get_autocomplete' in request.path_info
                                or 'expressions/return_yugene_filtered_graph_data' in request.path_info
                                or 'expressions/return_breakdown_of_yugene_filtered_data' in request.path_info
                                or 'help/json' in request.path_info
                                or 'expressions/graph_data' in request.path_info
                                or 'expressions/dataset_metadata' in request.path_info
                            ) else False

        if not skip_history:
            if request.query_string == '':
                session['page_history'].append({'title': title, 'path': request.path_info})
            else:
                if 'page_history' not in session:
                    session['page_history'] = []
                session['page_history'].append({'title': title, 'path': request.path_info + '?' + request.query_string})
            session.save()

    def _check_gene_status(self):
        request = self.request
        c = self.request.c
        ds_id = self._temp.ds_id
        db_id = self._temp.db_id
        this_url = self._temp.url
        geneSearch = self._temp.geneSearch

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
            c.message = "You have not entered a gene that was found. Please press your browser's back button and enter another gene. |"+h.url('/genes/search?gene='+str(geneSearch))+":Or click here to go to gene search"
            self._temp.render = render_to_response("S4M_pyramid:templates/workbench/error_message.mako",self.deprecated_pylons_data_for_view,request=self.request)
            return "0"

        if len(result) == 1 :
            temp_gene = next(iter(result.values()))
            ensemblID = temp_gene['EnsemblID']
            self._temp.db_id = db_id = temp_gene['db_id']
            c.db_id = db_id

            # check if gene is an ensembl id or not
            if ensemblID not in this_url:
                this_url = re.sub('gene=[\w\-\@]{2,}&','',this_url)
                this_url = this_url+'&gene='+ensemblID+ '&db_id='+str(db_id)
                raise redirect(this_url)

        else:
            # get a list together with some more details
            # and then choose
            c.db_id = db_id
            c.analysis = None
            c.show_probes_in_dataset = False
            c.multiple_genes = result
            c.url = request.environ.get('PATH_INFO')
            if request.environ.get('QUERY_STRING'):
                c.url += '?' + request.environ['QUERY_STRING']
            else:
                c.url += '?use=true'

            c.url = re.sub('gene=[\w\-\@]{2,}&','',c.url)
            c.url = re.sub('&db_id=[0-9]{2}','',c.url)
            c.url = re.sub('&db_id=','',c.url)
            c.breadcrumbs = [[h.url('/genes/search'),'Gene Search']]
            self._temp.render = render_to_response("S4M_pyramid:templates/workbench/choose_from_multiple_genes.mako",self.deprecated_pylons_data_for_view,request=self.request)
            return "many"

        self._temp.ensemblID = ensemblID
        self._temp.symbol = result[ensemblID]['symbol']
        return "1"

    def _check_dataset_status(self):
        c = self.request.c
        request = self.request
        session = self.request.session
        dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db, self._temp.ds_id, c.uid)

        # if no access and already logged in then error out
        # if no access and not already logged in then redirect
        if dataset_status == "Unavailable":
            if c.uid == '' or c.uid == 0:
                # got this code from decorator in model/stemformatics/stemformatics_auth.py
                c.user = None
                session['path_before_login'] = request.path_info + '?' + request.query_string
                session.save()
                raise redirect(h.url('/auth/login'))
            else:
                self._temp.error_message = "Dataset Not Found. Please Enter a Proper Dataset."
                raise redirect(url(controller='contents', action='index'), code=404)
        self._temp.dataset_status = dataset_status

    #---------------------NOT MIGRATED--------------------------------
    def _check_probe_status():
        probeSearch = self._temp.probeSearch
        if (probeSearch is None) or (len(probeSearch) < 1):
            error_handling_for_invalid_search_string()
            redirect(url(controller='contents', action='index'), code=404)

    def _setup_graphs(self,temp_object):
        """ What other values are needed to be setup here for it to work?
        From expressions.py / _get_inputs_for_graph()
            self._temp.line_graph_available = Stemformatics_Dataset.check_line_graph_for_dataset(db,ds_id)
            self._temp.feature_type = feature_type
            self._temp.feature_id = feature_id
            self._temp.probeSearch = probeSearch
            self._temp.geneSearch = geneSearch
            self._temp.db_id = db_id
            self._temp.graphType = graphType
            self._temp.sortBy = sortBy
            self._temp.ds_id = ds_id
            self._temp.choose_dataset_immediately  = choose_dataset_immediately
            self._temp.url = request.environ.get('PATH_INFO')
            self._temp.original_temp_datasets = original_temp_datasets
            self._temp.force_choose = force_choose

            if request.environ.get('QUERY_STRING'):
                self._temp.url += '?' + request.environ['QUERY_STRING']
            self._temp.large = request.params.get('size') == "large"

        Note that lib/base.py / _check_dataset_status() and _check_gene_status
        are only affecting self._temp.db_id and temp_object.ref_id

        """
        c = self.request.c
        ref_type = temp_object.ref_type
        ref_id = temp_object.ref_id
        graphType = temp_object.graphType
        sortBy = temp_object.sortBy
        if hasattr(temp_object,'select_probes'):
            select_probes = temp_object.select_probes
        else:
            select_probes = None

        list_of_samples_to_remove = []
        line_graph_available = temp_object.line_graph_available
        """ Build the graph data first using the temp_object and other information. And then choose the
        graph that is appropriate and then convert the data to be ready for the view """
        this_graph_data = Graph_Data(db,temp_object.ds_id,ref_type,ref_id,temp_object.db_id,list_of_samples_to_remove,c.species_dict,select_probes)

        if graphType == "scatter":
            this_graph = Scatterplot_Graph(this_graph_data,sortBy)
        if graphType == "box":
            this_graph = Box_Graph(this_graph_data,sortBy)
        if graphType =="bar":
            this_graph = Bar_Graph(this_graph_data,sortBy)
        if graphType =="line":
            this_graph = Line_Graph(this_graph_data,sortBy)

        this_view = Preview(this_graph,line_graph_available)
        return this_view

'''
The following are not copied from the Pylons repo, becase they seem redundant.

In __init__:
        if 'noCache' in config:
            c.noCache = asbool(config['noCache'])
        else:
            c.noCache = False

In __call__:
        try:
            db.session.close()
            meta.Session.close()

            return response
        except SA.exc.InternalError as instance:
            db.session.rollback()
            new_message ="NOTE: This has been caught and rolled back. "
            instance.orig.message = new_message + instance.orig.message
            instance.orig.args = (new_message + instance.orig.args[0],)
            raise SA.exc.InternalError(instance.statement, instance.params, instance.orig, instance.connection_invalidated)


'''
