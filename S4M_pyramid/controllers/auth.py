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
from pyramid.renderers import render_to_response

class AuthController(BaseController):

    def __init__(self, request):

        super(AuthController, self).__init__(request)

        db = self.db_deprecated_pylons_orm
        # clear out expired users first
        Stemformatics_Auth.clear_expired_unconfirmed_users(db)

        # clear out expired password resets too
        Stemformatics_Auth.clear_expired_password_resets(db)
        c.guest_username = config['guest_username']

    @action()
    def guest(self):

        db = self.db_deprecated_pylons_orm
        db_user = Stemformatics_Auth.get_user_from_username(db,c.guest_username)

        if db_user is None:
            c.error_message = "The guest account is not activated. Please try registering or logging in as a different user."
            c.username = ''
            return render_to_response("S4M_pyramid:templates/auth/signin.mako", self.deprecated_pylons_data_for_view, request=self.request)


        #Mark user as logged in
        session = self.request.session
        session['user'] = db_user.username
        session['uid'] = db_user.uid
        session['full_name'] = db_user.full_name
        session['role'] = db_user.role
        session.save()


        response = self.request.response
        response.delete_cookie('stay_signed_in')
        response.delete_cookie('stay_signed_in_md5')

        return redirect(url('/contents/index#tutorial=guest'))

    @action(renderer = "templates/auth/signin.mako")
    def login(self):
        """Show login form. Submits to /login/submit."""
        c.error_message = ""
        c.username = ""
        return self.deprecated_pylons_data_for_view

    @action()
    def submit(self): #CRITICAL-4
        request = self.request
        response = request.response
        session = request.session
        db = self.db_deprecated_pylons_orm

        """Verify username and password."""

        form_username = request.params.get('username')
        form_password = request.params.get('password')
        stay_signed_in = request.params.get('stay_signed_in')
        #Get user data from database
        #if form_username == 'pg_reviewer@stemformatics.org':
        #    c.error_message = "The Project Grandiose site is being finalised. Its completion is expected on Monday 20th October 2013, 0:00 GMT (Sunday midnight). Thank you for your patience."
        #    c.username = form_username
        #    return render('auth/signin.mako')

        db_user = Stemformatics_Auth.check_user_password(db,form_username,form_password)

        if db_user is None:
            c.error_message = "Your username/pass phrase was not correct or your account is not activated. Please try again."
            c.username = form_username
            return render_to_response("S4M_pyramid:templates/auth/signin.mako", self.deprecated_pylons_data_for_view, request=self.request)


        #Mark user as logged in
        session['user'] = db_user.username
        session['uid'] = db_user.uid
        session['full_name'] = db_user.full_name
        session['role'] = db_user.role
        session.save()

        if stay_signed_in == 'on':

            if 'days_to_stay_signed_in' in config:
                days_to_stay_signed_in = config['days_to_stay_signed_in']
            else:
                days_to_stay_signed_in = 90

            user_and_pwd_md5 = Stemformatics_Auth.create_stay_signed_in_md5(form_username,form_password)
            response.set_cookie('stay_signed_in',form_username,max_age=days_to_stay_signed_in*24*3600)
            response.set_cookie('stay_signed_in_md5',user_and_pwd_md5,max_age=90*24*3600)
        else:
            response.delete_cookie('stay_signed_in')
            response.delete_cookie('stay_signed_in_md5')

        #Send user back to the page he originally wanted to get to
        if session.get('path_before_login'):
            redirection = session.get('path_before_login')
            del session['path_before_login']
            session.save()
            redirect(url(str(redirection)))
        else:
            if session['page_history'] != []:
                log.debug('redirected using page history')
                lastpage = len(session['page_history']) - 1
                # changes for T#2527 - to stop redirect to API fetching data
                if 'expressions/graph_data' in str(session['page_history'][lastpage]['path']) or 'expressions/dataset_metadata' in str(session['page_history'][lastpage]['path']) :
                    lastpage = lastpage -1
                    while 'expressions/graph_data' in str(session['page_history'][lastpage]['path']) or 'expressions/dataset_metadata' in str(session['page_history'][lastpage]['path']) :
                        lastpage = lastpage - 1
                    redirection = url(str(session['page_history'][lastpage]['path']))
                else:
                    redirection = url(str(session['page_history'][lastpage]['path']))

                return redirect(redirection)

            else: # if previous target is unknown just send the user to a welcome page
                return redirect(url('/workbench/index'))
