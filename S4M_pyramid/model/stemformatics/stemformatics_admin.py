#-------Last synchronised with Pylons repo (master) on---------------#
#-------------------------8 Feb 2018---------------------------------#
#-------------------------by WU Yan----------------------------------#

#TODO-1
import logging
log = logging.getLogger(__name__)

import sqlalchemy as SA
from sqlalchemy import or_, and_, desc

import re
import string
import json


__all__ = ['Stemformatics_Admin']
import datetime, os, subprocess, hashlib
import psycopg2
import psycopg2.extras
from S4M_pyramid.lib.deprecated_pylons_globals import config

class Stemformatics_Admin(object):

    def __init__(self):
        pass

    @staticmethod
    def get_jar_processes():
        command_line = "nice -n 15 ps aux | grep jar "
        p = subprocess.Popen(command_line,shell=True,stdout=subprocess.PIPE)
        out, err = p.communicate()
        content = out.replace("\n","<br/>")
        return content


    @staticmethod
    def get_logfile(number):
        file_name =  config['logfile']
        command_line = "nice -n 15 tail -n "+str(number)+ " " +  file_name
        p = subprocess.Popen(command_line,shell=True,stdout=subprocess.PIPE)
        out, err = p.communicate()
        content = out.replace("\n","<br/>")
        return content


    """
    This is to check the health of the system for dns failover.
    Currently using datasets 1000 and 2000 to do this check for psql and redis
    To find the actual value of the redis command, you can go to the command line and run:
    redis-cli -s /data/redis/redis.sock GET 'gct_labels|2000'
    "1979409020_C|1979409021_F|1979409021_G|1979409021_B| ........."
    the sample_labels[0] should refer to the first sample_id on the line above: 1979409020_C
    """
    @staticmethod
    def health_check(db):

        ds_id = config['health_check_ds_id_psql']
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select chip_type from datasets where id = "+str(ds_id)+";"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        result= str(result[0][0])

        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression
        ds_id = config['health_check_ds_id_redis']
        sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)
        result += ':'+sample_labels[0]
        db.commit()
        db.flush()
        return result

    @staticmethod
    def is_user_admin(db,uid): #CRITICAL-2
        if isinstance(uid,int):
            db.schema = 'stemformatics'
            u = db.users
            try:
                user_result = u.filter(u.uid==uid).one()
                if user_result.role == "admin":
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False


    @staticmethod
    def dataset_override_users(db): #CRITICAL-6 #CRITICAL-2

        from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset # wouldn't work otherwise??


        db.schema = 'stemformatics'
        opd = db.override_private_datasets
        u = db.users
        g = db.groups
        db.schema = 'public'
        ds = db.datasets

        join = db.join(opd,ds,ds.id==opd.ds_id)
        result = join.filter(join.object_type=='User').all()
        dataset_override_users_result = []
        for row in result:
            uid = row.object_id
            ds_id = row.ds_id
            role = row.role

            handle = Stemformatics_Dataset.add_extra_to_handle(db,row.handle,row.private,row.show_limited)


            try:
                u_result = u.filter(u.uid==int(uid)).one()
                username = u_result.username
                status = u_result.status
                dataset_override_users_result.append({'role': role,'object_type':'User','object_id':uid,'ds_id':ds_id,'object_name':username,'handle':handle,'object_status':status})
            except:
                username = ""


        join = db.join(opd,ds,ds.id==opd.ds_id)
        result = join.filter(join.object_type=='Group').all()
        for row in result:
            ds_id = row.ds_id
            role = row.role
            handle = Stemformatics_Dataset.add_extra_to_handle(db,row.handle,row.private,row.show_limited)
            gid = row.object_id
            status = 1
            g_result = g.filter(g.gid==int(gid)).one()
            group_name = g_result.group_name
            dataset_override_users_result.append({'role':role,'ds_id':ds_id,'handle':handle,'object_type':'Group','object_id':gid,'object_name':group_name,'object_status':status})

        return dataset_override_users_result


    @staticmethod
    def all_users(db): #CRITICAL-2
        db.schema = 'stemformatics'
        u = db.users
        users_result = []
        result = u.all()
        for row in result:
            uid = row.uid
            username = row.username
            status = row.status
            organisation = row.organisation
            full_name = row.full_name
            role = row.role
            users_result.append({'uid':uid,'organisation':organisation,'username':username,'status':status,'full_name':full_name,'role':role})
        return users_result


    """
    get all the configs from database instead of ini file
    """
    @staticmethod
    def get_all_configs():

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select ref_type,ref_id from stemformatics.configs;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        result_dict = {}
        for row in result:
            ref_type = row['ref_type']
            ref_id = row['ref_id']

            # convert if it's an integer
            try:
                ref_id = int(ref_id)
            except:
                pass

            result_dict[ref_type] = ref_id

        return result_dict

    """
    Update configuration items
    """
    @staticmethod
    def trigger_update_configs():

        result = Stemformatics_Admin.get_all_configs()

        for key in result:
            config[key] = result[key]

        return config

    """
    Update config item. Do not change the ref_type, only the ref_id
    returns None if an error
    """
    @staticmethod
    def edit_config(ref_type, ref_id):

        error = True
        if isinstance(ref_type, str) and isinstance(ref_id, str):
            error = False

        if isinstance(ref_type, bytes) and isinstance(ref_id, bytes):
            error = False

        if error:
            return None

        # Now we have found it, now we can replace it
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "update stemformatics.configs set ref_id = %s where ref_type = %s;"
        cursor.execute(sql, (ref_id, ref_type,))
        conn.commit()
        cursor.close()
        conn.close()

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select ref_id from stemformatics.configs where ref_type = %s;"
        cursor.execute(sql, (ref_type,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) == 0:
            return None
        else:
            if result[0]['ref_id'] == ref_id:
                return True
            else:
                return False


