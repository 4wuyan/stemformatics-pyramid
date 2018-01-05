from S4M_pyramid.lib.empty_class import EmptyClass as c
from S4M_pyramid.lib.helper import Helper as h
from S4M_pyramid.config import config
from S4M_pyramid.model.stemformatics.stemformatics_help import Stemformatics_Help
from S4M_pyramid.lib import environ_helper
from S4M_pyramid.model import init_model
import json
import socket
from sqlalchemy import create_engine
import sqlsoup
class BaseController():

    #this is invoked every time an action is called
    def __init__(self,request):
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

        #set tutorial page
        c.tutorials_for_page = Stemformatics_Help.get_help_for_page("contents/contact_us",request.params)
        c.json_tutorials_for_page =  json.dumps(c.tutorials_for_page)
        c.tutorials = Stemformatics_Help.get_tutorial_list()

        # set up h
        # request.host_url returns the url through the host (e.g. https://www-pyramid2.stemformatics.org/)
        self.helper = h(self.request, self.request.host_url)

        # should be put at last, when self.helper and self.url have been declared
        self.deprecated_pylons_data_for_view = {'c': c, 'h': self.helper, 'project_url': '/','url':self.url}

