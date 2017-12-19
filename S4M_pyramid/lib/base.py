from S4M_pyramid.lib.empty_class import EmptyClass as c
from S4M_pyramid.lib.helper import Helper as h
from S4M_pyramid.config import *

class BaseController():

    def __init__(self,request):
        #set up the protocol
        self.request=request
        self.response=request.response
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
        c.notifycation = ""
        c.header_selected = "contents"
        c.hostname = "S4M_Host_Name"
        c.json_tutorials_for_page = "json_tute"
        c.role="user"
        c.debug = None
        c.header = ""

        # set up h(Note that the site url is hard coded)
        # site url for VM1:'https://www-pyramid1.stemformatics.org'
        self.helper = h(self.request,'https://www-pyramid1.stemformatics.org')

