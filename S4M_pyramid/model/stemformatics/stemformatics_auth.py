#TODO-1
import logging
log = logging.getLogger(__name__)

import sqlalchemy as SA
from sqlalchemy import or_, and_, desc
import psycopg2
import psycopg2.extras

import re
import string
import json

from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, config
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort, redirect

from decorator import decorator
import smtplib

__all__ = ['Stemformatics_Auth']

import formencode.validators as fe

SUBSCRIBER_NAME = fe.Regex("[\w ]*", not_empty=False, if_empty="Anonymous User")
SUBSCRIBER_STATE = fe.Regex("[\w ]*", not_empty=False, if_empty="PENDING")
DESCRIPTIVE_TEXT = fe.Regex("[\w ]*", not_empty=False, if_empty="")
POS_INT = fe.Int(min=1, not_empty=True)
NUMBER = fe.Number(not_empty=True)
IDENTIFIER = fe.PlainText(not_empty=True)
URL = fe.URL(not_empty=True)
VQ = re.compile(r"[^\'\"\`\$\\]*")

import hashlib

from random import random

import datetime

import S4M_pyramid.lib.helpers as h
from S4M_pyramid.model import redis_server as r_server



class Stemformatics_Auth(object):
    """\
    Stemformatics_Auth Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for login controller

    Please note for most of these functions you will have to pass in the db object

    All functions have a try that will return None if errors are found


    """
    @staticmethod
    def user_status_dict():
        status_dict = {0:'Inactive',1:'Active',2:'Pending'}
        return status_dict

    @staticmethod
    def get_status_dict_by_name():
        status_dict = Stemformatics_Auth.user_status_dict()
        status_dict_by_name = {}
        for status_id in status_dict:
            name = status_dict[status_id]
            status_dict_by_name[name] = status_id

        return status_dict_by_name

    @staticmethod
    def set_smart_redirect(redirect_url):
        magic_globals.fetch()
        session = magic_globals.session
        session['redirect_url'] = redirect_url
        session.save()
        return True

    """
    This is for checking if this uid is a real user, not using guest account either
    """
    @staticmethod
    def check_real_user(uid):

        status_dict_by_name = Stemformatics_Auth.get_status_dict_by_name()
        status_id = status_dict_by_name['Active']

        guest_username = config['guest_username']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select uid from stemformatics.users where uid = %s and status= %s and username != %s;"
        cursor.execute(sql,(uid,status_id,guest_username,))

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        try:
            if result[0][0] == uid:
                real_user = True
            else:
                real_user = False
        except:
            real_user = False

        return real_user


    @staticmethod
    def get_smart_redirect(default_redirect_url):
        magic_globals.fetch()
        session = magic_globals.session
        if 'redirect_url' in session:
            redirect_url = session['redirect_url']
        else:
            redirect_url = ""
        session['redirect_url'] = ""
        session.save()
        if redirect_url != "":
            return redirect_url
        else:
            return default_redirect_url





    def __init__ (self):
        pass

    @staticmethod
    def authorise(db=None):
        """\

            Usage:

                @Stemformatics_Auth.authorise()
                def summary(self):

        """
        def check_authorised(func, *args, **kwargs):

            log.debug('start of authorise')

            magic_globals.fetch()
            c = magic_globals.c
            session = magic_globals.session
            request = magic_globals.request
            if 'path_before_login' in session:
                del session['path_before_login']
                session.save()

            if 'user' in session:
                c.user = session.get('user').lower()
                c.uid = session.get('uid')
                c.full_name = session.get('full_name')
                c.role = session.get('role')
                c.notifications = 1
                return func(*args, **kwargs)
            else:
                c.user = None
                session['path_before_login'] = request.path_info + '?' + request.query_string
                session.save()
                return redirect(h.url('/auth/login'))

        return decorator(check_authorised)


    @staticmethod
    def check_user_password(db,username,password): #CRITICAL-2
        username = username.lower()
        try:
            db.schema = 'stemformatics'

            user = db.users

            m = hashlib.sha1()
            m.update(password.encode('utf-8'))
            sha1_password = m.hexdigest()

            where = and_(user.username==username,user.password==sha1_password,user.status == 1)
            result = db.users.filter(where).all()

            if len(result) != 1:
                return None

            db_user = result[0]
            return db_user

        except:
            return None

    @staticmethod
    def confirm_new_user(db,confirm_code,uid): #CRITICAL-2
        try:
            db.schema = 'stemformatics'

            user = db.users

            now_time = datetime.datetime.now()
            two_days = datetime.timedelta(days=2)

            check_time = now_time - two_days

            # where = and_(user.confirm_code==confirm_code,user.status==0,user.created > check_time)
            result = user.filter(user.uid==uid).all()

            if len(result) != 1:
                return "This user does not exist. Please register."

            if result[0].status == 1:
                return "This user is already registered"


            if result[0].confirm_code.strip() != confirm_code:
                return "This confirm code is invalid or has expired for this user"

            if result[0].created < check_time:
                return "This confirm code has expired for this user"


            db_user = result[0]

            result = user.filter(user.uid == db_user.uid).update({'status': 1, 'confirm_code': ''})
            db.commit()


            Stemformatics_Auth.create_base_export_key(db_user.uid)

            db_user.status = 1
            db_user.confirm_code = ""
            Stemformatics_Auth.triggers_for_change_in_user(db,uid = None)
            return db_user

        except:
            return "Unknown error with confirming"

    @staticmethod
    def clear_expired_unconfirmed_users(db): #CRITICAL-2
        try:
            db.schema = 'stemformatics'

            user = db.users

            now_time = datetime.datetime.now()
            two_days = datetime.timedelta(days=2)

            check_time = now_time - two_days

            # change to status 2 instead of deleting just in case we have override options for this uid
            where = and_(user.status==0,user.created < check_time)
            result = db.users.filter(where).update({'status':2})
            db.commit()

            return True

        except:
            return False


    @staticmethod
    def remove_user(db,username): #CRITICAL-2
        username = username.lower()
        try:
            db.schema = 'stemformatics'

            user = db.users
            gsi = db.gene_set_items
            gs = db.gene_sets

            where = and_(user.username==username)
            result = user.filter(where).all()

            for userFound in result:
                geneSets = gs.filter(gs.uid == userFound.uid).all()
                for geneSet in geneSets:
                    gsi.filter(gsi.gene_set_id == geneSet.id).delete()
                    gs.filter(gs.id == geneSet.id).delete()


            where = and_(user.username==username)
            user.filter(where).delete()
            db.commit()

            return True

        except:
            return False

    @staticmethod
    def register_new_user(db,registration_data): #CRITICAL-2

        username = registration_data['username'].lower()

        # Story #179 have to check for users who are set as 0 or 1. If status of 2, then have to update and not create new user
        db.schema = 'stemformatics'
        where = and_(db.users.username==username)
        result = db.users.filter(where).all()

        update_user = False

        # check if username already available
        if len(result) == 1:

            if result[0].status == 2:
                update_user = True
            else:
                return "This username is already taken"

        if len(result) > 1:
            return "This username is already taken"

        # check strong password

        validation_regex_text = config['validation_regex']

        validation_regex = re.compile(validation_regex_text)

        m = validation_regex.match(registration_data['password'])

        if m is None:
            return config['validation_warning']



        m = re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',username)

        if m is None:
            return "This username is not valid, it must be a valid email address"



        m = hashlib.sha1()
        m.update(registration_data['password'].encode('utf-8'))
        sha1_password = m.hexdigest()

        base_confirm_code = m.update(str(random()).encode('utf-8'))
        confirm_code = m.hexdigest()

        # create new user - but check that it's not an update for an existing user with status of 2
        if update_user:

            now_time = datetime.datetime.now()
            dict_change = {'password':sha1_password,'created':now_time,'status': 0, 'confirm_code': confirm_code,'full_name': registration_data['full_name'], 'organisation': registration_data['organisation'], 'send_email_marketing': registration_data['send_email_marketing'], 'send_email_job_notifications': registration_data['send_email_job_notifications']}
            result = db.users.filter(db.users.username == username).update(dict_change)
        else:
            result = db.users.insert(username=username, password=sha1_password,organisation=registration_data['organisation'],full_name = registration_data['full_name'],confirm_code=confirm_code, send_email_marketing= registration_data['send_email_marketing'], send_email_job_notifications = registration_data['send_email_job_notifications'])

        db.commit()
        db.flush()

        where = and_(db.users.username==username)
        result = db.users.filter(where).all()

        if len(result) != 1:
            return "The registration could not be saved"

        return result[0]
        #except:
        #   return "Error in this application in register_new_user"

    @staticmethod
    def set_confirm_forgot_password(db,username): #CRITICAL-2
        username = username.lower()
        try:
            db.schema = 'stemformatics'
            user = db.users
            # only select users with status of active
            where = and_(user.username==username, user.status == 1)
            result = user.filter(where).all()

            # check if username already available
            if len(result) != 1:
                return None

            m = hashlib.sha1()
            base_confirm_code = m.update(str(random()).encode('utf-8'))
            confirm_code = m.hexdigest()

            now_time = datetime.datetime.now()
            two_hours = datetime.timedelta(hours=2)

            expiry_password_time = now_time + two_hours

            # update confirm code for user
            result = user.filter(user.username == username).update({'confirm_code':confirm_code , 'password_expiry': expiry_password_time})

            db.commit()
            db.flush()

            where = and_(user.username==username, user.confirm_code == confirm_code, user.status ==1)
            result = user.filter(where).all()

            # check if found
            if len(result) != 1:
                return None

            db_user = result[0]

            return db_user
        except:
            return None

    @staticmethod
    def get_user_from_confirm_code(db,confirm_code): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            user = db.users

            where = and_(user.confirm_code == confirm_code)
            result = user.filter(where).all()

            if len(result) != 1:
                return None

            return result[0]
        except:
            return None


    @staticmethod
    def get_users_from_usernames(list_of_usernames):

        if not isinstance(list_of_usernames,list):
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from stemformatics.users where username = ANY(%(list_of_usernames)s) ;"
        cursor.execute(sql,{'list_of_usernames': list_of_usernames})

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def set_users_to_be_inactive_from_usernames(string_of_usernames):
        status_dict_by_name = Stemformatics_Auth.get_status_dict_by_name()
        status_id = status_dict_by_name['Inactive']

        if not isinstance(string_of_usernames,str) and not isinstance(string_of_usernames,bytes):
            return []

        list_of_usernames  = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", string_of_usernames)

        user_result = Stemformatics_Auth.get_users_from_usernames(list_of_usernames)
        list_of_uids = []
        return_dict_of_usernames_and_uids = {}
        for row in user_result:
            uid = row['uid']
            list_of_uids.append(uid)
            return_dict_of_usernames_and_uids[uid] = row['username']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "update stemformatics.users set status = %(status_id)s where uid = ANY(%(list_of_uids)s) ;"
        cursor.execute(sql,{'list_of_uids': list_of_uids,'status_id':status_id})

        conn.commit()
        cursor.close()
        conn.close()

        return return_dict_of_usernames_and_uids

    @staticmethod
    def unsubscribe_users_from_outage_critical_notifications(string_of_usernames):

        if not isinstance(string_of_usernames,str) and not isinstance(string_of_usernames,bytes):
            return []

        list_of_usernames  = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", string_of_usernames)

        user_result = Stemformatics_Auth.get_users_from_usernames(list_of_usernames)
        list_of_uids = []
        return_dict_of_usernames_and_uids = {}
        for row in user_result:
            uid = row['uid']
            list_of_uids.append(uid)
            return_dict_of_usernames_and_uids[uid] = row['username']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "update stemformatics.users set send_email_outages_critical = False where uid = ANY(%(list_of_uids)s) ;"
        cursor.execute(sql,{'list_of_uids': list_of_uids})

        conn.commit()
        cursor.close()
        conn.close()

        return return_dict_of_usernames_and_uids


    @staticmethod
    def get_user_from_username(db,username): #CRITICAL-2
        username = username.lower()
        try:
            db.schema = 'stemformatics'
            user = db.users
            # only select users with blank confirm codes and status of active
            where = and_(user.username == username)
            result = user.filter(where).all()

            if len(result) != 1:
                return None

            return result[0]
        except:
            return None

    @staticmethod
    def get_user_from_uid(db,uid): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            user = db.users
            # only select users with blank confirm codes and status of active
            where = and_(user.uid == uid)
            result = user.filter(where).all()

            if len(result) != 1:
                return None

            return result[0]
        except:
            return None

    @staticmethod
    def reset_password(db,confirmed_user,confirm_code,password):  #CRITICAL-2
        try:
            db.schema = 'public'
            user = db.users

            # check expiry of password
            now_time = datetime.datetime.now()
            if confirmed_user.password_expiry is None or confirmed_user.password_expiry < now_time:
                return "This has expired. Please try again"


            # reset password
            username = confirmed_user.username.lower()
            updated_user = Stemformatics_Auth.change_password(db,username,password)
            if isinstance(updated_user, str):
                return updated_user

            # clear out expiry
            result = user.filter(user.uid == confirmed_user.uid).update({'confirm_code':'','password_expiry': None })
            db.commit()
            db.flush()

            return result
        except:
            return "Error in application reset_password"

    @staticmethod
    def clear_expired_password_resets(db): #CRITICAL-2
        try:
            db.schema = 'stemformatics'

            user = db.users

            now_time = datetime.datetime.now()

            where = and_(user.status==1,user.password_expiry < now_time)
            result = db.users.filter(where).update({'confirm_code':'','password_expiry': None })
            db.commit()

            return True

        except:
            return False


    @staticmethod
    def change_password(db,username,password): #CRITICAL-2
        username = username.lower()
        try:
            validation_regex_text = config['validation_regex']

            validation_regex = re.compile(validation_regex_text)

            m = validation_regex.match(password)

            if m is None:
                return config['validation_warning']

            db.schema = 'stemformatics'
            user = db.users

            where = and_(user.username==username)
            result = user.filter(where).all()

            # check if username already available
            if len(result) != 1:
                return "There was an error finding this user"

            m = hashlib.sha1()
            m.update(password.encode('utf-8'))
            sha1_password = m.hexdigest()

            # update user
            result = user.filter(user.username == username).update({'password':sha1_password })
            db.commit()
            db.flush()

            where = and_(user.username==username)
            check = user.filter(where).all()

            if len(check) != 1:
                return "The user could not be updated"

            if check[0].password != sha1_password:
                return "The password could not be saved"

            return check[0]
        except:
            return "Error in application change_password"

    @staticmethod
    def update_user(db,username,update_user): #CRITICAL-2

        try:
            username = username.lower()
            db.schema = 'stemformatics'
            user = db.users
            where = and_(user.username==username)
            result = user.filter(where).all()

            # check if username already available
            if len(result) != 1:
                return "There was an error finding this user"


            if 'password' in update_user:

                # check strong password
                validation_regex_text = config['validation_regex']

                validation_regex = re.compile(validation_regex_text)

                m = validation_regex.match(update_user['password'])

                if m is None:
                    return config['validation_warning']

                m = hashlib.sha1()
                m.update(update_user['password'].encode('utf-8'))
                sha1_password = m.hexdigest()

                # update password too
                result = user.filter(user.username == username).update({'password':sha1_password,'full_name': update_user['full_name'], 'organisation': update_user['organisation'], 'send_email_marketing': update_user['send_email_marketing'], 'send_email_job_notifications': update_user['send_email_job_notifications']})
            else:
                result = user.filter(user.username == username).update({'full_name': update_user['full_name'], 'organisation': update_user['organisation'], 'send_email_marketing': update_user['send_email_marketing'], 'send_email_job_notifications': update_user['send_email_job_notifications']})

            db.commit()
            db.flush()

            if result != 1:
                return "The update could not be saved"

            return True

        except:
            return "Error in this application in saving details"

    @staticmethod
    def return_all_active_users(db):
        status_list = Stemformatics_Auth.get_status_dict_by_name()
        active_status = status_list['Active']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from stemformatics.users where status= %(status_id)s ;"
        cursor.execute(sql,{'status_id': active_status})

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def return_user_notifications(db): #CRITICAL-2
        db.schema = 'stemformatics'
        user = db.users
        result = db.users.filter(user.send_email_marketing == True).all()
        return result

    @staticmethod
    def return_new_users(db,from_date): #CRITICAL-2
        db.schema = 'stemformatics'
        user = db.users
        result = db.users.filter(user.created >= from_date).all()
        return result



    @staticmethod
    def check_stay_signed_in_md5(db,username,user_and_pwd_md5): #CRITICAL-2
        db.schema = 'stemformatics'

        user = db.users
        if username is not None:
            username = username.lower()
        where = and_(user.username==username,user.status == 1)
        result = db.users.filter(where).all()

        if len(result) != 1:
            return None

        db_user = result[0]

        sha1_password = db_user.password

        h = hashlib.sha1()
        h.update(username.encode('utf-8') + sha1_password.encode('utf-8'))
        check_user_and_pwd_md5 = h.hexdigest()

        if check_user_and_pwd_md5 == user_and_pwd_md5 :
            return db_user
        else:
            return None




    @staticmethod
    def create_stay_signed_in_md5(username,password): #CRITICAL-2
        username = username.lower()
        m = hashlib.sha1()
        m.update(password.encode('utf-8'))
        sha1_password = m.hexdigest()

        h = hashlib.sha1()
        h.update(username.encode('utf-8') + sha1_password.encode('utf-8'))
        user_and_pwd_md5 = h.hexdigest()

        return user_and_pwd_md5



    @staticmethod
    def create_new_pending_user(db,username): #CRITICAL-2

        username = username.lower()

        # Story #179 have to check for users who are set as 0 or 1. If status of 2, then have to update and not create new user
        db.schema = 'stemformatics'
        where = and_(db.users.username==username)
        result = db.users.filter(where).all()

        # check if username already available
        if len(result) == 1:
            return result[0]

        # create new user
        result = db.users.insert(username=username,status=2)
        db.commit()
        db.flush()

        where = and_(db.users.username==username)
        result = db.users.filter(where).all()

        if len(result) != 1:
            return "The pending user could not be saved"

        return result[0]
        #except:
        #   return "Error in this application in register_new_user"


    """
    This will check to see if the email already is assigned ot a user. If not it will create one and return the new user id.
    """
    @staticmethod
    def return_uid_from_email_for_sharing(db,email): #CRITICAL-2
        email = email.lower()
        return_user = Stemformatics_Auth.get_user_from_username(db,email)
        pending_user = False
        # if no uid then create one with status of 2 which is pending registration
        if return_user is None:
            # return the new user record
            new_user = Stemformatics_Auth.create_new_pending_user(db,email)

            # if this is a string then something errored
            if isinstance(new_user,str):
                error_message = email + ": " + new_user + " "
                return error_message
            else:
                return_user_id = new_user.uid
                pending_user = True
        else:
            return_user_id = return_user.uid
            if return_user.status == 2:
                pending_user = True

        return [return_user_id,pending_user]


    @staticmethod
    def update_user_status(db,uid,status): #CRITICAL-2

        try:

            db.schema = 'stemformatics'
            user = db.users
            where = and_(user.uid==uid)
            result = user.filter(where).all()

            # check if username already available
            if len(result) != 1:
                return "There was an error finding this user"

            result = user.filter(user.uid == uid).update({'status': status})

            db.commit()
            db.flush()

            if result != 1:
                return "The update could not be saved"

            return True

        except:
            return "Error in this application in saving details"

    ''' datasets is a list of integers'''
    @staticmethod
    def save_multi_datasets(db,uid,db_id,datasets): #CRITICAL-2

        md_name = 'multi_datasets_view_'+str(db_id)
        # turn list of integers into string comma separated list
        md_value = str(datasets).strip('[]').replace(' ','')

        db.schema = 'stemformatics'
        u = db.users
        umd = db.users_metadata

        where = and_(u.uid==uid)
        result = u.filter(where).all()

        # check if user available
        if len(result) != 1:
            return "No user found"


        where = and_(umd.uid==uid,umd.md_name==md_name)
        result = umd.filter(where).all()

        # check if user available
        if len(result) == 0:
            result_insert = umd.insert(uid=uid,md_name=md_name,md_value=md_value)
        else:
            umd.filter(where).update({'md_value':md_value})

        db.commit()
        db.flush()


        return True


    @staticmethod
    def get_publish_gene_set_email_address():
        return config['publish_gene_set_email_address']


    @staticmethod
    def get_multi_datasets(db,uid,db_id): #CRITICAL-2

        md_name = 'multi_datasets_view_'+str(db_id)
        db.schema = 'stemformatics'
        umd = db.users_metadata

        where = and_(umd.uid==uid,umd.md_name==md_name)

        try:
            result = umd.filter(where).one()
        except:
            return []

        temp_md_value = result.md_value.split(',')

        datasets = [ int(i) for i in temp_md_value ]

        return datasets

    # Method for making the dataset list to a dictionary of the keys
    @staticmethod
    def get_dict_users_private_datasets_metadata(ds_list):
        ds_id_list = []
        ds_attribute_list = ['Title', 'Organism']
        ds_dict = {}

        # Makes a list of ds_id's to search metadata and filters out the duplicate entries by
        # overriding group permissions with user permissions.
        for ds_row in ds_list:
            ds_id = ds_row[0]
            status = ds_row[1]
            permissions = ds_row[2]
            try:
                tmp = ds_dict[ds_id]
                ds_id_list.append(ds_id)
            except:
                ds_dict[ds_id] = {}
                ds_id_list.append(ds_id)

            ds_dict[ds_id]['status'] = status
            ds_dict[ds_id]['permissions'] = permissions

        # Get the metadata based on the ds_id's collected
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Joins the metadata table and the datasets table to get the tags above whether or not
        # it is a private dataset
        sql = "select  dm.ds_id, dm.ds_name, ds.handle, dm.ds_value, ds.private from dataset_metadata as dm left join datasets as ds on (dm.ds_id = ds.id) where dm.ds_name = any(%s) and dm.ds_id = any(%s);"

        cursor.execute(sql,(ds_attribute_list,ds_id_list,))
        metadata = cursor.fetchall()
        cursor.close()
        conn.close()

        #Add the information from the metadata dict to the dict containing the privalges and status
        for ds_row in metadata:
            ds_id = ds_row[0]
            ds_attribute = ds_row[1]
            attribute_val = ds_row[3]
            ds_dict[ds_id][ds_attribute] = attribute_val
            ds_dict[ds_id]["handle"] = ds_row[2]
            ds_dict[ds_id]["private"] = ds_row[4]

        return ds_dict

    # Method for getting private datasets, access and privleges for
    @staticmethod
    def get_list_users_private_datasets(uid):
        # Checks that the user id isn't going to cause an error
        if not isinstance(uid, int) or uid < 0:
            return None

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Makes a join on the private overrides table and group privileges table on a user and gives
        # the private datasets a user has access to either under group or user privileges
        sql = "select ds_id,o.role,o.object_type from stemformatics.override_private_datasets as o left join stemformatics.group_users as gu on o.object_id = CAST(gu.gid as TEXT) where (o.object_type = 'Group' and gu.uid = %s) or (o.object_type = 'User' and o.object_id = %s) order by object_type;"

        cursor.execute(sql,(uid,str(uid),))
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result



    @staticmethod
    def get_groups_for_uid(db,uid,role): #CRITICAL-2
        public_list = [0]

        if not isinstance( uid, int ):
            return public_list # at least return public

        if not isinstance( role, str) and not isinstance(role, bytes):
            role = '' # set role to none

        if uid == 0:
            return public_list

        if role in ['admin','annotator']:

            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select * from stemformatics.groups;"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            groups = [ row['gid'] for row in result ]


        else:

            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select * from stemformatics.group_users where uid = %s;"
            cursor.execute(sql,(uid,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            groups = [ row['gid'] for row in result ]

        if 0 not in groups:
            groups.append(0) # public group

        return sorted(groups)

    @staticmethod
    def add_group(db,group_name): #CRITICAL-2
        db.schema = 'stemformatics'
        g = db.groups
        result = g.insert(group_name=group_name)
        db.commit()
        db.flush()
        return True


    @staticmethod
    def get_all_group_names(db): #CRITICAL-2

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from stemformatics.groups;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        group_names_dict = {}
        for group in result:
            gid = group['gid']
            group_name = group['group_name']
            group_names_dict[gid] = group_name

        return group_names_dict

    @staticmethod
    def get_ucsc_links_for_uid(db,uid,db_id): #CRITICAL-2

        ucsc_links = {}
        if uid is None or not isinstance(uid, int):
            return ucsc_links


        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select gid from stemformatics.group_users where uid = %s;"
        cursor.execute(sql,(uid,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        gids = [0]  # Public group has 0 gid
        for row in result:
            gids.append(row['gid'])

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql ="select gc.config_name as link_name,gc.config_value as url,gc.db_id,g.gid, g.group_name from stemformatics.group_configs as gc left join stemformatics.groups as g on g.gid = gc.gid where gc.gid = ANY (%s) and gc.db_id = %s and gc.config_type = 'UCSC Links';"
        cursor.execute(sql,(gids,db_id,))
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        ucsc_links = {}
        for row in result:
            gid = row['gid']
            key_name = row['link_name'] + unicode(gid)
            ucsc_links[key_name] = {}
            ucsc_links[key_name]['link_name'] = row['link_name']
            ucsc_links[key_name]['url'] = row['url']
            ucsc_links[key_name]['db_id'] = db_id
            ucsc_links[key_name]['gid'] = gid
            ucsc_links[key_name]['group_name'] = row['group_name']

        return ucsc_links

    @staticmethod
    def add_user_to_group(db,uid,gid): #CRITICAL-2
        db.schema = 'stemformatics'
        gu = db.group_users
        # check if already there
        result_check = gu.filter(and_(gu.gid==gid,gu.uid==uid)).all()
        if len(result_check) == 0:
            # then create if already there
            result = gu.insert(gid=gid,uid=uid,role='User')
            Stemformatics_Auth.triggers_for_change_in_user(db,uid = None)
            db.commit()
            db.flush()
            return True
        else:
            return False


    @staticmethod
    def get_all_group_users(db): #CRITICAL-2
        db.schema = 'stemformatics'
        u = db.users
        gu = db.group_users
        join = db.join(gu,u,gu.uid==u.uid)
        result = [ {'uid':row.uid,'gid':row.gid,'role':row.role, 'username':row.username,'status':row.status}  for row in join.all() ]
        return result

    @staticmethod
    def hierarchy_roles(current_role,role): #CRITICAL-2
        new_role = current_role
        if role != current_role:
            if role == "admin":
                new_role = role
            else:
                if role == "annotator" and current_role != "admin":
                    new_role = role
                else:
                    if role == "view":
                        new_role = role

        return new_role

    @staticmethod
    def setup_dict_uid_permissions(db): #CRITICAL-2
        db.schema = 'stemformatics'
        o = db.override_private_datasets
        g = db.group_users
        dict_uid_permissions = {}

        group_dict = {}
        all_group_users = g.all()
        for row in all_group_users:
            uid = row.uid
            gid = row.gid
            if gid not in group_dict:
                group_dict[gid] = []
            group_dict[gid].append(uid)


        # the order by means that Group comes before User,
        # so that even though a user is part of a group
        # we can give that user annotator rights
        all_overrides = o.order_by(o.object_type).all()
        for override_row in all_overrides:
            object_type = override_row.object_type
            object_id = override_row.object_id
            role = override_row.role
            ds_id = override_row.ds_id
            if object_type == "User":
                uid = int(object_id)
                if uid not in dict_uid_permissions:
                    dict_uid_permissions[uid] = {}
                if ds_id not in dict_uid_permissions[uid]:
                    dict_uid_permissions[uid][ds_id] = ""

                current_role =dict_uid_permissions[uid][ds_id]
                dict_uid_permissions[uid][ds_id] = Stemformatics_Auth.hierarchy_roles(current_role,role)

            if object_type == "Group":
                gid = int(object_id)
                users_for_group = group_dict[gid]
                for uid in users_for_group:
                    if uid not in dict_uid_permissions:
                        dict_uid_permissions[uid] = {}
                    if ds_id not in dict_uid_permissions[uid]:
                        dict_uid_permissions[uid][ds_id] = ""

                    current_role = dict_uid_permissions[uid][ds_id]
                    dict_uid_permissions[uid][ds_id] = Stemformatics_Auth.hierarchy_roles(current_role,role)


        return dict_uid_permissions


    @staticmethod
    def get_dict_of_user_dataset_availability(db): #CRITICAL-2
        db.schema = 'public'
        ds = db.datasets
        db.schema = 'stemformatics'
        u = db.users
        all_ds = ds.all()
        all_users = u.all()

        # this is the permissions that are per dataset/uid or dataset/group
        uid_permissions = Stemformatics_Auth.setup_dict_uid_permissions(db)

        list_of_user_dataset_availability = {}
        for user_row in all_users:
            uid = user_row.uid
            role = user_row.role
            list_of_user_dataset_availability[uid] = {}

            for ds_row in all_ds:
                ds_id = ds_row.id
                if role =="admin":
                    status_for_this_user = "Admin"
                else:
                    if role =="annotator":
                        status_for_this_user = "Annotate"
                    else:
                        status_for_this_user = Stemformatics_Auth.calculate_dataset_status(uid,ds_row,uid_permissions)
                list_of_user_dataset_availability[uid][ds_id] = status_for_this_user


        return list_of_user_dataset_availability

    """ assumption is that uid is not an admin as this was checked beforehand """
    @staticmethod
    def calculate_dataset_status(uid,ds_row,uid_permissions):
        status_for_this_user = "Unavailable"
        ds_id = ds_row.id
        try:
            permission = uid_permissions[uid][ds_id]
        except:
            permission = None

        if not ds_row.published:
            if permission == "admin":
                status_for_this_user = "Admin"
            if permission == "annotator":
                status_for_this_user = "Annotate"
        else:
            if ds_row.private:

                if ds_row.show_limited:
                    if permission == "admin" :
                        status_for_this_user = "Admin"
                    else:
                        if permission == "annotator":
                            status_for_this_user = "Annotate"
                        else:
                            status_for_this_user = "Limited"

                else:
                    if permission == "admin":
                        status_for_this_user = "Admin"
                    if permission == "view":
                        status_for_this_user = "Available"
                    if permission == "annotator":
                        status_for_this_user = "Annotate"
            else:
                status_for_this_user = "Available"

        return status_for_this_user

    @staticmethod
    def setup_redis_get_dict_of_user_dataset_availability(db):
        delimiter = config['redis_delimiter']

        data_result = Stemformatics_Auth.get_dict_of_user_dataset_availability(db)
        guest_username = config['guest_username']
        db_user = Stemformatics_Auth.get_user_from_username(db,guest_username)
        guest_uid = db_user.uid

        for uid in data_result:
            # for non-logged in users
            if uid == guest_uid:
                label_name = "user_dataset_availability"+delimiter+str(0)
                label_value = json.dumps(data_result[uid])
                r_server.set(label_name,label_value)



            label_name = "user_dataset_availability"+delimiter+str(uid)
            label_value = json.dumps(data_result[uid])
            r_server.set(label_name,label_value)

    @staticmethod
    def triggers_for_change_in_user(db,uid = None):
        Stemformatics_Auth.setup_redis_get_dict_of_user_dataset_availability(db)


    @staticmethod
    def send_email_for_pending_user(db,uid): #CRITICAL-2 #CRITICAL-6
        magic_globals.fetch()
        c = magic_globals.c

        db.schema = 'stemformatics'
        users = db.users
        user = users.filter(users.uid==uid).one()
        from_email = config['from_email']
        to_email = user.username
        subject = c.site_name+" Pending User"
        feedback_email = config['feedback_email']
        external_base_url = url('/',qualified=True)

        full_name = user.full_name
        username = user.username
        registration_url = external_base_url+url('auth/register?username=')+username

        from guide.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
        dataset_names = ""
        datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,uid)
        for ds_id in datasets:
            if datasets[ds_id]['private']:
                handle = datasets[ds_id]['handle']
                authors = datasets[ds_id]['name']
                title = datasets[ds_id]['title']
                dataset_names += "- "+title + " (" + authors + "). In "+c.site_name+" this is called " + handle  + ".\n"

        feedback_email = config['feedback_email']
        body = "Hello %s, you have a pending user in %s that was created for you to get access to private datasets:\n\n%s\n\nBut first, you will need to register.  It is important that you use the email specified as your username. Click here to register: %s \n\nIf you have any questions or comments, please email us at %s " % (full_name,c.site_name,dataset_names,registration_url,feedback_email)

        # raise Error
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        from guide.model.stemformatics.stemformatics_notification import Stemformatics_Notification # wouldn't work otherwise??

        success = Stemformatics_Notification.send_email(from_email,to_email,subject,body)
        return success

    @staticmethod
    def change_user_role_for_ds(db,ds_id,object_type,object_id,role):



        ds_id = int(ds_id)
        object_id = str(object_id)
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("select * from stemformatics.override_private_datasets where ds_id = %s and object_type = %s and object_id = %s;",(ds_id,object_type,object_id))

        result = cursor.fetchall()
        cursor.close()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if len(result) == 0:
            cursor.execute("insert into stemformatics.override_private_datasets (ds_id,uid,role,object_type,object_id) values (%s,%s,%s,%s,%s);",(ds_id,0,role,object_type,object_id))
        else:
            cursor.execute("update stemformatics.override_private_datasets set role = %s where ds_id = %s and object_type = %s and object_id = %s;",(role,ds_id,object_type,object_id))


        # retrieve the records from the database
        conn.commit()
        cursor.close()
        conn.close()
        return "Success"


    @staticmethod
    def get_user_role(db,uid): #CRITICAL-2
        if isinstance(uid,int):
            try:
                conn_string = config['psycopg2_conn_string']
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("select role from stemformatics.users where uid = %s;",(uid,))
                # retrieve the records from the database
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result[0][0]
            except:
                return None
        else:
            return None

    @staticmethod
    def get_number_of_active_users():
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select count(*) from stemformatics.users where status = 1;")
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        number_of_active_users = result[0][0]
        return number_of_active_users

    @staticmethod
    def create_base_export_key(uid):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from stemformatics.users where uid = %s;",(uid,))
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) ==1:
            username = result[0]['username']
            date_stamp = result[0]['created']

            h = hashlib.sha1()
            h.update((date_stamp.strftime('%Y-%m-%d') + username + str(uid)).encode('utf-8'))
            base_export_key = h.hexdigest()


            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("update stemformatics.users set base_export_key = %s where uid = %s;",(base_export_key,uid,))
            conn.commit()
            cursor.close()
            conn.close()

            return True
        else:
            return False

    @staticmethod
    def create_export_key(uid):
        """
        get uid and username
        create md5 value to return
        """

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select username,base_export_key from stemformatics.users where uid = %s;",(uid,))
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) ==1:
            username = result[0]['username']
            base_export_key = result[0]['base_export_key']
            server_name=url('/',qualified=True)
            h = hashlib.sha1()
            h.update((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + username + str(uid)).encode('utf-8'))
            export_key = h.hexdigest()

            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("insert into stemformatics.export_key values (%s, %s) ;",(uid,export_key))
            conn.commit()
            cursor.close()
            conn.close()

            return export_key
        else:
            return None


    @staticmethod
    def validate_export_key(export_key,uid):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select date_created from stemformatics.export_key where uid = %s and key = %s;",(uid,export_key,))
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) ==1:
            date_created = result[0]['date_created']
            export_key_validity = int(config['export_key_validity'])
            expiry_time = date_created + datetime.timedelta(days=export_key_validity)
            current_date = datetime.datetime.now()
            if current_date <= expiry_time:
                return True
            return False
        else:
            return False


    @staticmethod
    def get_gid_by_name(group_name):

        if not isinstance( group_name, str ) and not isinstance(group_name,bytes):
            return False


        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from stemformatics.groups where group_name = %s;",(group_name,))
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) ==1:
            return result[0]['gid']
        else:
            return False



    @staticmethod
    def check_uid_in_group(uid,gid,role):
        #gid of 0 is public and therefore everyone can access this
        if gid == 0:
            return True

        # treat uid of None as 0
        if uid is None:
            uid = 0


        # Need at least a gid
        if gid is None:
            return False


        if not isinstance( gid, int ):
            return False

        if not isinstance( uid, int ):
            return False

        if not isinstance( role, str) and not isinstance(role,bytes):
            role = '' # set role to none

        # check if uid is admin or annotator
        # if so, we can simply check gid exists and return True
        if role in ['admin','annotator']:
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select gid from stemformatics.groups where gid = %s;",(gid,))
            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            if len(result)==1:
                return True
            else:
                return False

        else: # this is not admin or annotator

            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from stemformatics.group_users where uid = %s and gid = %s;",(uid,gid,))
            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            if len(result) ==1:
                return True
            else:
                return False



    @staticmethod
    def get_all_group_configs(config_type,uid,role):

        if uid is None:
            uid = 0

        if not isinstance( uid, int ):
            return False

        if not isinstance( role, str) and not isinstance(role,bytes):
            role = '' # set role to none

        if role in ['admin','annotator']:
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from stemformatics.group_configs;")
            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()
        else:
            db=None
            gids = Stemformatics_Auth.get_groups_for_uid(db,uid,role)
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from stemformatics.group_configs where gid = ANY(%s);",(gids,))
            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

        result_array = []
        for row in result:
            if (config_type is not None and row['config_type'] == config_type) or config_type is None:
                row_dict= {'gid':row['gid'],'config_type':row['config_type'],'config_name':row['config_name'],'config_value':row['config_value'],'db_id':row['db_id']}
                result_array.append(row_dict)

        #result_dict = [ {'gid':row['gid'],'config_type':row['config_type'],'config_name':row['config_name'],'config_value':row['config_value'],'db_id':row['db_id']} for row in result]


        return result_array

    @staticmethod
    def get_secret_unsubscribe_sha1(id_string):
        secret_hash_parameter = config['secret_hash_parameter_for_unsubscribe']
        m = hashlib.sha1()
        m.update((secret_hash_parameter + id_string).encode('utf-8'))
        return m.hexdigest()


