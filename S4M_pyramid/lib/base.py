import S4M_pyramid.lib.helpers as h
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
from S4M_pyramid.lib.deprecated_pylons_globals import url, config
from S4M_pyramid.model.stemformatics import db_deprecated_pylons_orm as db, Stemformatics_Notification, Stemformatics_Help, Stemformatics_Gene, Stemformatics_Auth, Stemformatics_Dataset
from S4M_pyramid.templates.external_db import externalDB, innateDB, stringDB
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

        self.deprecated_pylons_data_for_view = {'c': self.request.c, 'h': h, 'url':url, 'config':config}

        self.request.add_finished_callback(self._update_page_history)

    def _setup_c_deprecated_pylons_global(self):
        c = self.request.c
        request = self.request
        session = self.request.session

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
        c.header = ""#Stemformatics_Notification.get_header(db, request, c.uid) ##########################################################

        #----------------------------------------------------------------------------------

        c.species_dict = Stemformatics_Gene.get_species(db)

        #set up external db
        single_gene_url = "http://www.innatedb.com/getGeneCard.do?id="
        multiple_gene_url = "http://www.innatedb.com/batchSearch.do"
        c.innate_db_object = innateDB(single_gene_url,multiple_gene_url)

        single_gene_url = "http://string-db.com/newstring_cgi/show_network_section.pl?identifier="
        c.string_db_object = stringDB(single_gene_url)

        c.hostname = socket.gethostname()

        action = url.environ['pylons.routes_dict']['action']
        controller = url.environ['pylons.routes_dict']['controller']
        change_name = {'expressions':'graphs','workbench':'analyses'}
        if controller in change_name:
            controller = change_name[controller]
        c.title = config['site_name'] + ' ' + controller.capitalize() + ' - ' + action.replace('_',' ').title()
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
                            ) else False

        if not skip_history:
            if request.query_string == '':
                session['page_history'].append({'title': title, 'path': request.path_info})
            else:
                if 'page_history' not in session:
                    session['page_history'] = []
                session['page_history'].append({'title': title, 'path': request.path_info + '?' + request.query_string})
            session.save()

    def _check_dataset_status(self):
        c = self.request.c
        dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db, self._temp.ds_id, c.uid)

        # if no access and already logged in then error out
        # if no access and not already logged in then redirect
        if dataset_status == "Unavailable":
            if c.uid == '' or c.uid == 0:
                # got this code from decorator in model/stemformatics/stemformatics_auth.py
                c.user = None
                self.request.session['path_before_login'] = self.request.path_info + '?' + self.request.query_string
                self.request.session.save()
                raise redirect(h.url('/auth/login'))
            else:
                self._temp.error_message = "Dataset Not Found. Please Enter a Proper Dataset."
                raise redirect(url(controller='contents', action='index'), code=404)
        self._temp.dataset_status = dataset_status


    def _check_gene_status(self):
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
            c.url = self.request.environ.get('PATH_INFO')
            if self.request.environ.get('QUERY_STRING'):
                c.url += '?' + self.request.environ['QUERY_STRING']
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
