#TODO-1
import logging
log = logging.getLogger(__name__)

from S4M_pyramid.lib.base import BaseController

from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort, redirect

from S4M_pyramid.model.stemformatics.stemformatics_auth import Stemformatics_Auth

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from S4M_pyramid.config import config

from paste.deploy.converters import asbool

import S4M_pyramid.lib.helpers as h

from datetime import datetime, timedelta

import hashlib

from pyramid_handlers import action
from pyramid.renderers import render_to_response

class AuthController(BaseController):

    def __init__(self, request):
        c = self.c

        super(AuthController, self).__init__(request)

        db = self.db_deprecated_pylons_orm
        # clear out expired users first
        Stemformatics_Auth.clear_expired_unconfirmed_users(db)

        # clear out expired password resets too
        Stemformatics_Auth.clear_expired_password_resets(db)
        c.guest_username = config['guest_username']

    @action()
    def guest(self):
        c = self.c

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
        c = self.c
        """Show login form. Submits to /login/submit."""
        c.error_message = ""
        c.username = ""
        return self.deprecated_pylons_data_for_view

    @action()
    def submit(self): #CRITICAL-4
        c = self.c
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
            return redirect(url(str(redirection)))
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

    # Controller for displaying the private datasets a user has access to
    # and their respective access rights
    @Stemformatics_Auth.authorise()
    @action()
    def show_private_datasets(self):
        c = self.c
        """ Display private datasets a user has access to. """
        session = self.request.session
        if 'user' in session:
            user = session['user']
            uid = int(session['uid'])
            role = session['role']
        else:
            c.error_message = ""
            c.username = ""
            c.org = ""
            c.name = ""
            return render_to_response('S4M_pyramid:templates/auth/signin.mako', self.deprecated_pylons_data_for_view, request=self.request)

        # Get list of user datasets and metadata
        user_dataset_list = Stemformatics_Auth.get_list_users_private_datasets(uid)

        # If it is none an error has occured (i.e there was a low level error such as the
        # uid wasn't an int. User_dataset_list will come back as empty if the user doens't
        # have any specific access None != {}
        if user_dataset_list is None:
            # Raise error
            c.message = 'You do not have any private dataset.'
            return render_to_response('S4M_pyramid:templates/workbench/error_message.mako', self.deprecated_pylons_data_for_view, request=self.request)

        # Get the metadata for each of the datasets
        c.user_datasets = Stemformatics_Auth.get_dict_users_private_datasets_metadata(user_dataset_list)
        return render_to_response('S4M_pyramid:templates/auth/show_private_datasets.mako', self.deprecated_pylons_data_for_view, request=self.request)


    @action(renderer = 'templates/workbench/error_message.mako')
    def logout(self):
        c = self.c
        """Log out the user and display a confirmation message."""
        session = self.request.session
        if 'user' in session:
            del session['user']
        if 'uid' in session:
            del session['uid']
        session.save()
        c.user = ""
        c.uid = ""
        c.full_name = ""
        c.notifications = 0

        response = self.request.response
        response.delete_cookie('stay_signed_in')
        response.delete_cookie('stay_signed_in_md5')

        c.title = "Logged out"
        c.message = "You have been successfully signed out."
        return self.deprecated_pylons_data_for_view


    @action(renderer = 'templates/auth/register.mako')
    def register(self): #CRITICAL-4
        c = self.c
        session = self.request.session
        if 'user' in session:
            return redirect(url('/'))

        request = self.request
        username = request.params.get('username')
        pwd = request.params.get('password')
        pwd2 = request.params.get('password_confirm')
        org = request.params.get('organisation')
        name = request.params.get('name')

        # Story #158 email notifications
        send_email_marketing = request.params.get('send_email_marketing')
        send_email_job_notifications = request.params.get('send_email_job_notifications')

        if username is None:
            c.error_message = ""
            c.username = ""
            c.org = ""
            c.name = ""
            return self.deprecated_pylons_data_for_view

        if username is not None and pwd is None and pwd2 is None:
            c.error_message = ""
            c.username = username
            c.org = ""
            c.name = ""
            return self.deprecated_pylons_data_for_view

        c.username = username
        c.org = org
        c.name = name

        if pwd != pwd2:
            c.error_message = "Pass phrases did not match. Please try again"
            return self.deprecated_pylons_data_for_view

        if send_email_job_notifications is not None:
            send_email_job_notifications = True
        else:
            send_email_job_notifications = False

        if send_email_marketing is not None:
            send_email_marketing = True
        else:
            send_email_marketing = False

        registration_data = {
            'username': username,
            'password': pwd,
            'organisation': org,
            'full_name': name,
            'send_email_marketing': send_email_marketing,
            'send_email_job_notifications': send_email_job_notifications
        }

        # return the new user record
        db = self.db_deprecated_pylons_orm
        new_user = Stemformatics_Auth.register_new_user(db,registration_data)

        if isinstance(new_user, str) or isinstance(new_user, bytes):
            c.error_message = new_user
            return self.deprecated_pylons_data_for_view

        # Used to mark user as logged in, now we wait for confirmation email
        # c.user = username
        # session['user'] = username
        # session.save()

        confirm_code = new_user.confirm_code

        # send confirmation email
        from_email = config['from_email']
        to_email = username
        subject = c.site_name+" - Registration confirmation"
        external_base_url = url('/',qualified=True)
        body = "Welcome to %s! Please click here to confirm your registration. \n%sauth/confirm_new_user/%s?rego=%s\n\nIf you did not intend to register at %s, please ignore this email and no action will be taken." % (c.site_name,external_base_url,confirm_code.strip(),new_user.uid,external_base_url)


        message =  """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (from_email, to_email, subject,body)
        # Send the message via our own SMTP server, but don't include the
        # envelope header.


####### '''
####### email notification temporarily disabled!!!!!
####### '''
#######
#######
####### success = Stemformatics_Notification.send_email(from_email,to_email,subject,body)
#######
#######
#######
####### if not success:            # instead of deleting, just change status to 2
#######     result = Stemformatics_Auth.update_user_status(db,new_user.uid,2)
#######
#######     if result == True:
#######         # use "if result == True" instead of "if result", because the returned result from the model will
#######         # be either true or an error string.
#######         # The else condition will never be executed if using "if result"
#######         c.error_message = "There was an issue with sending the email, please re-enter your details"
#######     else:
#######         c.error_message = "There was an issue with sending the email and removing your account, please re-enter a new email or wait three days to try again."
#######     return self.deprecated_pylons_data_for_view
#######
####### return redirect(h.url('/contents/registration_submitted'))
#######
#######
####### '''
####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
####### REMOVE THE FOLLOWING TEMPORARY HACK
#######   AFTER ENABLING EMAIL !!!!!!
####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
####### '''
#######
        c.title = "(TEST MODE) Registration submitted"
        c.message = "(TEST MODE)"
        c.message += 'Thank you for registering! Please confirm your registration by following instructions in your confirmation email.'
        c.message += '(TEST MODE): CONFIRMATION LINK:'
        c.message += body
        return render_to_response('S4M_pyramid:templates/workbench/error_message.mako', self.deprecated_pylons_data_for_view)



    @Stemformatics_Auth.authorise()
    @action(renderer = 'templates/auth/history.mako')
    def history(self):
        c = self.c
        id = self.request.matchdict['id']
        session = self.request.session
        if id == 'clear':
            session['page_history'] = []
            session.save()

        base_history = session.get('page_history')
        c.page_history = base_history[:]
        c.page_history.reverse()
        c.breadcrumbs = [[h.url('/workbench/index'),'Workbench'],[h.url('/auth/history'),'My History']]
        # raise Error

        return self.deprecated_pylons_data_for_view

    @action()
    def confirm_new_user(self):
        c = self.c
        id = self.request.matchdict['id']

        uid = str(self.request.params.get('rego'))

        db = self.db_deprecated_pylons_orm
        confirmed_user = Stemformatics_Auth.confirm_new_user(db,id,uid)


        if isinstance(confirmed_user,str):
            c.error_message = confirmed_user
            c.username = ""
            c.org = ""
            c.name = ""
            return render_to_response('S4M_pyramid:templates/auth/register.mako', self.deprecated_pylons_data_for_view, request=self.request)

        # Do not log user in. Make them log in normally
        c.error_message = "You have successfully confirmed your account. You can now login."
        c.title = "Registration completed"
        c.username = confirmed_user.username
        return render_to_response('S4M_pyramid:templates/auth/signin.mako', self.deprecated_pylons_data_for_view, request=self.request)


    @action()
    def forgot_password(self):
        c = self.c
        request = self.request
        username = str(request.params.get('username'))

        if username == 'None':
            c.error_message = ""
            c.username = ""
            return render_to_response('S4M_pyramid:templates/auth/forgot_password.mako', self.deprecated_pylons_data_for_view, request=self.request)

        # firstly, check that the record exists and then return a confirm code if it does and then send it off
        db = self.db_deprecated_pylons_orm
        found_user = Stemformatics_Auth.set_confirm_forgot_password(db,username)

        if found_user is not None:

            confirm_code = found_user.confirm_code

            # send confirmation email
            from_email = config['from_email']
            external_base_url = url('/',qualified=True)
            to_email = found_user.username
            subject = c.site_name+" - Pass phrase reset request"
            body = "Please click the following link to reset your pass phrase. \n%sauth/confirm_new_password/%s\n\nIf you did not intend to update your password at %s, please ignore this email and no action will be taken." % (url(str(external_base_url)),confirm_code,url(str(external_base_url)))


########### '''
########### email notification temporarily disabled!!!!!
########### '''
###########
########### # Send the message via our own SMTP server, but don't include the
########### # envelope header.
########### success = Stemformatics_Notification.send_email(from_email,to_email,subject,body)
########### if not success:
###########     c.message = "There was an issue with sending the email to reset your account. Please try again or go to our Contact us page."
###########     c.title = "Pass Phrase Reset Error"
###########     return render ('workbench/error_message.mako')

        # Don't show difference if no user is shown
        c.message = "Request for pass phrase reset instructions have been processed. If the details match an existing user an email will be sent to your registered email address."

#######
#######
####### '''
####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
####### REMOVE THE FOLLOWING 2 hacking lines
#######   AFTER ENABLING EMAIL !!!!!!
####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
####### '''
#######
        if 'body' in locals():
            c.message += body
#######
#######
####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#######
        c.title = "Pass Phrase Reset Sent"
        return render_to_response('S4M_pyramid:templates/workbench/error_message.mako', self.deprecated_pylons_data_for_view, request=self.request)



    def confirm_new_password(self):
        c = self.c
        id = self.request.matchdict['id']

        db = self.db_deprecated_pylons_orm
        confirmed_user = Stemformatics_Auth.get_user_from_confirm_code(db,id)

        if confirmed_user is None:
            c.error_message = "Error in confirming pass phrase reset, please try again"
            c.username = ""
            return render_to_response('S4M_pyramid:templates/auth/forgot_password.mako', self.deprecated_pylons_data_for_view, request=self.request)

        c.id = id
        request = self.request
        pwd = str(request.params.get('password'))
        pwd2 = str(request.params.get('password_confirm'))


        if pwd == 'None':
            c.username = confirmed_user.username
            c.error_message = ""
            return render_to_response('S4M_pyramid:templates/auth/confirm_password_reset.mako', self.deprecated_pylons_data_for_view, request=self.request)

        if pwd != pwd2:
            c.username = confirmed_user.username
            c.error_message = "Pass phrases are different"
            return render_to_response('S4M_pyramid:templates/auth/confirm_password_reset.mako', self.deprecated_pylons_data_for_view, request=self.request)


        result = Stemformatics_Auth.reset_password(db,confirmed_user,id,pwd)

        if result != True:
            c.username = confirmed_user.username
            c.error_message = "Failed to reset pass phrase. " + result
            return render_to_response('S4M_pyramid:templates/auth/confirm_password_reset.mako', self.deprecated_pylons_data_for_view, request=self.request)
        else:
            c.message = "Successfully reset your pass phrase"
            c.title = "Pass phrase Reset"
            return render_to_response('S4M_pyramid:templates/workbench/error_message.mako', self.deprecated_pylons_data_for_view, request=self.request)

#    @Stemformatics_Auth.authorise()
#    def update_details(self):
#        this_user = Stemformatics_Auth.get_user_from_username(db,c.user)
#
#        c.breadcrumbs = [[h.url('/workbench/index'),'Workbench'],[h.url('/auth/update_details'),'My Account']]
#
#        if this_user is None:
#            c.message = "There has been an error. Please logoff and login and try again"
#            c.title = "Error with User Authentication"
#            return render ('workbench/error_message.mako')
#
#
#        if config['guest_username'] == this_user.username:
#            c.message = "You cannot update the guest user account"
#            c.title = "No Guest changes"
#            return render ('workbench/error_message.mako')
#
#
#        update = request.params.get('update')
#        name = request.params.get('name')
#        org = request.params.get('organisation')
#
#        # Story #158 email notifications
#        send_email_marketing = request.params.get('send_email_marketing')
#        send_email_job_notifications = request.params.get('send_email_job_notifications')
#
#
#
#        password = request.params.get('password')
#        password_confirm = request.params.get('password_confirm')
#        c.this_user = this_user
#
#
#        if update is None:
#            c.error_message = ""
#            return render ('auth/update_details.mako')
#
#        if send_email_job_notifications is not None:
#            send_email_job_notifications = True
#        else:
#            send_email_job_notifications = False
#
#        if send_email_marketing is not None:
#            send_email_marketing = True
#        else:
#            send_email_marketing = False
#
#
#        if password != "":
#
#            if password != password_confirm:
#                c.error_message = "Pass phrases are not the same"
#                return render('auth/update_details.mako')
#
#            updated_data = { 'password': password, 'organisation': org, 'full_name': name, 'send_email_marketing': send_email_marketing, 'send_email_job_notifications': send_email_job_notifications }
#        else:
#            updated_data = { 'organisation': org, 'full_name': name, 'send_email_marketing': send_email_marketing, 'send_email_job_notifications': send_email_job_notifications}
#
#        result = Stemformatics_Auth.update_user(db,this_user.username,updated_data)
#
#
#        if isinstance(result,str):
#            c.error_message = result
#        else:
#            c.error_message = "Successfully updated"
#
#
#        return render ('auth/update_details.mako')
#
#
#    def unsubscribe_job_notification(self,id):
#
#        uid = int(id)
#
#        this_user = Stemformatics_Auth.get_user_from_uid(db,uid)
#
#        updated_data = { 'organisation': this_user.organisation, 'full_name': this_user.full_name, 'send_email_marketing': this_user.send_email_marketing, 'send_email_job_notifications': False}
#
#        result = Stemformatics_Auth.update_user(db,this_user.username,updated_data)
#
#        if isinstance(result,str):
#            c.title = "Email Job Notification error"
#            c.message = result
#        else:
#            c.title = "Email Job Notifications turned off"
#            c.message = "You have been successfully turned off email job notifications."
#
#
#
#        return render ('workbench/error_message.mako')
#
#    @staticmethod
#    def _email_template_need_to_register(site_name,share_type,email,external_base_url,feedback_email):
#        temp_body = "\n\nNOTE: To access this shared %s you will need to register as %s - please click here >> %s/auth/register?username=%s \n If you already have an account then the user who shared this may be using the wrong email address. Please contact us via %s for more details.\n\nWhen you register:\nIt asks for a passphrase instead of a password.\nA \"pass phrase\" is more secure, and easier to remember. eg. \"yoghurt is just as nice as ice cream\".\nThe pass phrase should be a minimum of 12 characters with at least one space\nYou will receive an email to confirm your registration. Once you have confirmed your email address you can then login to %s.\n\n---------------------------------------------------------\n\n" % (share_type,email,external_base_url,email,feedback_email,site_name)
#        return temp_body
#
#
#    def share_gene_set(self,id):
#
#        return_message = ""
#        gene_set_id = int(id)
#        to_email = request.params.get('to_email')
#        from_email = config['from_email']
#        subject = request.params.get('subject')
#        body = request.params.get('body')
#        from_uid = c.uid
#        publish = request.params.get('publish')
#
#        available = Stemformatics_Auth.check_real_user(from_uid)
#        if not available:
#            return_message += "This email could not be sent. You need to be logged in with your own email address to be able to share links."
#            return return_message
#
#        # convert to_email to be a uid - can be multiple separated by a comma
#        to_email = to_email.split(',')
#
#        external_base_url = url('/',qualified=True)
#
#        for email in to_email:
#
#            if email == '':
#                continue
#
#
#            return_result = Stemformatics_Auth.return_uid_from_email_for_sharing(db,email)
#            return_user_id = return_result[0]
#            new_user = return_result[1]
#
#            if new_user:
#                share_type = "gene list"
#                temp_body = body + self._email_template_need_to_register(c.site_name,share_type,email,external_base_url,c.feedback_email)
#            else:
#                temp_body = body
#
#
#
#            # error message - should be an integer if working
#            if isinstance(return_user_id,str):
#                if publish is None:
#                    return_message += "Error sharing for email address: " + email + ". "
#                else:
#                    return_message += "Error sending publishing message to "+c.site_name+". "
#                continue
#
#            # copy gene set
#            to_uid = return_user_id
#
#            result = Stemformatics_Gene_Set.copy_gene_set(db,gene_set_id,from_uid,to_uid)
#
#            d = datetime.now()
#
#            gene_set = result[0]
#            if publish is None:
#                gene_set_name = gene_set.gene_set_name + ' (shared from '+ c.user +' '+ c.full_name +')' + str(datetime.now())
#                gene_set_description = ' (shared from '+ c.user +' '+ c.full_name +' on ' + d.strftime("%d-%m-%Y %H:%M:%S") + ')'
#            else:
#                gene_set_description = request.params.get('gene_set_description')
#                gene_set_name = gene_set.gene_set_name + ' (Permission to publish from '+ c.user +' '+ c.full_name +')' + str(datetime.now())
#
#
#            db_id = gene_set.db_id
#            mapping_genes = result[1]
#            list_of_genes = [ gene.gene_id for gene in mapping_genes]
#
#            result = Stemformatics_Gene_Set.addGeneSet(db,to_uid,gene_set_name,gene_set_description,db_id,list_of_genes)
#
#            if result is None:
#                if publish is None:
#                    return_message += "Error sharing by copying gene set for email address: " + email + ". "
#                else:
#                    return_message += "Error publishing by copying gene set to Stemformtics. "
#                continue
#
#            # create a notifications record for that user - can skip this for now
#
#            # send out an email
#            sender  = config['from_email']
#            recipient = email
#            try:
#                email_result = Stemformatics_Notification.send_email(sender,recipient,subject,temp_body)
#            except:
#                if publish is None:
#                    return_message += "Successful sharing but error in sending email for email address: " + email +". "
#                else:
#                    return_message += "Successful copying for publishing but error in sending email to "+c.site_name+". Please email manually. "
#                continue
#
#            if publish is None:
#                return_message += "Successful sharing for email address: " + email +". "
#            else:
#                return_message += "Successful publishing message sent to "+c.site_name+". "
#
#        return return_message
#
#
#    def share_job(self,id):
#
#        return_message = ""
#        job_id = int(id)
#        to_email = request.params.get('to_email')
#        from_email = config['from_email']
#        subject = request.params.get('subject')
#        body = request.params.get('body')
#        from_uid = c.uid
#
#        available = Stemformatics_Auth.check_real_user(from_uid)
#        if not available:
#            return_message += "This email could not be sent. You need to be logged in with your own email address to be able to share links."
#            return return_message
#
#
#        # convert to_email to be a uid - can be multiple separated by a comma
#        to_email = to_email.split(',')
#
#        external_base_url = url('/',qualified=True)
#
#        for email in to_email:
#
#            if email == '':
#                continue
#
#            return_result = Stemformatics_Auth.return_uid_from_email_for_sharing(db,email)
#            return_user_id = return_result[0]
#            new_user = return_result[1]
#
#            if new_user:
#                share_type = "job"
#                temp_body = body + self._email_template_need_to_register(c.site_name,share_type,email,external_base_url,c.feedback_email)
#            else:
#                temp_body = body
#
#
#            # error message - should be an integer if working
#            if isinstance(return_user_id,str):
#                return_message += "Error sharing for email address: " + email +". "
#                continue
#
#
#            # check if private dataset
#            check_private = Stemformatics_Job.check_shared_user_can_access_dataset(db,job_id,return_user_id)
#
#            if not check_private:
#                return_message += "This email address: " + email +" does not have access to this private dataset. "
#                continue
#
#
#
#
#            share_type = 'Job'
#            share_id = job_id
#            to_uid = return_user_id
#
#            # check shared resource exists first
#            check_result = Stemformatics_Shared_Resource.check_shared_resource(db,share_type,share_id,to_uid)
#
#            if len(check_result) != 0:
#                return_message += "User with email address: " + email +" already has access to this job. "
#                continue
#
#            result = Stemformatics_Shared_Resource.add_shared_resource(db,share_type,share_id,from_uid,to_uid)
#
#            if result is None:
#                return_message += "Error creating shared resource for email address: " + email +". "
#                continue
#
#            # create a notifications record for that user - can skip this for now
#
#            # send out an email
#            sender  = config['from_email']
#            recipient = email
#            try:
#                email_result = Stemformatics_Notification.send_email(sender,recipient,subject,temp_body)
#            except:
#                return_message += "Successful sharing but error in sending email for email address: " + email +". "
#                continue
#
#            return_message += "Successful sharing for email address: " + email +". "
#
#        return return_message
#
#
#
#
#
#
#    def share_gene_expression(self):
#        return_message = ""
#        to_email = request.params.get('to_email')
#        from_email = config['from_email']
#        subject = request.params.get('subject')
#        body = request.params.get('body')
#        ds_id = request.params.get('ds_id')
#        gene_set_id = request.params.get('gene_set_id')
#
#        from_uid = c.uid
#        available = Stemformatics_Auth.check_real_user(from_uid)
#        if not available:
#            return_message += "This email could not be sent. You need to be logged in with your own email address to be able to share links."
#            return return_message
#
#        ds_id = int(ds_id)
#        # convert to_email to be a uid - can be multiple separated by a comma
#        to_email = to_email.split(',')
#
#        external_base_url = url('/',qualified=True)
#
#        for email in to_email:
#
#            if email == '':
#                continue
#
#            return_result = Stemformatics_Auth.return_uid_from_email_for_sharing(db,email)
#            return_user_id = return_result[0]
#            new_user = return_result[1]
#
#            if new_user:
#                share_type = "gene expression graph"
#                temp_body = body + self._email_template_need_to_register(c.site_name,share_type,email,external_base_url,c.feedback_email)
#            else:
#                temp_body = body
#
#
#            # error message - should be an integer if working
#            if isinstance(return_user_id,str):
#                return_message += "Error sharing for email address: " + email +". "
#                continue
#
#
#            # check if private dataset
#            #check_private = Stemformatics_Job.check_shared_user_can_access_dataset(db,job_id,return_user_id)
#            available = Stemformatics_Dataset.check_dataset_availability(db,return_user_id,ds_id)
#
#            if not available:
#                return_message += "This email address: " + email +" does not have access to this private dataset. "
#                continue
#
#
#            try:
#                gene_set_id = int(gene_set_id)
#            except:
#                gene_set_id = None
#
#            if gene_set_id is not None and gene_set_id != 0:
#                available = Stemformatics_Gene_Set.check_gene_set_availability(gene_set_id,return_user_id)
#                if not available:
#                    return_message += "This email address: " + email +" does not have access to this gene list. You can only share public gene lists at this time. "
#                    continue
#
#
#            # send out an email
#            sender  = config['from_email']
#            recipient = email
#            try:
#                email_result = Stemformatics_Notification.send_email(sender,recipient,subject,temp_body)
#            except:
#                return_message += "Error in sending email for email address: " + email +". "
#                continue
#
#            return_message += "Successful sharing for email address: " + email +". "
#
#        return return_message
#
