#TODO-1
import logging
log = logging.getLogger(__name__)

from S4M_pyramid.lib.base import BaseController

from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort, redirect

# c is used to emulate the "from pylons import tmpl_context as c" functionality from Pylons
from S4M_pyramid.lib.empty_class import EmptyClass as c

# trying to find where db is set
#from S4M_pyramid.model.stemformatics import *

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from S4M_pyramid.config import config

from paste.deploy.converters import asbool

import S4M_pyramid.lib.helpers as h

from datetime import datetime, timedelta

CAPTCHA_ENABLED = asbool(config['captcha.enabled'])

import hashlib

class AuthController(BaseController):
    pass
#
#    def __before__(self):
#
#        super(AuthController, self).__before__ ()
#
#        # clear out expired users first
#        Stemformatics_Auth.clear_expired_unconfirmed_users(db)
#
#        # clear out expired password resets too
#        Stemformatics_Auth.clear_expired_password_resets(db)
#        c.guest_username = config['guest_username']

# heading off to Stemformatics_Auth

