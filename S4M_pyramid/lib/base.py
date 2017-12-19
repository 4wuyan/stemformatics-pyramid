from S4M_pyramid.lib.empty_class import EmptyClass as c
from S4M_pyramid.lib.helper import Helper as h
from S4M_pyramid.config import *
from S4M_pyramid.model.stemformatics.stemformatics_help import *
import json

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
        c.breadcrumbs = []

        #set tutorial page
        c.tutorials_for_page = Stemformatics_Help.get_help_for_page("contents/contact_us",request.params)
        c.json_tutorials_for_page =  json.dumps(c.tutorials_for_page)
        c.tutorials = Stemformatics_Help.get_tutorial_list()
        # set up h(Note that the site url is hard coded)
        # site url for VM1:'https://www-pyramid1.stemformatics.org'
        self.helper = h(self.request,'https://www-pyramid1.stemformatics.org')

