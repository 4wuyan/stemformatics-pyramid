#TODO-1
import logging
log = logging.getLogger(__name__)

from S4M_pyramid.model import r_server

import re , string , json , psycopg2 , psycopg2.extras

from S4M_pyramid.lib.deprecated_pylons_globals import config


__all__ = ['Stemformatics_Probe']

import formencode.validators as fe


class Stemformatics_Probe(object):
    """\
    Stemformatics_Probe Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for probe related data

    Please note for most of these functions you will have to pass in the db object

    All functions have a try that will return None if errors are found

    """

    def __init__ (self):
        pass

    @staticmethod
    def get_gene_mappings_for_probe(probe_ids,db_id,ds_id):
        if probe_ids == []:
            return {}

        result = Stemformatics_Probe.get_genes_for_probe(probe_ids,db_id,ds_id)
        probe_dict = {}
        for row in result:
            probe_id = row['to_id']
            gene_id = row['gene_id']
            symbol = row['associated_gene_name']
            if probe_id not in probe_dict:
                probe_dict[probe_id] = symbol
            else:
                probe_dict[probe_id] += ","+symbol

        return probe_dict


    @staticmethod
    def get_genes_for_probe(probe_ids,db_id,ds_id):
        if probe_ids == []:
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("Select mapping_id from datasets where id = %(ds_id)s",{"ds_id":ds_id})
        map_result = cursor.fetchall()
        cursor.close()
        conn.close()

        if map_result == []:
            return []

        mapping_id = map_result[0][0]
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("Select * from genome_annotations as ga left join stemformatics.feature_mappings as fm on fm.from_id = ga.gene_id and fm.from_type = 'Gene' where fm.mapping_id = %(mapping_id)s and fm.db_id = %(db_id)s and fm.to_id in %(probe_ids)s",{"mapping_id":mapping_id,"db_id":db_id,"probe_ids":tuple(probe_ids)})
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result


    @staticmethod
    def return_probe_information(db,ensemblID,db_id,ds_id):
        # http://stackoverflow.com/questions/1466741/parameterized-queries-with-psycopg2-python-db-api-and-postgresql
        # cursor.execute("SELECT * FROM student WHERE last_name = %(lname)s",
        #       {"lname": "Robert'); DROP TABLE students;--"})

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("Select * from stemformatics.feature_mappings as fm left join datasets as d on d.mapping_id = fm.mapping_id where d.id = %(ds_id)s and from_type = 'Gene' and to_type = 'Probe' and from_id = %(from_id)s and d.db_id = %(db_id)s",{"ds_id":ds_id,"from_id":ensemblID,"db_id":db_id})

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    # probe_list is a string
    @staticmethod
    def set_probe_list(uid,probe_list_string):
        delimiter = config['redis_delimiter']

        label_name = 'probe_list_string'+delimiter+str(uid)
        try:
            result = r_server.delete(label_name)
            result = r_server.set(label_name,probe_list_string)
            return True
        except:
            return False


    @staticmethod
    def get_probe_list(uid):
        delimiter = config['redis_delimiter']

        label_name = 'probe_list_string'+delimiter+str(uid)
        try:
            result = r_server.get(label_name)
            return result
        except:
            return None

    @staticmethod
    def get_multi_mapping_for_probes(probe_ids,db_id,chip_type):
        if probe_ids == []:
            return []
        probe_dict = Stemformatics_Probe.get_gene_mappings_for_probe(probe_ids,db_id,chip_type)
        multi_mapping_data = {}
        for probe in probe_dict:
            count = len(str(probe_dict[probe]).split(","))
            multi_mapping_data[probe] = count

        return [probe_dict,multi_mapping_data]
