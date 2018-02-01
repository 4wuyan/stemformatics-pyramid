#import logging,codecs,json,math,re,smtplib,os,subprocess
#
#from pylons import request, response, session, url, tmpl_context as c,config, app_globals as g
#from pylons.controllers.util import abort, redirect
#
from S4M_pyramid.lib.base import BaseController
#from guide.model.stemformatics import *
#from guide.controllers.workbench import WorkbenchController
#import guide.lib.helpers as h
#
#from sqlalchemy import or_, and_, desc
#from sqlalchemy.exceptions import *
#
#from paste.deploy.converters import asbool
#from datetime import datetime, timedelta
#
#log = logging.getLogger(__name__)
#connection = db.engine.connect()

class tempData(object):
    pass

class ApiController(BaseController):
    __name__ = 'ApiController'

    #---------------------NOT MIGRATED--------------------------------
    def __before__(self):  #CRITICAL-3 #CRITICAL-4 #TODO-2

        super(ApiController, self).__before__ ()
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db
        self._temp = tempData()
        self.default_human_dataset = int(config['default_human_dataset'])
        self.default_mouse_dataset = int(config['default_mouse_dataset'])
        self.useSqlSoup = True

        if 'useSqlSoup' in config:
            self.useSqlSoup = asbool(config['useSqlSoup'])

        # GenePattern modules
        self.GPQueue = config['GPQueue']
        self.StemformaticsQueue = config['StemformaticsQueue']
        self.StemformaticsController = config['StemformaticsController']
        self.GeneSetFiles = config['GeneSetFiles']
        self.DatasetGCTFiles = config['DatasetGCTFiles']
        self.analysis_by_name = Stemformatics_Job.return_all_analysis_by_name()



    #---------------------NOT MIGRATED--------------------------------
    def _copy_over_full_gct_file(self):
        # copy over dataset to job.gct
        datasetGCTFile = config['DatasetGCTFiles']+"dataset"+str(self._temp.ds_id)+".gct"
        command = "cp "+datasetGCTFile+ " " +self._temp.gct_filename
        p = subprocess.call(command,shell=True)

        # This is for User Defined Expression Profile, where a user chooses the expression profile for the sample types
        if 'expression_values' in self._temp.options:
            expression_values = self._temp.options['expression_values']
            gct_row_text = self._temp.probe_id + "\t"+"na"
            for sample in self._temp.sample_labels:
                chip_id = sample
                metaDataValues = g.all_sample_metadata[self._temp.chip_type][chip_id][self._temp.ds_id]
                sample_type = metaDataValues['Sample Type']

                expression_value = float(expression_values[sample_type])
                gct_row_text += "\t" + str(expression_value)

            gct_row_text += "\n"
            with open(self._temp.gct_filename,"a") as myfile: myfile.write(gct_row_text)
            command = "PROBES=`sed -n 2p "+self._temp.gct_filename+"| cut -f1 `; NEWPROBES=`expr $PROBES + 1`;sed 2s/$PROBES/$NEWPROBES/ -i "+self._temp.gct_filename
            p = subprocess.call(command,shell=True)
            return True
    # api create for RDS Monitoring of when we moved the HC processing to Galaxy
    #---------------------NOT MIGRATED--------------------------------
    def get_hc_stats(self):
        start_date  = request.params.get('start_date')
        end_date  = request.params.get('end_date')

        hc_stats = Stemformatics_Galaxy.get_hc_stats_from_s4m_db(start_date,end_date)
        hc_stats_json = json.dumps(hc_stats)
        return hc_stats_json

    #---------------------NOT MIGRATED--------------------------------
    def gene_pattern_download(self,id): #CRITICAL-4
        # getting all of these from the database
        self._temp.job_id = int(id)
        result = Stemformatics_Job.get_job_details_with_gene_set(db,self._temp.job_id)

        if result is None:
            redirect(url(controller='contents', action='index'), code=404)

        self._temp.ds_id = result.dataset_id
        self._temp.uid = result.uid
        self._temp.analysis = result.analysis
        self._temp.gene_set_id= result.gene_set_id
        self._temp.use_cls = result.use_cls
        self._temp.use_gct = result.use_gct
        self._temp.comparison_type = result.comparison_type
        self._temp.gene = result.gene
        self._temp.probe_id = result.probe
        self._temp.delimiter = config['redis_delimiter']
        try:
            self._temp.options = json.loads(result.options)
        except:
            self._temp.options = {}

        # create directory
        self._temp.base_path = self.StemformaticsQueue + str(self._temp.job_id) + '/'
        self._temp.ini_filename = self._temp.base_path + 'job.ini'
        self._temp.gct_filename = self._temp.base_path + 'job.gct'
        self._temp.cls_filename = self._temp.base_path + 'job.cls'

        if not os.path.exists(self._temp.base_path):
            os.mkdir(self._temp.base_path)
        # create gct file (if applicable)
        if self._temp.use_gct:
            self._temp.sample_labels = Stemformatics_Expression.get_sample_labels(self._temp.ds_id)
            self._temp.chip_type = Stemformatics_Dataset.getChipType(db,self._temp.ds_id)

            # all analysis that use a gct file except gene neighbourhood and UDEP will need a gct built
            if (self._temp.analysis == self.analysis_by_name['Gene Neighbourhood']['analysis_id'] or
                self._temp.analysis == self.analysis_by_name['User Defined Expression Profile']['analysis_id']):
                self._copy_over_full_gct_file()
            else:
                # checking if select_probes_override gene_set_id
                if 'select_probes' in self._temp.options and self._temp.options['select_probes'] != "":
                    ref_type = 'probes'
                    ref_id = self._temp.options['select_probes']
                else:
                    ref_type = 'gene_set_id'
                    ref_id = str(self._temp.gene_set_id)
                ds_id = self._temp.ds_id
                uid = self._temp.uid
                options = self._temp.options
                text = Stemformatics_Dataset.build_gct_from_redis(db,ref_type,ref_id,ds_id,uid,options)
                Stemformatics_Dataset.write_gct_file(text,self._temp.gct_filename)

        # create cls file (if applicable)
        if self._temp.use_cls:
            # if this is only sample type
            if comparison_type != "Sample Type":
                extra_name = comparison_type.replace(" ","_")
            else:
                extra_name = ""

            # copy over dataset to job.cls
            datasetCLSFile = config['DatasetCLSFiles']+str(self._temp.ds_id)+extra_name+".cls"
            command = "cp "+datasetCLSFile+ " " +cls_filename
            p = subprocess.Popen(command,shell=True)

    # This fetch all the pending jobs from s4m and updates them based on galaxy job status
    #---------------------NOT MIGRATED--------------------------------
    def get_galaxy_pending_jobs(self):
        import socket
        server_name = socket.gethostname()
        pending_jobs = Stemformatics_Job.get_pending_jobs_in_s4m()
        from guide.model.stemformatics.stemformatics_galaxy import Stemformatics_Galaxy
        galaxyInstance = Stemformatics_Galaxy.connect_to_galaxy()
        # check for galaxy status for pending jobs
        pending_job_list = {}
        for job in pending_jobs:
            job_id = job[0]
            analysis = job[1]
            options = job[16]
            if 'galaxy_server_url' in options: # checks if job is created on galaxy
                pending_job_list[job_id] = analysis

        status = Stemformatics_Galaxy.return_job_status(galaxyInstance,pending_job_list,server_name)
        # update jobs based on galaxy status
        Stemformatics_Galaxy.update_job_status(db,status,galaxyInstance)


    #---------------------NOT MIGRATED--------------------------------
    def update_job(self,id): #CRITICAL-4
        job_id = int(id)

        # 0 is for running, 1 is for success
        status  = request.params.get('status')

        # eg. GenePattern and GP job#
        reference_type  = request.params.get('reference_type')
        reference_id  = request.params.get('reference_id')

        job_details = {}

        if status is not None:
            job_details['status'] = status
            if status == '1':
                job_details['finished'] = datetime.now()

        if reference_type is not None:
            job_details['reference_type'] = reference_type
            job_details['reference_id'] = reference_id

        if job_details != {}:
            # raise Error
            result = Stemformatics_Job.update_job(db,job_id,job_details)

            if result is not True:
                return "error"
            else:
                if status == '1':
                    # send email
                    user = Stemformatics_Job.get_user_from_job_id(db,job_id)

                    if user.send_email_job_notifications:

                        from_email = config['from_email']
                        to_email = user.username
                        subject = c.site_name+" - Job completion #%s" % (str(job_id))


                        #external_base_url = 'http://'+config['external_base_url_for_api_controller']+'/'

                        job_details =  Stemformatics_Job.get_job_details(db,job_id)
                        job_options = json.loads(job_details.options)
                        external_base_url = job_options['base_url']
                        new_url = external_base_url+'workbench/job_view_result/'+str(job_id)



                        body = "Congratulations, your job #%s has been completed, you have 30 days until it expires and is removed from the system.\n\n Click here to view result: %s \n\n To stop receiving these emails click here: %s" % (str(job_id),new_url,external_base_url+url('auth/unsubscribe_job_notification/'+str(user.uid)+'_'+Stemformatics_Auth.get_secret_unsubscribe_sha1(str(user.uid)) )

                        # raise Error
                        # Send the message via our own SMTP server, but don't include the
                        # envelope header.
                        success = Stemformatics_Notification.send_email(from_email,to_email,subject,body)

                    return "success"
                if status == '2':
                    import socket
                    hostname = socket.gethostname()
                    # send email
                    user = Stemformatics_Job.get_user_from_job_id(db,job_id)

                    from_email = config['from_email']
                    to_email = config['email_to']
                    subject = c.site_name+" - Job Error #%s on %s" % (str(job_id),hostname)


                    #external_base_url = 'http://'+config['external_base_url_for_api_controller']+'/'

                    body = "Job #%s has an error (possibly stderr.txt) and cannot be completed. Please check %s Server is working." % (str(job_id),reference_type)

                    # Send the message via our own SMTP server, but don't include the
                    # envelope header.
                    success = Stemformatics_Notification.send_email(from_email,to_email,subject,body)


                    if user.send_email_job_notifications:

                        from_email = config['from_email']
                        to_email = user.username
                        subject = c.site_name+" - Job Error #%s" % (str(job_id))


                        #external_base_url = 'http://'+config['external_base_url_for_api_controller']+'/'

                        job_details =  Stemformatics_Job.get_job_details(db,job_id)
                        job_options = json.loads(job_details.options)
                        external_base_url = job_options['base_url']
                        new_url = external_base_url+'workbench/job_view_result/'+str(job_id)



                        body = "Unfortunately, your job #%s has an error and cannot be completed. We have been notified of this email and will get back to you soon.\n\nApologies for the inconvenience,\n\nThe %s Team" % (str(job_id),c.site_name)

                        # raise Error
                        # Send the message via our own SMTP server, but don't include the
                        # envelope header.
                        success = Stemformatics_Notification.send_email(from_email,to_email,subject,body)
                    return "success"

        else:
            return "error"

    #---------------------NOT MIGRATED--------------------------------
    def gene_set_annotation_job(self,id):  #CRITICAL-4

        job_id = int(id)
        result = Stemformatics_Job.get_job_details_with_gene_set(db,job_id)

        if result is None:
            redirect(url(controller='contents', action='index'), code=404)

        dataset_id  = result.dataset_id
        uid = result.uid
        analysis = result.analysis
        gene_set_id= result.gene_set_id
        use_cls = result.use_cls
        use_gct = result.use_gct
        comparison_type = result.comparison_type


        # get list of genes so we can get the db_id too
        result = Stemformatics_Gene_Set.getGeneSetData(db,uid,gene_set_id)
        raw_genes = result[1]

        # expecting at least one gene in the gene set
        db_id = raw_genes[0].db_id

        # create directory
        base_path = self.StemformaticsQueue + str(job_id) + '/'
        ini_filename = base_path + 'job.ini'
        main_filename = base_path + 'job.tsv'
        gene_pathways_filename = base_path + 'pathways.tsv'
        f_gene_sets = self.GeneSetFiles + 'db_id_'+str(db_id)+'_all_genes.tsv'
        gene_pathways_export = base_path + 'pathway_export.tsv'

        if not os.path.exists(base_path):
            os.mkdir(base_path)


        # now use the list of genes
        genes_in_gene_set_count = len(raw_genes)

        genes = []
        dict_gene_names = {}
        for gene_row in raw_genes:
            genes.append(gene_row.gene_id)
            dict_gene_names[gene_row.gene_id] = gene_row.associated_gene_name

        tx_dict = Stemformatics_Transcript.get_transcript_annotations(db,db_id,genes)

        # write the main job data file
        result = Stemformatics_Job.write_transcript_data_gene_set_annotation(db,main_filename,tx_dict)

        # read the gene sets large file to go through and work out the pathways this gene set is for
        gene_list = Stemformatics_Gene_Set.read_db_all_genes(f_gene_sets,genes)

        # write to file gene centric list of pathways that touch this gene set - returns dict_pathway and gene pathways list
        result = Stemformatics_Job.write_gene_pathways_gene_set_annotation(gene_pathways_filename,gene_list,dict_gene_names)

        dict_pathway = result[0]
        gene_pathways_list = result[1]

        public_uid = 0
        gene_set_details = Stemformatics_Gene_Set.get_gene_set_details(db,public_uid,gene_pathways_list)

        total_number_genes = Stemformatics_Gene.get_total_number_genes(db,db_id)

        gene_set_counts = Stemformatics_Gene_Set.get_gene_set_counts(db,public_uid,gene_pathways_list)

        dict_gene_set_details = {}
        for gene_set in gene_set_details:
            dict_gene_set_details[str(gene_set.id)] = gene_set


        # show export for gene pathways
        result = Stemformatics_Job.write_gene_pathways_export_gene_set_annotation(gene_pathways_export,dict_pathway,dict_gene_set_details,gene_set_counts,genes_in_gene_set_count,total_number_genes)


    #---------------------NOT MIGRATED--------------------------------
    def kill_pending_jobs(self):
        result = Stemformatics_Job.get_pending_jobs(db)
        kill_job_pending_hours = int(config['kill_job_pending_hours'])

        for job in result:

            delta_hours = timedelta(hours=kill_job_pending_hours)

            cutoff_time = job.created + delta_hours

            if cutoff_time < datetime.now():
                job_details = {}

                job_details['status'] = 2 # Job Failed

                # check if genepattern or galaxy
                if 'galaxy_server_url' in job.options:
                    server_used = 'Galaxy'
                else:
                    server_used = 'GenePattern'

                user = Stemformatics_Job.get_user_from_job_id(db,job.job_id)

                import socket
                hostname = socket.gethostname()

                from_email = config['from_email']
                to_email = config['email_to']
                subject = c.site_name+" - Job #%s was pending and will be cancelled on %s" % (str(job.job_id),hostname)

                body = "Job #%s was pending and will be cancelled via kill_pending_jobs. Please check %s Server is working." % (str(job.job_id),server_used)

                # Send the message via our own SMTP server, but don't include the
                # envelope header.
                success = Stemformatics_Notification.send_email(from_email,to_email,subject,body)


                result = Stemformatics_Job.update_job(db,job.job_id,job_details)
                grep_string = self.StemformaticsController +" " + str(job.job_id)
                command = "kill -9 `ps aux | grep \""+grep_string+"\" | awk '{print $2}'`"
                p = subprocess.Popen(command,shell=True)


    #---------------------NOT MIGRATED--------------------------------
    def remove_old_jobs(self):

        remove_old_job_days = int(config['remove_old_job_days'])
        delta_days = timedelta(days=remove_old_job_days)
        before_cutoff_time = datetime.now() - delta_days

        jobs = Stemformatics_Job.get_old_jobs(db,before_cutoff_time)

        Stemformatics_Job.bulk_delete_job(jobs)

    # This fetch all the old galaxy jobs and deletes the output files for those jobs on galaxy to free up disk space
    #---------------------NOT MIGRATED--------------------------------
    def remove_galaxy_old_jobs(self):
        remove_old_job_days = int(config['remove_old_job_days'])
        delta_days = timedelta(days=remove_old_job_days)
        before_cutoff_time = datetime.now() - delta_days

        jobs = Stemformatics_Job.get_old_jobs(db,before_cutoff_time)
        job_list = []
        for job in jobs:
            # checks if it is galaxy job and create list
            job_id = job[0]
            options = job[16]
            if 'galaxy_server_url' in options: # checks if job is created on galaxy
                job_list.append(job_id)

        from guide.model.stemformatics.stemformatics_galaxy import Stemformatics_Galaxy
        galaxyInstance = Stemformatics_Galaxy.connect_to_galaxy()
        import socket
        server_name = socket.gethostname()
        Stemformatics_Galaxy.delete_bulk_jobs(galaxyInstance, job_list, server_name)



    #---------------------NOT MIGRATED--------------------------------
    def remind_users_of_expiring_jobs(self):

        job_reminder_days = int(config['remove_old_job_days']) - 7
        delta_days = timedelta(days=job_reminder_days)
        reminder_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - delta_days

        result = Stemformatics_Job.get_jobs_created_between(db, reminder_date, (reminder_date + timedelta(days=1)))

        for job in result:
            user = Stemformatics_Job.get_user_from_job_id(db,job.job_id)

            if user.send_email_job_notifications:

                from_email = config['from_email']
                to_email = user.username
                subject = c.site_name+" - Job Expiry #%s" % (str(job.job_id))

                external_base_url = 'http://'+config['external_base_url_for_api_controller']+'/'

                job_url = external_base_url+url('workbench/job_view_result/'+str(job.job_id))
                unsubscribe_url = external_base_url+url('auth/unsubscribe_job_notification/'+str(user.uid))

                body = "Your job #%s is about to expire, you have 7 days until it will be removed from the system.\n\n Click here to view your job: %s \n\n To stop receiving these emails click here: %s" % (str(job.job_id), job_url, unsubscribe_url)

                Stemformatics_Notification.send_email(from_email, to_email, subject, body)


    #---------------------NOT MIGRATED--------------------------------
    def biosamples_metadata_unique(self):
        #if ds_id is not None:
        #    ds_id = int(ds_id)
        #bs_result = Stemformatics_Dataset.getBiosamplesMetadata(db,ds_id)
        bs_result = Stemformatics_Dataset.getBiosamplesMetadata(db)
        bs_result_uniq = []
        [bs_result_uniq.append(i) for i in bs_result if not bs_result_uniq.count(i)]
        return json.dumps(bs_result_uniq)


    #---------------------NOT MIGRATED--------------------------------
    def dataset_metadata_unique(self):
        ds_result = Stemformatics_Dataset.getDatasetMetadata(db)
        ds_result_uniq = []
        [ds_result_uniq.append(i) for i in ds_result if not ds_result_uniq.count(i)]
        return json.dumps(ds_result_uniq)


    #---------------------NOT MIGRATED--------------------------------
    def dataset_metadata_for_annotations(self,id):

        try:
            ds_id = int(id)
        except:
            return "Error with the dataset id"

        ds_result = Stemformatics_Dataset.getDatasetMetadata(db,ds_id)

        handle = ds_result[0]['ds_value']

        mapping_for_metastore = Stemformatics_Dataset.get_metastore_mappings()

        del response.headers['Cache-Control']
        del response.headers['Pragma']
        response.headers['Content-type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'filename=METASTORE'+str(ds_id)+'_'+handle
        response.charset= "utf8"
        data = ""
        for item in ds_result:
            ds_name = item['ds_name']

            if ds_name in mapping_for_metastore:
                ds_name = mapping_for_metastore[ds_name]

            data += ds_name+ "=" + item['ds_value']+ "\n"
        return data



    #---------------------NOT MIGRATED--------------------------------
    def biosamples_metadata_for_annotations(self,id):

        try:
            ds_id = int(id)
        except:
            return "Error with the dataset id"

        bs_result = Stemformatics_Dataset.getBiosamplesMetadata(db,ds_id)
        chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
        handle = Stemformatics_Dataset.getHandle(db,ds_id)

        del response.headers['Cache-Control']
        del response.headers['Pragma']
        response.headers['Content-type'] = 'text/tab-separated-values'
        response.headers['Content-Disposition'] = 'filename=biosamples_metadata_'+str(ds_id)+'_'+handle+'.txt.tsv'
        response.charset= "utf8"
        data = ""
        for item in bs_result:
            data += str(ds_id)+"\t"+str(chip_type)+"\t"+item['chip_id']+ "\t" +item['md_name']+ "\t" + item['md_value']+ "\n"

        return data



    #---------------------NOT MIGRATED--------------------------------
    def biosamples_metadata_summary_for_annotations(self,id):

        try:
            ds_id = int(id)
        except:
            return "Error with the dataset id"

        bs_result = Stemformatics_Dataset.getBiosamplesMetadata(db,ds_id)

        handle = Stemformatics_Dataset.getHandle(db,ds_id)

        del response.headers['Cache-Control']
        del response.headers['Pragma']
        response.headers['Content-type'] = 'text/tab-separated-values'
        response.headers['Content-Disposition'] = 'filename=biosamples_annotation_summary_'+str(ds_id)+'_'+handle+'.tsv'
        response.charset= "utf8"

        breakdown = {}

        for item in bs_result:
            md_name = item['md_name']
            md_value = item['md_value']

            if md_name not in breakdown:
                breakdown[md_name] = {}

            if md_value not in breakdown[md_name]:
                breakdown[md_name][md_value] = 1
            else:
                breakdown[md_name][md_value] += 1

        data = ""
        for md_name_item in breakdown:
            for md_value_item in breakdown[md_name_item]:
                data += md_name_item + "\t" + md_value_item + "\t" + str(breakdown[md_name_item][md_value_item]) + "\n"

        return data


    #---------------------NOT MIGRATED--------------------------------
    def get_dataset_list(self):

        result = Stemformatics_Dataset.get_all_dataset_ids(db)
        ds_id = None
        uid = 'admin'
        metadata = Stemformatics_Dataset.getAllDatasetDetails(db,uid,True)

        return json.dumps(metadata)


    #---------------------NOT MIGRATED--------------------------------
    def usage_statistics(self,id):

        delta = int(id)

        delta_days = timedelta(days=delta)
        from_date = datetime.now() - delta_days

        new_user_result = Stemformatics_Auth.return_new_users(db,from_date)

        # new_user_data = [ (user.username, user.full_name, user.organisation, user.created) for user in new_user_result]


        new_jobs_result = Stemformatics_Job.get_new_jobs(db,from_date)

        analysis = Stemformatics_Job.return_all_analysis()
        statuses = Stemformatics_Job.return_all_status()

        jobs_by_user = {}
        jobs_by_analysis = {}

        for job in new_jobs_result:
            if job.username not in jobs_by_user:
                jobs_by_user[job.username] = 1
            else:
                jobs_by_user[job.username] = jobs_by_user[job.username] + 1


            analysis_name = analysis[job.analysis]['name']

            if analysis_name not in jobs_by_analysis:
                jobs_by_analysis[analysis_name] = 1
            else:
                jobs_by_analysis[analysis_name] = jobs_by_analysis[analysis_name] + 1

        number_of_active_users = Stemformatics_Auth.get_number_of_active_users()

        public_samples_dict = Stemformatics_Dataset.get_number_public_samples(db)
        private_samples_dict = Stemformatics_Dataset.get_number_private_samples(db)

        number_of_public_datasets = Stemformatics_Dataset.get_number_of_datasets(db)



        body = "<h3>"+str(number_of_active_users)+" users active</h3>"
        body += "<h3>"+str(number_of_public_datasets['Public'])+" public datasets</h3>"
        body += "<h3>"+str(number_of_public_datasets['Private'])+" private datasets</h3>"

        body += "<h3>"+str(public_samples_dict['Human'])+" public human samples</h3>"
        body += "<h3>"+str(public_samples_dict['Mouse'])+" public mouse samples</h3>"

        body += "<h3>"+str(private_samples_dict['Human'])+" private human samples</h3>"
        body += "<h3>"+str(private_samples_dict['Mouse'])+" private mouse samples</h3>"

        body += "<h3>"+str(len(new_user_result))+" users created in the last "+str(delta)+" days</h3>"
        body +="<table class=breakdown><tr><th>Username</th><th>Full Name</th><th>Organisation</th><th>Created</th></tr>"
        for user in new_user_result:
            body += "<tr><td>"+user.username + "</td><td>" + unicode(user.full_name) + "</td><td>" + unicode(user.organisation) + "</td><td>" + unicode(user.created) + "</td></tr>"
        body +="</table>"
        body += "<h3>"+str(len(new_jobs_result))+" jobs run in the last "+str(delta)+" days</h3>"
        body += "<h3>Job breakdown by user</h3>"
        body +="<table class=breakdown><tr><th>Username</th><th>Jobs for this username</th></tr>"
        for username in jobs_by_user:
            body += "<tr><td>"+unicode(username) + "</td><td>" + unicode(jobs_by_user[username]) + "</td></tr>"
        body +="</table>"

        body += "<h3>Job breakdown by analysis</h3>"
        body +="<table class=breakdown><tr><th>Analysis</th><th>Jobs by Analysis</th></tr>"
        for name in jobs_by_analysis:
            body += "<tr><td>"+name + "</td><td>" + unicode(jobs_by_analysis[name]) + "</td></tr>"
        body +="</table>"


        return body

    #---------------------NOT MIGRATED--------------------------------
    def trigger_config_update(self):
        Stemformatics_Admin.trigger_update_configs()
        return "<br><br>Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"

    ''' This is to add one new dataset '''
    #---------------------NOT MIGRATED--------------------------------
    def setup_new_dataset(self,id):
        ds_id = int(id)
        show_text = Stemformatics_Dataset.setup_new_dataset(db,ds_id)
        return show_text

    #---------------------NOT MIGRATED--------------------------------
    def triggers_users_and_datasets(self):
        Stemformatics_Dataset.triggers_for_change_in_dataset(db)
        Stemformatics_Auth.triggers_for_change_in_user(db)
        g.all_sample_metadata = Stemformatics_Expression.setup_all_sample_metadata()
        return "Done! <a href='"+url('/admin/index')+"'>Now click to go back</a>"



    #---------------------NOT MIGRATED--------------------------------
    def setup_bulk_import_manager(self):
        gene_mapping_raw_file_base_name = config['gene_mapping_raw_file_base_name']
        feature_mapping_raw_file_base_name = config['feature_mapping_raw_file_base_name']
        result = Stemformatics_Gene.setup_bulk_import_manager_mappings(gene_mapping_raw_file_base_name,feature_mapping_raw_file_base_name)
        return "Done"

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
