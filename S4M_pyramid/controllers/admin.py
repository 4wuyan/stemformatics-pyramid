import logging, redis
log = logging.getLogger(__name__)
from subprocess import Popen, PIPE, STDOUT
from S4M_pyramid.model import twitter
from pyramid_handlers import action

# from pylons import request, response, session, url, tmpl_context as c
# from pylons.controllers.util import abort, redirect
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, app_globals as g, config
from S4M_pyramid.model.stemformatics import db_deprecated_pylons_orm as db
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Auth, Stemformatics_Dataset


# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from paste.deploy.converters import asbool

from datetime import date, timedelta, datetime

import json , cgi , urllib , os, subprocess , hashlib, ast

class AdminController(BaseController):
    """ Have to check for admin for all of the controllers"""

    def __init__(self,request):
        super().__init__(request)
        c = self.request.c
        if request.path_info in ('/admin/annotate_dataset','/admin/save_and_validate_dataset_annotations'):
                ds_id = int(request.params.get('ds_id'))
                uid = c.uid
                available = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id,'annotator')
                if not available: return redirect(url(controller='contents', action='index'), code=404)
        else:
            if not c.role =="admin":
                if request.path_info in ('/admin/audit_reports','/admin/controller_user_audit_report'):

                    try:
                        uids = config['audit_reports_uid_list']
                    except:
                        return redirect(url(controller='contents', action='index'), code=404)

                    # if only one number in audit_reports_uid_list, then it will be treated as an integer
                    if isinstance(uids,int):
                        if c.uid != uids:
                            redirect(url(controller='contents', action='index'), code=404)
                    else:
                        delimiter = config['delimiter']
                        uid_list = uids.split(delimiter)
                        uid_list = map(int, uid_list)
                        if c.uid not in uid_list:
                            return redirect(url(controller='contents', action='index'), code=404)
                else:
                    return redirect(url(controller='contents', action='index'), code=404)



    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def read_logfile(self):
        number  = request.params.get('number_of_lines')
        if number is None:
            number = 500
        logfile= Stemformatics_Admin.get_logfile(number)
        return logfile

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def check_jar_processes(self):
        content= Stemformatics_Admin.get_jar_processes()
        return content

    @Stemformatics_Auth.authorise()
    @action(renderer='templates/admin/index.mako')
    def index(self):
        return self.deprecated_pylons_data_for_view
    '''
    This is for troubleshooting page Gene Expression Graph for listing/deleting redis cache for a dataset.
    '''
    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def troubleshoot_geg(self):
        c.ds_id = ds_id = request.params.get('ds_id')
        output = request.params.get('output')
        expiry_seconds = request.params.get('expiry_seconds')
        delete_keys = request.params.get('delete')
        if expiry_seconds is not None:
            try:
                days = int(expiry_seconds)/86400
            except:
                days = config["sync_dataset_redis_after_x_days"]
        else:
            days = config["sync_dataset_redis_after_x_days"]
        c.expiry_time = int(config["expiry_time"])/3600
        c.count = Stemformatics_Expression.get_feature_mapping_stats(c.ds_id)
        run_script_automatically = False
        if output is not None:
            c.output = output
        info = Stemformatics_Expression.get_info_for_building_redis_short_term_keys([ds_id],db,run_script_automatically,days)
        ds_id_info = info[0]
        genes_info = info[1]
        gene_list_info = info[2]

        keys = Stemformatics_Expression.return_short_term_redis_keys(ds_id_info,genes_info,gene_list_info)
        if delete_keys == 'yes':
            exact_keys = True
            if ds_id in keys:
                output = Stemformatics_Expression.delete_data_from_redis(keys[ds_id],exact_keys)
                if output == True:
                    c.output = 'Deleted Successfully'
                elif output == False:
                    c.output = 'Some keys are not deleted Successfully'
            else:
                c.output = 'No Short Term Redis Keys present'
            redirect('/admin/troubleshoot_geg?ds_id='+c.ds_id+'&output='+c.output)

        if keys != {}:
            keys[ds_id].sort()
        c.result = keys
        return render('admin/troubleshoot_geg.mako')


    ''' This is to update the config['all_sample_metadata'] file '''
    @Stemformatics_Auth.authorise(db)
    @action(renderer="string")
    def setup_all_sample_metadata(self):
        g.all_sample_metadata = Stemformatics_Expression.setup_all_sample_metadata()
        return "Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def setup_all_user_dataset_availability(self):
        Stemformatics_Auth.setup_redis_get_dict_of_user_dataset_availability(db)
        return "Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def validation_replicate_group_id(self,id):

        tests_to_perform = id
        result = Stemformatics_Expression.validate_replicate_group_id(db,tests_to_perform)

        return result.replace("\n","<br/>")



    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def confirm(self):
       return "another wone"

    ''' This is to update the gct files '''
    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def setup_redis_gct(self,id):
        try:
            ds_id = int(id)
        except:
            return "Error with this. Must be an integer"

        if ds_id == 0:
            return "Error with the dataset id. Cannot be 0"

        # python initialise.py localhost /var/www/pylons-data/SHARED/GCTFiles 0
        redis_initialise = config['redis_initialise_gct']
        redis_server = config['redis_server']
        gct_base_dir = config['DatasetGCTFiles']



        cmd = redis_initialise + " " + redis_server + " " + gct_base_dir + " " + str(ds_id)
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read()

        return cmd + "<br><br>" + output.replace("\n","<br/>") + "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    ''' This is to update the cumulative files '''
    @Stemformatics_Auth.authorise(db)
    @action(renderer="string")
    def setup_redis_cumulative(self,id):
        try:
            ds_id = int(id)
        except:
            return "Error with this. Must be an integer"

        if ds_id == 0:
            return "Error with the dataset id. Cannot be 0"

        # python initialise.py localhost /var/www/pylons-data/SHARED/CUMULATIVEFiles 0
        redis_initialise = config['redis_initialise_x_platform']
        redis_server = config['redis_server']
        x_platform_base_dir = config['x_platform_base_dir']



        cmd = redis_initialise + " " + redis_server + " " + x_platform_base_dir + " " + str(ds_id)
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read()

        return cmd + "<br><br>" + output.replace("\n","<br/>") + "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"


    ''' This is to add one new dataset '''
    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def setup_new_dataset(self,id):
        ds_id = int(id)

        show_text = Stemformatics_Dataset.setup_new_dataset(db,ds_id)

        if ds_id != 0:
            audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
            result = Stemformatics_Audit.add_audit_log(audit_dict)
        return show_text


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def show_all_user_emails_critical_outage(self):

        result = Stemformatics_Auth.return_all_active_users(db)

        body = ""

        for user in result:
            if user['send_email_outages_critical']:
                body += user['username'] + ","


        return "<textarea style=\"width:800px;height:400px;\">"+body+"</textarea>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def show_subscriber_lists(self):

        result = Stemformatics_Auth.return_user_notifications(db)

        body = ""

        for user in result:
            body += user.username + ","


        return "<textarea style=\"width:800px;height:400px;\">"+body+"</textarea>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def dataset_override_users(self):

        c.result = Stemformatics_Admin.dataset_override_users(db)
        c.user_status_dict = Stemformatics_Auth.user_status_dict()
        return render('/admin/dataset_override_users.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def all_users(self):

        c.result = Stemformatics_Admin.all_users(db)
        c.user_status_dict = Stemformatics_Auth.user_status_dict()
        return render('/admin/all_users.mako')

    """ 127.0.0.1:5000/admin/add_users_to_groups_wizard?group_ids=1&user_ids=44&user_emails=rowland@mailinator.com,davidp@mailinator.com """
    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def add_users_to_groups_wizard(self): #CRITICAL-4 CRITICAL-5
        group_ids  = request.params.get('group_ids')
        user_emails  = request.params.get('user_emails')
        user_ids  = request.params.get('user_ids')
        c.title = c.site_name+' Workbench - Hierarchical Cluster Wizard'
        if group_ids is None:
            # choose group
            c.base_url = str(url('/admin/add_users_to_groups_wizard?'))
            c.groups_dict = Stemformatics_Auth.get_all_group_names(db)
            return render('/admin/choose_group.mako')

        if user_ids is None and user_emails is None:
            # choose group
            c.result = Stemformatics_Admin.all_users(db)
            c.user_status_dict = Stemformatics_Auth.user_status_dict()
            c.group_ids = group_ids
            c.base_url = str(url('/admin/add_users_to_groups_wizard?group_ids=')+group_ids)

            # textarea to enter in email and/or list users to select
            return render('/admin/choose_user.mako')

        group_ids_array = group_ids.split(',')
        user_ids_array = user_ids.split(',')
        user_emails_array = user_emails.split(',')
        error_message = ''
        for gid in group_ids_array:
            gid = int(gid)
            for uid in user_ids_array:
                if uid != '':
                    uid = int(uid)
                    result_uid_to_gid = Stemformatics_Auth.add_user_to_group(db,uid,gid)

            for user_email in user_emails_array:
                if user_email != '':
                    user_email = str(user_email)
                    result_user_email = Stemformatics_Auth.create_new_pending_user(db,user_email)
                    if isinstance(result_user_email,str):
                        error_message = error_message + '\n' + user_email + ": " + result_user_email + " "
                    else:
                        uid = result_user_email.uid
                        result_uid_to_gid = Stemformatics_Auth.add_user_to_group(db,uid,gid)

        Stemformatics_Auth.triggers_for_change_in_user(db)

        redirect('/admin/all_groups')




    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def all_groups(self):
        c.groups_dict = Stemformatics_Auth.get_all_group_names(db)
        c.user_status_dict = Stemformatics_Auth.user_status_dict()
        c.result = Stemformatics_Auth.get_all_group_users(db)
        return render('/admin/all_groups.mako')



    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def show_dataset_availability(self):
        user_ids  = request.params.get('user_ids')
        if user_ids is None :
            # choose group
            c.result = Stemformatics_Admin.all_users(db)
            c.user_status_dict = Stemformatics_Auth.user_status_dict()
            c.group_ids = 0
            c.base_url = str(url('/admin/show_dataset_availability?'))
            # textarea to enter in email and/or list users to select
            return render('/admin/choose_user.mako')
        c.output = {}
        user_id_array = user_ids.split(',')
        for uid in user_id_array:
            uid_result = Stemformatics_Dataset.get_dataset_availability(db,uid)
            c.output[uid] = uid_result

        return render('/admin/show_dataset_availability.mako')



    ''' This is to check a users access to a dataset'''
    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def check_uid_ds_id(self): #CRITICAL-5
        user_ids  = request.params.get('user_ids')
        ds_id  = request.params.get('datasetID')
        if user_ids is None :
            # choose group
            c.result = Stemformatics_Admin.all_users(db)
            c.user_status_dict = Stemformatics_Auth.user_status_dict()
            c.group_ids = 0
            c.base_url = str(url('/admin/check_uid_ds_id?'))
            # textarea to enter in email and/or list users to select
            return render('/admin/choose_user.mako')

        if ds_id is None:
            c.species = None
            c.datasets = Stemformatics_Dataset.getAllDatasetDetails(db,c.uid)
            if user_ids is None:
                user_ids = ''
            c.url = str(url('/admin/check_uid_ds_id'))+'?user_ids='+str(user_ids)
            c.breadcrumbs = []
            c.analysis = None
            return render('workbench/choose_dataset.mako')

        ds_id = int(ds_id)
        output = ""
        user_id_array = user_ids.split(',')
        for uid in user_id_array:
            uid_result = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)
            uid_annotator_result = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id,'annotator')

            result_user = Stemformatics_Auth.get_user_from_uid(db,uid)
            username = result_user.username
            output = output + str(username)+"["+str(uid) + "]:" + str(uid_result) + " access to "+str(ds_id)+" -- Annotator access =>" + str(uid_annotator_result) + "<br/>"


        return output


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def add_objects_to_datasets(self): #CRITICAL-5 CRITICAL-4
        ds_id  = request.params.get('datasetID')
        user_emails  = request.params.get('user_emails')
        group_ids  = request.params.get('group_ids')
        user_ids  = request.params.get('user_ids')
        c.title = c.site_name+' Workbench - Hierarchical Cluster Wizard'
        if group_ids is None:
            # choose group
            c.base_url = str(url('/admin/add_objects_to_datasets?'))
            c.groups_dict = Stemformatics_Auth.get_all_group_names(db)
            return render('/admin/choose_group.mako')

        if user_ids is None and user_emails is None:
            # choose group
            c.result = Stemformatics_Admin.all_users(db)
            c.user_status_dict = Stemformatics_Auth.user_status_dict()
            c.group_ids = group_ids

            c.base_url = str(url('/admin/add_objects_to_datasets?group_ids=')+group_ids)
            # textarea to enter in email and/or list users to select
            return render('/admin/choose_user.mako')

        if ds_id is None:
            c.species = None
            c.datasets = Stemformatics_Dataset.getAllDatasetDetails(db,c.uid)
            if user_ids is None:
                user_ids = ''
            if user_emails is None:
                user_emails = ''
            c.url = str(url('/admin/add_objects_to_datasets?group_ids='))+str(group_ids)+'&user_ids='+str(user_ids)+'&user_emails='+str(user_emails)
            c.breadcrumbs = []
            c.analysis = None
            return render('workbench/choose_dataset.mako')

        ds_id = int(ds_id)

        if group_ids != '':
            group_id_array = group_ids.split(',')
            for group_id in group_id_array:
                gid = int(group_id)
                object_type = 'Group'
                object_id = str(gid)
                result_gid = Stemformatics_Dataset.add_override_private_dataset(db,object_type,object_id,ds_id)

        if user_emails != '':
            user_email_array = user_emails.split(',')
            for user_email in user_email_array:
                user_email = str(user_email)
                result_user_email = Stemformatics_Auth.create_new_pending_user(db,user_email)
                if isinstance(result_user_email,str):
                    error_message = error_message + '\n' + user_email + ": " + result_user_email + " "
                else:
                    uid = result_user_email.uid
                    object_type = 'User'
                    object_id = str(uid)
                    result_uid = Stemformatics_Dataset.add_override_private_dataset(db,object_type,object_id,ds_id)


        if user_ids != '':
            user_id_array = user_ids.split(',')
            for user_id in user_id_array:
                uid = int(user_id)
                object_type = 'User'
                object_id = str(uid)
                result_uid = Stemformatics_Dataset.add_override_private_dataset(db,object_type,object_id,ds_id)

        Stemformatics_Auth.triggers_for_change_in_user(db)
        redirect('/admin/dataset_override_users')



    ''' This is to update the standard deviation files '''
    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def setup_redis_sd(self):
        # python initialise.py localhost /var/www/pylons-data/SHARED/StandardDeviationFiles 0
        redis_initialise = config['redis_initialise_sd']
        redis_server = config['redis_server']
        sd_base_dir = config['DatasetStandardDeviationFiles']

        cmd = redis_initialise + " " + redis_server + " " + sd_base_dir
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read()

        return cmd + "<br><br>" + output.replace("\n","<br/>") + "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def annotate_dataset(self):
        c.ds_id = ds_id  = int(request.params.get('ds_id'))
        c.instance = instance  = request.params.get('instance')
        private = Stemformatics_Dataset.check_private_dataset(ds_id)

        if not private:
            c.title = "This dataset is public and cannot be annotated"
            c.message = "This dataset "+str(ds_id)+" is public and cannot be annotated."
            return render ('workbench/error_message.mako')


        c.db_id = Stemformatics_Dataset.get_db_id(db,ds_id)




        # group settings
        c.gid = gid  = request.params.get('gid',None)
        c.list_of_gids = Stemformatics_Auth.get_groups_for_uid(db,c.uid,c.role)
        if gid is not None and gid not in c.list_of_gids:
            c.gid = 0

        c.list_of_groups = Stemformatics_Auth.get_all_group_names(db)
        config_type = 'Annotation'
        c.group_configs = Stemformatics_Auth.get_all_group_configs(config_type,c.uid,c.role)



        new_metadata  = request.params.get('new_metadata')

        c.columns_default = ['Replicate Group ID','Sample name','Sample name long','Sample Type','Sample type long','Generic sample type','Generic sample type long','Sample Description','Organism','Tissue/organism part','Parental cell type','Final cell type','Cell line','Reprogramming method','Developmental stage','Media','Disease State','Labelling','Genetic modification','FACS profile','Age','Sex']
        c.columns_default_json = json.dumps(c.columns_default);
        # technically all admins should have access to all datasets (perhaps including published)
        available = Stemformatics_Dataset.check_dataset_availability(db,c.uid,ds_id)

        if not available:
            redirect(url(controller='contents', action='index'), code=404)

        # get ds metadata for this dataset
        # convert this to json for handsontable
        result = Stemformatics_Dataset.convert_ds_md_into_json(db,ds_id,c.uid)
        c.json_ds_md = result[0]
        c.ds_md = result[1]
        c.handle = Stemformatics_Dataset.getHandle(db,ds_id)
        c.chip_type = Stemformatics_Dataset.getChipType(db,ds_id) #CRITICAL-2

        # get bs_md for this dataset
        # convert this to json for handson table
        result_array = Stemformatics_Dataset.convert_bs_md_into_json(db,ds_id,c.uid)
        c.json_headers = result_array[0]
        c.headers = json.loads(c.json_headers)
        c.json_bs_md = result_array[1]

        chip_ids = Stemformatics_Expression.get_sample_labels(ds_id)
        c.chip_ids = json.dumps(chip_ids)

        # call mako template

        audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        return render('admin/annotate_dataset.mako')


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def save_and_validate_dataset_annotations(self): #TODO-2
        # convert json to bs_md and md
        # save bs_md and md back to the database
        ds_id = request.params.get('ds_id')
        action = request.params.get('action')
        json_ds_md = request.params.get('json_ds_md')
        json_bs_md= request.params.get('json_bs_md')
        json_headers  = request.params.get('json_headers')
        delimiter = config['redis_delimiter']
        # bs_md_text is generated for troubleshoot only as it takes 2 sec, and forces timeout
        if action == "Troubleshoot":
            bs_md_text_required = "yes"
        else:
            bs_md_text_required = "no"

        bs_md_results = Stemformatics_Dataset.convert_json_into_bs_md(json_headers,json_bs_md,bs_md_text_required)
        bs_md_list = bs_md_results[1]
        bs_md_text = bs_md_results[0]
        ds_md_results = Stemformatics_Dataset.convert_json_into_ds_md(json_ds_md)
        ds_md_dict = ds_md_results[1]
        ds_md_text = ds_md_results[0]
        if action == "Save":
            result = Stemformatics_Dataset.save_updated_annotation_metadata(db,bs_md_list,ds_md_dict,ds_id)
            if result:
                #g.all_sample_metadata =  Stemformatics_Expression.setup_all_sample_metadata(db)
                #other_result = Stemformatics_Dataset.refresh_dataset_stats_summary(db)
                #result = Stemformatics_Dataset.write_cls_file(db,ds_id,c.uid)
                return_text = "This was saved successfully."
                audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
                result = Stemformatics_Audit.add_audit_log(audit_dict)
            else:
                return_text = "There was a problem saving."
        if action == "Troubleshoot":
            return_text = Stemformatics_Dataset.validate_updated_annotation_metadata(db,bs_md_text,ds_md_text,ds_id)
        if action == "Set Front End":
            run_script_automatically = False
            days = None # by default the days will be based on expiry_time in the config
            info  = Stemformatics_Expression.get_info_for_building_redis_short_term_keys([ds_id],db,run_script_automatically,days)
            ds_id_info = info[0]
            genes_info = info[1]
            gene_list_info = info[2]
            delete_keys = True
            redis_keys_list = Stemformatics_Expression.return_short_term_redis_keys(ds_id_info,genes_info,gene_list_info)
            if ds_id in redis_keys_list: #execute when keys are present in redis
                exact_keys = True
                output = Stemformatics_Expression.delete_data_from_redis(redis_keys_list[ds_id],exact_keys)
                if isinstance(output,str):
                    return output

            g.all_sample_metadata =  Stemformatics_Expression.setup_dataset_sample_metadata(db,g.all_sample_metadata,ds_id)
            other_result = Stemformatics_Dataset.refresh_dataset_stats_summary(db)
            Stemformatics_Dataset.triggers_for_change_in_dataset(db,ds_id)
            result = True

            audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
            result = Stemformatics_Audit.add_audit_log(audit_dict)
            if result:
                return_text = "This was pushed to the front end successfully."

        return return_text


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def update_datasets(self):
        ds_id = int(request.params.get('ds_id', 0))
        c.msc_values_access = config['msc_values_access']

        if ds_id != 0:
            datasets = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)
            c.datasets = {}
            c.datasets[ds_id] = datasets[ds_id]
        else:
            datasets = Stemformatics_Dataset.getAllDatasetDetails(db,c.uid,False)
            c.datasets = datasets

        return render('admin/update_datasets.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def make_dataset_public(self,id):
        try:
            ds_id = int(id)
        except:
            ds_id = 0

        if ds_id != 0:
            new_value = "False"
            updated_field = "private"
            update_dict = {}
            update_dict[updated_field] = new_value
            result = Stemformatics_Dataset.update_dataset_single_field(db,c.uid,ds_id,update_dict)
            external_base_url = url('/',qualified=True)
            #username = c.full_name
            #c.email= Stemformatics_Dataset.setup_email_to_contributing_author(c.dataset[ds_id],ds_id,username,external_base_url)
            c.dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)
            c.ds_id = ds_id
            c.external_base_url = external_base_url
        else:
            return "This needs to have a dataset selected."

        return render('admin/make_dataset_public.mako')




    #---------------------NOT MIGRATED--------------------------------
    def update_dataset_single_field(self,id):
        ds_id = int(id)
        new_value = request.params.get('new_value')
        updated_field = request.params.get('updated_field')
        update_dict = {}
        update_dict[updated_field] = new_value
        result = Stemformatics_Dataset.update_dataset_single_field(db,c.uid,ds_id,update_dict)
        if result:
            redirect ('/admin/update_datasets?ds_id='+str(ds_id))
        else:
            return "Problem with update"

    @Stemformatics_Auth.authorise(db)
    @action(renderer="string")
    def triggers_for_change_in_dataset(self):
        Stemformatics_Dataset.triggers_for_change_in_dataset(db)

        return "Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def triggers_for_change_in_user(self):
        Stemformatics_Auth.triggers_for_change_in_user(db)

        return "Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    ''' This is to update the cls files '''
    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def setup_cls_files(self,id):
        try:
            ds_id = int(id)
        except:
            return "Error with this. Must be an integer"

        if ds_id == 0:
            return "Error with the dataset id. Cannot be 0"

        # get ds_id and pass it into create/overwrite the cls for this dataset
        result = Stemformatics_Dataset.write_cls_file(db,ds_id,c.uid)

        return "<br><br>"+result+"<br><br> <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def help(self):
        c.help_list = Stemformatics_Help.get_all_help_list()
        return render('admin/all_help.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def delete_all_help(self):
        Stemformatics_Help.delete_all_help()
        c.help_list = Stemformatics_Help.get_all_help_list()
        return render('admin/all_help.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def edit_tutorial(self):
        c.help_type = "tutorial"
        c.help_name = request.params.get('name', "")
        c.start_page = ""
        c.help_json = ""
        if c.help_name != "":
            tutorial = Stemformatics_Help.get_tutorial(c.help_name)
            c.start_page = tutorial["start_page"]
            c.help_json = json.dumps(tutorial["data"], indent=4, separators=(',', ': '))
        return render('admin/edit_help.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def edit_pageguide(self):
        c.help_type = "page_guide"
        c.help_name = request.params.get('page', "")
        c.help_json = json.dumps(Stemformatics_Help.get_pageguide(c.help_name), indent=4, separators=(',', ': ')) if c.help_name != "" else ""
        return render('admin/edit_help.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def save_help(self):
        help_type = request.params.get('helptype', None)
        help_name = request.params.get('helpname', None)
        json_file = request.params.get('jsonfile', None)
        json_text = request.params.get('jsontext', None)
        tutorial_start_page = request.params.get('startpage', None)

        if help_type is None:
            return "Problem saving help: no help type"

        if Stemformatics_Help.help_exists(help_name):
            if help_type == 'tutorial':
                Stemformatics_Help.delete_tutorial(help_name)
            else:
                Stemformatics_Help.delete_pageguide(help_name)

        if (help_name and (isinstance(json_file, cgi.FieldStorage) or json_text)):
            json_to_save = json_file.value if isinstance(json_file, cgi.FieldStorage) else json_text
            if help_type == "tutorial":
                Stemformatics_Help.save_tutorial(help_name, tutorial_start_page, json_to_save)
            elif help_type == "page_guide":
                Stemformatics_Help.save_pageguide(help_name, json_to_save)
            else:
                return "Problem saving help: help type incorrect"
        else:
            return "Problem saving help: incorrect data"

        if request.params.get('close') == 'false':
            if help_type == 'tutorial':
                redirect('/admin/edit_tutorial?name=' + help_name)
            else:
                redirect('/admin/edit_pageguide?page=' + help_name)
        else:
            redirect('/admin/help')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def delete_tutorial(self):
        Stemformatics_Help.delete_tutorial(request.params.get('name', None))
        redirect ('/admin/help')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def delete_pageguide(self):
        Stemformatics_Help.delete_pageguide(request.params.get('page', None))
        redirect ('/admin/help')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def download_help_dump(self):
        filepath = Stemformatics_Help.get_help_dump(self)
        filename = 'helpsystem.dump'
        file_size = os.path.getsize(filepath)
        headers = [('Content-Disposition', 'attachment; filename=\"' + filename + '\"'),
                   ('Content-Type', 'application/zip'),
                   ('Content-Length', str(file_size))]
        from paste.fileapp import FileApp
        fapp = FileApp(filepath, headers=headers)
        return fapp(request.environ, self.start_response)

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def upload_help_dump(self):
        help_file = request.params.get('helpdump', None)
        if help_file is None or not isinstance(help_file, cgi.FieldStorage):
            return "No file submitted"
        Stemformatics_Help.save_help_dump(self, help_file)
        redirect ('/admin/help')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def email_pending_users(self):
        user_ids  = request.params.get('user_ids')
        c.title = 'Email Pending Users'
        if user_ids is None:
            # choose group
            result = Stemformatics_Admin.all_users(db)
            c.user_status_dict = Stemformatics_Auth.user_status_dict()
            c.result = []
            for user in result:
                if user['status'] ==2:
                    c.result.append(user)

            group_ids=""
            c.group_ids = group_ids

            c.base_url = str(url('/admin/email_pending_users?choose=true'))
            # textarea to enter in email and/or list users to select
            return render('/admin/choose_user.mako')
        result_text = ""
        if user_ids != '':
            user_id_array = user_ids.split(',')
            for user_id in user_id_array:
                uid = int(user_id)
                object_type = 'User'
                object_id = str(uid)
                result_uid = Stemformatics_Auth.send_email_for_pending_user(db,uid)
                result_text += ","+str(uid)
        return "Sent email for uids" + result_text
        #redirect('/admin/email_pending_users')


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def view_add_group(self):
        group_name  = request.params.get('group_name')
        c.title = 'View/Add Group'
        if group_name is not None:
            result = Stemformatics_Auth.add_group(db,group_name)

        # choose group
        c.base_url = str(url('/admin/view_add_group?'))
        c.groups_dict = Stemformatics_Auth.get_all_group_names(db)
        return render('/admin/view_group.mako')


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def setup_bulk_import_manager(self):
        gene_mapping_raw_file_base_name = config['gene_mapping_raw_file_base_name']
        feature_mapping_raw_file_base_name = config['feature_mapping_raw_file_base_name']
        result = Stemformatics_Gene.setup_bulk_import_manager_mappings(gene_mapping_raw_file_base_name,feature_mapping_raw_file_base_name)
        return "Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def re_run_job(self):
        job_id   = int(request.params.get('job_id', ""))
        self.GPQueue = config['GPQueue']
        self.StemformaticsQueue = config['StemformaticsQueue']
        self.StemformaticsController = config['StemformaticsController']
        self.FullJavaPath = config['FullJavaPath']


        # call java code from command line
        command_line = "nice -n 15 " + self.FullJavaPath + " -jar "+ self.StemformaticsController +" " + str(job_id)+ " " + config['__file__']
        p = subprocess.Popen(command_line,shell=True)
        return command_line + "<br/>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def change_user_to_annotator_for_dataset(self): #CRITICAL-5 CRITICAL-4
        user_ids  = request.params.get('user_ids')
        ds_id  = request.params.get('datasetID')
        user_emails  = request.params.get('user_emails')

        if user_ids is None :
            # choose group
            c.result = Stemformatics_Admin.all_users(db)
            c.user_status_dict = Stemformatics_Auth.user_status_dict()
            c.group_ids = 0
            c.base_url = str(url('/admin/change_user_to_annotator_for_dataset?'))
            # textarea to enter in email and/or list users to select
            return render('/admin/choose_user.mako')

        if ds_id is None:
            c.species = None
            c.datasets = Stemformatics_Dataset.getAllDatasetDetails(db,c.uid)
            if user_ids is None:
                user_ids = ''
            c.url = str(url('/admin/change_user_to_annotator_for_dataset'))+'?user_ids='+str(user_ids)+'&user_emails='+user_emails
            c.breadcrumbs = []
            c.analysis = None
            return render('workbench/choose_dataset.mako')

        return_text = ""

        user_email_array = user_emails.split(',')
        for user_email in user_email_array:
            user_email = str(user_email)
            if len(user_email) != 0:
                result_user_email = Stemformatics_Auth.create_new_pending_user(db,user_email)
                if isinstance(result_user_email,str):
                    error_message = error_message + '\n' + user_email + ": " + result_user_email + " "
                else:
                    uid = result_user_email.uid
                    object_type = 'User'
                    object_id = str(uid)
                    text =Stemformatics_Auth.change_user_role_for_ds(db,ds_id,'User',object_id,'annotator')
                    return_text += "<br/>User " + str(object_id) + " " +text  + "<br/>"
                    temp = user_ids.split(',')
                    temp.append(object_id)
                    user_ids = ','.join(temp)


        for object_id in user_ids.split(','):
            if len(object_id) != 0:
                text =Stemformatics_Auth.change_user_role_for_ds(db,ds_id,'User',object_id,'annotator')
                return_text += "<br/>User " + str(object_id) + " " +text  + "<br/>"

                Stemformatics_Auth.triggers_for_change_in_user(db)

                uid = int(object_id)
                uid_result = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)
                uid_annotator_result = Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id,'annotator')

                result_user = Stemformatics_Auth.get_user_from_uid(db,uid)
                username = result_user.username
                return_text = return_text  + str(username)+"["+str(uid) + "]:" + str(uid_result) + " access to "+str(ds_id)+" -- Annotator access =>" + str(uid_annotator_result) + "<br/>"

                handle= Stemformatics_Dataset.getHandle(db,ds_id)
                external_base_url = url('/',qualified=True)
                return_text += "<br/><br/>"+h.create_letter_for_annotator(ds_id,uid,result_user,handle,external_base_url)


        return return_text +   "<br/><br/><br/>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"



    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def get_raw_twitter_response(self):
        force_refresh   = request.params.get('force_refresh', "true")

        if force_refresh == "false":
            force_refresh = False

        number = 3
        result = twitter.get_recent_tweets(number,force_refresh)
        tweets = result[0]
        last_call = result[1]

        try:
            del last_call['cookies']
            del last_call['content']
            del last_call['headers']
        except:
            pass

        return json.dumps(last_call)

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def delete_job_files(self):
        job_id   = int(request.params.get('job_id', ""))
        if job_id == 0:
            return "You have to set the job_id manually in the URL"

        self.GPQueue = config['GPQueue']
        self.StemformaticsQueue = config['StemformaticsQueue']
        job = Stemformatics_Job.get_job(db,job_id)
        output = ""
        # delete directory
        if job.reference_type == 'GenePattern':
            # delete Gene Pattern queue
            command = "rm -fR " + self.GPQueue + str(job.reference_id)
            p = subprocess.Popen(command,shell=True)
            output += command + " | "
        # delete stemformatics queue
        command = "rm -fR " + self.StemformaticsQueue + str(job.job_id)
        p = subprocess.Popen(command,shell=True)
        output += command + " | "

        return output




    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def create_letter_for_annotator(self):
        ds_id   = int(request.params.get('ds_id', ""))
        uid   = int(request.params.get('uid', ""))
        user =  Stemformatics_Auth.get_user_from_uid(db,uid)
        handle= Stemformatics_Dataset.getHandle(db,ds_id)
        external_base_url = url('/',qualified=True)
        text = h.create_letter_for_annotator(ds_id,uid,user,handle,external_base_url)
        return text

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def add_line_graph(self):
        ds_id = int(request.params.get('ds_id', ""))
        if ds_id == 0:
            return "You have to set the ds_id manually in the URL"

        output = ""

        Stemformatics_Dataset.add_metadata_for_line_graph(ds_id)

        check_url = str(url('/admin/annotate_dataset?ds_id='+str(ds_id)))

        output = " You can check that the metadata was added here: <a href="+check_url+">Link</a>"
        return output



    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def add_msc_project(self):
        ds_id = int(request.params.get('ds_id', ""))
        if ds_id == 0:
            return "You have to set the ds_id manually in the URL"

        output = ""

        Stemformatics_Dataset.add_metadata_for_msc_project(ds_id)

        check_url = str(url('/admin/annotate_dataset?ds_id='+str(ds_id)))

        output = " You can check that the metadata was added here: <a href="+check_url+">Link</a>"
        return output


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def add_project_banner(self):
        ds_id = int(request.params.get('ds_id', ""))
        if ds_id == 0:
            return "You have to set the ds_id manually in the URL"

        output = ""
        metadata_name = 'project'
        default_value = ''
        Stemformatics_Dataset.add_dataset_metadata(ds_id,metadata_name,default_value)

        check_url = str(url('/admin/annotate_dataset?ds_id='+str(ds_id)))

        output = " You can check that the metadata was added here: <a href="+check_url+">Link</a>"
        return output



    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def view_resident_memory(self):
        import socket
        hostname = socket.gethostname()
        cmd = "ps aux | grep paster | grep -v grep | grep -v defunct | awk -v host_name="+hostname+" '{ print \"Pylons/Paster resident memory on \" host_name \" is \" int($6 / 1024) \"MB\"; }'"


        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read()

        return cmd + "<br><br>" + output.replace("\n","<br/>") + "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def run_regression_nosetests(self):
        import socket
        hostname = socket.gethostname()
        cmd = config['regression_nosetests_script']

        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read()

        return cmd + "<br><br>" + output.replace("\n","<br/>") + "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def login_as_user(self):
        uid = request.params.get('uid')
        if uid is None:
            redirect('/admin/all_users')
        else:
            uid = int(uid)
            user = Stemformatics_Auth.get_user_from_uid(db,uid)
            #Mark user as logged in
            session['user'] = user.username
            session['uid'] = user.uid
            session['full_name'] = user.full_name
            session['role'] = Stemformatics_Auth.get_user_role(db,user.uid)
            session.save()
            redirect('/')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def refresh_base_export_keys(self):
        result = Stemformatics_Auth.return_all_active_users(db)
        for user in result:
            Stemformatics_Auth.create_base_export_key(user['uid'])

        return "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def refresh_probe_mappings_to_download(self):
        result = Stemformatics_Dataset.refresh_probe_mappings_to_download()
        result = result.replace("\n","<br/>")

        return "<br><br>" + result + "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def config_index(self):
        c.configs = Stemformatics_Admin.get_all_configs()
        return render('admin/config_index.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def edit_config(self):
        ref_type = request.params.get('ref_type')
        ref_id = request.params.get('ref_id')
        result = Stemformatics_Admin.edit_config(ref_type,ref_id)
        if result == True:
            Stemformatics_Admin.trigger_update_configs()
            return 'Success in editing config '+ref_type
        else:
            redirect(url(controller='contents', action='index'), code=404)

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def audit_reports(self):
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        limit = request.params.get('limit')

        if limit is not None:
            start_date = str(start_date)
            end_date = str(end_date)
            limit = int(limit)
        else:
            diff = timedelta(days=30)
            temp_start_date = date.today() - diff
            start_date = temp_start_date.isoformat()
            end_date = date.today().isoformat()
            limit = 20

        c.result = {}
        c.result['user'] = Stemformatics_Audit.get_user_statistics(start_date,end_date,limit)
        c.result['dataset'] = Stemformatics_Audit.get_dataset_statistics(start_date,end_date,limit)
        c.result['dataset_user'] = Stemformatics_Audit.get_dataset_user_statistics(start_date,end_date,limit)
        c.result['gene'] = Stemformatics_Audit.get_gene_statistics(start_date,end_date,limit)
        c.result['controller'] = Stemformatics_Audit.get_controller_statistics(start_date,end_date,limit)
        c.result['controller_user'] = Stemformatics_Audit.get_controller_user_statistics(start_date,end_date,limit)

        c.start_date = start_date
        c.end_date = end_date
        c.limit = limit

        return render('admin/audit_reports.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def controller_user_audit_report(self):
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        limit = request.params.get('limit')

        if limit is not None:
            start_date = str(start_date)
            end_date = str(end_date)
            limit = int(limit)
        else:
            diff = timedelta(days=30)
            temp_start_date = date.today() - diff
            start_date = temp_start_date.isoformat()
            end_date = date.today().isoformat()
            limit = 10

        c.result = {}
        c.result['controller_user'] = Stemformatics_Audit.get_controller_user_statistics(start_date,end_date,limit)

        c.start_date = start_date
        c.end_date = end_date
        c.limit = limit

        return render('admin/controller_user_audit_report.mako')



    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def check_error_response(self):
        x = int('a')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def trigger_config_update(self):
        Stemformatics_Admin.trigger_update_configs()
        return "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def redis_check(self):

        result = Stemformatics_Dataset.redis_check()
        c.ok_list = result['ok_list']
        c.problem_list = result['problem_list']
        c.result_dict = result['result_dict']
        return render('admin/redis_check.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def check_redis_consistency_for_datasets(self):
        try:
            days = int(request.params.get('days'))
        except:
            days = config["sync_dataset_redis_after_x_days"]

        try:
            num_of_datasets = request.params.get('num_of_datasets') # checks for all the datasets
        except:
            num_of_datasets = "new" # this checks only for datasets that has been setup using setup_new_dataset_in_redis using audit_log table

        try:
            reset_redis_required = request.params.get('reset')
        except:
            reset_redis_required = 'no'

        return_str = Stemformatics_Expression.check_redis_consistency_for_datasets(days,num_of_datasets,reset_redis_required,db)

        return return_str

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def delete_dataset(self,id):
        try:
            ds_id = int(id)
        except:
            return "Error with this. Must be an integer"

        if ds_id == 0:
            return "Error with the dataset id. Cannot be 0"
        # unload dataset
        try:
            redis_result = Stemformatics_Dataset.delete_dataset_redis(ds_id)
            file_result = Stemformatics_Dataset.delete_dataset_files_from_disk(ds_id)
            database_result = Stemformatics_Dataset.delete_dataset_from_database(ds_id)

            # create audit
            audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
            result = Stemformatics_Audit.add_audit_log(audit_dict)
        except:
            return "Error in deleting data"
        return "For dataset "+ str(ds_id) + "</br>" + file_result + "</br>" + database_result + "</br>" + redis_result


    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def set_users_to_inactive(self):
        string_of_usernames = request.params.get('string_of_usernames')
        c.string_of_usernames = string_of_usernames


        if string_of_usernames is not None:
            result = Stemformatics_Auth.set_users_to_be_inactive_from_usernames(string_of_usernames)
            c.result = result
        else:
            c.result = []

        return render('admin/set_users_to_inactive.mako')

    @Stemformatics_Auth.authorise(db)
    #---------------------NOT MIGRATED--------------------------------
    def unsubscribe_users_from_outage_critical_notifications(self):
        string_of_usernames = request.params.get('string_of_usernames')
        c.string_of_usernames = string_of_usernames


        if string_of_usernames is not None:
            result = Stemformatics_Auth.unsubscribe_users_from_outage_critical_notifications(string_of_usernames)
            c.result = result
        else:
            c.result = []

        return render('admin/unsubscribe_users_from_outage_critical_notifications.mako')
