from pyramid_handlers import action
from pyra.lib.carrier import EmpClass as c
from pyra.lib.helper import Helper as h

class BaseController():

    def __init__(self,request):
        #set up the protocol
        self.request=request
        self.response=request.response
        #
        c.site_name = "Stemformatics"
        c.feedback_email = "S4M@unimelb.edu.au"
        c.stemformatics_version = 1.0
        c.hostname = "S4M_Host_Name"
        c.json_tutorials_for_page="json_tute"
        c.role="user"
        c.production = "true"
        c.debug = None
