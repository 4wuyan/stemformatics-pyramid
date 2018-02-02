import string, json, redis
import psycopg2
import psycopg2.extras
from sqlalchemy import or_, and_, desc
from datetime import datetime, timedelta

# for list_authorised_users
import hmac
import S4M_pyramid.lib.helpers as h

import psycopg2, _pickle as cPickle
import psycopg2.extras
from S4M_pyramid.model import s4m_psycopg2
from S4M_pyramid.lib.deprecated_pylons_globals import config,url
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import redirect
from S4M_pyramid.model.stemformatics import Stemformatics_Job

from bioblend import galaxy
from bioblend.galaxy.tools.inputs import inputs, dataset


class Stemformatics_Galaxy(object):
    """\
    Stemformatics_Galaxy Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for galaxy data

    This model will have function to make connection to galaxy and run galaxy tools and perform  other processing jobs on galaxy server

    """

    def __init__ (self):
        pass

    @staticmethod
    def connect_to_galaxy():
        galaxy_server_url = config['galaxy_server_url']
        galaxy_server_api_key= config['galaxy_server_api_key']
        galaxyInstance = galaxy.GalaxyInstance(url=galaxy_server_url, key=galaxy_server_api_key)
        return galaxyInstance

    @staticmethod
    def run_HC_tool(galaxyInstance,job_id,file_path,uid,column_distance_measure,row_distance_measure,colour_by,chip_type):
        historyClient = galaxy.histories.HistoryClient(galaxyInstance)
        toolClient = galaxy.tools.ToolClient(galaxyInstance)
        datasetClient = galaxy.datasets.DatasetClient(galaxyInstance)

        if colour_by == 'row':
            distance = 'z-score'
        else:
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select y_axis_label from assay_platforms where chip_type = "+str(chip_type)+";"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            distance = result[0][0]

        import socket
        host_name = socket.gethostname()
        try:
            history = historyClient.create_history(str(job_id) + '_HC_'+host_name)
            dataset_id = toolClient.upload_file(path=file_path,history_id=history['id'])
            # this set input data for galaxy tool based on name for that field used in xml
            tool_inputs = inputs().set('infile',dataset(dataset_id['outputs'][0]["id"])).set('value_description',distance).set('clustering_distance_rows',row_distance_measure).set('clustering_distance_columns',column_distance_measure).set('colour_scale',colour_by)
            result = toolClient.run_tool(history_id= history['id'], tool_id='hierarchical_cluster', tool_inputs= tool_inputs)
            return history['id']
        except:
            # now update job with status 2 this will also send email
            status = '2'
            reference_id = 'None'
            reference_type = "Galaxy HC"
            Stemformatics_Job.update_job_status(db,job_id,status, reference_id, reference_type)

            # redirect to 404 as something went wrong and job is not submiteed to galaxy
            redirect(url(controller='contents', action='index'), code=404)

    @staticmethod
    def run_GN_tool(galaxyInstance,job_id,file_path,uid,row,analysis):
        historyClient = galaxy.histories.HistoryClient(galaxyInstance)
        toolClient = galaxy.tools.ToolClient(galaxyInstance)
        datasetClient = galaxy.datasets.DatasetClient(galaxyInstance)

        import socket
        host_name = socket.gethostname()

        if analysis == 2:
            analysis_name = '_GN_'
        else:
            analysis_name = '_UDEP_'

        try:
            history = historyClient.create_history(str(job_id) + analysis_name +host_name)
            dataset_id = toolClient.upload_file(path=file_path,history_id=history['id'])
            # this set input data for galaxy tool based on name for that field used in xml
            tool_inputs = inputs().set('infile', dataset(dataset_id['outputs'][0]["id"])).set('rowId',row)
            result = toolClient.run_tool(history_id= history['id'], tool_id='gene_neighbourhood', tool_inputs= tool_inputs)
            return history['id']
        except:
            # now update job with status 2 this will also send email
            status = '2'
            reference_id = 'None'
            reference_type = "Galaxy GN/UDEP"
            Stemformatics_Job.update_job_status(db,job_id,status, reference_id, reference_type)

            # redirect to 404 as something went wrong and job is not submiteed to galaxy
            redirect(url(controller='contents', action='index'), code=404)


    @staticmethod
    def get_output_for_job(galaxyInstance, path, job_id, galaxy_history_id,analysis_name):
        historyClient = galaxy.histories.HistoryClient(galaxyInstance)
        datasetClient = galaxy.datasets.DatasetClient(galaxyInstance)
        dataset = historyClient.show_matching_datasets(history_id=galaxy_history_id)
        if analysis_name == "HC" :
            # dataset[1]['dataset_id'] is hardcoded as the second output file is img
            output_dataset_file1 = datasetClient.download_dataset(dataset_id = dataset[1]['dataset_id'],wait_for_completion=True, maxwait= 12000,file_path= path+ '/hc.png',use_default_filename=False)
            output_dataset_file2 = datasetClient.download_dataset(dataset_id = dataset[2]['dataset_id'],wait_for_completion=True, maxwait= 12000,file_path= path+ '/na_rows.txt',use_default_filename=False)
        elif analysis_name == "GN" or analysis_name == "UDEP":
            # url to show output files for history - /api/histories/history_id/contents
            output_dataset_file1 = datasetClient.download_dataset(dataset_id = dataset[1]['dataset_id'],wait_for_completion=True, maxwait= 12000,file_path= path+ '/job.txt',use_default_filename=False)

    @staticmethod # test_method to check if galaxy jobs can be run successfully
    def run_hc_input_tool(galaxyInstance,job_id,file_path,ds_id,user_id):
        historyClient = galaxy.histories.HistoryClient(galaxyInstance)
        toolClient = galaxy.tools.ToolClient(galaxyInstance)
        datasetClient = galaxy.datasets.DatasetClient(galaxyInstance)
        history = historyClient.create_history(str(job_id) + '_HCinput')

        dataset_id = toolClient.upload_file(path=file_path,history_id=history['id'])
        tool_inputs = inputs().set('raw_gct', dataset(dataset_id['outputs'][0]["id"])).set('dataset_id', ds_id).set('user_id', user_id).set('probe_list', 'ILMN_2174394, ILMN_2174395').set('gene_to_probe_mapping','ILMN_2174394, ILMN_2174395').set('cluster_type','pearson_row').set('chip_id_list','ILMN_2174394, ILMN_2174395')
        result = toolClient.run_tool(history_id= history['id'], tool_id='hc_inputs', tool_inputs= tool_inputs)
        return history['id']

    @staticmethod
    def return_job_status(galaxyInstance, job_list,server_name):
        historyClient = galaxy.histories.HistoryClient(galaxyInstance)
        status_object = {}
        try:
            for job in job_list:
                analysis_number = job_list[job]
                if analysis_number == 0:
                    analysis_name = "HC"
                elif analysis_number == 2:
                    analysis_name = "GN"
                elif analysis_number == 7:
                    analysis_name = "UDEP"
                status_object[str(job)] = {}
                history = historyClient.get_histories(name = str(job) + '_'+analysis_name+'_'+str(server_name))
                galaxy_status = historyClient.get_status(history[0]['id'])
                status_object[str(job)]['state'] = galaxy_status['state']
                status_object[str(job)]['galaxy_job_id'] = history[0]['id']
                status_object[str(job)]['analysis_name'] = analysis_name
        except:
            print("=====Please Check if any Galaxy processed Job is sitting with status 0 and is not found in Galaxy====")
            pass
        return status_object

    @staticmethod
    def delete_bulk_jobs(galaxyInstance, job_list, server_name):
        historyClient = galaxy.histories.HistoryClient(galaxyInstance)
        for job in job_list:
            try:
                # get history_id for each job
                history = historyClient.get_histories(name = str(job) + '_HC_'+str(server_name))
                galaxy_history_id = history[0]['id']
                history_dict = historyClient.show_history(history_id= galaxy_history_id)
                for output_files in history_dict['state_ids']['ok']:
                    historyClient.delete_dataset(history_id=galaxy_history_id, dataset_id=output_files)
            except:
                pass


    @staticmethod
    def update_job_status(db,status,galaxyInstance):
        for job_id in status:
            analysis_name = status[job_id]['analysis_name']
            reference_type = 'Galaxy '+ analysis_name
            if status[job_id]['state'] == 'ok':
                # first download image for hc or output for analysis as it might take while for long files
                StemformaticsQueue = config['StemformaticsQueue']
                path = StemformaticsQueue +str(job_id) + "/"
                Stemformatics_Galaxy.get_output_for_job(galaxyInstance, path, job_id,status[job_id]['galaxy_job_id'],analysis_name)
                # update job after downloading files
                Stemformatics_Job.update_job_status(db,job_id,'1',status[job_id]['galaxy_job_id'],reference_type)
            else:
                if status[job_id]['state'] == 'queued' or status[job_id]['state'] == 'running' :
                    return json.dumps(status)
                else:
                    Stemformatics_Job.update_job_status(db,job_id,'2',status[job_id]['galaxy_job_id'],reference_type)
