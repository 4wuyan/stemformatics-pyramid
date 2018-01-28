import re,string,json,numpy,os,redis,logging
import subprocess
log = logging.getLogger(__name__)
import sqlalchemy as SA
from sqlalchemy import or_, and_, desc
from datetime import datetime, timedelta
from S4M_pyramid.model.stemformatics import *
import psycopg2,psycopg2.extras,_pickle as cPickle

# Task #500 - wouldn't work otherwise
from S4M_pyramid.model.stemformatics.stemformatics_probe import *

# Task#465 x PLATFORM
#CRITICAL-6
from S4M_pyramid.model.stemformatics.stemformatics_gene import Stemformatics_Gene # wouldn't work otherwise??
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset # wouldn't work otherwise??
from S4M_pyramid.lib.deprecated_pylons_globals import app_globals as g, config



__all__ = ['Stemformatics_Expression']

import formencode.validators as fe

SUBSCRIBER_NAME = fe.Regex("[\w ]*", not_empty=False, if_empty="Anonymous User")
SUBSCRIBER_STATE = fe.Regex("[\w ]*", not_empty=False, if_empty="PENDING")
DESCRIPTIVE_TEXT = fe.Regex("[\w ]*", not_empty=False, if_empty="")
POS_INT = fe.Int(min=1, not_empty=True)
NUMBER = fe.Number(not_empty=True)
IDENTIFIER = fe.PlainText(not_empty=True)
URL = fe.URL(not_empty=True)
class tempData(object):
    pass

def is_multiple(num,divisor):
    """Return whether the number num is even."""
    return num % divisor == 0

class Stemformatics_Expression(object):
    """\
    Stemformatics_Expression Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for expression result and mini graphs in gene search

    Please note for most of these functions you will have to pass in the db object

    All functions have a try that will return None if errors are found

    """

    def __init__ (self):
        pass



    @staticmethod
    def get_all_samples_from_dataset(db,ds_id): #CRITICAL-2
        db.schema = 'public'
        bm = db.biosamples_metadata
        metaDataValues = bm.filter(and_(bm.ds_id==ds_id,bm.md_name=='Replicate Group ID')).all()

        sample_list = [  ]
        for item in metaDataValues:
            new_dict = {}
            for this_item in item.__dict__:
                if '_sa_instance_state' not in this_item:
                    new_dict[this_item] = item.__dict__[this_item]

            sample_list.append(new_dict)




        return sample_list



    def get_mapping_choose_to_view_by_x_platform(self):
        mapping_dict = {2:"View by Dataset",4:"View by Cell Type",5:"View by Tissue",7:"View by Sample Type"}
        return mapping_dict



    """
    This method is to
    - clean up the cumulative value (it can be 0)
    - sample the data based on the value of the YuGene data

    split it up into two lists
    - one containing the sampled data
    - one containing the full data

    store both these lists in Redis
    - the sampled data is for other users to be able to re-use this more quickly and
    - the full data is for filtering and being able to provide breakdowns of the data quickly
    """
    @staticmethod
    def _sampling_of_yugene_data(sort_values):
        full_data = []
        sample_data = []
        graph_values = {}
        # sampling to limit the total values to 2000 or less
        if len(sort_values) > 1000:
            divisor = int(len(sort_values)/1000)
        else:
            divisor = 1

        count_split = 0
        for row in sort_values:

            cumulative_value = row[0]

            # YuGene cannot be over 1. If that is the case,
            # this is bad and this value should be ditched.
            if cumulative_value > 1:
                continue

            if cumulative_value < 0:
                cumulative_value = 0


            temp_list = [cumulative_value] + row[1:]
            full_data.append(temp_list)

            count_split = count_split + 1
            if not is_multiple(count_split,divisor):
                continue


            # this is the minimum data we need to draw an outline of the graph
            sample_data.append(temp_list)


        graph_values['full_data'] = full_data
        graph_values['sample_data'] = sample_data
        return graph_values



    """
    Merging filtered and sample data to make it easy to display
    """
    @staticmethod
    def calculate_yugene_data_for_display(sample_values,filtered_result,merge=False):
        if merge == True:
            temp_data = sample_values + filtered_result
        else:
            temp_data = sample_values

        final_data = []

        temp_data.sort(reverse=True)
        x_position = 0
        for row in temp_data:
            if row not in final_data:
                x_position += 1
                row = row + [x_position]
                final_data.append(row)
        return final_data

    """
    This converts the sample_values into a TSV or CSV format.
    It is based on the line in _sampling_of_yugene_data:
        temp_list = [cumulative_value,probe_id,ds_id,chip_type,x_position]

    """
    @staticmethod
    def convert_yugene_data_to_tsv_csv(sample_values,format_type):
        delimiter = None
        list_of_headers = ['yugene_value','probe_id','sample_id','ds_id','chip_type','x_position']
        if format_type == 'tsv':
            delimiter = "\t"

        if format_type == 'csv':
            delimiter = ","

        if delimiter == None:
            return ""


        text = delimiter.join(list_of_headers)+"\n"
        for row in sample_values:
            row = map(str, row)
            text += delimiter.join(row)+"\n"
        return text

    """
    This converts the breakdown data into TSV or CSV

    """
    @staticmethod
    def convert_yugene_breakdown_data_to_tsv_csv(values,format_type):
        delimiter = None
        list_of_headers = ['type','name','number','hover','full_count','coverage']
        if format_type == 'tsv':
            delimiter = "\t"

        if format_type == 'csv':
            delimiter = ","

        if delimiter == None:
            return ""

        text = delimiter.join(list_of_headers)+"\n"
        for breakdown_type in values:
            for name in values[breakdown_type]:
                number = values[breakdown_type][name]['value']
                hover = values[breakdown_type][name]['hover']
                full_count = values[breakdown_type][name]['full_count']
                coverage = int(values[breakdown_type][name]['coverage'])
                row = [breakdown_type,name,number,hover,full_count,coverage]
                row = map(str, row)
                text += delimiter.join(row)+"\n"
        return text




    """
    This will set the redis key for the uid and the gene
    (as different users may have different access to datasets)

    eg. key would be 3|ENSMUSG00000057666|sample_data

    it can then be saved later on
    have to store it as json

    Both full_data and sample_data will be saved.
    full_data is for using for filtering based on the values
    sample_data is for showing the general line graph
    """
    @staticmethod
    def set_yugene_graph_values(uid,ensembl_id,db_id,graph_values):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        expiry_time = config['expiry_time']

        label_name = 'full_data'+delimiter+str(uid)+delimiter+ensembl_id+delimiter+str(db_id)
        data = Stemformatics_Expression.store_yugene_graph_values(graph_values['full_data'])
        result = r_server.set(label_name,data)
        if result == True:
            # expire previous key if it worked
            result = r_server.expire(label_name,expiry_time)

            label_name = 'sample_data'+delimiter+str(uid)+delimiter+ensembl_id+delimiter+str(db_id)
            data = Stemformatics_Expression.store_yugene_graph_values(graph_values['sample_data'])
            result = r_server.set(label_name,data)
            if result == True:
                # expire previous key if it worked
                r_server.expire(label_name,expiry_time)

        return result

    """
    Separate out the final data format from the method
    """
    @staticmethod
    def store_yugene_graph_values(data):
        store_data = cPickle.dumps(data)
        return store_data

    """
    This will get the redis key for the uid and the gene
    (as different users may have different access to datasets)

    eg. key would be 3|ENSMUSG00000057666|full_data

    full_data is for using for filtering based on the values
    have to store it as json

    returns NONE if not available
    """
    @staticmethod
    def get_yugene_full_data_graph_values(uid,ensembl_id,db_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        label_name = 'full_data'+delimiter+str(uid)+delimiter+ensembl_id+delimiter+str(db_id)
        result = r_server.get(label_name)
        if result is not None:
            result = Stemformatics_Expression.restore_yugene_graph_values(result)
        return result

    """
    Separate out the final data format from the method
    """
    @staticmethod
    def restore_yugene_graph_values(data):
        restore_data = cPickle.loads(data)
        return restore_data


    """
    This will get the redis key for the uid and the gene
    (as different users may have different access to datasets)

    eg. key would be 3|ENSMUSG00000057666|sample_data

    sample_data is for using for drawing the approximate graph
    have to store it as json
    returns NONE if not available
    """
    @staticmethod
    def get_yugene_sample_data_graph_values(uid,ensembl_id,db_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        label_name = 'sample_data'+delimiter+str(uid)+delimiter+ensembl_id+delimiter+str(db_id)
        result = r_server.get(label_name)
        if result is not None:
            result = Stemformatics_Expression.restore_yugene_graph_values(result)
        return result




    """
    Main function to get the expression data back for Yugene
    x_platform is the old name for YuGene

    Will also save this into redis for later use and expire within 3 hours.
    """
    @staticmethod
    def return_x_platform_matricks_data(db_id,datasets_dict,ensemblID,all_sample_metadata):

        #metadata_list = Stemformatics_Expression.get_all_metadata_list_for_x_platform()

        result = Stemformatics_Gene.get_probe_mappings_for_datasets(db_id,datasets_dict,ensemblID)

        ds_id_mapping_id_dict = result['ds_id_mapping_id_dict']
        mapping_id_probe_list = result['mapping_id_probe_list']

        sort_values = []
        list_view_by_value = []

        for ds_id in datasets_dict:
            chip_type = datasets_dict[ds_id]['chip_type']
            handle = datasets_dict[ds_id]['handle']

            try:
                mapping_id = ds_id_mapping_id_dict[ds_id]
                probe_list = mapping_id_probe_list[mapping_id]
            except:
                probe_list = []

            if probe_list == []:
                continue

            cumulative_rows = Stemformatics_Expression.get_cumulative_rows(ds_id,probe_list)
            sample_labels = Stemformatics_Expression.get_cumulative_sample_labels(ds_id)
            sort_values =  Stemformatics_Expression._process_yugene_rows(cumulative_rows,sample_labels,ds_id,chip_type,sort_values)

        graph_values = Stemformatics_Expression._sampling_of_yugene_data(sort_values)
        return graph_values


    """
    This gets the absolute minimum we need to draw a line and then find out the metadata we need later on.
    it returns a list of lists so that we can sort on the value easily

    cumulative_rows is a list of values for all the probes for a dataset
    cumulative_sample_labels is a list of all the samples in order
    """
    @staticmethod
    def _process_yugene_rows(cumulative_rows,sample_labels,ds_id,chip_type,sort_values):
        for row in cumulative_rows:
            sample_count = 0
            for expression_value in cumulative_rows[row]:
                probe_id = row
                if expression_value != '' and expression_value != 'None':
                    expression_value = float(expression_value)
                else:
                    expression_value = -999999999
                chip_id  = sample_labels[sample_count]
                sample_count += 1
                value = expression_value

                row_values_list = [value,probe_id,chip_id,ds_id,chip_type]


                # store all the row values including the metadata in sort_values
                sort_values.append(row_values_list)

        return sort_values




    @staticmethod
    def return_stepped_colours(list_of_start_end_colours,number_of_steps):
        if list_of_start_end_colours is None:
            list_of_start_end_colours = [['#FFFFFF','#000000']]
        #add in extra step to stop it from going so close to black
        number_of_steps = number_of_steps +1
        for colour_range in list_of_start_end_colours:
            start_colour = colour_range[0]
            end_colour = colour_range[1]

            colour = []

            # split the colours into characters
            colour.append([int(start_colour[1:3],16),int(end_colour[1:3],16)])
            colour.append([int(start_colour[3:5],16),int(end_colour[3:5],16)])
            colour.append([int(start_colour[5:7],16),int(end_colour[5:7],16)])
            step = {}
            for item in colour:
                step_value = (item[1] - item[0]) / number_of_steps
                for i in range(0,number_of_steps):
                    if i not in step:
                        step[i] = '#'
                    step[i] = step[i] + '%02x' % round(item[0] + step_value * i)

            step[number_of_steps] = end_colour

        return step

    @staticmethod
    def get_all_sample_metadata():
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from biosamples_metadata;")
        # retrieve the records from the database
        result_ds = cursor.fetchall()
        cursor.close()
        conn.close()
        return result_ds



    @staticmethod
    def setup_all_sample_metadata(): #CRITICAL-2
        result = Stemformatics_Expression.get_all_sample_metadata()
        all_sample_metadata = {}
        for row in result:
            if row['chip_type'] not in all_sample_metadata:
                all_sample_metadata[row['chip_type']] = {}
            if row['chip_id'] not in all_sample_metadata[row['chip_type']]:
                all_sample_metadata[row['chip_type']][row['chip_id']] = {}

            if row['ds_id'] not in all_sample_metadata[row['chip_type']][row['chip_id']]:
                all_sample_metadata[row['chip_type']][row['chip_id']][row['ds_id']] = {}

            all_sample_metadata[row['chip_type']][row['chip_id']][row['ds_id']][row['md_name']] = row['md_value']

        return all_sample_metadata
        # now update the g.all_sample_metadata


    @staticmethod
    def get_dataset_sample_metadata(db,ds_id): #CRITICAL-2
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from biosamples_metadata where ds_id = %(ds_id)s;",{"ds_id":ds_id})
        # retrieve the records from the database
        result_ds = cursor.fetchall()
        cursor.close()
        conn.close()
        return result_ds



    @staticmethod
    def setup_dataset_sample_metadata(db,all_sample_metadata,ds_id): #CRITICAL-2
        result = Stemformatics_Expression.get_dataset_sample_metadata(db,ds_id)
        identifiers_used = []
        for row in result:

            identifier = str(row['chip_type']) + "|" + str(row['chip_id']) + "|" + str(ds_id)

            if row['chip_type'] not in all_sample_metadata:
                all_sample_metadata[row['chip_type']] = {}
            if row['chip_id'] not in all_sample_metadata[row['chip_type']]:
                all_sample_metadata[row['chip_type']][row['chip_id']] = {}


            if identifier not in identifiers_used:
                all_sample_metadata[row['chip_type']][row['chip_id']][row['ds_id']] = {}
                identifiers_used.append(identifier)

            all_sample_metadata[row['chip_type']][row['chip_id']][row['ds_id']][row['md_name']] = row['md_value']

        file_name =  config['all_sample_metadata_cpickle_file']

        f = open(file_name, 'wb')
        f.write(json.dumps(all_sample_metadata))
        f.close()
        return all_sample_metadata
        # now update the g.all_sample_metadata

    @staticmethod
    def get_cumulative_sample_labels(ds_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        label_name = 'cumulative_labels'+delimiter+str(ds_id)
        try:
            label_names = r_server.get(label_name).split(delimiter)
            return label_names
        except:
            return None


    @staticmethod
    def get_sample_labels(ds_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        label_name = 'gct_labels'+delimiter+str(ds_id)
        try:
            label_names = r_server.get(label_name).decode("utf-8").split(delimiter)
            return label_names
        except:
            return None

    @staticmethod
    def get_expression_rows(ds_id,probe_list):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        result = {}
        for probe in probe_list:
            temp_row = r_server.get('gct_values'+delimiter+str(ds_id)+delimiter+probe).decode("utf-8")
            if temp_row is not None:
                row = temp_row.split(delimiter)
                result[probe] = row
        return result


    @staticmethod
    def get_cumulative_rows(ds_id,probe_list):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        result = {}
        for probe in probe_list:
            temp_row = r_server.get('cumulative_values'+delimiter+str(ds_id)+delimiter+probe)
            if temp_row is not None:
                row = temp_row.split(delimiter)
                result[probe] = row
        return result

    @staticmethod
    def get_standard_deviation(ds_id,chip_id,probe_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        row_name = str('standard_deviation'+delimiter+str(ds_id)+delimiter+chip_id+delimiter+probe_id)
        sd_value = r_server.get(row_name)
        #~ raise Error
        if sd_value is None:
            sd_value = 0

        return float(sd_value)


    @staticmethod
    def validate_replicate_group_id(db,tests_to_perform): #CRITICAL-2
        output = ''

        db.schema = 'public'
        bs_md = db.biosamples_metadata
        ds = db.datasets

        chip_id_table = {}

        result_bs_md = bs_md.filter(bs_md.md_name == 'Replicate Group ID').all()
        for item in result_bs_md:
            ds_id = int(item.ds_id)
            chip_id = item.chip_id

            if ds_id not in chip_id_table:
                chip_id_table[ds_id] = {}

            if chip_id not in chip_id_table[ds_id]:
                chip_id_table[ds_id][chip_id] = 'b'


        result_ds = ds.all()
        problem_datasets = 0
        list_of_problem_datasets = ''
        problem_datasets_list = []
        for dataset in result_ds:
            ds_id = dataset.id

            # get the gct

            gct_labels = Stemformatics_Expression.get_sample_labels(ds_id)
            # Name and description two first labels

            if gct_labels is not None:
                for chip_id in gct_labels:
                    if chip_id != 'Description' and chip_id != 'NAME':
                        if ds_id not in chip_id_table:
                            chip_id_table[ds_id] = {}

                        if chip_id not in chip_id_table[ds_id]:
                            chip_id_table[ds_id][chip_id] = 'g'
                        else:
                            chip_id_table[ds_id][chip_id] = chip_id_table[ds_id][chip_id] + 'g'
            else:
                if ds_id not in problem_datasets_list:
                    list_of_problem_datasets = str(ds_id)+","+list_of_problem_datasets
                    problem_datasets += 1
                    problem_datasets_list.append(ds_id)


            if tests_to_perform == 'bgc':
                # get the cumulative

                cumulative_labels = Stemformatics_Expression.get_cumulative_sample_labels(ds_id)

                # Name and description two first labels
                if cumulative_labels is not None:
                    for chip_id in cumulative_labels:
                        if chip_id != 'Description' and chip_id != 'NAME' and chip_id != 'Probe':
                            if ds_id not in chip_id_table:
                                chip_id_table[ds_id] = {}

                            if chip_id not in chip_id_table[ds_id]:
                                chip_id_table[ds_id][chip_id] = 'c'
                            else:
                                chip_id_table[ds_id][chip_id] = chip_id_table[ds_id][chip_id] + 'c'
                else:
                    if ds_id not in problem_datasets_list:
                        list_of_problem_datasets = str(ds_id)+","+list_of_problem_datasets
                        problem_datasets += 1
                        problem_datasets_list.append(ds_id)

        count_datasets = 0

        for ds_id in chip_id_table:
            issue = False
            count_datasets += 1
            for chip_id in chip_id_table[ds_id]:
                value = chip_id_table[ds_id][chip_id]
                if value != tests_to_perform:
                    output = output  + str(ds_id) + "|" + chip_id.decode('utf-8') + "|" + value + "\n "
                    issue = True
            if issue:
                if ds_id not in problem_datasets_list:
                    list_of_problem_datasets = str(ds_id)+","+list_of_problem_datasets
                    problem_datasets += 1
                    problem_datasets_list.append(ds_id)

        output = output + str(problem_datasets) + "/" + str(count_datasets) + "\n"
        output = output + list_of_problem_datasets + "\n"
        return output




    @staticmethod
    def return_sample_type_display_group_colours(sampleTypeDisplayGroups):
        if sampleTypeDisplayGroups is None:
            return []
        # newColourArray = ['#CC0066','#000099','#006600','#666600','#0AD3EF','#82DC27','#FDD50C','#FD0CF4','#783255','#11A81A','#E99F19','#19E9AC','#4119E9','#B219E9','#E05B50','#EEEA48', '#A72E71', '#AB5090', '#ABCD34', '#AC4401', '#AD1049', '#B2A139', '#B42DA1', '#B4E0B8', '#B5D2BC', '#B937B7', '#B9D0E6', '#BBF90E', '#BE5415', '#C43C25', '#C6C9BE', '#CAB861', '#CDAAB9', '#D0490F', '#D09F85', '#D34AE9', '#D794D7', '#DC93C1', '#DE3C93', '#E2F8E1', '#E3EE73', '#E52700', '#E5B9DE', '#EC3198', '#EF4DDD', '#EFDE92', '#F04874', '#F0A4E1', '#F31AEC', '#F45CC4', '#F4C928', '#F8FC9E', '#F9DCE9', '#FE466C']

        sample_type_colours = config['sample_type_colours']
        newColourArray = json.loads(sample_type_colours)
        data = json.loads(sampleTypeDisplayGroups)
        group_members = {}
        return_stepped_colours = {}
        for sample_type in data:
            group = data[sample_type]
            if group not in group_members:
                group_members[group] = 0
            group_members[group] = group_members[group] + 1
        for group in group_members:
            start_colour = newColourArray[group]
            end_colour = '#000000'
            list_of_start_end_colours = [[start_colour,end_colour]]
            number_of_steps = group_members[group]
            return_stepped_colours[group] = Stemformatics_Expression.return_stepped_colours(list_of_start_end_colours,number_of_steps)
        return return_stepped_colours


    @staticmethod
    def return_binning_range(start,end,step_value,value):
        top = start + step_value
        bottom = start
        step_count = 0
        while value > top:
            top = top + step_value
            bottom = bottom + step_value
            step_count += 1
        step_string = str(bottom)+' - '+ str(top)
        return [step_string,step_count]

    @staticmethod
    def return_gct_file_sample_headers_as_replicate_group_id(db,ds_id,chip_ids,remove_chip_ids,gct_header="NAME\tDescription"):
        mapping = Stemformatics_Dataset.get_chip_id_to_replicate_group_id_mappings(db,ds_id)
        if chip_ids is not None:
            for chip_id in chip_ids:
                if chip_id not in remove_chip_ids:
                    replicate_group_id = mapping[chip_id]
                    gct_header +="\t"+replicate_group_id
            gct_header +="\n"
        else:
            gct_header +="\tIssue with finding chip_ids. Please contact the "+  c.site_name+" team.\n"
        return gct_header


    @staticmethod
    def return_sample_details(db,ds_id):
        chip_ids = Stemformatics_Expression.get_sample_labels(ds_id)
        mapping = Stemformatics_Dataset.get_chip_id_to_replicate_group_id_mappings(db,ds_id)
        sample_details = {}
        for chip_id in chip_ids:
            replicate_group_id = mapping[chip_id]
            sample_details[chip_id] = {'replicate_group_id':replicate_group_id}
        return sample_details


    """
    Returns a True or False

    It saves a list of json values into redis. It saves the full_data and the sample_data.
    First it checks if the value is there (sample_data) and if it's there it returns True.
    Secondly, if it's not there, it will build it from scratch and then store it in Redis.

    db_id is integer
    uid is integer
    ensemblID has to be unique
    all_sample_metadata is from the global
    role is admin,annotator,normal or None

    """
    @staticmethod
    def return_yugene_graph_data(db_id,uid,ensembl_id,all_sample_metadata,role):

        # first check that this doesn't already exist in redis
        sample_values = Stemformatics_Expression.get_yugene_sample_data_graph_values(uid,ensembl_id,db_id)
        if sample_values is not None and sample_values != '[]':
            return True

        datasets_dict = Stemformatics_Dataset.get_all_x_platform_datasets_for_user(uid,db_id,role)

        # graph_values has two keys, full_data and sample_data returned
        graph_values = Stemformatics_Expression.return_x_platform_matricks_data(db_id,datasets_dict,ensembl_id,all_sample_metadata)

        # set both full_data and sample_data
        result = Stemformatics_Expression.set_yugene_graph_values(uid,ensembl_id,db_id,graph_values)
        return result


    """
    Gets the full data and filters it based on the filters variable.
    Currently only filtering on ds_id and start/end value
    Later will use filter on "search" term

    Returns a cut down list of lists or and error text if stated in max_length_action
    Expects the order of the values in the list to be [value,probe_id,chip_id,ds_id,chip_type]


    filters are the filter types (see below)
    full_data is the full data from redis
    max_length is the max # of items eg. 100 or None for no limit
    max_length_action is the action to take when finding over the length
        options are 'truncate' or 'error'

    eg. filters = {'filter_value_start':0,'filter_value_end':0.1} # start must have an end
    eg. filters = {'ds_ids':[1000,2000]} # multiple dataset ids supported
    eg. filters = {'filter_value_start':0,'filter_value_end':0.1,'ds_ids':[1000]} # search for all three at the same time
    eg. filters = {'search':'human and ipsc'} # not implemented yet

    """
    @staticmethod
    def filter_yugene_graph(filters,db_id,full_data,metadata_list, all_sample_metadata,max_length,uid,ensembl_id, max_length_action='error'):
        filtered_result = full_data

        # no filters means we should return empty
        if filters is None or filters == '{}' or filters =='':
            return []

        if full_data is None:
            return None

        if filters is not None and 'ds_ids' in filters:
            ds_ids = filters['ds_ids']
            if isinstance(ds_ids,list):
                filtered_result= [x for x in filtered_result if x[3] in ds_ids]


        if filters is not None and 'filter_value_start' in filters and 'filter_value_end' in filters:
            try:
                filter_value_start = float(filters['filter_value_start'])
                filter_value_end = float(filters['filter_value_end'])
                if isinstance(filter_value_start, float) and  isinstance(filter_value_end, float):
                    # filtered_result = [x for x in filtered_result if x[0] >= filter_value_start and x[0] <= filter_value_end]
                    data_dicts = Stemformatics_Expression.return_full_data_dict_and_filter_data_dict(filters, full_data, metadata_list, all_sample_metadata)
                    breakdown_dict  = data_dicts[0]
                    full_data_dict = data_dicts[1]
                    # now iterate over breakdown_dict to add full_sample_count for each generic sample type in breakdown_dict
                    for metadata_name in metadata_list:
                        for metadata_value in breakdown_dict[metadata_name]:
                            breakdown_dict[metadata_name][metadata_value]['full_count'] = full_data_dict[metadata_name][metadata_value]['value']
                            breakdown_dict[metadata_name][metadata_value]['coverage'] = (float(breakdown_dict[metadata_name][metadata_value]['value'])/float(full_data_dict[metadata_name][metadata_value]['value'])) * 100
                    result = Stemformatics_Expression.set_breakdown_dict_to_redis(uid,ensembl_id,db_id,breakdown_dict, filter_value_start,filter_value_end)
            except:
                pass


        # option of cutting off the length or returning a text with an error - default is error
        if max_length is not None:
            actual_length = len(filtered_result)
            if actual_length > max_length:
                if max_length_action == 'error':
                    error_text =  "Error as the actual length "+str(actual_length) + " is greater than the cutoff "+ str(max_length)
                    return error_text
                if max_length_action == 'truncate':
                    filtered_result = filtered_result[0:max_length]
        return breakdown_dict

    @staticmethod
    def set_breakdown_dict_to_redis(uid,ensembl_id,db_id,data,filter_value_start,filter_value_end):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        expiry_time = config['yugene_breakdown_dict_expiry_time']

        label_name = 'breakdown_data'+delimiter+str(uid)+delimiter+ensembl_id+delimiter+str(db_id)+delimiter+str(filter_value_start) + delimiter+ str(filter_value_end)
        data = Stemformatics_Expression.store_yugene_graph_values(data)
        result = r_server.set(label_name,data)

        if result == True:
            result = r_server.expire(label_name,expiry_time)
        return result

    @staticmethod
    def get_breakdown_dict_from_redis(uid,ensembl_id,db_id,filter_value_start,filter_value_end):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        label_name = 'breakdown_data'+delimiter+str(uid)+delimiter+ensembl_id+delimiter+str(db_id)+delimiter+str(filter_value_start) + delimiter+ str(filter_value_end)
        result = r_server.get(label_name)
        if result is not None:
            result = Stemformatics_Expression.restore_yugene_graph_values(result)
        return result

    @staticmethod
    def return_yugene_filtered_dataset_breakdown(breakdown_data):
        dataset_breakdown_dict = {}
        dataset_breakdown_dict['dataset_id'] = {}
        dataset_list = []
        for dataset in breakdown_data['datasets']:
            dataset_breakdown_dict['dataset_id'][dataset] = {}
            dataset_breakdown_dict['dataset_id'][dataset]['chip_id_info']= {}
            dataset_breakdown_dict['dataset_id'][dataset]['sample_count'] = len(breakdown_data['datasets'][dataset])
            for chip_id in breakdown_data['datasets'][dataset]:
                dataset_breakdown_dict['dataset_id'][dataset]['chip_id_info'][chip_id] = breakdown_data['datasets'][dataset][chip_id]
            dataset_list.append(dataset)
        # now get handle, title, species
        dataset_data = Stemformatics_Dataset.get_handle_title_and_species(dataset_list)

        for dataset in breakdown_data['datasets']:
            dataset_breakdown_dict['dataset_id'][dataset]['handle'] = dataset_data[dataset]['handle']
            dataset_breakdown_dict['dataset_id'][dataset]['number_of_samples'] = dataset_data[dataset]['number_of_samples']
            dataset_breakdown_dict['dataset_id'][dataset]['species'] = dataset_data[dataset]['Organism']
            dataset_breakdown_dict['dataset_id'][dataset]['Title'] = dataset_data[dataset]['Title']
        return dataset_breakdown_dict

    @staticmethod
    def return_full_data_dict_and_filter_data_dict(filters,full_data,metadata_list,all_sample_metadata):
        breakdown_dict = {}
        full_sample_count_dict = {}
        list_of_errors = []
        list_of_chip_ids_already_used = set()
        list_of_chip_ids_already_used_in_breakdown_dict = set()

        filter_value_start = float(filters['filter_value_start'])
        filter_value_end = float(filters['filter_value_end'])
        for metadata_name in metadata_list:
            breakdown_dict[metadata_name] = {}
            full_sample_count_dict[metadata_name] = {}

        sample_metadata_values_exception = False

        for row in full_data:
            yugene_value = row[0]
            probe = row[1]
            chip_id = row[2]
            ds_id = row[3]
            chip_type = row[4]
            uid = str(chip_id) + str(ds_id) # instead of using unique chip_id, we need to use chip_id + dsid as some chip_ids had different generic sample type value across different datasets
            try:
                sample_metadata_values =  all_sample_metadata[chip_type][chip_id][ds_id]
            except Exception as e:
                sample_metadata_values_exception = True
                list_of_errors.append([ds_id,chip_type,chip_id])
            try:
                # calculates full sample count dict
                if uid not in list_of_chip_ids_already_used:
                    list_of_chip_ids_already_used.add(uid)
                    for metadata_name in metadata_list:
                        metadata_value = sample_metadata_values[metadata_name]
                        if metadata_value not in full_sample_count_dict[metadata_name]:
                            full_sample_count_dict[metadata_name][metadata_value] = {}
                            full_sample_count_dict[metadata_name][metadata_value]['value'] = 1
                        else:
                            full_sample_count_dict[metadata_name][metadata_value]['value'] += 1

                # calculates breakdown dict
                if yugene_value >= filter_value_start and yugene_value <= filter_value_end:
                    if uid not in list_of_chip_ids_already_used_in_breakdown_dict:
                        list_of_chip_ids_already_used_in_breakdown_dict.add(uid)
                        for metadata_name in metadata_list:
                            metadata_value = sample_metadata_values[metadata_name]
                            hover = sample_metadata_values['Generic sample type long']
                            if metadata_value not in breakdown_dict[metadata_name]:
                                breakdown_dict[metadata_name][metadata_value] = {}
                                breakdown_dict[metadata_name][metadata_value]['value'] = 1
                                breakdown_dict[metadata_name][metadata_value]['hover']= hover
                                breakdown_dict[metadata_name][metadata_value]['datasets'] = {}
                                if ds_id not in breakdown_dict[metadata_name][metadata_value]['datasets']:
                                    breakdown_dict[metadata_name][metadata_value]['datasets'][ds_id] = {}
                                    breakdown_dict[metadata_name][metadata_value]['datasets'][ds_id][chip_id] = chip_type
                                else:
                                    breakdown_dict[metadata_name][metadata_value]['datasets'][ds_id][chip_id] = chip_type
                            else:
                                breakdown_dict[metadata_name][metadata_value]['value'] += 1
                                if ds_id not in breakdown_dict[metadata_name][metadata_value]['datasets']:
                                    breakdown_dict[metadata_name][metadata_value]['datasets'][ds_id] = {}
                                    breakdown_dict[metadata_name][metadata_value]['datasets'][ds_id][chip_id] = chip_type
                                else:
                                    breakdown_dict[metadata_name][metadata_value]['datasets'][ds_id][chip_id] = chip_type
            except:
                pass
            # send email with list of exceptions to alert staff
            # this does slow down the values getting returned
        if sample_metadata_values_exception == True:
            from S4M_pyramid.model.stemformatics.stemformatics_notification import Stemformatics_Notification
            import sys, os,socket
            hostname = socket.gethostname()

            error_name = 'YuGene sample_metadata_values'
            subject = error_name
            body = "Failure on metadata search in return_breakdown_of_filtered_results:\n"
            for row in list_of_errors:
                ds_id = row[0]
                chip_type = row[1]
                chip_id = row[2]
                body += "ds_id: "+str(ds_id) + " chip_type:" + str(chip_type) + " chip_id: "+ str(chip_id) + "\n"

            Stemformatics_Notification.send_error_email(subject,body)
        return [breakdown_dict,full_sample_count_dict]

    @staticmethod
    def get_expression_graph_data(ds_id,ref_id,ref_type,db_id):
        # ref_type can be ensemblID,gene_set_id,probeID,miRNA
        # ref_id passed is a list of ref_id's

        if ref_type == "ensemblID":
            data = Stemformatics_Expression.get_expression_data_from_genes(ref_id, ds_id, db_id)
            return data

        if ref_type == "gene_set_id":
            data = Stemformatics_Expression.get_expression_data_from_gene_set(ref_id, ds_id, db_id)
            return data

        if ref_type == "probeID":
            data = Stemformatics_Expression.get_expression_data_from_probes(ref_id,ds_id,db_id)
            return data

        if ref_type == "miRNA":
            feature_id = ref_id[0]
            species = Stemformatics_Dataset.returnSpecies(db_id)
            use_json = False
            feature_mapping_data = Stemformatics_Expression.get_mappings_for_miRNA(feature_id, species, ref_type, use_json, ds_id, db_id)
            probe_list = feature_mapping_data[feature_id]
            # now get the data for all probes
            data =  Stemformatics_Expression.get_expression_data_from_probes(probe_list,ds_id,db_id)
            return data

    @staticmethod
    def get_expression_data_from_genes(ref_id, ds_id, db_id):
        # first get the gene mapping data
        gene_mapping_data = Stemformatics_Gene.get_mapping_for_genes(ref_id,ds_id,db_id)
        probe_list = gene_mapping_data[0]
        # now get the data for all the probes
        data = Stemformatics_Expression.get_expression_data_from_probes(probe_list,ds_id,db_id)
        return data

    @staticmethod
    def get_expression_data_from_gene_set(ref_id, ds_id, db_id):
        gene_set_mapping_data = Stemformatics_Gene.get_mapping_for_gene_set(ref_id,db_id,ds_id)

        # create a gene list from gene set mapping
        gene_list = []
        for gene_set_id in gene_set_mapping_data:
             gene_list.extend(gene_set_mapping_data[gene_set_id])

        # now get the mapping data for all gene
        gene_mapping_data = Stemformatics_Gene.get_mapping_for_genes(gene_list,ds_id,db_id)
        probe_list = gene_mapping_data[0]
        # now get the data for all the probes
        data = Stemformatics_Expression.get_expression_data_from_probes(probe_list,ds_id,db_id)
        return data

    @staticmethod
    def get_mappings_for_miRNA(feature_id, species, ref_type, use_json,ds_id, db_id):
        # first check if mapping is in redis
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        ref_type = 'miRNA'
        feature_mapping = {}
        miRNA_not_in_redis = []

        label_name = "miRNA_mapping_data"+ delimiter + str(ds_id) + delimiter + str(feature_id) + delimiter + str(ref_type) + delimiter + str(db_id)
        result = r_server.get(label_name)
        if result is not None:
            unpickled_data = Stemformatics_Expression.unpickle_expression_data(result)
            return unpickled_data
        else:
            miRNA_not_in_redis.append(feature_id)
            # now get the data from database
            probe_list = []
            result = Stemformatics_Gene.find_feature_search_items(feature_id,species,ref_type,use_json)

            for feature in result:
                aliases_array = feature['aliases'].split(",")
                probe_list = probe_list + aliases_array
                # probe_list.append(feature['feature_id'])

            lower_case_probe_list = []
            for probe in probe_list:
                lower_case_probe_list.append(probe.lower())
                probe_list = list(set(lower_case_probe_list))

            feature_mapping[feature_id] = probe_list

            # now save in the redis
            expiry_time = config['expiry_time']
            label_name = "miRNA_mapping_data"+ delimiter + str(ds_id) + delimiter + str(feature_id) + delimiter + str(ref_type) + delimiter + str(db_id)
            data = Stemformatics_Expression.pickle_expression_data(feature_mapping)
            result = r_server.set(label_name,data)
            if result == True:
                expiry = r_server.expire(label_name,expiry_time)
                # if expiry == False:
                #     return None #returns if data not set properly

            # now return the data
            return feature_mapping

    @staticmethod
    def get_expression_data_from_probes(probe_list,ds_id,db_id):
        # setting db = None as we don't use it when getting chip Type
        db = None
        # check in redis
        unique_probe_list = set(probe_list)
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        expiry_time = config['expiry_time']
        ref_type = 'probeID'
        probes_not_in_redis = []
        probe_data_redis = []
        for probe in unique_probe_list:
            label_name = "probe_graph_data"+ delimiter + str(ds_id) + delimiter + str(probe) + delimiter + str(ref_type) + delimiter + str(db_id)
            result = r_server.get(label_name)
            if result is not None:
                unpickled_data = Stemformatics_Expression.unpickle_expression_data(result)
                probe_data_redis.extend(unpickled_data)
            else:
                probes_not_in_redis.append(probe)

        # now check the probes not found list
        if not probes_not_in_redis:
            return probe_data_redis
        else:
            # get cumulative probe expression rows from redis
            expression_rows = Stemformatics_Expression.get_expression_rows(ds_id,probes_not_in_redis)
            chip_type = Stemformatics_Dataset.getChipType(ds_id)
            sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)

            # now get the multi mapping info for for all probes
            probe_mapping_data = Stemformatics_Probe.get_multi_mapping_for_probes(probes_not_in_redis,db_id,ds_id)
            multi_mapping_data = probe_mapping_data[1]
            multi_mapped_genes = probe_mapping_data[0]

            # now manipulate the data for all probes not found in redis
            probe_data_database =  Stemformatics_Expression.get_expression_graph_data_from_database(ds_id,expression_rows,sample_labels,chip_type,multi_mapping_data,multi_mapped_genes)
            for probe in probes_not_in_redis:
                # now save the manipulated data for each probe
                label_name = "probe_graph_data"+ delimiter + str(ds_id) + delimiter + str(probe) + delimiter + str(ref_type) + delimiter + str(db_id)

                if probe in probe_data_database:
                    data = Stemformatics_Expression.pickle_expression_data(probe_data_database[probe])
                    result = r_server.set(label_name,data)
                    if result == True:
                        result = r_server.expire(label_name,expiry_time)
                    # if result == False:
                    #     return 'data not set properly'
                # combine the data for this probe with other probes data
                    probe_data_redis.extend(probe_data_database[probe])

            return probe_data_redis

    @staticmethod
    def get_expression_graph_data_from_database(ds_id,probe_expression_rows,sample_labels,chip_type,multi_mapping_data,multi_mapped_genes):
        probe_data = {}

        # get the dataset metadata limitSortby info as we need this to decide what all graph data values we need
        ds_md = Stemformatics_Dataset.get_expression_dataset_metadata(ds_id)
        limitSortBy = ds_md["limitSortBy"]
        limitSortBy_values = limitSortBy.split(",")
        for row in probe_expression_rows:
            if row in multi_mapping_data:
                if multi_mapping_data[row] == 1:#replaced 1L with 1
                    multi_mapping_value = "no"
                else:
                    multi_mapping_value = "yes"
            else:
                multi_mapping_value = "no"

            data =[]
            sample_count = 0
            probe_id = row
            ds_id = ds_id
            for expression_value in probe_expression_rows[row]:
                chip_id = sample_labels[sample_count]
                standard_deviation = Stemformatics_Expression.get_standard_deviation(ds_id,chip_id,probe_id)
                sample_count += 1
                metaDataValues = g.all_sample_metadata[chip_type][chip_id][ds_id]
                sample_id = metaDataValues['Replicate Group ID']
                limitSortby_data = {}
                for value in limitSortBy_values:
                    value_with_no_spaces = value.replace(" ","_")
                    if value in metaDataValues:
                        limitSortby_data[value_with_no_spaces] = metaDataValues[value]
                    else:
                        limitSortby_data[value_with_no_spaces] = ""

                try: # this is for line graph
                    day = metaDataValues['Day']
                    line_graph_group = metaDataValues['LineGraphGroup']
                except:
                    day = None
                    line_graph_group = None

                if expression_value != '' and expression_value != 'None':
                    expression_value = float(expression_value)

                data_row = {}
                data_row["ds_id"] = str(ds_id)
                data_row["Probe"] = probe_id
                data_row["chip_Id"] = chip_id
                data_row["Replicate_ID"] = sample_id
                data_row["Expression_Value"] = str(expression_value)
                data_row["Standard_Deviation"] = str(standard_deviation)
                data_row["Day"] = day
                data_row["LineGraphGroup"] = line_graph_group
                data_row["Multi_Mapping"] = multi_mapping_value
                if probe_id in multi_mapped_genes: # expressions/feature_result?graphType=box&feature_type=miRNA&feature_id=MI0000139&db_id=46&datasetID=6128 has no mapping info
                    data_row["Mapped_gene"] = multi_mapped_genes[probe_id]
                else:
                    data_row["Mapped_gene"] = ""
                for value in limitSortby_data:
                    data_row[value] = (limitSortby_data[value])
                # check if sample type has been added in data row - this is for dataset 6370
                if "Sample_Type" not in data_row:
                    data_row["Sample_Type"] = (metaDataValues["Sample Type"])
                try:
                    data_row["Sample_Type_Long"] = (metaDataValues["Sample type long"])

                except: # when no record is present for Sample type long
                    data_row["Sample_Type_Long"] = ""
                data.append(data_row)
            probe_data[row] = data
        return probe_data

    @staticmethod
    def pickle_expression_data(data):
        store_data = cPickle.dumps(data)
        return store_data

    @staticmethod
    def unpickle_expression_data(data):
        restore_data = cPickle.loads(data)
        return restore_data

    @staticmethod
    def change_graph_data_format(graph_data, format_type):
        if format_type == "json":
            json_data = json.dumps(graph_data)
            return json_data

        if format_type == "tsv":
            # create a list from dict
            graph_data_list = []
            for row in graph_data:
                temp_data = []
                for key,value in row.items():
                    temp_data.append(value)
                graph_data_list.append(temp_data)

            delimiter = "\t"
            list_of_headers = graph_data[0].keys()
            text = delimiter.join(list_of_headers)+'\n'
            for row in graph_data_list:
                for item in row:
                    if item == None:
                        item = "NULL"
                    text += item + delimiter
                text +=  '\n'
            return text

        """
        This method should accept user id and dataset id as parameters.
        Based on the user id value, it will check if a colours list has been stored for a particular dataset.
        and if not should return default colours.
        However at present it will be returning default colours, that are being fetched from database.
        """
    @staticmethod
    def get_colours_for_graph(userid, dataset_id):
        # this returns the colours for probes for scatter plot
        unicode_colours = config['graph_colours']
        colours = json.loads(unicode_colours)
        return colours

    """
    pattern for redis keys
    dataset_metadata -> dataset_metadata|ds_id
    dataset_metadata|5030
    gene mapping data -> gene_mapping_data|mapping_id|ensemblID|db_id
    gene_mapping_data|21|ENSG00000170581|ensemblID|56
    probe_graph_data -> probe_graph_data|ds_id|probe_id|probeID|db_id
    probe_graph_data|6071|ENSMUST00000087717|probeID|46
    """

    @staticmethod
    def delete_data_from_redis(matching_pattern,exact_keys=False):
        my_keys = []
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        for label_name in matching_pattern:
            label_name = label_name.encode('utf-8')
            if exact_keys == False:
                # get keys for each matching pattern
                matching_keys_list = r_server.keys(pattern=label_name+"*")
                my_keys.extend(matching_keys_list)
            else:
                my_keys.append(label_name)
        # now del keys
        try:
            for key in my_keys:
                output = r_server.delete(key)
        except:
            output = 'Error in deleting data for ' + str(my_keys)

        return output

    @staticmethod
    def get_feature_mapping_stats(ds_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
        # get the mapping id for ds_id
        result = r_server.get("dataset_mapping_data")
        mapping_id = Stemformatics_Expression.unpickle_expression_data(result)

        try:
            mapping_id_for_ds_id = mapping_id[int(ds_id)]
        except:
            return "Mapping ID not found"

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select count(*) from stemformatics.feature_mappings where mapping_id = %(mapping_id_for_ds_id)s;",{"mapping_id_for_ds_id":mapping_id_for_ds_id})
        # retrieve the records from the database
        count = cursor.fetchall()
        cursor.close()
        conn.close()

        return count[0][0]

    @staticmethod
    def create_gct_file_for_analysis(ds_id,analysis,gct_file_path,chip_type,options,probe):

        datasetGCTFile = config['DatasetGCTFiles']+"dataset"+str(ds_id)+".gct"
        command = "cp "+datasetGCTFile+ " " +gct_file_path
        p = subprocess.call(command,shell=True)

        if analysis == 7:
            expression_values = options['expression_values']
            sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)
            gct_row_text = probe + "\t"+"na"

            for sample in sample_labels:
                chip_id = sample
                metaDataValues = g.all_sample_metadata[chip_type][chip_id][int(ds_id)]
                sample_type = metaDataValues['Sample Type']

                expression_value = float(expression_values[sample_type])
                gct_row_text += "\t" + str(expression_value)

            gct_row_text += "\n"

            with open(gct_file_path,"a") as myfile: myfile.write(gct_row_text)
            command = "PROBES=`sed -n 2p "+gct_file_path+"| cut -f1 `; NEWPROBES=`expr $PROBES + 1`;sed 2s/$PROBES/$NEWPROBES/ -i "+gct_file_path
            p = subprocess.call(command,shell=True)


    @staticmethod
    def get_samples_via_biosamples(ds_id):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        data = {"ds_id":ds_id}
        cursor.execute("select chip_id from biosamples_metadata where ds_id = %(ds_id)s and md_name = 'Replicate Group ID' order by chip_id;",data)

        # retrieve the records from the database
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        samples_from_biosamples_table = []
        for row in result:
            sample_id = row[0]
            samples_from_biosamples_table.append(sample_id)

        return samples_from_biosamples_table

    @staticmethod
    def get_sample_ids_from_expression_file(ds_id,expression_type):
        if expression_type == 'yugene':
            x_platform_base_dir = config['x_platform_base_dir']
            cmd = "head -1 "+ x_platform_base_dir + "dataset"+ str(ds_id) + ".cumulative.txt "


        if expression_type == 'gct':
            gct_base_dir = config['DatasetGCTFiles']
            #head -3 /var/www/pylons-data/prod/GCTFiles/dataset6370.gct | tail -1
            cmd = "head -3 "+ gct_base_dir + "dataset"+ str(ds_id) + ".gct | tail -1"


        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        output = p.stdout.read()
        p.stdout.close()

        samples_to_return = output.split('\n')[0].split('\t')

        # Remove the \n first and then split on \t
        if expression_type == 'gct':
            try:
                samples_to_return.remove('NAME')
            except:
                pass
            try:
                samples_to_return.remove('Description')
            except:
                pass

        if expression_type == 'yugene':
            try:
                samples_to_return.remove('Probe')
            except:
                pass

        return samples_to_return

    @staticmethod
    def get_last_line_of_expression_file(ds_id,expression_type):

        if expression_type == 'yugene':
            x_platform_base_dir = config['x_platform_base_dir']
            # yugene redis
            cmd = redis_initialise_yugene + " " + redis_server + " " + x_platform_base_dir + " " + str(ds_id)
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
            output = p.stdout.read()
            p.stdout.close()

        if expression_type == 'gct':
            gct_base_dir = config['DatasetGCTFiles']
            cmd = "tail -n 1 "+ gct_base_dir +"dataset"+str(ds_id)+".gct"
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
            output = p.stdout.read()
            p.stdout.close()

        return output

    @staticmethod
    def return_short_term_redis_keys(ds_id_data,accessed_gene_graphs_info,accessed_gene_list_graphs_info):

        unpickled_gene_mapping_data = {}
        redis_keys_list = {} #this is all the possible keys taht can exsit based on audit log
        exsiting_redis_keys_list = {} #this is list of keys from redis_keys_list that actually exist in redis
        delimiter = config["delimiter"]
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        for ds_id in ds_id_data:
            dataset_metadata_key = "dataset_metadata|"+ds_id
            redis_keys_list[ds_id] = [dataset_metadata_key]

            if ds_id_data[ds_id]['data_type_id'] != 8:
                #check if graph was accessed for that dataset, if not we dont need to delete keys for gene mapping and probe data
                if ds_id in accessed_gene_graphs_info:
                    # we only want unique genes
                    unique_genes = set(accessed_gene_graphs_info[ds_id]['gene_id'])
                    unique_genes_list = list(unique_genes)

                    for gene in unique_genes_list:
                        redis_gene_mapping_key  = "gene_mapping_data"+delimiter+str(ds_id_data[ds_id]['mapping_id'])+delimiter+gene+delimiter+"ensemblID"+delimiter+str(ds_id_data[ds_id]['db_id'])
                        redis_keys_list[ds_id].append(redis_gene_mapping_key)

                        # get data for this key to get all mapped probes
                        redis_data_for_gene_mapping = r_server.get(redis_gene_mapping_key)
                        if redis_data_for_gene_mapping is not None:
                            unpickled_gene_mapping_data[gene] = Stemformatics_Expression.unpickle_expression_data(redis_data_for_gene_mapping)
                            # create key for probe data
                            for probe in unpickled_gene_mapping_data[gene]:
                                redis_probe_data_key = "probe_graph_data"+delimiter+ds_id+delimiter+probe+delimiter+"probeID"+delimiter+str(ds_id_data[ds_id]['db_id'])
                                redis_keys_list[ds_id].append(redis_probe_data_key)

                if ds_id in accessed_gene_list_graphs_info:
                    # we only want unique gene lists
                    unique_gene_lists = set(accessed_gene_list_graphs_info[ds_id]['gene_set_id'])
                    unique_gene_lists_list = list(unique_gene_lists)

                    for gene_set_id in unique_gene_lists_list:
                        redis_gene_set_mapping_key  = "gene_set_mapping_data"+delimiter+str(ds_id_data[ds_id]['mapping_id'])+delimiter+gene_set_id+delimiter+"gene_set_id"+delimiter+str(ds_id_data[ds_id]['db_id'])
                        redis_keys_list[ds_id].append(redis_gene_set_mapping_key)
            else:
                # remove miRNA mapping from redis
                if ds_id in accessed_gene_graphs_info:
                    # we only want unique genes
                    unique_genes = set(accessed_gene_graphs_info[ds_id]['gene_id'])
                    unique_genes_list = list(unique_genes)

                    for miRNA in unique_genes_list:
                        redis_gene_mapping_key  = "miRNA_mapping_data"+delimiter+ds_id+delimiter+miRNA+delimiter+"miRNA+delimiter"+str(ds_id_data[ds_id]['db_id'])
                        redis_keys_list[ds_id].append(redis_gene_mapping_key)

                        # get data for this key to get all mapped probes
                        redis_data_for_gene_mapping = r_server.get(redis_gene_mapping_key)
                        if redis_data_for_gene_mapping is not None:
                            unpickled_gene_mapping_data[gene] = Stemformatics_Expression.unpickle_expression_data(redis_data_for_gene_mapping)
                            # create key for probe data
                            for probe in unpickled_gene_mapping_data[gene]:
                                redis_probe_data_key = "probe_graph_data"+delimiter+ds_id+delimiter+probe+delimiter+"probeID"+delimiter+str(ds_id_data[ds_id]['db_id'])
                                redis_keys_list[ds_id].append(redis_probe_data_key)

            # check if keys actually exists in redis
            for key in redis_keys_list[ds_id]:
                if r_server.exists(key):
                    if ds_id not in exsiting_redis_keys_list:
                        exsiting_redis_keys_list[ds_id] = []
                    exsiting_redis_keys_list[ds_id].append(key)
        return exsiting_redis_keys_list


    """
    This method will be passed in list of datasets, number of days for which we want to delete redis data for that dataset
    This will not delete redis keys, nor build redis keys
    This will only get the info such as mapping_id for ds_id, number of genes/gene list/miRNA that have their data stored in redis for that dataset using audit_log table
    """
    @staticmethod
    def get_info_for_building_redis_short_term_keys(list_of_ds_ids,db,run_script_automatically,days_to_subtract=None):
        list_of_changed_ds_ids = list_of_ds_ids
        list_of_changed_str_ds_ids= []
        expiry_amplifier = 2
        for ds_id in list_of_changed_ds_ids:
            list_of_changed_str_ds_ids.append(str(ds_id))
        do_yugene_check = False
        if days_to_subtract is None: #if days_to_subtract is not passed in that use expiry time from config
            days_to_subtract = (config['expiry_time']/86400) * expiry_amplifier
        d = datetime.today() - timedelta(days=days_to_subtract)
        date_formatted = d.strftime('%Y-%m-%d')
        run_script_log = {}

        if run_script_automatically:
            for ds_id in list_of_ds_ids:
                show_text = Stemformatics_Dataset.setup_new_dataset(db,ds_id)
                run_script_log[str(ds_id)] = show_text

        if list_of_changed_ds_ids != []:
            # get extra info for changed ds_id's
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select id,mapping_id,data_type_id,db_id from datasets where id in %(list_of_changed_ds_ids)s;",{"list_of_changed_ds_ids":tuple(list_of_changed_ds_ids)})

            result_changed_ds_id_info = cursor.fetchall()

            data = {"date":date_formatted,"list_of_changed_ds_ids":tuple(list_of_changed_str_ds_ids)}

            # get the extra info for gene lists whose graph has been accessed from audit log
            cursor.execute("select ref_id,extra_ref_id from stemformatics.audit_log where date_created >= %(date)s and extra_ref_type = 'gene_set_id' and action = 'histogram_wizard' and ref_id in %(list_of_changed_ds_ids)s;",data)
            result_gene_set_id_info = cursor.fetchall()
            # get info for gene set items for gene list
            cursor.execute("select ref_id,extra_ref_id from stemformatics.audit_log where date_created >= %(date)s and extra_ref_type = 'gene_set_items' and action = 'histogram_wizard' and ref_id in %(list_of_changed_ds_ids)s;",data)
            result_gene_set_items_info = cursor.fetchall()
            # get the extra info for genes whose graph has been accessed from audit log
            cursor.execute("select ref_id,extra_ref_id from stemformatics.audit_log where date_created >= %(date)s and extra_ref_type = 'gene_id' and action = 'graph_data' and ref_id in %(list_of_changed_ds_ids)s;",data)
            result_gene_id_info = cursor.fetchall()

            cursor.close()
            conn.close()

            changed_ds_id_info = {}
            for row in result_changed_ds_id_info:
                ds_id = str(row['id'])
                mapping_id = row['mapping_id']
                data_type_id = row['data_type_id']
                db_id = row['db_id']

                changed_ds_id_info[ds_id] = {}
                changed_ds_id_info[ds_id]['mapping_id'] = mapping_id
                changed_ds_id_info[ds_id]['data_type_id'] = data_type_id
                changed_ds_id_info[ds_id]['db_id'] = db_id

            accessed_gene_graphs_info ={}
            for row in result_gene_id_info:
                ds_id = str(row['ref_id'])
                gene_id = row['extra_ref_id']

                accessed_gene_graphs_info[ds_id] = {}
                if 'gene_id' not in accessed_gene_graphs_info[ds_id]:
                    accessed_gene_graphs_info[ds_id]['gene_id'] = []
                accessed_gene_graphs_info[ds_id]['gene_id'].append(gene_id)

            # this will append the genes found mapped to gene list into the accessed_gene_graphs_info list
            for row in result_gene_set_items_info:
                ds_id = str(row['ref_id'])
                gene_ids = json.loads(row['extra_ref_id'])
                if ds_id not in accessed_gene_graphs_info:
                    accessed_gene_graphs_info[ds_id] = {}
                if 'gene_id' not in accessed_gene_graphs_info[ds_id]:
                    accessed_gene_graphs_info[ds_id]['gene_id'] = []
                accessed_gene_graphs_info[ds_id]['gene_id'].extend(gene_ids)


            accessed_gene_list_graphs_info ={}
            for row in result_gene_set_id_info:
                ds_id = str(row['ref_id'])
                gene_set_id = row['extra_ref_id']

                accessed_gene_list_graphs_info[ds_id] = {}
                if 'gene_set_id' not in accessed_gene_list_graphs_info[ds_id]:
                    accessed_gene_list_graphs_info[ds_id]['gene_set_id'] = []
                accessed_gene_list_graphs_info[ds_id]['gene_set_id'].append(gene_set_id)

            return [changed_ds_id_info,accessed_gene_graphs_info,accessed_gene_list_graphs_info,run_script_log]
        else:
            return 'The Datasets chosen are in sync as of '+str(datetime.now())


    """
    This method get called by both admin and api controller for finding unsync datasets
    """
    @staticmethod
    def check_redis_consistency_for_datasets(days,num_of_datasets,reset_redis_required,db):
        do_yugene_check = False
        return_str = pre_return_str = post_return_str =  ''


        if num_of_datasets == "all":
            list_of_ds_ids = Stemformatics_Dataset.get_all_datasets()
        else:
            # get list of datasets affected in last few days
            list_of_ds_ids = Stemformatics_Dataset.get_list_of_new_or_updated_datasets(days)

        pre_return_str += "</br>"+"=============================================================="+"</br>"
        pre_return_str += "As on "+str(datetime.now())+"</br>"
        pre_return_str += "List of Datasets that has been checked for - " + str(list_of_ds_ids) + " in last " +str(days) +" days"
        pre_return_str += "</br>"+"=============================================================="+"</br>"

        post_return_str += "</br>"+"=============================================================="+"</br>"
        post_return_str += "</br> To check for all Datasets, please add num_of_datasets=all in the above url </br>"
        post_return_str += "</br> To check for last one week, please add days=7 in above url </br>"
        post_return_str += "</br> To Reset the UnSync Datasets, please add reset=yes in the above url </br>"
        post_return_str += "</br>"+"=============================================================="+"</br>"
        post_return_str += "</br> Kindly refrain from using num_of_datasets=all with reset=yes if too many unsync datasets are found, as it may take a very long time to set up large number of datasets in redis </br>"
        post_return_str += "</br>"+"=============================================================="+"</br>"

        # check gct vs redis for each dataset
        unsync_datasets = {}
        list_of_changed_ds_ids = []
        for ds_id in list_of_ds_ids:
            result = Stemformatics_Dataset.check_dataset_is_in_sync_in_redis(ds_id,do_yugene_check)
            if result != []:
                unsync_datasets[ds_id] = result
                list_of_changed_ds_ids.append(ds_id)

        deleted_datasets = Stemformatics_Dataset.get_list_of_deleted_datasets()

        if reset_redis_required == "yes":

            if list_of_changed_ds_ids == []: #when all datasets are in sync return quickly
                return_str = pre_return_str + "The Datasets chosen are in sync" + post_return_str

            run_script_automatically = True
            delete_keys = True
            # get info for the accessed genes/gene list for each dataset affected in last few days
            info = Stemformatics_Expression.get_info_for_building_redis_short_term_keys(list_of_changed_ds_ids,db,run_script_automatically)
            pre_return_str += "</br>" +"Deleted datasets - " + str(deleted_datasets) +"</br>"
            pre_return_str += "</br>"+"=============================================================="+"</br>"
            for ds_id in deleted_datasets:
                try:
                    redis_result = Stemformatics_Dataset.delete_dataset_redis(ds_id)
                    pre_return_str += "</br>" +"Deleted redis for dataset " + str(ds_id) +"</br>"
                except:
                    pass
            if not isinstance(info,str):
                ds_id_info = info[0]
                genes_info = info[1]
                gene_list_info = info[2]
                run_script_log = info[3] # this is log of set_up_new_dataset_in_redis
            else:
                return_str = pre_return_str + info + post_return_str
                return return_str

            # now delete short term redis for all genes/genelist/probe for all teh affected datasets
            redis_keys_dict = Stemformatics_Expression.return_short_term_redis_keys(ds_id_info,genes_info,gene_list_info)
            if delete_keys:
                output_log = {}
                for ds_id in list_of_changed_ds_ids:
                    if str(ds_id) in redis_keys_dict:
                        result = Stemformatics_Expression.delete_data_from_redis(redis_keys_dict[str(ds_id)],exact_keys=True)
                        if isinstance(result, bool):
                            output_redis_keys_log = redis_keys_dict[str(ds_id)]
                        else:
                            output_redis_keys_log = result
                    else:
                        output_redis_keys_log = "No keys found in Redis"
                    output_log[str(ds_id)] = output_redis_keys_log
            # now concatenate both the logs
            output_dict_list = [run_script_log,output_log]
            concatenated_logs = {}

            # https://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key
            for k in output_log.iterkeys():
                concatenated_logs[k] = tuple(concatenated_logs[k] for concatenated_logs in output_dict_list)

            for ds_id in output_log:
                return_str += "Synced Dataset "+ str(ds_id) +"</br>"
                return_str += "Long term Redis output"+"</br>"
                return_str += concatenated_logs[str(ds_id)][0]+"</br></br>"
                return_str += "Short Term Redis keys deleted"+"</br>"
                return_str += json.dumps(concatenated_logs[str(ds_id)][1])+"</br></br>"


        else:
            return_str += "</br>" +"Deleted datasets - " + str(deleted_datasets) +"</br>"
            return_str += "</br>"+"=============================================================="+"</br>"

            if unsync_datasets == {}:
                return_str += 'The Datasets chosen are in sync '
            else:
                for ds_id in unsync_datasets:
                    return_str += "UnSynced Dataset "+ str(ds_id) +"</br>"
                    return_str += "Issue: "+ str(unsync_datasets[ds_id]) +"</br></br>"


        return_str = pre_return_str + return_str +post_return_str

        return return_str
