# coding=utf-8
#TODO-1
import logging
log = logging.getLogger(__name__)

import sqlalchemy as SA
from sqlalchemy import or_, and_, desc
from datetime import datetime, timedelta

# for list_authorised_users
import hmac
import S4M_pyramid.lib.helpers as h

import psycopg2, _pickle as cPickle
import psycopg2.extras
from S4M_pyramid.model import s4m_psycopg2
from S4M_pyramid.lib.deprecated_pylons_globals import config
#from S4M_pyramid.lib.state import *
from S4M_pyramid.model.stemformatics.stemformatics_auth import Stemformatics_Auth # wouldn't work otherwise??
#from S4M_pyramid.model.stemformatics.stemformatics_admin import Stemformatics_Admin # wouldn't work otherwise??

__all__ = ['Stemformatics_Dataset']

import formencode.validators as fe, time ,os , codecs , redis ,subprocess , re , string , json, datetime,glob#urllib2
#from poster.encode import multipart_encode
#from poster.streaminghttp import register_openers


POS_INT = fe.Int(min=1, not_empty=True)
NUMBER = fe.Number(not_empty=True)
IDENTIFIER = fe.PlainText(not_empty=True)
URL = fe.URL(not_empty=True)

class Stemformatics_Dataset(object):
    """\
Stemformatics_Dataset Model Objects
========================================

A simple model of static functions to make the controllers thinner for datasets and dataset_metadata tables

Please note for most of these functions you will have to pass in the db object

All functions have a try that will return None if errors are found

"""
    def __init__ (self):
        pass

    @staticmethod
    def check_graphType_for_dataset(db,ds_id,graphType,list_of_valid_graphs):
        if graphType == 'default' or graphType =='line':

            if 'line' in list_of_valid_graphs:
                return 'line'
            else:
                return 'box'
        else:
            return graphType

    """
    Pass in the ds_id and return the db_id which gives you information on the species and eventually, Ensembl version of this dataset
    """
    @staticmethod
    def get_db_id(ds_id):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select an_database_id from datasets as d left join annotation_databases as ad on ad.an_database_id = d.db_id where d.id = %(ds_id)s;",{"ds_id":ds_id})
        # retrieve the records from the database
        result_ds = cursor.fetchall()
        cursor.close()
        conn.close()
        return result_ds[0][0]

    @staticmethod
    def get_probe_name(ds_id):

        if isinstance(ds_id, int):
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select ds_value from dataset_metadata where ds_name = 'probeName' and ds_id = %(ds_id)s",{"ds_id":ds_id})
            # retrieve the records from the database
            result_ds = cursor.fetchall()
            cursor.close()
            conn.close()
            return result_ds[0][0]
        else:
            return ''


    @staticmethod
    def get_citations_for_dataset_list(ds_ids):

        if not isinstance(ds_ids,list):
            return {}
        temp_ds_ids = ds_ids
        ds_ids = [x for x in temp_ds_ids if isinstance(x, int)]

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from dataset_metadata where ds_id = ANY(%s) and ds_name in ('Publication Citation','Publication Title','First Authors');"
        cursor.execute(sql,(ds_ids,))

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        dict_result = {}
        for row in result:
            ds_id = row['ds_id']
            ds_name = row['ds_name'] # can be Publication Title, Publication Citation or First Authors
            ds_value = row['ds_value']
            if ds_id not in dict_result:
                dict_result[ds_id] = {}
            dict_result[ds_id][ds_name] = ds_value
        return dict_result



    @staticmethod
    def z_check_line_graph_for_dataset(db,ds_id): #CRITICAL-2
        db.schema = 'public'
        ds_md = db.dataset_metadata
        where = and_(ds_md.ds_name=='lineGraphOrdering',ds_md.ds_id==ds_id)
        result = ds_md.filter(where).all()
        if result == []:
            return False
        else:
            value = result[0].ds_value
            if value is None or value == '' or value == 'NULL':
                return False
            else:
                return True


    @staticmethod
    def list_of_valid_graphs_for_dataset(ds_id):
        list_of_valid_violin_plot_data_type_ids = [3,9]
        list_of_valid_graphs = ['box','bar','scatter']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select data_type_id from datasets where id = %s and data_type_id = ANY (%s);"
        cursor.execute(sql,(ds_id,list_of_valid_violin_plot_data_type_ids,))

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) == 1:
            list_of_valid_graphs.append('violin')


        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select ds_value from dataset_metadata where ds_id = %s and ds_name = 'lineGraphOrdering';"
        cursor.execute(sql,(ds_id,))

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if result != []:
            ds_name = result[0][0]
            if ds_name != 'NULL' and ds_name != '':
                list_of_valid_graphs.insert(0,'line')

        return list_of_valid_graphs





    @staticmethod
    def getChipType(ds_id): #CRITICAL-2
        try:

            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select chip_type from datasets where id = %s;"
            cursor.execute(sql,(ds_id,))

            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            chip_type = result[0][0]

            return chip_type
        except:
            return None



    @staticmethod
    def add_extra_to_handle(db,handle,private,show_limited):
        extra = ""
        if private and not show_limited:
            extra = "_PRIVATE"

        return handle + extra


    # Could remove the uid for getHandle but doesn't do anything
    @staticmethod
    def getHandle(db,ds_id,uid=None): #CRITICAL-2

        # check if valid ds_id
        try:
            ds_id = POS_INT.to_python(ds_id)
            # Ignore the check for handle - too minor
            db.schema = 'public'
            ds = db.datasets
            dataSet = ds.filter(ds.id == ds_id).first()

            new_handle = Stemformatics_Dataset.add_extra_to_handle(db,dataSet.handle,dataSet.private,dataSet.show_limited)
            return new_handle
        except:
            return None

    @staticmethod
    def get_handle_title_and_species(ds_ids):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # cursor.execute("select ds_id, Title, Organism from dataset_metadata where ds_id in %s;",(ds_id_list,))
        cursor.execute("select * from dataset_metadata where ds_id = ANY (%s) and (ds_name = 'Title' or ds_name = 'Organism');",(ds_ids,))

        # retrieve the records from the database
        result_ds_md = cursor.fetchall()
        cursor.close()
        conn.close()

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # cursor.execute("select ds_id, Title, Organism from dataset_metadata where ds_id in %s;",(ds_id_list,))
        cursor.execute("select id, handle, number_of_samples from datasets where id = ANY (%s) ;",(ds_ids,))

        # retrieve the records from the database
        result_ds_handle = cursor.fetchall()
        cursor.close()
        conn.close()

        dataset_info_dict = {}
        # combine results
        for row in result_ds_md:
            ds_id = row[0]
            ds_name =  row[1]
            ds_value =  row[2]
            if ds_id not in dataset_info_dict:
                dataset_info_dict[ds_id] = {}
            dataset_info_dict[ds_id][ds_name] = ds_value
        for row in result_ds_handle:
            ds_id = row[0]
            handle = row[1]
            number_of_samples = row[2]
            dataset_info_dict[ds_id]['handle'] = handle
            dataset_info_dict[ds_id]['number_of_samples'] = number_of_samples
        return dataset_info_dict



    """
    As at 09/03/2015:

    getChooseDatasetDetails

    This function is deprecated. We will be transitioning to another way of searching that is
    based on Stemformatics_Dataset.dataset_search

    model/stemformatics/stemformatics_auth.py
    1051:        datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,uid)

    model/stemformatics/stemformatics_dataset.py
    165:    def getChooseDatasetDetails(db,uid,show_limited=False):

    controllers/expressions.py
    209:            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited)
    238:            c.all_datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited)
    285:        c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited)
    398:            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)

    controllers/workbench.py
    233:            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)
    1746:            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)
    1869:        c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited)
    1931:            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)
    2049:            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)
    2144:            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)
    """
    @staticmethod
    def getChooseDatasetDetails(db,uid,show_limited=False,db_id=None):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        label_name = 'choose_dataset_details'
        result = r_server.get(label_name)
        result = result.decode('utf-8')
        temp_datasets = json.loads(result)
        choose_datasets = {}

        for ds_id in temp_datasets:
            db = None
            dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,uid)
            if dataset_status == "Unavailable":
                continue
            if dataset_status == "Limited" and show_limited == False:
                continue
            if temp_datasets[ds_id]['db_id'] != db_id and db_id != None:
                continue

            choose_datasets[ds_id] = temp_datasets[ds_id]
        return choose_datasets

    """
    As at 09/03/2015:
    This will be the hub of all the dataset searches and queries in Stemformatics:
        - dataset search
        - dataset search in Rohart MSC
        - dataset search in Gene Expression Graph when changing datasets
        - dataset search for Multiview
        - dataset search for Analyses
        - etc

    want to eventually be able to pass in:
        - uid
        - search => also return all as a stopgap
        - filter_dict
        - format_type (eg. choose_dataset or all)

    want to split the data between:
        - get the list of dataset ids using the filter and the uid
        - pass in list of dataset ids along with the format_type to get back data

    format_type options: 'all','front_end' and 'choose_dataset'

    This will replace the following:
        - getChooseDatasetDetails
        - getAllDatasetDetails
        - getDatasetDetails
        - getDatasetMetadataDetails
        - getDatasetMetadata


    Currently used:
        - Main dataset search
        - Ajax search for Rohart MSC Test
        - want to add more in the future

    """
    @staticmethod
    def dataset_search(uid,search,filter_dict,format_type="all"): #CRITICAL-2
        # http://stackoverflow.com/questions/1466741/parameterized-queries-with-psycopg2-python-db-api-and-postgresql
        # cursor.execute("SELECT * FROM student WHERE last_name = %(lname)s",
        #       {"lname": "Robert'); DROP TABLE students;--"})

        ds_ids = Stemformatics_Dataset.get_ds_ids_for_dataset_search(uid,search,filter_dict)
        result = Stemformatics_Dataset.get_dataset_metadata(ds_ids,format_type)
        return result

    @staticmethod
    def get_ds_ids_for_dataset_search(uid,search,filter_dict):
        resultList = {}
        if search is None:
            return []
        list_of_search_terms = search.split('and')
        temp_result_list = []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        for search_term in list_of_search_terms:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select ds_id from dataset_metadata where ds_value ilike %s"
            sql = sql + " group by ds_id;"
            data =("%"+search_term.strip()+"%",)
            cursor.execute(sql,data)
            # retrieve the records from the database
            result = cursor.fetchall()
            temp_result_list.append(result)
            cursor.close()
        conn.close()


        ds_lists = []
        for temp in temp_result_list:
            temp_list = []
            for row in temp:
                ds_id = row[0]
                temp_list.append(ds_id)
            ds_lists.append(temp_list)

        for x in range(0,len(ds_lists)):
            if x == 0:
                temp_compare = set(ds_lists[x])
            else:
                temp_compare = temp_compare.intersection(ds_lists[x])

        temp_ds_ids = list(temp_compare)
        temp_ds_ids.sort()

        # This is to try and search for a dataset id by using the search term
        try:
            ds_id = int(search)
            temp_ds_ids.append(ds_id)
        except:
            pass

        if 'rohart_msc_test' in filter_dict:
            filter_rohart_msc_test = filter_dict['rohart_msc_test']
        else:
            filter_rohart_msc_test = False

        if filter_rohart_msc_test:
            from S4M_pyramid.model.stemformatics.stemformatics_msc_signature import Stemformatics_Msc_Signature
            list_of_msc_ds_ids = Stemformatics_Msc_Signature.get_all_dataset_msc_access()


        if 'show_limited' in filter_dict:
            show_limited = filter_dict['show_limited']
        else:
            show_limited = False

        ds_ids = {}
        for ds_id in temp_ds_ids:
            db=None # this is not used at the moment
            dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,uid)
            if dataset_status == "Unavailable":
                continue
            if dataset_status == "Limited" and show_limited == False:
                continue

            ds_id = int(ds_id)

            if filter_rohart_msc_test:
                if ds_id not in list_of_msc_ds_ids:
                    continue

            ds_ids[ds_id] = {'dataset_status':dataset_status}


        return ds_ids

    """
    This will provide a list of all the dataset metadata in a format appropriate
    to what is needed. Currently the options are:
        - "choose_dataset" for choosing datasets for dataset/search and ajax
        - "front_end" to get all dataset metadata for exports and dataset summary
        - "all" to get all dataset metadata

    NOTE: The assumption is that all ds_ids have been checked before being
    passed into this method
    """
    @staticmethod
    def get_dataset_metadata(dict_of_ds_ids,format_type):

        ds_ids = []
        for ds_id in dict_of_ds_ids:
            ds_ids.append(ds_id)

        result_dict = temp_result_dict = {}

        # this is supposed to be fast, so we use redis to help speed this up
        # very limited number of fields to be shown
        if format_type == "choose_dataset":
            # Note we now have a list of ds_ids and we just want to check them for access
            # and then get the metadata
            r_server = redis.Redis(unix_socket_path=config['redis_server'])
            label_name = 'choose_dataset_details'
            result = r_server.get(label_name)
            temp_datasets = json.loads(result)

            for ds_id in ds_ids:
                # this is because the datasets from "choose_dataset_details" in redis is stored
                # as a string and not as an integer
                temp_ds_id = str(ds_id)
                ds_id = int(ds_id)

                temp_result_dict[ds_id] = temp_datasets[temp_ds_id]

        if format_type == "all" or format_type == "front_end":

            # This is for all values that are encoded
            # Get the metadata values and then get the values on the datasets table
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            ds_mt_result = {}
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from dataset_metadata where ds_id = ANY (%s) ;",(ds_ids,))
            # retrieve the records from the database
            ds_metadata_result = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in ds_metadata_result:
                ds_id = row['ds_id']
                ds_name =  row['ds_name']
                ds_value =  row['ds_value']

                if ds_id not in temp_result_dict:
                    temp_result_dict[ds_id] = {}
                    hosted_reports_dict = {}
                    external_analysis_links_dict = {}
                    pca_links_dict = {}

                # append buttons info if available
                if ds_name == 'showReportOnDatasetSummaryPage':
                    ds_value = json.loads(ds_value)
                    hosted_reports_dict[ds_value['name']]= ds_value['url']
                elif ds_name == 'ShowExternalLinksOnDatasetSummaryPage':
                    ds_value = json.loads(ds_value)
                    external_analysis_links_dict[ds_value['name']]= ds_value['url']
                elif ds_name == 'ShowPCALinksOnDatasetSummaryPage':
                    ds_value = json.loads(ds_value)
                    pca_links_dict[ds_value['name']]= ds_value['url']
                else:
                    temp_result_dict[ds_id][ds_name] = ds_value

            # if you add in new dataset_metadata field, don't forget to add the same in _encodeData method as it is where actual ds_md dict is created that is returned
            try:
                temp_result_dict[ds_id]['showReportOnDatasetSummaryPage'] = sorted(hosted_reports_dict.items())
                temp_result_dict[ds_id]['ShowExternalLinksOnDatasetSummaryPage'] = sorted(external_analysis_links_dict.items())
                temp_result_dict[ds_id]['ShowPCALinksOnDatasetSummaryPage'] = sorted(pca_links_dict.items())
                temp_result_dict[ds_id]['has_data'] = ds_row.has_data
            except:
                pass # when no ds_id found (eg. jjjj) this will be executed
            """
            When running datasets/search you need to have very specific data for the front end
            This is the breakdown of samples and the list of genes of interest
            To do this processing on a multiple list is wildly inefficient, so we only do it
            when there is one dataset shown
            """
            if len(ds_ids) == 1:
                ds_id = ds_ids[0]
                if 'topDifferentiallyExpressedGenes' in temp_result_dict[ds_id]:
                    top_diff_exp_genes_temp = temp_result_dict[ds_id]["topDifferentiallyExpressedGenes"]
                    top_genes = {}

                    top_genes_list = top_diff_exp_genes_temp.split(',')
                    conn_string = config['psycopg2_conn_string']
                    conn = psycopg2.connect(conn_string)
                    ds_mt_result = {}
                    conn = psycopg2.connect(conn_string)
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute("select associated_gene_name,gene_id,db_id from genome_annotations where gene_id = ANY (%s);",(top_genes_list,))
                    temp_result = cursor.fetchall()
                    cursor.close()
                    conn.close()

                    for row in temp_result:
                        name = row['associated_gene_name']
                        gene_id = row['gene_id']
                        db_id = row['db_id']
                        top_genes[name] = {'ensemblID':gene_id, 'db_id':db_id}
                    temp_result_dict[ds_id]["topDifferentiallyExpressedGenes"] = top_genes


                temp_result_dict[ds_id]['breakDown'] = {}
                conn_string = config['psycopg2_conn_string']
                conn = psycopg2.connect(conn_string)
                ds_mt_result = {}
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("select * from stemformatics.stats_datasetsummary where ds_id = %s order by md_name;",(ds_id,))
                # retrieve the records from the database
                ds_summary = cursor.fetchall()
                cursor.close()
                conn.close()

                for row in ds_summary:
                    name = row['md_name']
                    value = row['md_value']
                    count = row['count']
                    temp_result_dict[ds_id]['breakDown'][name + ': ' + value] = count
            for ds_id in temp_result_dict:
                encoded_metadata = Stemformatics_Dataset._encodeData(temp_result_dict[ds_id])
                result_dict[ds_id] = encoded_metadata
            # get the data on the datasets table
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from datasets where id  = ANY (%s) ;",(ds_ids,))
            # retrieve the records from the database
            result_ds = cursor.fetchall()
            cursor.close()
            conn.close()
            for ds_detail in result_ds:

                ds_id = ds_detail['id']
                db=None #This is not used
                new_handle = Stemformatics_Dataset.add_extra_to_handle(db,ds_detail['handle'],ds_detail['private'],ds_detail['show_limited'])

                result_dict[ds_id]['handle'] = new_handle
                result_dict[ds_id]['private'] = ds_detail['private']
                result_dict[ds_id]['number_of_samples'] = ds_detail['number_of_samples']
                result_dict[ds_id]['published'] = ds_detail['published']
                result_dict[ds_id]['show_yugene'] = ds_detail['show_yugene']
                result_dict[ds_id]['show_limited'] = ds_detail['show_limited']
                result_dict[ds_id]['dataset_status'] = dict_of_ds_ids[ds_id]['dataset_status']
                result_dict[ds_id]['chip_type'] = ds_detail['chip_type']
        return result_dict


    @staticmethod
    def _encodeData (ds_mt_result): #CRITICAL-2

        if not ds_mt_result:
            return dict()


        returnList =  {
            "project": ds_mt_result.get("project", {}),
            "top_miRNA": ds_mt_result.get("top_miRNA", {}),
            "accession_id": ds_mt_result.get("Accession", "N/A"),
            "geo_accession_id": ds_mt_result.get("GEO Accession", "N/A"),
            "ae_accession_id": ds_mt_result.get("AE Accession", "N/A"),
            "sra_accession_id": ds_mt_result.get("SRA Accession", "N/A"),
            "pxd_accession_id": ds_mt_result.get("PXD Accession", "N/A"),
            "ena_accession_id": ds_mt_result.get("ENA Accession", "N/A"),
            "gene_pattern_analysis_access": ds_mt_result.get("genePatternAnalysisAccess", "Allow"),
            "cells_samples_assayed": ds_mt_result.get("cellsSamplesAssayed", "N/A"),
            "probeName": ds_mt_result.get("probeName", ""),
            "sample_type_order": ds_mt_result.get("sampleTypeDisplayOrder", "N/A"),
            "title": ds_mt_result.get("Title", "N/A"),
            "publication_title": ds_mt_result.get("Publication Title", "N/A"),
            "name": ds_mt_result.get("Contact Name", "N/A"),
            "email": ds_mt_result.get("Contact Email", "N/A"),
            "affiliation": ds_mt_result.get("Affiliation", "N/A"),
            "authors" : ds_mt_result.get("Authors", "N/A"),
            "probes detected" : ds_mt_result.get("probesDetected", "N/A"),
            "breakDown" : ds_mt_result.get("breakDown", "N/A"),
            "public_release_date" : ds_mt_result.get("Release Date", "N/A"),
            "pub_med_id": ds_mt_result.get("PubMed ID", "N/A"),
            "description": ds_mt_result.get("Description", "N/A"),
            "platform": ds_mt_result.get("Platform", "N/A"),
            "RohartMSCAccess": ds_mt_result.get("RohartMSCAccess", "N/A"),
            "probes": ds_mt_result.get("probeCount", "N/A"),
            "organism": ds_mt_result.get("Organism", "N/A"),
            "top_diff_exp_genes": ds_mt_result.get("topDifferentiallyExpressedGenes", "N/A"),
            "replicates": ds_mt_result.get("minReplicates", "N/A") + '/' +  ds_mt_result.get("maxReplicates", "N/A"),
            "showReportOnDatasetSummaryPage": ds_mt_result.get("showReportOnDatasetSummaryPage", []),
            "ShowExternalLinksOnDatasetSummaryPage": ds_mt_result.get("ShowExternalLinksOnDatasetSummaryPage", []),
            "ShowPCALinksOnDatasetSummaryPage": ds_mt_result.get("ShowPCALinksOnDatasetSummaryPage", []),
            "has_data": ds_mt_result.get("has_data", 'yes'),
            "datasetStatus": ds_mt_result.get("datasetStatus", '')
            }

        return returnList





    """
    For this method, we need to have a way to easily add and remove fields
    that works with Stemformatics_Dataset.get_dataset_metadata
    """
    @staticmethod
    def setup_redis_choose_dataset_details(db): #CRITICAL-2
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        choose_dataset_dict = {}

        db.schema = 'public'
        ds = db.datasets
        ds_md = db.dataset_metadata

        all_ds = ds.all()

        for ds_row in all_ds:
            ds_id = ds_row.id
            choose_dataset_dict[ds_id] = {}

            new_handle = Stemformatics_Dataset.add_extra_to_handle(db,ds_row.handle,ds_row.private,ds_row.show_limited)

            choose_dataset_dict[ds_id]['handle'] = new_handle
            choose_dataset_dict[ds_id]['number_of_samples'] = ds_row.number_of_samples
            choose_dataset_dict[ds_id]['chip_type'] = ds_row.chip_type
            choose_dataset_dict[ds_id]['gene_pattern_analysis_access'] = "Allow"
            choose_dataset_dict[ds_id]['name'] = "No contact"
            choose_dataset_dict[ds_id]['private'] = ds_row.private
            choose_dataset_dict[ds_id]['db_id'] = ds_row.db_id

        md_fields =  ['Title','Contact Name','cellsSamplesAssayed','Organism','genePatternAnalysisAccess','has_data']
        all_ds_md = ds_md.filter(ds_md.ds_name.in_(md_fields)).all()

        for ds_md_row in all_ds_md:
            ds_id = ds_md_row.ds_id
            if ds_md_row.ds_name == "Contact Name":
                choose_dataset_dict[ds_id]['name'] = ds_md_row.ds_value
            if ds_md_row.ds_name == "cellsSamplesAssayed":
                choose_dataset_dict[ds_id]['cells_samples_assayed'] = ds_md_row.ds_value
            if ds_md_row.ds_name == "Title":
                choose_dataset_dict[ds_id]['title'] = ds_md_row.ds_value
            if ds_md_row.ds_name == "Organism":
                choose_dataset_dict[ds_id]['organism'] = ds_md_row.ds_value
            if ds_md_row.ds_name == "genePatternAnalysisAccess":
                choose_dataset_dict[ds_id]['gene_pattern_analysis_access'] = ds_md_row.ds_value
            if ds_md_row.ds_name == "has_data":
                choose_dataset_dict[ds_id]['has_data'] = ds_md_row.ds_value

        label_name = 'choose_dataset_details'
        result = r_server.set(label_name,json.dumps(choose_dataset_dict))



    """
    As at 09/03/2015:

    getAllDatasetDetails

    This function is deprecated. We will be transitioning to another way of searching that is
    based on Stemformatics_Dataset.dataset_search

    """
    @staticmethod
    def getAllDatasetDetails(db,uid,show_limited=False): #CRITICAL-2

        # check if valid ds_id

        db.schema = 'public'
        ds = db.datasets
        ds_md = db.dataset_metadata


        allDataSets = ds.order_by(ds.id).all()


        resultList = {}

        for ds in allDataSets:

            if uid != 'admin':
                # now check if dataset is available
                dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds.id,uid)
                if dataset_status == "Unavailable":
                    continue
                if dataset_status == "Limited" and show_limited == False:
                    continue
            else:
                dataset_status = 'Available'

            ds_mt_result = {}
            metadataValues = ds_md.filter(ds_md.ds_id==ds.id).all()
            for r in metadataValues:
                ds_mt_result[r.ds_name] = r.ds_value

            resultList[ds.id] = Stemformatics_Dataset._encodeData(ds_mt_result)
            new_handle = Stemformatics_Dataset.add_extra_to_handle(db,ds.handle,ds.private,ds.show_limited)

            resultList[ds.id]['handle'] = new_handle
            resultList[ds.id]['number_of_samples'] = ds.number_of_samples
            resultList[ds.id]['private'] = ds.private
            resultList[ds.id]['published'] = ds.published
            resultList[ds.id]['show_yugene'] = ds.show_yugene
            resultList[ds.id]['show_limited'] = ds.show_limited
            resultList[ds.id]['db_id'] = ds.db_id
            resultList[ds.id]['dataset_status'] = dataset_status

        return resultList



    # only for miRNA datasets
    @staticmethod
    def get_all_datasets_of_a_data_type(uid,data_type):

        resultList = {}
        if data_type != 'miRNA':
            return resultList

        # in agile_org, data_type_id of 8 is for miRNA
        data_type_id = 8
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from datasets where data_type_id = %s ;",(data_type_id,))
        # retrieve the records from the database
        ds_metadata_result = cursor.fetchall()
        cursor.close()
        conn.close()

        db = None
        db = None

        for ds in ds_metadata_result:

            ds_id = ds['id']
            # now check if dataset is available
            dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,uid)
            if dataset_status == "Unavailable":
                continue
            if dataset_status == "Limited" and show_limited == False:
                continue

            ds_mt_result = {}

            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from dataset_metadata where ds_id = %s ;",(ds_id,))
            # retrieve the records from the database
            ds_metadata_result = cursor.fetchall()
            cursor.close()
            conn.close()

            for r in ds_metadata_result:
                ds_mt_result[r['ds_name']] = r['ds_value']

            resultList[ds_id] = Stemformatics_Dataset._encodeData(ds_mt_result)


            new_handle = Stemformatics_Dataset.add_extra_to_handle(db,ds['handle'],ds['private'],ds['show_limited'])
            resultList[ds_id]['handle'] = new_handle

        return resultList

    """
    As at 09/03/2015:

    getDatasetDetails

    This function is deprecated. We will be transitioning to another way of searching that is
    based on Stemformatics_Dataset.dataset_search

    model/stemformatics/stemformatics_dataset.py
    279:        - getDatasetDetails
    502:    def getDatasetDetails(db,ds_id,uid): #CRITICAL-2

    controllers/admin.py
    476:            datasets = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)
    501:            c.dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)

    controllers/msc_signature.py
    148:        c.dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)

    controllers/projects.py
    19:        dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)

    controllers/datasets.py
    65:                    c.dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)
    78:                c.dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)
    """
    @staticmethod
    def getDatasetDetails(db,ds_id,uid): #CRITICAL-2

        # check if valid ds_id
        ds_id = POS_INT.to_python(ds_id)
        db.schema = 'public'
        ds = db.datasets
        ds_md = db.dataset_metadata

        # now check if dataset is available
        dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,uid)
        if dataset_status =="Unavailable":
            return None

        dataSet = ds.filter(ds.id==ds_id).first()


        resultList = {}
        ds_mt_result = {}

        metadataValues = ds_md.filter(ds_md.ds_id==ds_id).all()
        for r in metadataValues:
            ds_mt_result[r.ds_name] = r.ds_value

        db.schema = 'stemformatics'
        ds_stats = db.stats_datasetsummary

        ds_mt_result['breakDown'] = {}

        for breakDown in ds_stats.filter(ds_stats.ds_id==ds_id).order_by(ds_stats.md_name).all():
             ds_mt_result['breakDown'][breakDown.md_name + ': ' + breakDown.md_value] = breakDown.count

        # have to get values for topDifferentiallyExpressedGenes
        try:
            top_diff_exp_genes_temp = ds_mt_result["topDifferentiallyExpressedGenes"]
        except:
            top_diff_exp_genes_temp = ""

        top_diff_exp_genes = {}

        if top_diff_exp_genes_temp == "NULL" or top_diff_exp_genes_temp == "" :
            top_diff_exp_genes = {}

#            if ds_mt_result['Organism'] == 'Homo sapiens':
#                top_diff_exp_genes_temp = config['human_default_genes_of_interest']
#            else:
#                top_diff_exp_genes_temp = config['mouse_default_genes_of_interest']
#
        try:

            for symbol in top_diff_exp_genes_temp.split(','):
                db.schema="public"
                findGene = db.genome_annotations.filter(db.genome_annotations.gene_id==symbol).first()
                top_diff_exp_genes[findGene.associated_gene_name] = { 'ensemblID':symbol, 'db_id':findGene.db_id}
        except:
            top_diff_exp_genes = {}
        ds_mt_result["topDifferentiallyExpressedGenes"] = top_diff_exp_genes




        resultList[dataSet.id] = Stemformatics_Dataset._encodeData(ds_mt_result)
        new_handle = Stemformatics_Dataset.add_extra_to_handle(db,dataSet.handle,dataSet.private,dataSet.show_limited)
        resultList[dataSet.id]['handle'] = new_handle
        resultList[dataSet.id]['limitSortBy'] = ds_mt_result["limitSortBy"]
        resultList[dataSet.id]['dataset_status'] = dataset_status
        resultList[dataSet.id]['number_of_samples'] = dataSet.number_of_samples
        resultList[dataSet.id]['db_id'] = dataSet.db_id
        resultList[dataSet.id]['chip_type'] = dataSet.chip_type
        resultList[dataSet.id]['private'] = dataSet.private
        resultList[dataSet.id]['published'] = dataSet.published
        resultList[dataSet.id]['show_yugene'] = dataSet.show_yugene
        resultList[dataSet.id]['show_limited'] = dataSet.show_limited


        return resultList



    """
    As at 09/03/2015:

    getDatasetMetadataDetails

    This function is deprecated. We will be transitioning to another way of searching that is
    based on Stemformatics_Dataset.dataset_search

    model/stemformatics/stemformatics_dataset.py
    280:        - getDatasetMetadataDetails
    595:    def getDatasetMetadataDetails(db,ds_id,uid,raw=True): #CRITICAL-2
    1240:        ds_md = Stemformatics_Dataset.getDatasetMetadataDetails(db,ds_id,uid)
    """
    @staticmethod
    def getDatasetMetadataDetails(db,ds_id,uid,raw=True): #CRITICAL-2

        try:
            ds_id = POS_INT.to_python(ds_id)


            # now check if dataset is available
            available = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)

            if not available:
                return None


            db.schema = 'public'

            ds = db.datasets
            ds_md = db.dataset_metadata

            ds_mt_result = {}

            metadataValues = ds_md.filter(ds_md.ds_id==ds_id).all()

            for r in metadataValues:
                ds_mt_result[r.ds_name] = r.ds_value

            db.schema = 'stemformatics'
            ds_stats = db.stats_datasetsummary

            ds_mt_result['breakDown'] = {}

            for breakDown in ds_stats.filter(ds_stats.ds_id==ds_id).order_by(ds_stats.md_name).all():
                 ds_mt_result['breakDown'][breakDown.md_name + ': ' + breakDown.md_value] = breakDown.count

            # have to get values for topDifferentiallyExpressedGenes
            if "topDifferentiallyExpressedGenes" in ds_mt_result:
                top_diff_exp_genes_temp = ds_mt_result["topDifferentiallyExpressedGenes"]
            else:
                top_diff_exp_genes_temp = "N/A"

            top_diff_exp_genes = {}
            if not raw:
                if top_diff_exp_genes_temp != "N/A":
                    for symbol in top_diff_exp_genes_temp.split(','):
                        db.schema="public"
                        findGene = db.genome_annotations.filter(db.genome_annotations.gene_id==symbol).first()
                        top_diff_exp_genes[findGene.associated_gene_name] = { 'ensemblID':symbol, 'db_id':findGene.db_id}
                else:
                    top_diff_exp_genes = "N/A"
            else:
                top_diff_exp_genes = top_diff_exp_genes_temp

            ds_mt_result["topDifferentiallyExpressedGenes"] = top_diff_exp_genes
            return ds_mt_result

        except:
            return None

    @staticmethod
    def getExpressionDatasetMetadata(db,ds_id,uid,show_limited=False): #CRITICAL-2
        # uid not used anymore
        # try:
            # check if valid ds_id

            ds_id = POS_INT.to_python(ds_id)

            db.schema = 'public'
            ds_md = db.dataset_metadata


            filter_or = or_(ds_md.ds_name=='lineGraphOrdering',ds_md.ds_name=='sampleTypeDisplayGroups',ds_md.ds_name=='sampleTypeDisplayOrder',ds_md.ds_name=='Organism',ds_md.ds_name=='detectionThreshold',ds_md.ds_name=='medianDatasetExpression',ds_md.ds_name=='limitSortBy',ds_md.ds_name=='maxGraphValue')

            result = db.dataset_metadata.filter(and_(filter_or,ds_md.ds_id==ds_id)).all()

            for record in result:
                if record.ds_name == "lineGraphOrdering":
                    lineGraphOrdering = record
                if record.ds_name == "Organism":
                    speciesResult = record

                if record.ds_name == "detectionThreshold":
                    detectionThreshold = record

                if record.ds_name == "medianDatasetExpression":
                    medianDatasetExpression = record

                if record.ds_name == "limitSortBy":
                    limitSortBy = record

                if record.ds_name == "sampleTypeDisplayOrder":
                    sampleTypeDisplayOrderResult = record

                if record.ds_name == "sampleTypeDisplayGroups":
                    sampleTypeDisplayGroupsResult = record

                if record.ds_name == "maxGraphValue":
                    maxGraphValue = record


            returnList = {}
            try:
                if lineGraphOrdering != None:
                    returnList['lineGraphOrdering'] = lineGraphOrdering.ds_value
                else:
                    returnList['lineGraphOrdering'] = None
            except:
                returnList['lineGraphOrdering'] = None

            if detectionThreshold != None:
                returnList['detection_threshold'] = detectionThreshold.ds_value
            else:
                returnList['detection_threshold'] = 0

            if medianDatasetExpression != None:
                returnList['median_dataset_expression'] = medianDatasetExpression.ds_value
            else:
                returnList['median_dataset_expression'] = 0

            if limitSortBy != None:
                returnList['limit_sort_by'] = limitSortBy.ds_value
            else:
                returnList['limit_sort_by'] = 'Sample Type'

            if speciesResult != None:
                returnList['species'] = speciesResult.ds_value
            else:
                return None

            if sampleTypeDisplayOrderResult != None:
                returnList['sampleTypeDisplayOrder'] = sampleTypeDisplayOrderResult.ds_value
            else:
                return None

            if sampleTypeDisplayGroupsResult != None:
                returnList['sampleTypeDisplayGroups'] = sampleTypeDisplayGroupsResult.ds_value
            else:
                returnList['sampleTypeDisplayGroups'] = None

            try:
                if maxGraphValue != None:
                    returnList['maxGraphValue'] = maxGraphValue.ds_value
                else:
                    returnList['maxGraphValue'] = 30
            except:
                returnList['maxGraphValue'] = 30


            return returnList

        #except:
        #    return None


        # rewriting to use psycopg2
    @staticmethod
    def returnSpecies(db_id): #CRITICAL-2
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from annotation_databases where an_database_id =  %s;"
        cursor.execute(sql,(db_id,))

        # retrieve the records from the database
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result[1]

    @staticmethod
    def check_dataset_with_limitations(db,ds_id,uid):
        if uid == "":
            uid = 0
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        label_name = "user_dataset_availability"+delimiter+str(uid)
        try:
            dict_uid = json.loads(r_server.get(label_name).decode('utf-8'))
            #.decode('utf-8') is added for python3
            status= dict_uid[str(ds_id)]

            if status in ("Annotate","Admin"):
                status = "Available"
        except:
            status = "Unavailable"
        return status

    @staticmethod
    def check_dataset_availability(db,uid,ds_id,role=None):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        try:
            label_name = "user_dataset_availability"+delimiter+str(uid)
            dict_uid = json.loads(r_server.get(label_name))
        except:
            uid = 0 #default guest account
            label_name = "user_dataset_availability"+delimiter+str(uid)
            dict_uid = json.loads(r_server.get(label_name))

        if role is None:
            role = 'view'

        try:
            status= dict_uid[str(ds_id)]
        except:
            status = "None"

        if role == "view" and status in ("Admin","Annotate","Available"):
            return True

        if role == "annotator" and status in ("Admin","Annotate"):
            return True

        return False


    @staticmethod
    def get_dataset_availability(db,uid):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        try:
            label_name = "user_dataset_availability"+delimiter+str(uid)
            dict_uid = json.loads(r_server.get(label_name))
        except:
            uid = 0 #default guest account
            label_name = "user_dataset_availability"+delimiter+str(uid)
            dict_uid = json.loads(r_server.get(label_name))

        return dict_uid


    # only used through the api
    @staticmethod
    def getBiosamplesMetadata(db,ds_id=None): #CRITICAL-2
        returnList = Stemformatics_Dataset.get_biosamples_metadata(db,ds_id)
        return returnList

    # only used through the api
    @staticmethod
    def get_biosamples_metadata(db,ds_id=None): #CRITICAL-2
        returnList = []
        # Get biosamples metadata for a given dataset

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if ds_id is not None:

            sql = "select * from biosamples_metadata where ds_id = %s order by md_name,md_value;"
            data =(ds_id,)
            cursor.execute(sql,data)
        else:
            sql = "select * from biosamples_metadata order by md_name, md_value;"
            cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()
        conn.close()


        for row in result:
            returnList.append({
                'ds_id': row['ds_id'],
                'chip_id': row['chip_id'].encode('utf-8'),
                'md_name': row['md_name'].encode('utf-8'),
                'md_value': row['md_value'].encode('utf-8')
            })

        return returnList


    """
    As at 09/03/2015:

    getDatasetMetadata

    This function is deprecated. We will be transitioning to another way of searching that is
    based on Stemformatics_Dataset.dataset_search

    model/stemformatics/stemformatics_dataset.py
    280:        - getDatasetMetadataDetails
    281:        - getDatasetMetadata
    603:    280:        - getDatasetMetadataDetails
    604:    595:    def getDatasetMetadataDetails(db,ds_id,uid,raw=True): #CRITICAL-2
    605:    1240:        ds_md = Stemformatics_Dataset.getDatasetMetadataDetails(db,ds_id,uid)
    608:    def getDatasetMetadataDetails(db,ds_id,uid,raw=True): #CRITICAL-2
    909:    def getDatasetMetadata(db,ds_id=None): #CRITICAL-2
    1259:        ds_md = Stemformatics_Dataset.getDatasetMetadataDetails(db,ds_id,uid)

    controllers/api.py
    349:        ds_result = Stemformatics_Dataset.getDatasetMetadata(db)
    362:        ds_result = Stemformatics_Dataset.getDatasetMetadata(db,ds_id)

    Note: only used through the api
    """
    @staticmethod
    def getDatasetMetadata(db,ds_id=None): #CRITICAL-2
        ds_result = []
        db.schema = 'public'
        ds_md = db.dataset_metadata
        ds = db.datasets
        returnList = []

        if ds_id is not None:
            ds_md_result = ds_md.filter(ds_md.ds_id==ds_id).order_by('ds_name,ds_value').all()
            ds_result = ds.filter(ds.id == ds_id).first()
            handle = Stemformatics_Dataset.add_extra_to_handle(db,ds_result.handle,ds_result.private,ds_result.show_limited)
            returnList.append({
                'ds_name': 'handle',
                'ds_value': handle.encode('utf-8')
            })
            returnList.append({
                'ds_name': 's4m_dataset_id',
                'ds_value': str(ds_result.id).encode('utf-8')
            })
            returnList.append({
                'ds_name': 's4m_chip_type',
                'ds_value': str(ds_result.chip_type).encode('utf-8')
            })

        # Get ALL dataset metadata
        else:
            ds_md_result = ds_md.order_by('ds_name,ds_value').all()


        for tuple in ds_md_result:
            returnList.append({
                'ds_name': tuple.ds_name.encode('utf-8'),
                'ds_value': tuple.ds_value.encode('utf-8')
            })



        return returnList

    """
        Want to return None,"Public" or list of md5 list to be checked
    """
    @staticmethod
    def list_authorised_users(db,ds_id): #CRITICAL-2

        db.schema = 'public'
        ds = db.datasets

        ds_result = ds.filter(ds.id == ds_id).one()


        if ds_result.private or not ds_result.published:

            db.schema = 'stemformatics'
            override = db.override_private_datasets
            users = db.users

            join1 = db.join(override, users, override.uid == users.uid)

            result = join1.filter(override.ds_id == ds_id).all()

            if result == []:
                # if no override, return False
                return None
            else:
                # get list of overrides
                if ds_result.published:
                    list_authorised_users = [ hmac.new("stemformatics",user.username).hexdigest() for user in result]
                else:
                    list_authorised_users = []
                    for user in result:
                        if user.role=='annotator':
                            list_authorised_users.append(hmac.new("stemformatics",user.username).hexdigest())
                return list_authorised_users
        else:
            # ds_result is not private
            return "Public"


    @staticmethod
    def get_datasets_from_chip_type(db,chip_type,uid): #CRITICAL-2
        try:
            db.schema = 'public'
            ds = db.datasets

            where = (ds.chip_type == chip_type)
            result = ds.filter(where).all()

            return_result = []
            for dataset in result:
                ds_id = dataset.id

                if dataset.private:
                    available = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)
                else:
                    available = True

                if available:
                    return_result.append(ds_id)

            return return_result
        except:
            return None

    @staticmethod
    def get_metastore_mappings():
        mapping_for_metastore = {
            'AE Accession':'dataset_accession_ae',
            'Accession':'accession_id',
            'Affiliation': 'dataset_contributor_affiliation',
            'Assay Manufacturer': 'array_manufacturer',
            'Assay Platform': 'array_platform',
            'Assay Version': 'array_version',
            'Authors': 'publication_authors',
            'Contact Email': 'publication_contact_email',
            'Contact Name': 'publication_contact',
            'Contributor Email': 'dataset_contributor_email',
            'Contributor Name': 'dataset_contributor',
            'Description': 'publication_description',
            'Experimental Design': 'experiment_type',
            'GEO Accession': 'dataset_accession_geo',
            'Organism': 'species_long',
            'Platform': 'array_platform',
            'PubMed ID': 'publication_pubmed_id',
            'Publication Citation': 'publication_citation',
            'Publication Date': 'publication_date',
            'showAsPublication': 'show_as_publication',
            'Publication Title': 'publication_title',
            'Release Date': 'dataset_release_date',
            'Title': 'dataset_title',
            'cellSurfaceAntigenExpression': 'cell_surface_antigen_expression',
            'cellsSamplesAssayed': 'cells_samples_assayed',
            'cellularProteinExpression': 'cellular_protein_expression',
            'detectionThreshold': 'postnorm_expression_threshold',
            'handle': 'dataset_handle',
            'maxReplicates': 'max_replicates',
            'medianDatasetExpression': 'postnorm_expression_median',
            'minReplicates': 'min_replicates',
            'nucleicAcidExtract': 'nucleic_acid_extract',
            'probeCount': 'array_probe_count',
            'probesDetected': 'postnorm_probes_detected',
            's4mCurationDate': 's4m_curation_date',
            's4mCurator': 's4m_curator',
            'technologyUsed': 'technology_used',
            'topDifferentiallyExpressedGenes': 'top_genes'
            }
        return mapping_for_metastore


    @staticmethod
    def get_all_datasets_by_manufacturer(db,uid,db_id): #CRITICAL-2  #CRITICAL-3

        if db_id == int(config['human_db']): # 56
            species_set = "Human"
        if db_id == int(config['mouse_db']): # 46
            species_set = "Mouse"


        db.schema = 'public'
        ds = db.datasets
        ap = db.assay_platforms

        result = ds.all()

        return_result = {}
        for dataset in result:
            ds_id = dataset.id

            if dataset.private:
                available = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)
            else:
                available = True

            # check which manufacturer and type
            if available:
                platform_result = ap.filter(ap.chip_type==dataset.chip_type).one()

                manufacturer = platform_result.manufacturer
                platform_text = platform_result.platform
                species = platform_result.species

                if species == species_set:

                    if manufacturer not in return_result:
                        return_result[manufacturer] = {}

                    if "ST" in platform_text:
                        if "ST" not in return_result[manufacturer]:
                            return_result[manufacturer]['ST'] = []
                        return_result[manufacturer]['ST'].append(ds_id)
                    else:
                        if "NONST" not in return_result[manufacturer]:
                            return_result[manufacturer]['NONST'] = []
                        return_result[manufacturer]['NONST'].append(ds_id)



        return return_result

    @staticmethod
    def list_of_platforms():
        platforms={"Illumina:NONST":"Illumina", "Affymetrix:ST": "Affymetrix ST", "Affymetrix:NONST":"Affymetrix Gene Arrays", "Life Technologies:NONST": "Life Technologies SOLiD HTS" }
        return platforms

    @staticmethod
    def get_all_dataset_ids(db): #CRITICAL-2
        db.schema = 'public'
        ds = db.datasets
        result = ds.all()
        return result


    @staticmethod
    def get_all_datasets_for_user(db,uid,db_id): #CRITICAL-2 #CRITICAL-3

        if db_id == int(config['human_db']): # 56
            species_set = "Human"
        if db_id == int(config['mouse_db']): # 46
            species_set = "Mouse"


        db.schema = 'public'
        ds = db.datasets
        ap = db.assay_platforms

        result = ds.all()

        dataset_list = []
        for dataset in result:
            ds_id = dataset.id

            if dataset.private:
                available = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)
            else:
                available = True

            # check which manufacturer and type
            if available:
                platform_result = ap.filter(ap.chip_type==dataset.chip_type).one()
                manufacturer = platform_result.manufacturer
                platform_text = platform_result.platform
                species = platform_result.species

                if species == species_set:
                    dataset_list.append(ds_id)

        return dataset_list


    @staticmethod
    def add_override_private_dataset(db,object_type,object_id,ds_id): #CRITICAL-2
        db.schema = 'stemformatics'
        override = db.override_private_datasets
        # check if already there
        result_check = override.filter(and_(override.ds_id==ds_id,override.object_type==object_type,override.object_id==object_id)).all()
        if len(result_check) == 0:
            # then create if already there
            result = override.insert(ds_id=ds_id,object_type=object_type,object_id=object_id,role='view')
            Stemformatics_Dataset.triggers_for_change_in_dataset(db,ds_id)
            db.commit()
            db.flush()
            return True
        else:
            return False

    """
    this is used in get_all_x_platform_datasets_for_user to make it reusable
    """
    @staticmethod
    def _organise_yugene_datasets(result):
        dataset_dict = {}
        for row_result in result:
            ds_id = row_result['id']
            chip_type = row_result['chip_type']
            handle = row_result['handle']
            dataset_dict[ds_id] = {}
            dataset_dict[ds_id]['chip_type'] = chip_type
            dataset_dict[ds_id]['handle'] = handle

        return dataset_dict


    """
    x_platform was the original name for YuGene stuff
    Returns the ds_id, chip_type and availability of datasets for the user for Yugene graph

    uid is integer
    db_id is integer
    role is either normal, admin or annotator
    """
    @staticmethod
    def get_all_x_platform_datasets_for_user(uid,db_id,role = 'normal'): #CRITICAL-2 #CRITICAL-3

        # Cannot show yugene for more than one species. Therefore it is safe to always search on db_id
        if role == 'admin' or role == 'annotator':
            sql = "select id,handle,chip_type from datasets where show_yugene = true and db_id = %(db_id)s;"
            data = {"db_id":db_id}

            result = s4m_psycopg2._get_psycopg2_sql(sql,data)
            dataset_dict = Stemformatics_Dataset._organise_yugene_datasets(result)

        # Quicker to get all the datasets that the user can access from Redis
        if role == 'normal' or role == None:
            if uid == "":
                uid = 0
            r_server = redis.Redis(unix_socket_path=config['redis_server'])
            delimiter = config['redis_delimiter']
            label_name = "user_dataset_availability"+delimiter+str(uid)
            try:
                dict_ds_ids = json.loads(r_server.get(label_name).decode('utf-8'))
                temp_list_of_ds_ids = []
                for str_ds_id in dict_ds_ids:
                    ds_id = int(str_ds_id)
                    try:
                        status= dict_ds_ids[str_ds_id]
                    except:
                        status = "None"

                    if status in ("Admin","Annotate","Available"):
                        temp_list_of_ds_ids.append(ds_id)
            except Exception as e:
                #print(e)
                temp_list_of_ds_ids = None



            if temp_list_of_ds_ids is not None  :
                sql = "select id,handle,chip_type from datasets where show_yugene = true  and db_id = %(db_id)s and id = ANY (%(temp_list_of_ds_ids)s) ;"
                data = {"db_id":db_id,'temp_list_of_ds_ids':temp_list_of_ds_ids}
                result = s4m_psycopg2._get_psycopg2_sql(sql,data)
                dataset_dict = Stemformatics_Dataset._organise_yugene_datasets(result)
            else:
                dataset_dict = {}
        return dataset_dict


    # This is for returning search values to send via ajax to the front end for all dataset searching
    @staticmethod
    def search_and_choose_datasets(uid,searchQuery,filter_dict):

        if searchQuery is not None and searchQuery != "":
            datasets = Stemformatics_Dataset.dataset_search(uid,searchQuery, filter_dict)
        else:
            return "{}"

        data = {}
        temp_data = {}
        for ds_id in datasets:
            temp_dict = {}
            temp_dict['organism'] = datasets[ds_id]['organism']
            temp_dict['name'] = datasets[ds_id]['handle']
            temp_dict['title'] = datasets[ds_id]['title']
            temp_dict['cells_samples_assayed'] = datasets[ds_id]['cells_samples_assayed']

            data[ds_id] = temp_dict

        temp_data['filter'] = searchQuery
        temp_data['datasets'] = data
        temp_data['order'] = {} # implement later

        return temp_data


    @staticmethod
    def get_autocomplete_probes_for_dataset(search_term,ds_id,use_json):
        search_term = search_term.strip()
        search_term = search_term.split(' ')[0]
        search_term = search_term.split("\t")[0]

        probes_per_dataset_dir = config['DatasetProbeFiles']
        cmd ="grep "+search_term+" "+probes_per_dataset_dir+"/"+ds_id+".probes; exit 0"
        output = subprocess.check_output(cmd,shell=True)
        if output == "":
            return json.dumps(["No probes returned, please change your search"])
        output_list = output.split("\n")
        if len(output_list) > 100:
            return json.dumps(["Over 100 probes returned, please make your search more specific"])

        last_position = len(output_list) - 1
        if output_list[last_position] == "":
            output_list.pop(-1)
        #return temp_output_list
        if use_json:
            result = json.dumps(output_list)
        return result


    @staticmethod
    def allow_genePattern_analysis(db,ds_id): #CRITICAL-2
        db.schema = 'public'
        ds_md = db.dataset_metadata
        where = and_(ds_md.ds_id ==ds_id, ds_md.ds_name == 'genePatternAnalysisAccess',ds_md.ds_value=='Disable')
        result = ds_md.filter(where).all()
        if len(result) == 1:
            return False
        else:
            return True;


    @staticmethod
    def convert_ds_md_into_json(db,ds_id,uid): #CRITICAL-2
        json_ds_md = []
        ds_md = Stemformatics_Dataset.getDatasetMetadataDetails(db,ds_id,uid)
        del ds_md['breakDown']
        for item in ds_md:
             json_ds_md.append([item,ds_md[item]])

        ds_md = Stemformatics_Dataset._encodeData(ds_md)
        return [json.dumps(json_ds_md),ds_md]

    @staticmethod
    def convert_bs_md_into_json(db,ds_id,uid): #CRITICAL-2
        chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
        json_ds_md = []
        base_array = {}
        #header_array = ['chip_id','ds_id','chip_type','Sample Type','Replicate Group ID','Sample Description','Tissue','Cell Type','Organism'] # these are the first three columns all the time
        header_array = ['chip_id','ds_id','chip_type','Replicate Group ID','Sample name','Sample name long','Sample Type','Sample type long','Generic sample type','Generic sample type long','Sample Description','Tissue/organism part','Parental cell type','Final cell type','Cell line','Reprogramming method','Developmental stage','Media','Disease State','Labelling','Genetic modification','FACS profile','Age','Sex','Organism','Organism Part']

        bs_md = Stemformatics_Dataset.getBiosamplesMetadata(db,ds_id)
        for item in bs_md:
            chip_id = item['chip_id']
            ds_id = item['ds_id']
            annotation_type = item['md_name']
            annotation_value = item['md_value']

            if annotation_type not in header_array:
                header_array.append(annotation_type)

            if chip_id not in base_array:
                base_array[chip_id] = {}

            base_array[chip_id]['ds_id'] = ds_id
            base_array[chip_id]['chip_id'] = chip_id
            base_array[chip_id]['chip_type'] = chip_type
            base_array[chip_id][annotation_type] = annotation_value

        final_array = []
        for chip_id in base_array:
            chip_id_array = []

            for item in header_array:
                try:
                    chip_id_array.append(base_array[chip_id][item])
                except:
                    chip_id_array.append("")

            final_array.append(chip_id_array)

        return [json.dumps(header_array),json.dumps(final_array)]


    @staticmethod
    def convert_json_into_ds_md(json_ds_md):
        raw_ds_array = json.loads(json_ds_md)
        return_dict = {}
        return_text_data = ""
        for item in raw_ds_array:
            name = item[0]
            value = item[1]
            return_text_data += name+"="+value+"\n"
            return_dict[name] = value
        return [return_text_data,return_dict]


    @staticmethod
    def convert_json_into_bs_md(json_headers,json_bs_md,bs_md_text_required):
        raw_headers_array = json.loads(json_headers)
        from datetime import datetime
        raw_bs_md_array = json.loads(json_bs_md)
        first_chip_id = raw_bs_md_array[0]
        ds_id_key = raw_headers_array.index('ds_id')
        ds_id = first_chip_id[ds_id_key]
        chip_type_key = raw_headers_array.index('chip_type')
        chip_type = first_chip_id[chip_type_key]
        chip_id_key = raw_headers_array.index('chip_id')
        return_text_data = ""
        return_array = []

        # if statement is not added inside loop so as to save time when big dataset(6646,6936) with over 100 samples are being iterated over
        if(bs_md_text_required == "yes"):
            for item in raw_bs_md_array:
                chip_id = item[chip_id_key]
                count = 0
                for annotation_value in item:
                    if count not in [chip_type_key,chip_id_key,ds_id_key]:
                        annotation_type = raw_headers_array[count]
                        return_array.append({'ds_id':ds_id,'chip_type':chip_type,'chip_id':chip_id,'md_name':annotation_type,'md_value':annotation_value})
                        return_text_data += str(ds_id)+"\t"+str(chip_type)+"\t"+str(chip_id)+"\t"+annotation_type+"\t"+annotation_value+"\n"
                    count +=1

        else:
            for item in raw_bs_md_array:
                chip_id = item[chip_id_key]
                count = 0
                for annotation_value in item:
                    if count not in [chip_type_key,chip_id_key,ds_id_key]:
                        annotation_type = raw_headers_array[count]
                        return_array.append({'ds_id':ds_id,'chip_type':chip_type,'chip_id':chip_id,'md_name':annotation_type,'md_value':annotation_value})
                    count +=1



        return [return_text_data,return_array]


    @staticmethod
    def save_updated_annotation_metadata(db,bs_md_list,ds_md_dict,ds_id): #CRITICAL-2
        try:
            db.schema = 'public'
            b = db.biosamples_metadata
            d = db.dataset_metadata

            #delete all from biosamples_metadata for that ds_id
            b.filter(b.ds_id==ds_id).delete()
            # delete all from dataset_metadata for that ds_id
            d.filter(d.ds_id==ds_id).delete()

            for item in bs_md_list:
                chip_type = item['chip_type']
                chip_id = item['chip_id']
                md_name = item['md_name']
                md_value = item['md_value']
                result = b.insert(ds_id=ds_id, chip_type=chip_type,chip_id=chip_id,md_name = md_name,md_value=md_value)
            for ds_name in ds_md_dict:
                ds_value = ds_md_dict[ds_name]
                result = d.insert(ds_id=ds_id, ds_name = ds_name,ds_value=ds_value)
            db.commit()
            db.flush()
        except:
            db.session.rollback()
            return False

        return True

    @staticmethod
    def validate_updated_annotation_metadata(db,bs_md_text,ds_md_text,ds_id):
        # save the files
        unique_id = str(time.time())+str(ds_id)
        file_bs_md ='/tmp/validate_bs_md_'+unique_id
        f_bs_md = codecs.open(file_bs_md, 'w',"utf-8-sig")
        f_bs_md.write(bs_md_text)
        f_bs_md.close()

        file_ds_md ='/tmp/validate_ds_md_'+unique_id
        f_ds_md = codecs.open(file_ds_md, 'w',"utf-8-sig")
        f_ds_md.write(ds_md_text)
        f_ds_md.close()

        #then call curl
        # Register the streaming http handlers with urllib2
        register_openers()

        # Start the multipart/form-data encoding of the file "DSC0001.jpg"
        # "image1" is the name of the parameter, which is normally set
        # via the "name" parameter of the HTML <input> tag.

        # headers contains the necessary Content-Type and Content-Length
        # datagen is a generator object that yields the encoded parameters
        datagen, headers = multipart_encode({
            "biosamples_metadata": open(file_bs_md, "rb"),
            "metastore": open(file_ds_md, "rb"),
            "annotation-submit": "Validate Annotation Files"
        })

        # Create the Request object
        url = config['validator_url']
        request = urllib2.Request(url, datagen, headers)
        # Actually do the request, and get the response
        return_text = urllib2.urlopen(request).read()

        os.remove(file_bs_md)
        os.remove(file_ds_md)
        return return_text


    @staticmethod
    def get_chip_id_to_replicate_group_id_mappings(db,ds_id): #CRITICAL-2
        db.schema = 'public'
        bs_md = db.biosamples_metadata

        result_dict = {}
        result = bs_md.filter(and_(bs_md.ds_id==ds_id,bs_md.md_name == 'Replicate Group ID')).all()
        for row in result:
            result_dict[row.chip_id] = row.md_value
        return result_dict

    @staticmethod
    def refresh_dataset_stats_summary(db,ds_id=None):

        if ds_id is None:
            sql = "DELETE FROM stemformatics.stats_datasetsummary; INSERT INTO stemformatics.stats_datasetsummary SELECT bsm.ds_id, bsm.md_name, bsm.md_value, count(distinct bsm.chip_id) FROM biosamples_metadata bsm WHERE bsm.md_name IN ('Age', 'Cell Line', 'Cell Type', 'Cells Sorted For', 'Derived From', 'Developmental Stage', 'Differentiated To', 'Disease State', 'Gender', 'Organism', 'Organism Part', 'Pregnancy Status', 'Sample Type', 'Tissue') AND bsm.chip_id IN (SELECT chip_id FROM biosamples_metadata WHERE md_name='Replicate' AND md_value='1') GROUP BY bsm.ds_id, bsm.md_name, bsm.md_value ORDER BY bsm.ds_id, bsm.md_name, bsm.md_value;"
            db.execute(sql)

            sql = " update datasets set number_of_samples = (select count(distinct bsm.chip_id) from biosamples_metadata as bsm where bsm.md_name = 'Replicate Group ID' and bsm.ds_id = datasets.id and bsm.chip_id in (select chip_id from biosamples_metadata where md_name = 'Replicate' and md_value = '1') ) ;"

            db.execute(sql)

            db.commit()
            db.flush()
        else:

            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "DELETE FROM stemformatics.stats_datasetsummary where ds_id = %s; INSERT INTO stemformatics.stats_datasetsummary SELECT bsm.ds_id, bsm.md_name, bsm.md_value, count(distinct bsm.chip_id) FROM biosamples_metadata bsm WHERE bsm.md_name IN ('Age', 'Cell Line', 'Cell Type', 'Cells Sorted For', 'Derived From', 'Developmental Stage', 'Differentiated To', 'Disease State', 'Gender', 'Organism', 'Organism Part', 'Pregnancy Status', 'Sample Type', 'Tissue') AND bsm.chip_id IN (SELECT chip_id FROM biosamples_metadata WHERE md_name='Replicate' AND md_value='1') AND bsm.ds_id = %s GROUP BY bsm.ds_id, bsm.md_name, bsm.md_value ORDER BY bsm.ds_id, bsm.md_name, bsm.md_value;"
            data =(ds_id,ds_id,)
            cursor.execute(sql,data)
            sql = " update datasets set number_of_samples = (select count(distinct bsm.chip_id) from biosamples_metadata as bsm where bsm.md_name = 'Replicate Group ID' and bsm.ds_id = %s and bsm.chip_id in (select chip_id from biosamples_metadata where md_name = 'Replicate' and md_value = '1') ) ;"

            data =(ds_id,ds_id,)
            cursor.execute(sql,data)

            cursor.close()
            conn.close()








    """
    Originally this relied on the values being changed as being on the dataset record itself
    Will take into account MSC Access that is actually on the dataset_metadata record.
    Will have to look into this further on to handle more exceptions in a nicer way.
    """

    @staticmethod
    def update_dataset_single_field(db,uid,ds_id,update_dict): #CRITICAL-2
        try:
            # check uid is admin
            is_admin = Stemformatics_Admin.is_user_admin(db,uid)
            if not is_admin:
                return False
            else:



                db.schema = 'public'
                ds = db.datasets
                for field in update_dict:
                    value = update_dict[field]


                    # NOTE: this is just for the RohartMSCAccess which is in the dataset_metadata table
                    # check if this field is in the dataset metadata first, if it is, then make the change
                    conn_string = config['psycopg2_conn_string']
                    conn = psycopg2.connect(conn_string)
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                    sql = "select * from dataset_metadata where ds_id = %s and ds_name = %s;"
                    data = (ds_id,field,)
                    cursor.execute(sql,data)
                    # retrieve the records from the database
                    temp_result = cursor.fetchall()
                    cursor.close()
                    conn.close()


                    # if empty, then use dataset table, not dataset_metadata
                    if temp_result == []:
                        if value =="True":
                            value = True
                        if value =="False":
                            value = False
                        ds_result = ds.filter(ds.id == ds_id).update({field:value})
                        Stemformatics_Dataset.triggers_for_change_in_dataset(db,ds_id)
                        db.commit()

                    else:
                        # now save this into dataset metadata
                        conn_string = config['psycopg2_conn_string']
                        conn = psycopg2.connect(conn_string)
                        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                        sql = "update dataset_metadata set ds_value = %s where ds_id = %s and ds_name = %s;"
                        data = (value,ds_id,field,)
                        cursor.execute(sql,data)
                        conn.commit()
                        cursor.close()
                        conn.close()


                return True

        except:
            return False

    @staticmethod
    def triggers_for_change_in_dataset(db,ds_id = None):
        Stemformatics_Auth.setup_redis_get_dict_of_user_dataset_availability(db)
        Stemformatics_Dataset.setup_redis_choose_dataset_details(db)
        from S4M_pyramid.model.stemformatics.stemformatics_notification import Stemformatics_Notification # wouldn't work otherwise??
        Stemformatics_Notification.set_project_headers(db)


    @staticmethod
    def write_cls_file(db,ds_id,uid): #CRITICAL-6
        ds_id = int(ds_id)
        pylons.app_globals._push_object(config['pylons.app_globals'])
        redis_server = config['redis_server']
        cls_base_dir = config['DatasetCLSFiles']
        ds_result = Stemformatics_Dataset.getExpressionDatasetMetadata(db,ds_id,uid,True)
        return_text =ds_result['limit_sort_by'] + "<br/>"
        sort_type_list = ds_result['limit_sort_by'].split(',')
        build_dict = {}
        chip_type = Stemformatics_Dataset.getChipType(db,ds_id)

        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??

        sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)
        number_of_samples = len(sample_labels)
        for chip_id in sample_labels:
            for sort_by_type in sort_type_list:
                if sort_by_type not in build_dict:
                    build_dict[sort_by_type] = []
                if sort_by_type == 'Sample Type':
                    value = g.all_sample_metadata[chip_type][chip_id][ds_id]['Sample type long']
                else:
                    value = g.all_sample_metadata[chip_type][chip_id][ds_id][sort_by_type]+"_" + g.all_sample_metadata[chip_type][chip_id][ds_id]['Sample type long']

                build_dict[sort_by_type].append(value)


        for sort_by_type in build_dict:
            text_file = ""
            values_list = build_dict[sort_by_type]
            number_of_unique_values = len(set(values_list))
            text_file+=str(number_of_samples)+"\t"+str(number_of_unique_values)+"\t1\n"
            values_used = []
            second_line_text_file = "#"
            third_line_text_file = ""
            for value in values_list:
                if value not in values_used:
                    values_used.append(value)
                    if second_line_text_file == "":
                        second_line_text_file = value
                    else:
                        second_line_text_file +=" "+value
                cls_value = str(values_used.index(value))
                if third_line_text_file == "":
                    third_line_text_file =cls_value
                else:
                    third_line_text_file +=" "+cls_value

            text_file+=second_line_text_file+"\n"+third_line_text_file

            # now write this to the cls file
            if sort_by_type =='Sample Type':
                filename = cls_base_dir + str(ds_id) + '.cls'
            else:
                filename = cls_base_dir + str(ds_id) + sort_by_type.replace(' ','_')+'.cls'
            cls_file = codecs.open(filename,"w","utf-8")
            cls_file.write(text_file)
            cls_file.close()
            return_text+=filename  + "<br/>"

        return return_text



    @staticmethod
    def get_assay_platform_list(db):

        db.schema = 'public'
        ap = db.assay_platforms

        result = ap.all()
        return result

    @staticmethod
    def setup_new_dataset(db,ds_id):

        try:
            ds_id = int(ds_id)
        except:
            return "Error with this. Must be an integer"

        if ds_id == 0:
            return "Error with the dataset id. Cannot be 0"

        redis_remove_ds_id = config['redis_remove_ds_id']
        cmd = redis_remove_ds_id + " " + str(ds_id)

        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        p.stdout.close()


        # all samples
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        g.all_sample_metadata = Stemformatics_Expression.setup_dataset_sample_metadata(db,g.all_sample_metadata,ds_id)


        # python initialise.py localhost /var/www/pylons-data/SHARED/CUMULATIVEFiles 0
        redis_initialise_yugene = config['redis_initialise_x_platform']
        redis_initialise_gct = config['redis_initialise_gct']
        redis_server = config['redis_server']
        x_platform_base_dir = config['x_platform_base_dir']
        gct_base_dir = config['DatasetGCTFiles']


        # yugene redis
        cmd = redis_initialise_yugene + " " + redis_server + " " + x_platform_base_dir + " " + str(ds_id)
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        output = p.stdout.read()
        p.stdout.close()



        # gct redis
        cmd2 = redis_initialise_gct + " " + redis_server + " " + gct_base_dir + " " + str(ds_id)
        p2 = subprocess.Popen(cmd2, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        output2 = p2.stdout.read()
        p2.stdout.close()

        # user and dataset triggers
        Stemformatics_Dataset.triggers_for_change_in_dataset(db)



        Stemformatics_Auth.triggers_for_change_in_user(db)




        show_text = cmd + "<br><br>" + output.replace("\n","<br/>") + cmd2 + "<br><br>" + output2.replace("\n","<br/>") + "<br><br> Including all_sample_metadata and triggers for change in dataset and change in user.<br><br>Done! <a href='"+('/admin/index')+"'>Now click to go back</a> or go to <a href='" + ('/datasets/summary?datasetID='+str(ds_id))+"'>the dataset summary</a>"


        return show_text

    @staticmethod
    def get_number_of_datasets():
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select private,count(*) from datasets  where published group by private ;")

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        dataset_breakdown = {}
        for row in result:
            if row[0]:
                dataset_breakdown['Private'] = row[1]
            else:
                dataset_breakdown['Public'] = row[1]
        return dataset_breakdown

    @staticmethod
    def get_number_public_samples():
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select model_id as species,count(*) from biosamples_metadata as b left join datasets as d on d.id = b.ds_id left join annotation_databases as ad on ad.an_database_id = d.db_id where private = false and md_name = 'Replicate Group ID' group by model_id;")


        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        result_dict = {}
        for row in result:
            species = row['species']
            if species is not None:
                result_dict[species] = row['count']

        return result_dict

    @staticmethod
    def get_number_private_samples(db):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select species,count(*) from biosamples_metadata as b left join assay_platforms as ap on ap.chip_type = b.chip_type left join datasets as d on d.id = b.ds_id where private = true and md_name = 'Replicate Group ID' group by species;")

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        result_dict = {}
        for row in result:
            species = row['species']
            if species is not None:
                result_dict[species] = row['count']

        return result_dict




    @staticmethod
    def get_sample_chip_ids_in_order(db,chip_type,chip_ids,sort_by,ds_id):   #CRITICAL-2
        ds_id = int(ds_id)
        pylons.app_globals._push_object(config['pylons.app_globals'])
        temp_result_dict = {}
        map_replicate_group_id_to_chip_id = {}
        for chip_id in chip_ids:
            meta_data_values = g.all_sample_metadata[chip_type][chip_id][ds_id]
            replicate_group_id = meta_data_values['Replicate Group ID']
            sort_by_value = meta_data_values[sort_by]
            map_replicate_group_id_to_chip_id[replicate_group_id] = chip_id
            if sort_by_value not in temp_result_dict:
                temp_result_dict[sort_by_value] = {}
                temp_result_dict[sort_by_value]['replicate_group_id_list'] = []
            if replicate_group_id not in temp_result_dict[sort_by_value]:
                temp_result_dict[sort_by_value][replicate_group_id] = chip_id
                temp_result_dict[sort_by_value]['replicate_group_id_list'].append(replicate_group_id)

        if sort_by == 'Sample Type':
            db.schema = 'public'
            ds_md = db.dataset_metadata
            result = db.dataset_metadata.filter(and_(ds_md.ds_name=='sampleTypeDisplayOrder',ds_md.ds_id==ds_id)).all()
            for record in result:
                sample_type_display_order = record.ds_value.split(',')

            result_list = []
            #for sort_by_value in temp_result_dict:
            for sort_by_value in sample_type_display_order:
                replicate_group_id_list = temp_result_dict[sort_by_value]['replicate_group_id_list']
                replicate_group_id_list.sort()
                for replicate_group_id in replicate_group_id_list:
                    chip_id = map_replicate_group_id_to_chip_id[replicate_group_id]
                    result_list.append(chip_id)
                    #result_list.append(replicate_group_id)
        return result_list


    @staticmethod
    def get_msc_samples(db,msc_set):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


        if msc_set == 'All':
            sql = "select * from biosamples_metadata where md_name = 'project_msc_set' and md_value != '' and md_value != 'NULL';"
            cursor.execute(sql)
        else:
            sql = "select * from biosamples_metadata where md_name = 'project_msc_set' and md_value = %s"
            cursor.execute(sql,(msc_set,))
        result = cursor.fetchall()
        cursor.close()

        list_of_ds_ids = []
        list_of_chip_types = []
        result_dict = {}
        for row in result:
            ds_id = row['ds_id']
            chip_type = row['chip_type']
            md_name = row['md_name']
            md_value = row['md_value']
            chip_id = row['chip_id']


            if ds_id not in result_dict:
                result_dict[ds_id] = {}

            if chip_id not in result_dict[ds_id]:
                result_dict[ds_id][chip_id] = {}

            # this should be msc_set as the md_name
            result_dict[ds_id][chip_id][md_name] = md_value

            list_of_ds_ids.append(str(ds_id))
            list_of_chip_types.append(str(chip_type))




        list_of_ds_id = list(set(list_of_ds_ids))
        list_of_chip_types = list(set(list_of_chip_types))

        if len(list_of_chip_types) == 0:
            return {}

        sql_list_of_ds_ids = ",".join(list_of_ds_ids)
        sql_list_of_chip_types = ",".join(list_of_chip_types)
        sql = "select * from biosamples_metadata where md_name in ('Replicate Group ID','Sample Type','project_msc_type','project_msc_why') and chip_type in ("+sql_list_of_chip_types+") and ds_id in ("+sql_list_of_ds_ids+");"

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql)
        result_msc_other = cursor.fetchall()
        cursor.close()
        conn.close()


        for row in result_msc_other:
            ds_id = row['ds_id']
            chip_type = row['chip_type']
            md_name = row['md_name']
            md_value = row['md_value']
            chip_id = row['chip_id']


            if chip_id not in result_dict[ds_id]:
                continue

            # this should be msc_flag or msc_why as the md_name
            result_dict[ds_id][chip_id][md_name] = md_value


        return result_dict


    @staticmethod
    def build_gct_from_redis(db,ref_type,ref_id,ds_id,uid,options): #CRITICAL-4

        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        from S4M_pyramid.model.stemformatics.stemformatics_gene_set import Stemformatics_Gene_Set # wouldn't work otherwise??
        use_galaxy = config['use_galaxy_server']

        # get chip type from dataset id
        sort_by = 'Sample Type'
        human_db = config['human_db']
        mouse_db = config['mouse_db']
        db_id = Stemformatics_Dataset.get_db_id(db,ds_id)
        chip_type = Stemformatics_Dataset.getChipType(db,ds_id)

        sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)
        sample_chip_ids_in_order = Stemformatics_Dataset.get_sample_chip_ids_in_order(db,chip_type,sample_labels,sort_by,ds_id)

        if ref_type == 'gene_set_id':
            gene_set_id = int(ref_id)
            result = Stemformatics_Gene_Set.get_probes_from_gene_set_id(db,db_id,ds_id,gene_set_id)
            probe_list = result[0]
            probe_dict = result[1] # this has probe to gene symbols

        if ref_type == 'probes':
            delimiter = config['delimiter']
            if use_galaxy == "no":
                temp_probes = ref_id.split(delimiter)
                probe_list = [ probe.strip() for probe in temp_probes]
            else:
                probe_list = ref_id
            from S4M_pyramid.model.stemformatics.stemformatics_probe import Stemformatics_Probe # wouldn't work otherwise??
            probe_dict = Stemformatics_Probe.get_gene_mappings_for_probe(probe_list,db_id,chip_type)

        # now go through gct file and convert probe ids to be gene name and probe ids
        remove_chipids_position = []
        remove_chip_ids = []
        if 'remove_chip_ids' in options:
            remove_chip_ids = options['remove_chip_ids']
            for chip_id in remove_chip_ids:
                position = sample_labels.index(chip_id)
                remove_chipids_position.append(position)

        # Check for duplicate probe_list
        known_probes = set()
        temp_probe_list = []
        for probe in probe_list:
            if probe not in known_probes:
                temp_probe_list.append(probe)
                known_probes.add(probe)
        probe_list = temp_probe_list

        probe_expression_rows = Stemformatics_Expression.get_expression_rows(ds_id,probe_list)

        returnList = {}
        number_of_rows = 0
        metaDataList = {}
        gct_text = ""
        for row in probe_list:
            probe_id = row

            # Task #1686 - if probe not in probe expression rows, then ingore
            if probe_id not in probe_expression_rows:
                continue

            try:
                gene = probe_dict[probe_id] + " "
            except:
                gene = ""

            if 'no_gct_header' in options:
                gct_row_text = gene+ probe_id
            else:
                gct_row_text = gene+ probe_id + "\t"+"na"



            for chip_id in sample_chip_ids_in_order:
                sample_count = sample_labels.index(chip_id)
                if sample_count not in remove_chipids_position:
                    expression_value = probe_expression_rows[probe_id][sample_count]
                    if expression_value != '' and expression_value != 'None':
                        expression_value = float(expression_value)
                    else:
                        # this was for Next Gen Sequencing data. Shouldn't really be used at all
                        # Problem is setting a value like 0, -1, or -9999 causes issues with the data
                        # and you cannot just set the value to be blank

                        # 2017-02-15 Setting this to be blank and let things error out.
                        expression_value = ""
                    gct_row_text += "\t" + str(expression_value)

            gct_row_text += "\n"
            gct_text += gct_row_text
            number_of_rows = number_of_rows + 1;


        # Have to count the number of rows by probe - as we are removing anything that isn't in the list
        number_of_samples = len(sample_labels) - len(remove_chip_ids)
        if 'no_gct_header' in options:
            new_gct_header = Stemformatics_Expression.return_gct_file_sample_headers_as_replicate_group_id(db,ds_id,sample_chip_ids_in_order,remove_chip_ids,"NAME")
            gct_text = new_gct_header + gct_text
        else:
            new_gct_header = Stemformatics_Expression.return_gct_file_sample_headers_as_replicate_group_id(db,ds_id,sample_chip_ids_in_order,remove_chip_ids)
            gct_text = "#1.2\n"+str(number_of_rows)+"\t"+str(number_of_samples)+"\n"+new_gct_header + gct_text

        return gct_text


    @staticmethod
    def write_gct_file(gct_text,gct_filename):
        gct_file = codecs.open(gct_filename,"w","utf-8")
        gct_file.write(gct_text)
        gct_file.close()



    @staticmethod
    def add_sample_metadata(ds_id,metadata_name,default_value):
        ds_id = int(ds_id)
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = "insert into biosamples_metadata (chip_type, chip_id,md_name,md_value,ds_id) select chip_type,chip_id,%s,%s,ds_id from biosamples_metadata where md_name = 'Replicate Group ID' and ds_id = %s"
        cursor.execute(sql,(metadata_name,default_value,ds_id,))
        conn.commit()
        cursor.close()


        return True


    @staticmethod
    def add_dataset_metadata(ds_id,metadata_name,default_value):
        ds_id = int(ds_id)
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = "insert into dataset_metadata (ds_id,ds_name,ds_value) VALUES (%s,%s,%s);"
        cursor.execute(sql,(ds_id,metadata_name,default_value,))
        conn.commit()
        cursor.close()

        return True

    @staticmethod
    def add_metadata_for_msc_project(ds_id):
        default_value = ''
        metadata_name = 'project_msc_set'
        Stemformatics_Dataset.add_sample_metadata(ds_id,metadata_name,default_value)

        metadata_name = 'project_msc_type'
        Stemformatics_Dataset.add_sample_metadata(ds_id,metadata_name,default_value)

        metadata_name = 'project_msc_why'
        Stemformatics_Dataset.add_sample_metadata(ds_id,metadata_name,default_value)
        return True

    @staticmethod
    def add_metadata_for_line_graph(ds_id):
        default_value = ''
        metadata_name = 'Day'
        Stemformatics_Dataset.add_sample_metadata(ds_id,metadata_name,default_value)

        metadata_name = 'LineGraphGroup'
        Stemformatics_Dataset.add_sample_metadata(ds_id,metadata_name,default_value)

        metadata_name = 'lineGraphOrdering'
        default_value = 'NULL'
        Stemformatics_Dataset.add_dataset_metadata(ds_id,metadata_name,default_value)
        return True

    @staticmethod
    def get_thomson_reuters_feed():

        this_time = datetime.datetime.now()
        current_date = this_time.strftime("%Y-%m-%d")
        email = config['feedback_email']
        conn_string = config['psycopg2_conn_string']
        repo_name = config['site_name']
        language = 'English'


        mapping_dict = {'Authors':'Author elements','Title':'Title','Description':'Abstract','Organism':'Organism Name','PubMed ID':'Citations','topDifferentiallyExpressedGenes':'Gene name'}


        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from datasets as d left join dataset_metadata as ds_md on ds_md.ds_id = d.id where d.private = false and ds_md.ds_name in ('Authors','Title','Description','Organism','Contact Name','Contact Email','AE Accession','GEO Accession','PubMed ID','topDifferentiallyExpressedGenes','Platform');"
        cursor.execute(sql)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        datasets = {}
        for row in result:
            ds_id = row['id']
            if ds_id not in datasets:
                handle = row['handle']
                year = handle.split('_')[1]
                external_base_url = url('/',qualified=True)
                base_url = external_base_url + url('datasets/search?ds_id=')+str(ds_id)
                #base_url = '/datasets/search?ds_id='+str(ds_id)
                datasets[ds_id] = {'Record ID': ds_id,'Language':language,'Repository Name': repo_name,'SourceRepository': repo_name,'Date Provided':current_date,'Year': year,'Source URL':base_url,'Owner':email}

            ds_name = row['ds_name']
            ds_value = row['ds_value']

            try:
                meta_name = mapping_dict[ds_name]
            except:
                meta_name = ds_name
            datasets[ds_id][meta_name] = ds_value

        return datasets

    @staticmethod
    def create_thomson_reuters_xml_file(datasets):

        file_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<feed>\n"

        for ds_id in datasets:
            row = datasets[ds_id]
            file_text += "\t<dataset id='"+str(ds_id)+"'>\n"
            for temp_ds_name in row:
                ds_value = str(row[temp_ds_name])
                ds_name  = temp_ds_name.replace(' ','_')
                file_text += "\t\t<"+ds_name+"><![CDATA["+ds_value+"]]></"+ds_name+">\n"

            file_text += "\t</dataset>\n"
        file_text +="</feed>\n"
        return file_text


    # This gets the results from the searches and outputs a list of dataset ids
    # example of temp_result_list - [[[6371], [6544], [6834], [6288], [6278]]]
    @staticmethod
    def _extract_ds_ids_for_datasets_and_samples_search(temp_result_list):
        ds_ids = []
        for temp in temp_result_list:
            for row in temp:
                ds_id = row[0]
                ds_ids.append(ds_id)

        ds_ids = list(set(ds_ids))
        ds_ids.sort()

        return ds_ids


    """
    returns all samples and datasets based on sample and metadata search.

    basic use of the 'and' variable

    used in download_multiple_datasets and yugene search
    """
    @staticmethod
    def find_datasets_and_samples(search,get_samples,uid,all_sample_metadata=None):


        resultList = {}

        # https://stackoverflow.com/questions/9519734/python-regex-to-find-a-string-in-double-quotes-within-a-string
        search_on_double_quotes_list=re.findall(r'\"(.+?)\"',search)

        for item in search_on_double_quotes_list:

            search = search.replace(item,"")


        search = search.replace('"','')

        list_of_search_terms = search_on_double_quotes_list

        split_on_space_list = search.split(' ')

        for term in split_on_space_list:
            if term == '':
                continue
            list_of_search_terms.append(term.strip())


        temp_result_list_dataset = []
        temp_result_list_sample = []

        all_samples = []
        all_samples_by_ds_id = {}

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        for search_term in list_of_search_terms:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select ds_id from dataset_metadata where ds_value ilike %s"
            sql = sql + " group by ds_id;"
            data =("%"+search_term.strip()+"%",)
            cursor.execute(sql,data)
            # retrieve the records from the database
            result = cursor.fetchall()
            #result is a list of lists of lists
            temp_result_list_dataset.append(result)
            cursor.close()


            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # need to ensure that ds_id is the first field shown for either sql query
            if get_samples == True:
                sql = "select ds_id,max(chip_type),chip_id from biosamples_metadata where md_value ilike %s group by ds_id,chip_id order by ds_id,chip_id;"
            else:
                sql = "select ds_id from biosamples_metadata where md_value ilike %s group by ds_id order by ds_id;"

            data =("%"+search_term.strip()+"%",)
            cursor.execute(sql,data)
            # retrieve the records from the database
            result = cursor.fetchall()

            if get_samples == True:
                for sample in result:
                    ds_id = sample[0]
                    all_samples.append(sample)
                    if ds_id not in all_samples_by_ds_id:
                        all_samples_by_ds_id[ds_id] = []
                    if sample not in all_samples_by_ds_id[ds_id]:
                        all_samples_by_ds_id[ds_id].append(sample)

            temp_result_list_sample.append(result)
            cursor.close()
        conn.close()



        # we want to just get the datasets for the dataset search and the sample search and do an OR
        # so we get the maximum amount of datasets
        # example of temp_result_list_dataset - [[[6371], [6544], [6834], [6288], [6278]]]
        # expecting the initial field in the final list to be the ds_id
        ds_ids_dataset = Stemformatics_Dataset._extract_ds_ids_for_datasets_and_samples_search(temp_result_list_dataset)
        ds_ids_sample = Stemformatics_Dataset._extract_ds_ids_for_datasets_and_samples_search(temp_result_list_sample)
        ds_ids = []



        for ds_id in ds_ids_dataset:
            ds_ids.append(ds_id)

        for ds_id in ds_ids_sample:
            ds_ids.append(ds_id)

        ds_ids = list(set(ds_ids))

        used_ds_ids = []

        for ds_id in ds_ids:
            db= None
            dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,uid)
            if dataset_status == "Unavailable":
                continue
            if dataset_status == "Limited" and show_limited == False:
                continue

            ds_mt_result = {}


            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from dataset_metadata where ds_id = %s ;",(ds_id,))
            # retrieve the records from the database
            ds_metadata_result = cursor.fetchall()
            cursor.close()
            conn.close()


            for r in ds_metadata_result:
                ds_mt_result[r['ds_name']] = r['ds_value']

            used_ds_ids.append(ds_id)
            resultList[ds_id] = Stemformatics_Dataset._encodeData(ds_mt_result)
            extra = ""

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from datasets where id  = ANY (%s) ;",(used_ds_ids,))
        # retrieve the records from the database
        result_ds = cursor.fetchall()
        cursor.close()
        conn.close()


        for ds_detail in result_ds:

            ds_id = ds_detail['id']
            new_handle = Stemformatics_Dataset.add_extra_to_handle(db,ds_detail['handle'],ds_detail['private'],ds_detail['show_limited'])

            resultList[ds_id]['handle'] = new_handle
            resultList[ds_id]['private'] = ds_detail['private']
            resultList[ds_id]['published'] = ds_detail['published']
            resultList[ds_id]['show_yugene'] = ds_detail['show_yugene']
            resultList[ds_id]['number_of_samples'] = ds_detail['number_of_samples']
            resultList[ds_id]['show_limited'] = ds_detail['show_limited']
            resultList[ds_id]['dataset_status'] = dataset_status
            resultList[ds_id]['breakDown'] = {}

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from stemformatics.stats_datasetsummary where ds_id  = ANY (%s) ;",(used_ds_ids,))
        # retrieve the records from the database
        ds_stats = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in ds_stats:
            ds_id = int(row['ds_id'])
            md_name = row['md_name']
            md_value = row['md_value']
            count = row['count']

            if 'breakDown' not in resultList[ds_id]:
                resultList[ds_id]['breakDown'] = {}

            resultList[ds_id]['breakDown'][md_name +': '+ md_value]= count



        return {'datasets':resultList,'all_samples':all_samples,'all_samples_by_ds_id':all_samples_by_ds_id}

    @staticmethod
    def check_dataset_availability_by_export_key(db,uid,export_key,ds_id):
        valid_key = Stemformatics_Auth.validate_export_key(export_key,uid)
        if valid_key:
            available = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)
            return available
        else:
            return False

    """
    Please note that the public datasets will first check the uid (of 0) and
    will always use the validation of logged_in.
    """
    @staticmethod
    def audit_download_dataset(uid,ds_id,download_type,ip_address,permission_used):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        date_created = datetime.datetime.now()
        cursor.execute("insert into stemformatics.dataset_download_audits values(%s,%s,%s,%s,%s,%s) ;",(uid,ds_id,download_type,ip_address,date_created,permission_used,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    """
    datasets must be a dict of with datasets[ds_id]['handle'] at the minimum
    filter_ds_ids is a list of ds_ids that is the list of ds_ids that are selected
    """
    @staticmethod
    def create_download_script_for_multiple_datasets(datasets,uid,username,filter_ds_ids,file_types=['yugene','gct']):
        if uid == 0:
            export_key = 'na'
        else:
            export_key = Stemformatics_Auth.create_export_key(uid)

        url_yugene_download = h.url('/datasets/download_yugene/',qualified=True)
        url_gct_download = h.url('/datasets/download_gct/',qualified=True)
        return_data = "#!/bin/bash\n"
        return_data += "####################################################################\n"
        return_data += "# This is a script to download from a Mac/Linux/Unix computer\n"
        return_data += "# You will need to have wget installed \n"
        return_data += "# You will need to run this script within "+str(config['export_key_validity']) +" days.\n"
        return_data += "# The following commands assume that you are on a terminal in the same directory as the script\n"
        return_data += "# You will need to make this script executable by using the command below\n"
        return_data += "# chmod 744 multi_download_script.sh \n"
        return_data += "# You will need to run by using the command below \n"
        return_data += "# ./multi_download_script.sh \n"
        return_data += "####################################################################\n"
        for ds_id in datasets:
            if filter_ds_ids is not None and ds_id not in filter_ds_ids:
                continue

            for temp_type in file_types:
                if temp_type == 'yugene':
                    return_data += "wget \""+url_yugene_download+str(ds_id)+"?username="+username+"&export_key="+export_key+"\" -O "+ str(ds_id) + "_" + datasets[ds_id]['handle']+ ".yugene.txt\n"
                if temp_type == 'gct':
                    return_data += "wget \""+url_gct_download+str(ds_id)+"?username="+username+"&export_key="+export_key+"\" -O "+ str(ds_id) + "_" + datasets[ds_id]['handle']+ ".gct\n"
        return return_data


    @staticmethod
    def get_dataset_mapping_id(ds_id=0):
        result = {}
        try:
            ds_id = int(ds_id)
        except:
            return result

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if ds_id == 0:
            sql = "select id as ds_id,d.mapping_id from datasets as d left join assay_platforms as ap on ap.chip_type = d.chip_type;"
            cursor.execute(sql)
        else:
            sql = "select id as ds_id,d.mapping_id from datasets as d left join assay_platforms as ap on ap.chip_type = d.chip_type where id = %s;"
            cursor.execute(sql,(ds_id,))

        temp_result = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in temp_result:
            try:
                ds_id = int(row['ds_id'])
                mapping_id = int(row['mapping_id'])
            except:
                ds_id = 0
                mapping_id = 0

            result[ds_id] = mapping_id


        return result

    @staticmethod
    def set_datasets_mapping_id_into_redis():
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "Select id from datasets ;"
        cursor.execute(sql,)
        ds_id_list = cursor.fetchall()
        ds_ids = []
        for row in ds_id_list:
            ds_ids.append(row[0])
        cursor.close()
        conn.close()

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select id as ds_id,d.mapping_id from datasets as d left join assay_platforms as ap on ap.chip_type = d.chip_type where id in %(ds_ids)s;",{"ds_ids":tuple(ds_ids)})
        temp_result = cursor.fetchall()
        cursor.close()
        conn.close()

        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        expiry_time = config['expiry_time']

        data = {}
        for row in temp_result:
            ds_id = (row['ds_id'])
            mapping_id = (row['mapping_id'])
            data[ds_id] = mapping_id

        label_name = "dataset_mapping_data"
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        mapping_id_data = Stemformatics_Expression.pickle_expression_data(data)
        result = r_server.set(label_name,mapping_id_data)
        if result == True:
            # expiry = r_server.expire(label_name,expiry_time)
            return True
        else:
            return False

    @staticmethod
    def text_for_download_ds_id_mapping_id_file(ds_id_mapping_id_dictionary):
        if not isinstance(ds_id_mapping_id_dictionary, dict):
            text = "Invalid data."
            return text

        text_header = "ds_id\tmapping_id\n"
        text = ""
        for ds_id in ds_id_mapping_id_dictionary:
            columns= []
            mapping_id = str(ds_id_mapping_id_dictionary[ds_id])
            ds_id = str(ds_id)
            columns.append(ds_id)
            columns.append(mapping_id)
            text += "\t".join(columns)+ "\n"

        if text == "":
            text = "No data found."
        else:
            text = text_header + text

        return text


    @staticmethod
    def refresh_probe_mappings_to_download():
        try:
            cmd = "/data/repo/git-working/stemformatics_tools/feature_mappings/setup_download_mappings.sh  prod localhost portal_prod"
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
            output = p.stdout.read()
            p.stdout.close()
        except:
            output = 'Error in refreshing the probe mappings to download.'
        return output

    @staticmethod
    def export_download_dataset_metadata(data,export_type,ds_ids,all_sample_metadata,uid,user):
        try:
            filter_ds_ids = []
            temp_filter_ds_ids = ds_ids.split(',')
            for ds_id in temp_filter_ds_ids:
                filter_ds_ids.append(int(ds_id))
        except:
            filter_ds_ids = None

        all_samples_by_ds_id = data['all_samples_by_ds_id']

        if export_type == 'datasets':
            row_list = ['ds_id','handle','title','organism','samples found','all_samples']
            return_data = "\t".join(row_list) + "\n"
            for ds_id in data['datasets']:
                if filter_ds_ids is not None and ds_id not in filter_ds_ids:
                    continue

                row_list = []
                row_list.append(str(ds_id))
                row_list.append(data['datasets'][ds_id]['handle'])
                row_list.append(data['datasets'][ds_id]['title'])
                row_list.append(data['datasets'][ds_id]['organism'])

                if ds_id in all_samples_by_ds_id:
                    row_list.append(str(len(all_samples_by_ds_id[ds_id])))
                else:
                    row_list.append('0')

                row_list.append(str(data['datasets'][ds_id]['number_of_samples']))
                row = "\t".join(row_list) + "\n"
                return_data  += row
        if export_type =='samples':
            row_list = ['species','ds_id','handle','chip_id','sample_id','sample_type']
            return_data = "\t".join(row_list) + "\n"
            for ds_id in data['datasets']:
                if filter_ds_ids is not None and ds_id not in filter_ds_ids:
                    continue
                if ds_id in all_samples_by_ds_id:
                    for sample in all_samples_by_ds_id[ds_id]:
                        row_list = []
                        row_list.append(data['datasets'][ds_id]['organism'])
                        row_list.append(str(ds_id))
                        row_list.append(data['datasets'][ds_id]['handle'])
                        chip_type = sample[1]
                        chip_id = sample[2]
                        metadata_values = all_sample_metadata[chip_type][chip_id][ds_id]
                        row_list.append(chip_id)
                        row_list.append(metadata_values['Replicate Group ID'])
                        row_list.append(metadata_values['Sample Type'])
                        row = "\t".join(row_list) + "\n"
                        return_data +=row
        if export_type == 'download_script':
            #c.user is actually username eg. rowland.mosbergen@mailinator.com
            return_data = Stemformatics_Dataset.create_download_script_for_multiple_datasets(data['datasets'],uid,user,filter_ds_ids)
        return return_data


    @staticmethod
    def get_data_publications():
        result = {}
        order_publications = []
        return_result = []
        try:
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            sql = "select * from dataset_metadata where ds_id in (select ds_id from dataset_metadata where ds_name = 'showAsPublication' and ds_value = 'True');"

            cursor.execute(sql)

            temp_result = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in temp_result:
                ds_id = row['ds_id']
                ds_name = row['ds_name']
                ds_value = row['ds_value']

                if ds_id not in result:
                    result[ds_id] = {}

                result[ds_id][ds_name] = ds_value
                if ds_name == 'Publication Date':
                    date = ds_value
                    order_publications.append([date,ds_id])


            order_publications.sort(reverse=True)
            for row in order_publications:
                ds_id = row[1]
                data = result[ds_id]
                data['ds_id'] = ds_id
                return_result.append(data)
        except:
            pass

        return return_result

    @staticmethod
    def get_default_dataset(db_id):

        try:
            db_id = int(db_id)
        except:
            ds_id = None
            return ds_id

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select id from datasets where db_id = %s order by id asc limit 1;"
        data = (db_id,)
        cursor.execute(sql, data)

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if result == []:
            ds_id = None
        else:
            ds_id = int(result[0]['id'])
        return ds_id



    @staticmethod
    def redis_check():

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select id from datasets order by id;"
        cursor.execute(sql)

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        #Get a list of ds_ids from the database
        db_list_of_ds_ids = []
        for row in result:
            ds_id = row['id']
            db_list_of_ds_ids.append(ds_id)

        gct_dir = config['DatasetGCTFiles']

        #Get a list of ds_ids from the gct files
        os.chdir(gct_dir)
        gct_files = glob.glob('dataset*.gct')
        gct_list_of_ds_ids = []
        for file_name in gct_files:
            temp = re.findall(r'\d+',file_name)
            ds_id = int(temp[0])
            gct_list_of_ds_ids.append(ds_id)


        # merge the two lists and find the unique list from them
        full_list_of_ds_ids = list(set(gct_list_of_ds_ids + db_list_of_ds_ids))

        full_list_of_ds_ids.sort()


        result_dict = {}


        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??

        problem_list = []
        ok_list = []
        # now go through complete list and check for missing things
        for ds_id in full_list_of_ds_ids:

            status_ok = True

            in_db = True
            if ds_id not in db_list_of_ds_ids:
                in_db = False
                status_ok = False

            in_gct = True
            if ds_id not in gct_list_of_ds_ids:
                in_gct = False
                status_ok = False

            in_redis = True
            result = Stemformatics_Expression.get_sample_labels(ds_id)
            if result is None:
                in_redis = False
                status_ok = False


            if status_ok:
                ok_list.append(ds_id)
            else:
                problem_list.append(ds_id)

            result_dict[ds_id] = {'in_db':in_db,'in_gct':in_gct,'in_redis':in_redis}


        return {'ok_list':ok_list,'problem_list':problem_list,'result_dict':result_dict}


    @staticmethod
    def get_expression_dataset_metadata(ds_id):
        # first check in redis
        redis_data = Stemformatics_Dataset.get_expression_dataset_metadata_from_redis(ds_id)
        if redis_data is not None:
            return redis_data
        # otherwise get the data from database
        data = Stemformatics_Dataset.get_expression_dataset_metadata_from_database(ds_id)
        # set into redis
        result = Stemformatics_Dataset.set_expression_dataset_metadata_into_redis(ds_id,data)
        if result == True:
            return data
        else:
            return "Something went wrong in setting the data"



    @staticmethod
    def get_expression_dataset_metadata_from_database(ds_id):
        user_id = 0
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from dataset_metadata where ds_id = %(ds_id)s;",{"ds_id":ds_id})

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        ds_md = {}
        for row in result:
            ds_name = row[1]
            ds_value = row[2]
            ds_md[ds_name] = ds_value

        # this is the minimum metadata required for creating a d3 graph
        ds_md_for_graph = {}
        ds_md_for_graph["limitSortBy"] = ds_md["limitSortBy"]
        ds_md_for_graph["Title"] = ds_md["Title"]
        ds_md_for_graph["detectionThreshold"] = ds_md["detectionThreshold"]
        ds_md_for_graph["medianDatasetExpression"] = ds_md["medianDatasetExpression"]
        ds_md_for_graph["sampleTypeDisplayOrder"] = ds_md["sampleTypeDisplayOrder"]
        ds_md_for_graph["cellsSamplesAssayed"] = ds_md["cellsSamplesAssayed"]
        ds_md_for_graph["yAxisLabel"] = ds_md["yAxisLabel"]
        ds_md_for_graph["sampleTypeDisplayGroups"] = sampleTypeDisplayGroups=  ds_md["sampleTypeDisplayGroups"]
        # get colours
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        ds_md_for_graph['sampleTypeDisplayGroupColours'] = Stemformatics_Expression.return_sample_type_display_group_colours(sampleTypeDisplayGroups)
        ds_md_for_graph['probeColours'] = Stemformatics_Expression.get_colours_for_graph(user_id,ds_id)
        if "lineGraphOrdering" in ds_md:
            if (ds_md["lineGraphOrdering"]) != u'NULL' and (ds_md["lineGraphOrdering"]) != u'':
                ds_md_for_graph["lineGraphOrdering"] = lineGraphOrdering = ds_md["lineGraphOrdering"]
                ds_md_for_graph['lineGraphColours'] = Stemformatics_Expression.return_sample_type_display_group_colours(lineGraphOrdering)


        return ds_md_for_graph


    @staticmethod
    def set_expression_dataset_metadata_into_redis(ds_id,dataset_metadata):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        expiry_time = config['expiry_time']

        label_name = "dataset_metadata"+ delimiter + str(ds_id)
        # pickle the data
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        data = Stemformatics_Expression.pickle_expression_data(dataset_metadata)
        # store pickled data in redis with labelname
        result = r_server.set(label_name,data)

        if result == True:
            result = r_server.expire(label_name,expiry_time)

        return result


    @staticmethod
    def get_expression_dataset_metadata_from_redis(ds_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        label_name = "dataset_metadata"+ delimiter + str(ds_id)
        result = r_server.get(label_name)
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        if result is not None:
            result = Stemformatics_Expression.unpickle_expression_data(result)
        return result

    @staticmethod
    def check_private_dataset(ds_id):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select private from datasets where id = %(ds_id)s;",{"ds_id":ds_id})
        # retrieve the records from the database
        private = cursor.fetchone()
        cursor.close()
        conn.close()

        private_dataset_field = (private[0])

        if not private_dataset_field:
            private_dataset = 'False'
        else:
            private_dataset = 'True'

        return private_dataset

    @staticmethod
    def get_list_of_new_or_updated_datasets(days_to_subtract):

        d = datetime.datetime.today() - timedelta(days=days_to_subtract)
        date_formatted = d.strftime('%Y-%m-%d')

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        data = {"date":date_formatted}
        cursor.execute("select distinct ref_id from stemformatics.audit_log where date_created >= %(date)s and controller = 'admin' and action = 'setup_new_dataset' and ref_type = 'ds_id' group by ref_id;",data)

        # retrieve the records from the database
        result = cursor.fetchall()

        list_of_ds_ids = []
        for row in result:
            try:
                ds_id = int(row[0])
                list_of_ds_ids.append(ds_id)
            except:
                pass

        cursor.close()
        conn.close()
        return list_of_ds_ids

    @staticmethod
    def check_dataset_is_in_sync_in_redis(ds_id,do_yugene_check):
        message_list = []
        if ds_id == 0 or not isinstance(ds_id,int):
            return message_list
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)
        samples_from_biosamples_table = Stemformatics_Expression.get_samples_via_biosamples(ds_id)
        samples_from_gct = Stemformatics_Expression.get_sample_ids_from_expression_file(ds_id,'gct')

        expression_values_from_gct = Stemformatics_Expression.get_last_line_of_expression_file(ds_id,'gct')
        expression_values_from_gct_list = re.split(r'\t',expression_values_from_gct)
        probe = expression_values_from_gct_list[0]
        expression_values_from_gct = expression_values_from_gct_list[2:]
        expression_values_from_redis = Stemformatics_Expression.get_expression_rows(ds_id,[probe])
        try:
            expression_values_from_redis = expression_values_from_redis[probe]
        except:
            expression_values_from_redis = [] # when no gct_values in redis

        if do_yugene_check:
            cumulative_sample_labels = Stemformatics_Expression.get_cumulative_sample_labels(ds_id)
            samples_from_yugene = Stemformatics_Expression.get_sample_ids_from_expression_file(ds_id,'yugene')

        if do_yugene_check and len(samples_from_yugene) == 1:
            message = samples_from_yugene[0]
            message_list.append(message)

        if len(samples_from_gct) == 1:
            message = samples_from_gct[0]
            message_list.append(message)


        if sample_labels != samples_from_gct:
            message_list.append('Sample labels for gct in redis are not identical to gct file.')

        if do_yugene_check  and cumulative_sample_labels != samples_from_yugene:
            message_list.append('Sample labels for yugene in redis are not identical to yugene file.')

        try:
            sample_labels.sort()
        except:
            message_list.append('Sample labels for gct are not valid in redis. Could not sort.')

        if do_yugene_check:
            try:
                cumulative_sample_labels.sort()
            except:
                message_list.append('Sample labels for yugene are not valid in redis. Could not sort.')

        try:
            samples_from_biosamples_table.sort()
        except:
            message_list.append('Sample labels for biosamples are not valid in redis. Could not sort.')


        if do_yugene_check and sample_labels != cumulative_sample_labels:
            message_list.append('Sample labels for gct and yugene are not consistent with each other in redis.')

        if sample_labels != samples_from_biosamples_table and ds_id != 2000:
            # for datasets with technical replicates sample_labels will always be different form samples_from_biosamples_table
            message_list.append('Sample labels for gct in redis are not consistent with biosamples_metadata')

        # ok everytime you deal with expression values remember there are empty values to be handled
        if len(expression_values_from_redis) != len(expression_values_from_gct) :
            message_list.append("Expression values missing from Redis")
        else:
            # The values are rounded of to 5 decimal places when comparing, I can see the expression values are only stored till 11 decimal places . while in gct files the number of decimal places are more than that
            for value in range(0,len(expression_values_from_gct)-1):
                try:
                    if round(float(expression_values_from_gct[value]),5) != round(float(expression_values_from_redis[value]),5):
                        message_list.append("Expression values does not match with expression values in Redis")
                        break
                except:
                    if expression_values_from_redis[value] != 'None':
                    #this will check if expression value to be 'None' in redis when expression value in gct cannot be converted to float and the value in gct file could be None,'None','NA','na' etc. in gct files
                        message_list.append("Expression value gct "+expression_values_from_redis[value]+ " cannot be compared to redis value "+expression_values_from_redis[value])

        return message_list

    @staticmethod
    def get_all_datasets():
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        data = {}
        cursor.execute("select id from datasets;",data)

        # retrieve the records from the database
        result = cursor.fetchall()

        all_ds_ids = []
        for row in result:
            all_ds_ids.append(row[0])

        cursor.close()
        conn.close()
        return all_ds_ids

    @staticmethod
    def return_pca_data_files(ds_id,pca_type,file_name):
        import csv
        path = config['DatasetPCAFiles']+ ds_id +'/' + pca_type + '/'+file_name+'.tsv'
        # the data is returned as tsv only as gets converted to dict by d3.tsv as it was taking more time to create python dict by iterating over each line of file.
        data_file = open(path,"r")
        data = data_file.readlines()
        return data

    @staticmethod
    def get_pca_types_for_dataset(ds_id):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select ds_value from dataset_metadata where ds_id = %(ds_id)s and ds_name = 'ShowPCALinksOnDatasetSummaryPage';",{"ds_id":ds_id})

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        pca_types = []
        for row in result:
            row = json.loads(row[0])
            pca_types.append(row['name'])

        return pca_types

    @staticmethod
    def delete_dataset_files_from_disk(ds_id):
       #delete dataset files from disk
        try:
            cumulative_file_directory =  config['x_platform_base_dir']
            cumulative_file_path = cumulative_file_directory + 'dataset'+str(ds_id) +'.cumulative.txt'
            if os.path.exists(cumulative_file_path):
                os.remove(cumulative_file_path)

            cls_file_directory = config['DatasetCLSFiles']
            cls_file_path = cls_file_directory + str(ds_id) + '*'
            if os.path.exists(cls_file_path):
                os.remove(cls_file_path)

            probe_file_directory = config['DatasetProbeFiles']
            probe_file_path = probe_file_directory + str(ds_id) + '.probes'
            if os.path.exists(probe_file_path):
                os.remove(probe_file_path)

            gct_file_directory = config['DatasetGCTFiles']
            gct_file_path = gct_file_directory + 'dataset'+str(ds_id) + '.cls'
            if os.path.exists(gct_file_path):
                os.remove(gct_file_path)

            sd_files_directory = config['DatasetStandardDeviationFiles']
            sd_file_path = sd_files_directory + 'probe_expression_avg_replicates_'+str(ds_id) + '.txt'
            if os.path.exists(sd_file_path):
                os.remove(sd_file_path)
            return "Removed CLS FIles, GCT Files, Standard Deviation Files, Probe Files, Cumulative Files"
        except:
            return "Failed to remove Files"

    @staticmethod
    def delete_dataset_redis(ds_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        probe_file = config['DatasetGCTFiles']+ 'dataset' +str(ds_id)+ '.gct'
        probes = []
        with open(probe_file) as f:
            f.next()
            f.next # skip lines
            for line in f:
                columns = line.split() # split line into columns
                if len(columns) == 1:
                    probes.append(column[0])   # column 1
        cumulative_value_keys = []
        gct_value_keys = []
        for probe in probes:
            cumulative_value_keys.append('cumulative_values'+delimiter+str(ds_id)+delimiter+probe)
            gct_value_keys.append('gct_values'+delimiter+str(ds_id)+delimiter+probe)
        gct_label_keys = 'gct_labels'+delimiter +str(ds_id)
        cumulative_label_keys = 'cumulative_labels'+delimiter+ str(ds_id)
        all_keys = []
        all_keys.append(cumulative_label_keys)
        all_keys.append(gct_label_keys)
        all_keys.extend(cumulative_value_keys)
        all_keys.extend(gct_value_keys)

        try:
            for key in all_keys:
                r_server.delete(key)
            return "Redis deleted Successfully"
        except:
            return "Error in deleting Redis"

    @staticmethod
    def delete_dataset_from_database(ds_id):
        try:
            return_str = ''
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("delete from biosamples_metadata where ds_id = %(ds_id)s;",{"ds_id":ds_id})
            return_str = return_str + "Deleted data from biosamples_metadata"

            cursor.execute("delete from biosamples where ds_id=%(ds_id)s; ",{"ds_id":ds_id})
            return_str = return_str + "Deleted data from biosamples"

            cursor.execute("delete from dataset_metadata where ds_id= %(ds_id)s; ",{"ds_id":ds_id})
            return_str = return_str + "Deleted data from dataset_metadata"

            cursor.execute("delete from stemformatics.override_private_datasets where ds_id=%(ds_id)s; ",{"ds_id":ds_id})
            return_str = return_str + "Deleted data from override_private_datasets"

            cursor.execute("delete from stemformatics.stats_datasetsummary where ds_id= %(ds_id)s;",{"ds_id":ds_id})
            return_str = return_str + "Deleted data from stats_datasetsummary"

            cursor.execute("delete from datasets where id= %(ds_id)s;",{"ds_id":ds_id})
            cursor.close()
            conn.commit()
            conn.close()
            return return_str
        except:
            return "Failed to remove entries from database"

    @staticmethod
    def get_list_of_deleted_datasets():
        days_to_subtract = 1
        d = datetime.datetime.today() - timedelta(days=days_to_subtract)
        date_formatted = d.strftime('%Y-%m-%d')
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select ref_id from stemformatics.audit_log where controller = 'admin' and action ='delete_dataset' and date_created >= %(date)s;",{"date":date_formatted})
        # retrieve the records from the database
        result_ds_list = cursor.fetchall()
        cursor.close()
        conn.close()
        delete_dataset = []
        for ds_id in result_ds_list:
            delete_dataset.extend(ds_id)
        return delete_dataset
