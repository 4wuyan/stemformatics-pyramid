__all__ = ['Stemformatics_Msc_Signature']

# CRITICAL-6
from guide.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
from guide.model.stemformatics.stemformatics_auth import Stemformatics_Auth
from pylons import config
import psycopg2, psycopg2.extras, redis, json
import os.path


class Stemformatics_Msc_Signature(object):
    @staticmethod
    def get_msc_samples(db, msc_set):
        return Stemformatics_Dataset.get_msc_samples(db, msc_set)

    @staticmethod
    def get_lwr_upr_msc_test():
        horizontal_lines = {'lwr': 0.4337, 'upr': 0.5169}
        return horizontal_lines

    """
    This is only used to add more columns in Stemformatics_Msc_Signature.get_msc_values
    """

    @staticmethod
    def get_sample_information_for_msc_signature(db, ds_id, uid):
        sample_dict = {}
        sample_information = Stemformatics_Dataset.get_biosamples_metadata(db, ds_id)
        for item in sample_information:
            md_name = item['md_name']
            md_value = item['md_value']
            chip_id = item['chip_id']
            if chip_id not in sample_dict:
                sample_dict[chip_id] = {}

            sample_dict[chip_id][md_name] = md_value

        return sample_dict

    @staticmethod
    def get_choose_dataset_details(db, uid):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        label_name = 'choose_dataset_details'
        result = r_server.get(label_name)
        temp_datasets = json.loads(result)
        choose_datasets = {}
        list_of_msc_ds_ids = Stemformatics_Msc_Signature.get_all_dataset_msc_access()
        show_limited = False

        for ds_id in temp_datasets:
            dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db, ds_id, uid)
            if dataset_status == "Unavailable":
                continue
            if dataset_status == "Limited" and show_limited == False:
                continue

            temp_ds_id = ds_id
            ds_id = int(ds_id)

            if ds_id not in list_of_msc_ds_ids:
                continue

            choose_datasets[ds_id] = temp_datasets[temp_ds_id]
        return choose_datasets

    @staticmethod
    def get_file_name_of_msc_values(ds_id, full=True):
        try:
            msc_values_dir = config['msc_values_dir']
            file_name = 'dataset' + str(ds_id) + '.rohart.MSC.txt'
            if full:
                file_name = msc_values_dir + file_name
            return file_name
        except:
            return None

    """
    Main function to get all the values from the filename
    """

    @staticmethod
    def get_msc_values(db, ds_id, uid):
        available = Stemformatics_Msc_Signature.get_dataset_msc_access(db, ds_id, uid)
        if not available:
            return {'error': 'This dataset is not available for msc access.'}

        file_name = Stemformatics_Msc_Signature.get_file_name_of_msc_values(ds_id)
        if file_name is None:
            return {'error': 'There was an error with naming the msc file for this dataset.'}

        text_data = ""

        # get the sample information
        extra_sample_info = Stemformatics_Msc_Signature.get_sample_information_for_msc_signature(db, ds_id, uid)

        if not os.path.isfile(file_name):
            return {'error': 'There was an error with finding the msc file for this dataset.'}

            # read in the values
        with open(file_name, 'r') as f:
            count = 0
            for line in f:
                count += 1
                # skip the first line
                if count == 1:
                    text_data += "MSC_Type\tReplicate_Group_ID\tSample_Type\tSample_Type_Long\t" + line
                    continue

                # Note that lwr must be fourth column and upr must be fifth
                list_of_line = line.split("\t")
                chip_id = list_of_line[0]
                rep_id = extra_sample_info[chip_id]['Replicate Group ID']
                sample_type = extra_sample_info[chip_id]['Sample Type']
                sample_type_long = extra_sample_info[chip_id]['Sample type long']
                lwr = list_of_line[3]
                upr = list_of_line[4]
                msc_type = Stemformatics_Msc_Signature.calculate_msc_type(lwr, upr)
                text_data += msc_type + "\t" + rep_id + "\t" + sample_type + "\t" + sample_type_long + "\t" + line

        # finalise the text and return
        return text_data

    """
    This makes the assumption that the lwr will be lower than the prediction
    and that the upr will be highier than the prediction score
    this is expecting a string
    """

    @staticmethod
    def calculate_msc_type(string_lwr, string_upr):

        lwr_upr_values = Stemformatics_Msc_Signature.get_lwr_upr_msc_test()
        lwr = float(string_lwr)
        upr = float(string_upr)
        if lwr > lwr_upr_values['upr']:
            # this is definitely a MSC
            msc_type = 'MSC';
        elif upr < lwr_upr_values['lwr']:
            # this is definitely not a MSC
            msc_type = 'Non-MSC';
        else:
            # this is unknown
            msc_type = 'Unsure';

        return msc_type

    """
    This is supposed to handle only one at a time
    """

    @staticmethod
    def get_dataset_msc_access(db, ds_id, uid):

        if not isinstance(ds_id, int):
            return False

        # uid is checked for in this function
        available = Stemformatics_Dataset.check_dataset_availability(db, uid, ds_id)
        if not available:
            return False

        msc_values_access = config['msc_values_access']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = "select ds_id from dataset_metadata where ds_name = '" + msc_values_access + "'and ds_id = %s and ds_value = 'True'"
        data = (ds_id,)
        cursor.execute(sql, data)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        try:
            if result[0][0] == ds_id:
                return True
            else:
                return False
        except:
            return False

    """
    This is supposed to handle all datasets that are available for MSC
    """

    @staticmethod
    def get_all_dataset_msc_access():
        list_of_ds_ids = []

        msc_values_access = config['msc_values_access']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = "select ds_id from dataset_metadata where ds_name = '" + msc_values_access + "' and ds_value = 'True'"
        cursor.execute(sql)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()

        for row in result:
            ds_id = row[0]
            list_of_ds_ids.append(ds_id)

        return list_of_ds_ids

    @staticmethod
    def get_user_access(db, uid):
        role = Stemformatics_Auth.get_user_role(db, uid)
        groups = Stemformatics_Auth.get_groups_for_uid(db, uid, '')
        group_id_for_msc_signature = 4  # unfortunately this is hardcoded. Group was created first
        if role == 'admin' or role == 'annotator' or group_id_for_msc_signature in groups:
            return True
        else:
            return False

    @staticmethod
    def get_msc_samples_summary_by_ds_id(db, msc_set):
        msc_samples = Stemformatics_Dataset.get_msc_samples(db, msc_set)
        summary_data = {}

        for ds_id in msc_samples:
            if ds_id not in summary_data:
                summary_data[ds_id] = {}
                summary_data[ds_id]['handle'] = Stemformatics_Dataset.getHandle(db, ds_id)
                summary_data[ds_id]['Total'] = 0
                summary_data[ds_id]['MSC'] = 0
                summary_data[ds_id]['Non-MSC'] = 0
                summary_data[ds_id]['Training'] = 0
                summary_data[ds_id]['Testing'] = 0
                summary_data[ds_id]['Excluded'] = 0
                summary_data[ds_id]['MSC Training'] = 0
                summary_data[ds_id]['Non-MSC Training'] = 0
                summary_data[ds_id]['MSC Testing'] = 0
                summary_data[ds_id]['Non-MSC Testing'] = 0

            for sample in msc_samples[ds_id]:
                row = msc_samples[ds_id][sample]
                msc_type = row['project_msc_type']
                msc_set = row['project_msc_set']

                summary_data[ds_id]['Total'] += 1

                if msc_set == 'Excluded':
                    summary_data[ds_id]['Excluded'] += 1
                if msc_set == 'Testing':
                    summary_data[ds_id]['Testing'] += 1
                if msc_set == 'Training':
                    summary_data[ds_id]['Training'] += 1
                if msc_type == 'MSC':
                    summary_data[ds_id]['MSC'] += 1
                if msc_type == 'Non-MSC':
                    summary_data[ds_id]['Non-MSC'] += 1

                if msc_type == 'MSC' and msc_set == 'Training':
                    summary_data[ds_id]['MSC Training'] += 1
                if msc_type == 'Non-MSC' and msc_set == 'Training':
                    summary_data[ds_id]['Non-MSC Training'] += 1
                if msc_type == 'MSC' and msc_set == 'Testing':
                    summary_data[ds_id]['MSC Testing'] += 1
                if msc_type == 'Non-MSC' and msc_set == 'Testing':
                    summary_data[ds_id]['Non-MSC Testing'] += 1

        return summary_data

