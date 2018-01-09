#TODO-1
import logging
log = logging.getLogger(__name__)

from S4M_pyramid.lib.base import BaseController

from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort, redirect

# c is used to emulate the "from pylons import tmpl_context as c" functionality from Pylons
from S4M_pyramid.lib.empty_class import EmptyClass as c

# trying to find where db is set
from S4M_pyramid.model.stemformatics import Stemformatics_Auth

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from S4M_pyramid.config import config

from paste.deploy.converters import asbool

import S4M_pyramid.lib.helpers as h

from datetime import datetime, timedelta

CAPTCHA_ENABLED = asbool(config['captcha.enabled'])

import hashlib

from pyramid_handlers import action

class AuthController(BaseController):

    def __init__(self, request):

        super(AuthController, self).__init__(request)

        db = self.db_deprecated_pylons_orm
        # clear out expired users first
        Stemformatics_Auth.clear_expired_unconfirmed_users(db)

        # clear out expired password resets too
        Stemformatics_Auth.clear_expired_password_resets(db)
        c.guest_username = config['guest_username']

    @action(renderer = "templates/auth/signin.mako")
    def guest(self):

        db = self.db_deprecated_pylons_orm
        db_user = Stemformatics_Auth.get_user_from_username(db,c.guest_username)

        if db_user is None:
            c.error_message = "The guest account is not activated. Please try registering or logging in as a different user."
            c.username = ''
            return self.deprecated_pylons_data_for_view


        #Mark user as logged in
        magic_globals.fetch()
        session = magic_globals.session
        session['user'] = db_user.username
        session['uid'] = db_user.uid
        session['full_name'] = db_user.full_name
        session['role'] = db_user.role
        session.save()


        response = magic_globals.response
        response.delete_cookie('stay_signed_in')
        response.delete_cookie('stay_signed_in_md5')

        return redirect(url('/contents/index#tutorial=guest'))
