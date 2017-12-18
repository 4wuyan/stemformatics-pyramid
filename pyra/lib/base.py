from pyra.lib.empty_class import EmpClass as c
from pyra.lib.helper import Helper as h
from pyra.config import *

class BaseController():

    def __init__(self,request):
        #set up the protocol
        self.request=request
        self.response=request.response
        #set up c
        c.site_name = config['site_name']
        c.feedback_email = "S4M@unimelb.edu.au"
        c.stemformatics_version = 1.0
        c.hostname = "S4M_Host_Name"
        c.json_tutorials_for_page="json_tute"
        c.role="user"
        c.production = "true"
        c.debug = None
        c.title = "S4M_title"
        c.header = ""
        c.user = ""
        c.uid = 0
        c.full_name = ""
        c.notifycation = ""
        c.header_selected = "contents"
        # set up h(Note that the site url is hard coded)
        # site url for VM1:'https://www-pyramid1.stemformatics.org'
        self.helper = h(self.request,'https://www-pyramid1.stemformatics.org')

