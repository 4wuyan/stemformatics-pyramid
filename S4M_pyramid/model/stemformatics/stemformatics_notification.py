#TODO-1
import logging
log = logging.getLogger(__name__)

import sqlalchemy as SA
from sqlalchemy import or_, and_, desc

from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, config

from decorator import decorator

import formencode.validators as fe

import datetime,smtplib

import S4M_pyramid.lib.helpers as h
import psycopg2
import psycopg2.extras

# Import smtplib for the actual sending function
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
#from S4M_pyramid.model.stemformatics.stemformatics_job import Stemformatics_Job # wouldn't work otherwise??
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset # wouldn't work otherwise??


import redis
import json
# HEADER_DATASETS = [{'name':'grandiose', 'datasetIDs':['5037', '6073', '6082', '6084', '6089', '6111']}]


class Stemformatics_Notification(object):
    """\
    Stemformatics_Notification Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for login controller

    Please note for most of these functions you will have to pass in the db object



    """



    def __init__ (self):
        pass

    @staticmethod
    def add_notification(db,notify_type,uid,subject,body):


        return "OK"

    @staticmethod
    def send_email(sender,recipient,subject,body):

        if not isinstance(recipient,list):
            recipient = recipient.split(',')

        """
        http://mg.pov.lt/blog/unicode-emails-in-python

        Send an email.

        All arguments should be Unicode strings (plain ASCII works as well).

        Only the real name part of sender and recipient addresses may contain
        non-ASCII characters.

        The email will be properly MIME encoded and delivered though SMTP to
        localhost port 25.  This is easy to change if you want something different.

        The charset of the email will be the first one out of US-ASCII, ISO-8859-1
        and UTF-8 that can represent all the characters occurring in the email.
        """

        # Header class is smart enough to try US-ASCII, then the charset we
        # provide, then fall back to UTF-8.
        header_charset = 'ISO-8859-1'

        # We must choose the body charset manually
        for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
            try:
                body.encode(body_charset)
            except UnicodeError:
                pass
            else:
                break

        # Split real name (which is optional) and email address parts
        sender_name, sender_addr = parseaddr(sender)
        recipient_name, recipient_addr = parseaddr(recipient)

        # We must always pass Unicode strings to Header, otherwise it will
        # use RFC 2047 encoding even on plain ASCII strings.
        sender_name = str(Header(unicode(sender_name), header_charset))
        recipient_name = str(Header(unicode(recipient_name), header_charset))

        # Make sure email addresses do not contain non-ASCII characters
        sender_addr = sender_addr.encode('ascii')
        recipient_addr = recipient_addr.encode('ascii')

        # Create the message ('plain' stands for Content-Type: text/plain)
        msg = MIMEText(body.encode(body_charset), 'plain', body_charset)
        msg['From'] = formataddr((sender_name, sender_addr))
        msg['To'] = 'Undisclosed recipients'
        msg['Subject'] = Header(unicode(subject), header_charset)

        try:
            s = smtplib.SMTP(config['smtp_server'],config['smtp_port'])
            s.ehlo()
            s.starttls()
            s.ehlo
            # Task 2823 - problems using postmarkapp.com's password without string conversion
            s.login(config['smtp_username'], str(config['smtp_password']))


            s.sendmail(sender, recipient, msg.as_string())
            s.quit()
        except:
            return False

        return True


    @staticmethod
    def send_basic_email(recipient, subject, message):
        magic_globals.fetch()
        c = magic_globals.c
        sender = config['from_email']
        body = "Hi there,\n\n"+message+"\n\n\nRegards,\n"+c.site_name+" Team"
        return Stemformatics_Notification.send_email(sender, recipient, subject, body)


    @staticmethod
    def get_header(db, request, uid):
        datasetID = request.params.get('datasetID', request.params.get('ds_id', None))

        if datasetID is not None:
            if Stemformatics_Dataset.check_dataset_availability(db, uid, datasetID):
                return Stemformatics_Notification.get_header_name_from_datasetId(datasetID)
        else: # Check other urls that might be under project grandiose
            controller = request.urlvars['controller']
            action = request.urlvars['action']
            if controller == 'workbench':
                if action == 'job_view_result' \
                  or action == 'analysis_confirmation_message':
                    datasetID = Stemformatics_Job.get_datasetId_from_job_id(db, request.urlvars['id'])
                    return Stemformatics_Notification.get_header_name_from_datasetId(datasetID)
        return None

    @staticmethod
    def get_header_name_from_datasetId(datasetID):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        try:
            header = r_server.hget('project_headers',str(datasetID))
            return header
        except:
            return None

    @staticmethod
    def set_project_headers(db):
        # Using dataset_metadata 'project' with ds_value of 3iii or grandiose
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select ds_id,ds_value from dataset_metadata where ds_name= 'project';")
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        for row in result:
            ds_id = row['ds_id']
            header = row['ds_value']
            if header == 'NULL':
                header = ''
            r_server.hset('project_headers',ds_id,header)


    @staticmethod
    def send_error_email(error_subject,error_body):
        magic_globals.fetch()
        c = magic_globals.c
        import socket
        hostname = socket.gethostname()
        sender = config['feedback_email']
        recipient = sender
        error_subject = "[" + hostname + "] " + c.site_name+" Error: " + error_subject
        result = Stemformatics_Notification.send_email(sender,recipient,error_subject,error_body)
        return  result
