import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import url
from pylons import config
from guide.lib.base import BaseController, render

import json

from guide.model.stemformatics import *


class HelpController(BaseController):

    #---------------------NOT MIGRATED--------------------------------
    def json(self):
        redirect(url(controller='contents', action='index'), code=404)
        #response.headers['Content-Type'] = 'application/json'
        #return json.dumps(Stemformatics_Help.get_help_for_page(request.params))
