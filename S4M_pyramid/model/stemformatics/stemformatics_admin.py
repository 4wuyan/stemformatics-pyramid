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

        if isinstance(ref_type, unicode) and isinstance(ref_id, unicode):
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


