from pyramid_handlers import action
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Auth, Stemformatics_Dataset, Stemformatics_Gene, Stemformatics_Audit, Stemformatics_Expression, Stemformatics_Gene_Set,Stemformatics_Probe,Stemformatics_Job,Stemformatics_Galaxy, db_deprecated_pylons_orm as db
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, app_globals as g, config
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
import json
import formencode.validators as fe
import re
from pyramid.renderers import render_to_response
from asbool import asbool
import S4M_pyramid.lib.helpers as h
import os
import subprocess

class WorkbenchController(BaseController):

    # 'sca' is short for scatter.  Makes validity checking easier.
    _graphTypes = {'sca': 'scatter', 'bar': 'bar', 'box': 'box', 'default': 'scatter'}


    def __init__(self,request): #CRITICAL-3
        super().__init__(request)
        c = self.request.c
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db


        self.default_human_dataset = int(config['default_human_dataset'])
        self.default_mouse_dataset = int(config['default_mouse_dataset'])

        # GenePattern modules
        #self.GPQueue = config['GPQueue']
        #self.StemformaticsQueue = config['StemformaticsQueue']
        #self.StemformaticsController = config['StemformaticsController']
        #self.FullJavaPath = config['FullJavaPath']

    @action(renderer = 'templates/workbench/index.mako')
    def index(self):
        c = self.request.c
        c.title = c.site_name+' Analyses - Home'
        return self.deprecated_pylons_data_for_view


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_upload(self):

        c.title = c.site_name+' Analyses - Upload New Gene List'
        c.gene_set_id = None
        posted  = request.params.get('posted')
        gene_set_name  = request.params.get('gene_set_name')
        db_id = request.params.get('db_id')
        search_type = request.params.get('search_type')

        if search_type is None:
            search_type = 'all'

        c.search_type = search_type

        if posted == None:
            c.error_message = ""
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],['','Upload New Gene List']]
            return render('workbench/gene_set_upload.mako')

        myfile = request.POST['gene_set_file']

        if gene_set_name == '':
            c.error_message = "You must provide a gene list name."
            return render('workbench/gene_set_upload.mako')

        if myfile == '':
            c.error_message = "Error in uploading the file."
            return render('workbench/gene_set_upload.mako')

        if db_id is None:
            c.error_message = "Error in choosing species."
            return render('workbench/gene_set_upload.mako')


        geneSetRaw = myfile.value

        m = re.findall('[\w\.\-\@]{1,}',geneSetRaw)

        # now input this list into a gene function that will return a dictionary
        # { 'ILMN_2174394' : { 'original' : 'ILMN_2174394', 'symbol' : 'STAT1', 'status' : 'OK' } }
        # If we make it a list of objects then we can sort, we cannot sort on a dictionary
        select_all_ambiguous = False
        c.select_all_ambiguous = select_all_ambiguous
        resultData = Stemformatics_Gene.get_unique_gene_fast(db,m,db_id,search_type,select_all_ambiguous)
        c.gene_set_raw = geneSetRaw
        c.gene_set_raw_list = m
        c.gene_set_name = gene_set_name
        c.gene_set_processed = resultData
        c.db_id = db_id
        c.error_message = ""
        c.hide_save = False
        c.search_type = search_type
        # return 'Successfully uploaded: %s, size: %i rows' % (myfile.filename, len(m))
        c.title = c.site_name+' Analyses  - New Gene List'
        c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/gene_set_upload'),'Upload New Gene List'],['','Bulk Import Manager']]
        c.description = ''
        return render('workbench/gene_set_manage_bulk_import.mako')


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def delete_gene_from_set(self,id):
        gene_set_item_id = int(id)

        result = Stemformatics_Gene_Set.delete_gene_set_item(db,c.uid,gene_set_item_id)

        if result is None:
            return redirect(url(controller='contents', action='index'), code=404)

        gene_set_id = result

        # now delete redis keys for that gene list
        Stemformatics_Gene_Set.delete_short_term_redis_keys_for_a_gene_list(gene_set_id)

        return redirect(url('/workbench/gene_set_view/'+str(gene_set_id)))

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def add_gene_to_set(self):
        gene_set_id  = request.params.get('gene_set_id')
        db_id  = request.params.get('db_id')
        gene  = request.params.get('gene')

        # pass in all these details including db and c.uid
        result = Stemformatics_Gene_Set.add_gene_to_set(db,c.uid,gene_set_id,db_id,gene)

        if result is None:
            message = "There was an error with adding a gene to a gene list. Please try again."
        else:
            message = ""

        return redirect(url('/workbench/gene_set_view/'+str(gene_set_id)+'?message='+message))

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def update_gene_set_name(self):
        gene_set_id  = int(request.params.get('gene_set_id'))
        gene_set_name  = request.params.get('gene_set_name')
        gene_set_description  = request.params.get('gene_set_description')
        change_name_result = Stemformatics_Gene_Set.update_gene_set_name(db,c.uid,gene_set_id,gene_set_name)
        change_description_result = Stemformatics_Gene_Set.update_gene_set_description(db,c.uid,gene_set_id,gene_set_description)

        if change_name_result is None or change_description_result is None:
            message = "There was an error with updating the gene list name or description."
        else:
            message = ""
        default_url =url('/workbench/gene_set_view/'+str(gene_set_id))
        redirect_url = Stemformatics_Auth.get_smart_redirect(default_url)
        return redirect(redirect_url)


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_delete(self,id):
        gene_set_id = int(id)

        result = Stemformatics_Gene_Set.delete_gene_set(db,c.uid,gene_set_id)

        if result is None:
            message = "There was an error with deleting the gene list"
            return redirect(url('/workbench/gene_set_index?message='+message))
        else:
            message = ""
            default_url =url('/workbench/gene_set_index?message='+message)
            return redirect(default_url)



    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def analysis(self,id):
        gene_set_id = int(id)
        species = Stemformatics_Gene_Set.get_species(db,c.uid,gene_set_id)
        gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db,c.uid,gene_set_id)
        c.species = species
        c.gene_set_id = gene_set_id
        c.analysis = {'0': {'name': 'Hierarchical Cluster' , 'description': 'Hierarchical clustering groups genes and samples to highlight co-regulated gene lists.', 'url': h.url('/workbench/hierarchical_cluster_wizard?gene_set_id=')+str(gene_set_id)} }

        c.title = c.site_name+' Analyses - Choose Analysis '
        c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/gene_set_index'),'Manage Gene Lists'],[h.url('/workbench/gene_set_view/'+str(gene_set_id)),'Gene List View'],['','Choose Analysis for Gene List']]
        return render('workbench/choose_analysis.mako')

    @Stemformatics_Auth.authorise(db)
    def hierarchical_cluster_wizard(self): #CRITICAL-5
        c = self.request.c
        request = self.request
        delimiter = config['redis_delimiter']
        c.use_galaxy_server = use_galaxy = config['use_galaxy_server']
        probes_saved = 'saved'
        analysis  = 0
        c.analysis = analysis
        gene_set_id  = request.params.get('gene_set_id')
        select_probes  = request.params.get('select_probes')
        c.title = c.site_name+' Analyses - Hierarchical Cluster Wizard'


        ds_id = dataset_id  = request.params.get('datasetID')

        if dataset_id is None:
            #now get the dataset ID
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)
            c.species = None

            # T#1695 - handle when you have a gene set id but no dataset id (eg. from gene lists -> HC)
            if gene_set_id is not None:
                gene_set_id = int(gene_set_id)
                c.species = Stemformatics_Gene_Set.get_species(db,c.uid,gene_set_id)
                c.url = h.url('/workbench/hierarchical_cluster_wizard')+'?gene_set_id='+str(gene_set_id)
            else:
                c.url = h.url('/workbench/hierarchical_cluster_wizard')
            c.breadcrumbs = [
                [h.url('/workbench/index'),'Analyses'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Dataset']
                ]
            return render_to_response('S4M_pyramid:templates/workbench/choose_dataset.mako',self.deprecated_pylons_data_for_view,request=self.request)
        chip_type = Stemformatics_Dataset.getChipType(ds_id)

        if gene_set_id is None and select_probes is None:
            # call a gene set chooser for
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
            c.filter_by_db_id = Stemformatics_Dataset.get_db_id(ds_id)
            c.public_result = Stemformatics_Gene_Set.getGeneSets(db,0)

            c.result = result
            c.url = h.url('/workbench/hierarchical_cluster_wizard?datasetID=')+str(ds_id)

            c.breadcrumbs = [
                [h.url('/workbench/index'),'Analyses'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Dataset'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Gene List']
                ]

            return render_to_response('S4M_pyramid:templates/workbench/choose_gene_set.mako',self.deprecated_pylons_data_for_view,request=self.request)

        if gene_set_id is None:
            gene_set_id = 0

        gene_set_id = int(gene_set_id)


        if gene_set_id != 0:
            ref_type = 'gene_set_id'
            ref_id = gene_set_id
            select_probes = ""
            # check if user has access to gene list
            status = Stemformatics_Gene_Set.check_gene_set_availability(gene_set_id,c.uid)
            if status == False:
                return redirect(url(controller='contents', action='index'), code=404)
            species = Stemformatics_Gene_Set.get_species(db,c.uid,gene_set_id)
            gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db,c.uid,gene_set_id)

            db_id = Stemformatics_Dataset.get_db_id(ds_id)
            result = Stemformatics_Gene_Set.get_probes_from_gene_set_id(db,db_id,ds_id,gene_set_id)
            probe_list = result[0]

        else:
            gene_set_id = 0
            ref_type = 'probes'
            if select_probes is None:
                select_probes = ""
                probe_list = [] #pretty sure probe_list == [] was a typo?
            elif select_probes != probes_saved:

                temp_probe_list = re.sub('\s{1,}',delimiter,select_probes)

                # This saves the probe list into redis for the uid as a string with delimiters
                # You can then retrieve it with get_probe_list(uid)
                result = Stemformatics_Probe.set_probe_list(c.uid,temp_probe_list)
                select_probes =probes_saved
                probe_list = temp_probe_list.split(delimiter)
            else:
                # retrieve this from redis
                result = Stemformatics_Probe.get_probe_list(c.uid)
                select_probes =probes_saved
                probe_list = result.split(delimiter)
            ref_id = probe_list

        probe_expression_rows = Stemformatics_Expression.get_expression_rows(ds_id,probe_list)

        # if no probes then ask for another
        if len(probe_expression_rows) < 2:
            # call a gene set chooser for
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
            c.filter_by_db_id = Stemformatics_Dataset.get_db_id(ds_id)
            c.public_result = Stemformatics_Gene_Set.getGeneSets(db,0)

            c.result = result
            c.url = h.url('/workbench/hierarchical_cluster_wizard?datasetID=')+str(ds_id)

            c.breadcrumbs = [
                [h.url('/workbench/index'),'Analyses'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Dataset'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Gene List']
                ]
            c.error_message = "The target dataset contains no expression data for this gene list. Please try again."
            return render_to_response('S4M_pyramid:templates/workbench/choose_gene_set.mako',self.deprecated_pylons_data_for_view,request=self.request)




        cluster_type  = request.params.get('cluster_type')
        if cluster_type is None:
            c.url = h.url('/workbench/hierarchical_cluster_wizard?gene_set_id=')+str(gene_set_id) + '&select_probes='+select_probes+'&datasetID='+str(ds_id)
            c.breadcrumbs = [
                [h.url('/workbench/index'),'Analyses'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Dataset'],
                [h.url('/workbench/hierarchical_cluster_wizard?datasetID='+str(ds_id)),'Hierarchical Cluster - Choose Gene List'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Cluster Type']
                ]

            return render_to_response('S4M_pyramid:templates/workbench/choose_cluster_type.mako',self.deprecated_pylons_data_for_view,request=self.request)

        cluster_size  = "None"
        colour_by  = request.params.get('colour_by')

        if colour_by is None:
            c.url = h.url('/workbench/hierarchical_cluster_wizard?gene_set_id=')+str(gene_set_id) + '&select_probes='+select_probes+'&datasetID='+str(ds_id)+'&cluster_type='+str(cluster_type)+'&cluster_size='+cluster_size
            c.breadcrumbs = [
                [h.url('/workbench/index'),'Analyses'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Dataset'],
                [h.url('/workbench/hierarchical_cluster_wizard?datasetID='+str(ds_id)),'Hierarchical Cluster - Choose Gene List'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Colour By']
                ]
            return render_to_response('S4M_pyramid:templates/workbench/choose_colour_by.mako',self.deprecated_pylons_data_for_view,request=self.request)

        remove_chip_ids  = request.params.get('remove_chip_ids')

        if remove_chip_ids is None:
            chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
            c.chip_id_details = Stemformatics_Expression.return_sample_details(db,ds_id)
            sort_by = 'Sample Type'
            sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)
            c.sample_chip_ids_in_order = Stemformatics_Dataset.get_sample_chip_ids_in_order(db,chip_type,sample_labels,sort_by,ds_id)
            c.url = h.url('/workbench/hierarchical_cluster_wizard?gene_set_id=')+str(gene_set_id) + '&select_probes='+select_probes+'&datasetID='+str(ds_id)+'&cluster_type='+str(cluster_type)+'&cluster_size='+cluster_size+'&colour_by='+colour_by
            c.breadcrumbs = [
                [h.url('/workbench/index'),'Analyses'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Dataset'],
                [h.url('/workbench/hierarchical_cluster_wizard?datasetID='+str(ds_id)),'Hierarchical Cluster - Choose Gene List'],
                [h.url('/workbench/hierarchical_cluster_wizard'),'Hierarchical Cluster - Choose Samples']
                ]

            return render_to_response('S4M_pyramid:templates/workbench/remove_samples.mako',self.deprecated_pylons_data_for_view,request=self.request)


        remove_chip_ids = []
        for item in request.params:
            if 'remove_chip_ids_' in item:
                remove_chip_id = item.replace('remove_chip_ids_','')
                remove_chip_ids.append(remove_chip_id)
        c.dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,c.uid)
        if c.dataset_status != "Available":
            return redirect(url(controller='contents', action='index'), code=404)

        base_path = self.StemformaticsQueue

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        use_cls = False
        use_gct = True
        # create job here
        options = {}
        options['remove_chip_ids'] = remove_chip_ids
        options['cluster_type'] = cluster_type
        options['cluster_size'] = cluster_size
        options['galaxy_server_url'] = config['galaxy_server_url']
        options['colour_by'] = colour_by

        if select_probes == probes_saved:
            select_probes = Stemformatics_Probe.get_probe_list(c.uid)
        else:
            select_probes = ""

        options['select_probes'] = select_probes


        job_details = { 'analysis': analysis, 'status': 0, 'dataset_id': dataset_id, 'gene_set_id': gene_set_id, 'uid': c.uid, 'use_cls': use_cls, 'use_gct': use_gct, 'gene': None, 'probe': None, 'options':json.dumps(options)}

        job_id = Stemformatics_Job.create_job(db,job_details)

        if job_id is None:
            return redirect(url(controller='contents', action='index'), code=404)

        if not os.path.exists(base_path+str(job_id)):
            os.mkdir(base_path+str(job_id))

        pearson_correlation = 'pearson'
        euclidean_correlation = 'euclidean'
        no_correlation = 'none'


        if cluster_type == 'pearson_both' or cluster_type == 'pearson_row':
            row_distance_measure = pearson_correlation
        elif cluster_type == 'euclidean_both' or cluster_type == 'euclidean_row':
            row_distance_measure = euclidean_correlation
        else:
            row_distance_measure = no_correlation


        if cluster_type == 'pearson_both' or cluster_type == 'pearson_column':
            column_distance_measure = pearson_correlation
        elif cluster_type == 'euclidean_both' or cluster_type == 'euclidean_column':
            column_distance_measure = euclidean_correlation
        else:
            column_distance_measure = no_correlation

        # now create gct file for galaxy
        gct_file_path = self.StemformaticsQueue + str(job_id) + '/' +'job.gct'

        text = Stemformatics_Dataset.build_gct_from_redis(db,ref_type,ref_id,ds_id,c.uid,options)
        Stemformatics_Dataset.write_gct_file(text,gct_file_path)

        gene_probe_ordered_row_list = self.StemformaticsQueue + str(job_id) + '/' +'job_mapping.text'
        job_mapping_text = ''
        with open(self.StemformaticsQueue + str(job_id) + '/' +'job.gct', 'r') as f:
            all_lines = f.readlines()[3:] #ignore first three lines of gct
            for line in all_lines:
                job_mapping_text += line.strip().split("\t")[0]  #gets the first column
                job_mapping_text += "\n"
        # write to file
        job_mapping_file = open(gene_probe_ordered_row_list,'w')
        job_mapping_file.writelines(job_mapping_text)
        job_mapping_file.close()

        # connect to galaxy now
        from guide.model.stemformatics.stemformatics_galaxy import Stemformatics_Galaxy
        galaxyInstance = Stemformatics_Galaxy.connect_to_galaxy()
        # run tool
        galaxy_history_id = Stemformatics_Galaxy.run_HC_tool(galaxyInstance,job_id,gct_file_path,c.uid,column_distance_measure,row_distance_measure,colour_by,chip_type)


        audit_dict = {'ref_type':'gene_set_id','ref_id':gene_set_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type':'ds_id','ref_id':dataset_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return redirect(h.url('/workbench/analysis_confirmation_message/'+str(job_id)))


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def comparative_marker_selection_wizard(self): #CRITICAL-5 DELETE
        return redirect(url('/contents/removal_of_comparative_marker_selection'))


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def jobs_index(self):
        c.status = Stemformatics_Job.return_all_status()
        c.analysis = Stemformatics_Job.return_all_analysis()
        c.jobs = Stemformatics_Job.get_jobs_for_user(db,c.uid)

        c.shared_jobs = Stemformatics_Job.get_shared_jobs_for_user(db,c.uid)

        if c.jobs is not None and c.shared_jobs is not None:
            c.jobs.extend(c.shared_jobs)
        if c.jobs is None and c.shared_jobs is not None:
            c.jobs = c.shared_jobs

        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],['','Manage Analysis Jobs']]
        c.title = c.site_name+' Analyses  - Jobs index'
        # raise Error
        return render('workbench/jobs_index.mako')


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def job_view_result(self,id):  #CRITICAL-4
        job_id = int(id)
        use_galaxy_server = config['use_galaxy_server']
        c.use_galaxy_server = use_galaxy_server
        output_file  = request.params.get('output_file')

        # check which analysis the job_id has eg. HC, CMS etc
        job_detail = Stemformatics_Job.get_job_details(db,job_id)
        analysis_server = job_detail.reference_type

        if job_detail is None:
            return redirect(url(controller='contents', action='index'), code=404)

        # check if this could be a shared resource if user not the job owner
        if c.uid != job_detail.uid:
            share_type = "Job"
            share_id = job_id
            check_shared_resource = Stemformatics_Shared_Resource.check_shared_resource(db,share_type,share_id,c.uid)
            if len(check_shared_resource) == 0:
                return redirect(url(controller='contents', action='index'), code=404)

            use_uid = check_shared_resource[0].from_uid

            c.job_shared = True
            c.shared_user = Stemformatics_Auth.get_user_from_uid(db,use_uid)

        else:
            use_uid = c.uid
            c.job_shared = False
            c.shared_user = None

        # if dataset is not 0, find out if user can still access this dataset
        if job_detail.dataset_id != 0:
            # now check if dataset is available
            available = Stemformatics_Dataset.check_dataset_availability(db,use_uid,job_detail.dataset_id)

            if not available:
                c.title = "You no longer have access to this dataset"
                c.message = "This dataset is private and you no longer have access to it. Please contact "+c.site_name+" for further details."
                return render('workbench/error_message.mako')


        c.job_id = job_id
        c.analysis = job_detail.analysis

        if job_detail.analysis == 4: # Annotate gene set redirect straight away
            return redirect(h.url('/workbench/gene_set_annotation_view/'+str(job_id)))

        c.title = c.site_name+' Analyses  - View Result for Job #' + str(c.job_id)
        # check job queue created
        try:
            c.gp_job_id = job_detail.reference_id
            if analysis_server != "GenePattern": # Hierarchical cluster
                c.gp_job_id = int(id)
                path = self.StemformaticsQueue +str(id) + "/"
                dirList = os.listdir(path)
            else:
                path = self.GPQueue+str(c.gp_job_id) + "/"
                dirList = os.listdir(path)

        except:
            return redirect(url(controller='contents', action='index'), code=404)


        if job_detail.analysis == 0: # Hierarchical Cluster
            c.job_detail = job_detail
            # get job details to check if galaxy or gene pattern job
            c.HC_server = analysis_server

            result = Stemformatics_Job.get_job_view_result_for_HC(job_detail)
            if result == "Files not found":
                c.title = "No files found for this output"
                c.message = "Not all output files were found for this Hierarchical Cluster. Please try running the job again."
                return render('workbench/error_message.mako')

            c.text = result["text"]
            c.gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db,use_uid,c.job_detail.gene_set_id)
            c.handle = Stemformatics_Dataset.getHandle(db,c.job_detail.dataset_id,use_uid)
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],['','Hierarchical Cluster Result']]
            c.text_remove_sample_ids = result["text_remove_sample_ids"]
            c.cluster_type = result["cluster_type"]
            c.colour_by = result["colour_by"]
            c.db_id = result["db_id"]

            return render('workbench/view_hc_job.mako')

        elif job_detail.analysis == 2 or job_detail.analysis == 7: # Gene Neighbourhood
            c.url = h.url('/workbench/job_view_result/')+str(job_id)
            p_value  = request.params.get('p_value')
            if p_value is None:
                c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],['','Choose P Value']]
                return render('workbench/choose_p_value.mako')
            c.p_value = float(p_value)
            c.job_detail = job_detail

            odfList = []
            for fname in dirList:
                if analysis_server == "GenePattern": #if job is analysis 7, than .odf file will be generated
                    if fname.find('.odf') != -1 and fname.find('.swp') == -1:
                        odfList.append(fname)
                else:
                    if fname.find('.txt') != -1 :
                        odfList.append(fname)

            # error out if odfList is not equal to one
            fileTotals = len(odfList)
            if fileTotals == 0:
                c.title = "No files found for this output"
                c.message = "No files were found for this Gene Neighbourhood. Please try running the job again."
                return render('workbench/error_message.mako')
            elif fileTotals == 1:
                openFile = path+odfList[0]
                if not os.path.isfile(openFile):
                    c.title = "No files found for this output"
                    c.message = "No output files were found for this Gene Neighbourhood. Please try running the job again."
                    return render('workbench/error_message.mako')

            # get db_id for this dataset
            c.db_id = Stemformatics_Dataset.get_db_id(db,c.job_detail.dataset_id)
            c.handle = Stemformatics_Dataset.getHandle(db,c.job_detail.dataset_id,use_uid)
            c.gene = job_detail.gene
            c.probe = job_detail.probe
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],['','Gene Neighbourhood Result']]
            if job_detail.analysis ==7:
                show_limited = False
                c.dataset_metadata = Stemformatics_Dataset.getExpressionDatasetMetadata(db,c.job_detail.dataset_id,c.uid,show_limited)
                c.options = job_detail.options
            c.job_id = job_id
            return self._view_gene_neighbour_output_file(openFile,job_id,c.db_id,c.p_value,analysis_server)

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def view_cms_image(self):
        gp_job_id = int(request.params.get('gp_job_id'))
        output_file= int(request.params.get('output_file'))
        download = request.params.get('download')
        # check job queue created
        try:
            path = self.GPQueue+str(gp_job_id) + "/"
            dirList = os.listdir(path)
        except:
            return redirect(url(controller='contents', action='index'), code=404)

        odfList = []

        for fname in dirList:
            if fname.find('.odf') != -1:
                odfList.append(fname)

        src = str(gp_job_id) + "/" + odfList[output_file].replace('.odf','.filt.png')
        f = open(self.GPQueue+src,'r')
        response.headers['Content-type'] = 'image/png'

        if download is not None:
            response.headers['Content-Disposition'] = 'attachment;download_image.png'

        response.charset= "utf8"

        text = f.read()

        f.close()

        return text

    # Can set &download=true and it will download instead of display
    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def view_image(self):
        src = request.params.get('src')
        download = request.params.get('download')
        HC_server = request.params.get('hc_server')

        if HC_server != "GenePattern":
            f = open(self.StemformaticsQueue  + src,'r')
        else:
            f = open(self.GPQueue  + src,'r')

        if download is not None:
            response.headers['Content-Disposition'] = 'attachment;download_image.png'

        response.headers['Content-type'] = 'image/png'

        response.charset= "utf8"

        text = f.read()

        f.close()

        return text

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def job_delete(self,id):
        job_id = int(id)
        result = Stemformatics_Job.delete_job(db,job_id,c.uid)
        return redirect(url('/workbench/jobs_index'))

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def job_remove_shared(self,id):
        job_id = int(id)
        result = Stemformatics_Shared_Resource.delete_shared_resource(db,"Job",job_id,c.uid)

        return redirect(url('/workbench/jobs_index'))

    #---------------------NOT MIGRATED--------------------------------
    def _view_cms_output_file(self,openFile,job_id,use_uid):
        f = open(openFile,'r')
        c.text = f.readlines()
        f.close()

        c.openFile = openFile

        temp = openFile.split('/')
        c.file_name = temp[len(temp)-1].replace('.odf','.filt.png')

        c.job_id = job_id

        result = {}
        data = False
        zScoreInputMean = []
        zScoreInputFoldChange = []
        listGenesInOrderODF = []

        for line in c.text:

            if line.find('COLUMN_NAMES') != -1:
                headers = line.replace('COLUMN_NAMES:','')
                splitTempHeaders = headers.split('\t')
                sampleTypeA = splitTempHeaders[13].replace(' Mean','')
                sampleTypeB = splitTempHeaders[15].replace(' Mean','')

            if data:
                splitTemp = line.split('\t')
                geneName = splitTemp[1]
                foldChange = splitTemp[12]
                sampleType1Mean = splitTemp[13]
                sampleType2Mean = splitTemp[15]

                listGenesInOrderODF.append(geneName)

                sampleType1Mean = float(sampleType1Mean)
                sampleType1Mean = round(sampleType1Mean,2)

                sampleType2Mean = float(sampleType2Mean)
                sampleType2Mean = round(sampleType2Mean,2)
                result[geneName] = {'sampleType1Mean': sampleType1Mean, 'sampleType2Mean': sampleType2Mean, 'foldChange': foldChange}
                zScoreInputMean.append(sampleType1Mean)
                zScoreInputMean.append(sampleType2Mean)
                zScoreInputFoldChange.append(foldChange)


            if line.find('DataLines') != -1:
                data = True


        c.sampleTypeA = sampleTypeA
        c.sampleTypeB = sampleTypeB
        c.listGenesInOrderODF = listGenesInOrderODF


        c.result = result

        c.gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db,use_uid,c.job_detail.gene_set_id)
        c.handle = Stemformatics_Dataset.getHandle(db,c.job_detail.dataset_id,use_uid)
        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/job_view_result/'+str(job_id)),'Comparative Marker Selection - Choose comparison'],['','Comparative Marker Selection Result']]

        return render('workbench/view_cms_job.mako')



    #---------------------NOT MIGRATED--------------------------------
    def _view_gene_neighbour_output_file(self,openFile,job_id,db_id,p_value,analysis_server):

        f = open(openFile,'r')
        c.text = f.readlines()
        f.close()

        return_data = Stemformatics_Job.get_GN_data_from_output_file(c.text,p_value,analysis_server)
        c.job_id = job_id
        # c.handle = Stemformatics_Dataset.getHandle(db,c.job_detail.dataset_id,c.uid)
        c.listProbesInOrderODF = return_data["listProbesInOrderODF"]
        c.result = return_data["result"]

        select_all_ambiguous = False
        search_type = 'probes_using_chromosomal_locations' # this doesn't clean up the probe name
        c.geneList = Stemformatics_Gene.get_unique_gene_fast(db,c.listProbesInOrderODF,db_id,search_type,select_all_ambiguous)
        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],['','Gene Neighbourhood Result']]
        return render('workbench/view_gene_neighbour_job.mako')



    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def save_gene_set(self):
        db_id  = request.params.get('db_id')
        probe_list = request.params.get('probe_list')
        job_id = request.params.get('job_id')

        c.gene_set_name = request.params.get('gene_set_name')
        c.description = request.params.get('description')

        save = request.params.get('save')

        if c.gene_set_name is None:
            # get the list of ensemblIDs and then save this against the user
            c.gene_set_name = "From job#"+str(job_id)
            c.description = "From job#"+str(job_id)


        c.description = c.description + " Created:" +strftime("%Y-%m-%d %H:%M", gmtime())

        if save is None:
            c.db_id = db_id
            c.probe_list = probe_list
            c.job_id = job_id
            c.message = ""
            return render('workbench/save_gene_set.mako')

        old_probe_list = probe_list
        probe_list = probe_list.split('\r\n')

        ensembl_list = Stemformatics_Gene.get_ensembl_from_probe(db,probe_list,db_id)

        # check if gene set name and uid are unique!
        gene_set_id = Stemformatics_Gene_Set.addGeneSet(db,c.uid,c.gene_set_name,c.description,int(db_id),ensembl_list)

        if gene_set_id is None:
            c.db_id = db_id
            c.probe_list = old_probe_list
            c.job_id = job_id
            c.message = "Please check this gene list name is unique"
            # get the list of ensemblIDs and then save this against the user
            #c.gene_set_name = "From job#"+str(job_id)
            c.gene_set_name = c.gene_set_name + " " +strftime("%Y-%m-%d %H:%M", gmtime())

            return render('workbench/save_gene_set.mako')


        return redirect(h.url('/workbench/gene_set_view/'+str(gene_set_id)))

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def uniquely_identify_gene(self):
        original = request.params.get('original')
        db_id = request.params.get('db_id')

        # for cage probes
        original = original.replace('plus','+')
        try:
            db_id = int(db_id)
        except:
            return redirect(url(controller='contents', action='index'), code=404)
        search_type = 'all'
        one_search_term = True
        geneSet = [original]
        select_all_ambiguous = True
        get_description = True
        chip_type = 0
        returnData = Stemformatics_Gene.get_unique_gene_fast(db,geneSet,db_id,search_type,select_all_ambiguous,get_description,chip_type,one_search_term)
        c.data = returnData
        c.original = original
        c.title = c.site_name+' Analyses  - Uniquely Identify Gene'
        return render('workbench/uniquely_identify_gene.mako')


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_gene_preview(self,id):
        gene_set_id = int(id)

        result = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
        resultGeneSet = result[0]
        resultGeneSetData = result[1]
        c.result = resultGeneSetData
        c.gene_set = resultGeneSet
        c.db_id = resultGeneSet.db_id
        c.message = request.params.get('message')
        c.title = c.site_name+' Analyses  - View Gene List Preview for ' + resultGeneSet.gene_set_name
        # return render('workbench/gene_set_view.mako')
        return render('/workbench/gene_set_gene_preview.mako')



    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def public_gene_set_gene_preview(self,id):
        gene_set_id = int(id)

        result = Stemformatics_Gene_Set.getGeneSetData(db,0,gene_set_id)
        resultGeneSet = result[0]
        resultGeneSetData = result[1]
        c.result = resultGeneSetData
        c.gene_set = resultGeneSet
        c.db_id = resultGeneSet.db_id
        c.message = request.params.get('message')
        c.title = c.site_name+' Analyses  - View Gene List Preview for ' + resultGeneSet.gene_set_name
        # return render('workbench/gene_set_view.mako')
        return render('/workbench/gene_set_gene_preview.mako')

    @Stemformatics_Auth.authorise(db)
    @action(renderer='templates/workbench/analysis_confirmation_message.mako')
    def analysis_confirmation_message(self,id):
        c = self.request.c
        job_id = int(id)
        result = Stemformatics_Job.get_job_details_with_gene_set(db,job_id)

        if result is None:
            return redirect(url(controller='contents', action='index'), code=404)

        if result.uid != c.uid:
            return redirect(url(controller='contents', action='index'), code=404)

        c.job = result
        c.status = Stemformatics_Job.return_all_status()
        c.analysis = Stemformatics_Job.return_all_analysis()

        c.message = "This analysis was submitted to the analysis server as job #"+str(job_id)+". "+c.site_name+" will send a notification email (if selected) when your results are able to be viewed in \"My Analysis Jobs\"."
        c.title = c.site_name+" Analyses - Analysis Submitted"
        return self.deprecated_pylons_data_for_view


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def help_gene_neighbourhood(self):
        c.message  = request.params.get('message')
        c.title = c.site_name+' Analyses  - View Gene Neighbourhood Help'
        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/'),'Gene Neighbourhood Help']]

        return render('workbench/help_gene_neighbourhood.mako')

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def help_gene_set_annotation(self):
        c.message  = request.params.get('message')
        c.title = c.site_name+' Analyses  - View Gene List Annotation Help'
        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/'),'Gene List Annotation Help']]

        return render('workbench/help_gene_set_annotation.mako')

    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def help_hierarchical_cluster(self):
        c.message  = request.params.get('message')
        c.title = c.site_name+' Analyses  - View Hierarchical Cluster Help'
        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/'),'Hierarchical Cluster Help']]

        return render('workbench/help_hierarchical_cluster.mako')


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def help_comparative_marker_selection(self):
        c.message  = request.params.get('message')
        c.title = c.site_name+' Analyses  - View Comparative Marker Selection Help'
        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/'),'Comparative Marker Selection Help']]

        return render('workbench/help_comparative_marker_selection.mako')


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_annotation_wizard(self):  #CRITICAL-5

        analysis  = 4
        transcripts_per_page = request.params.get('transcripts_per_page')

        if transcripts_per_page is None:
            transcripts_per_page = 50
        else:
            transcripts_per_page = int(transcripts_per_page)

        c.analysis = analysis
        gene_set_id  = request.params.get('gene_set_id')
        c.title = c.site_name+' Analyses  - Gene List Annotation'

        if gene_set_id is None:
            # call a gene set chooser for
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
            c.result = result
            c.public_result = Stemformatics_Gene_Set.getGeneSets(db,0)
            c.url = h.url('/workbench/gene_set_annotation_wizard')
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/gene_set_annotation_wizard'),'Gene List Annotation - Choose Gene List  (Step 1 of 2)']]
            return render('workbench/choose_gene_set.mako')

        else:
            gene_set_id = int(gene_set_id)
            species = Stemformatics_Gene_Set.get_species(db,c.uid,gene_set_id)
            gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db,c.uid,gene_set_id)


        dataset_id = 0


        # this is where it should create a job
        base_path = self.StemformaticsQueue

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        use_cls = False
        use_gct = False

        # create job here

        job_details = { 'analysis': analysis, 'status': 0, 'dataset_id': dataset_id, 'gene_set_id': gene_set_id, 'uid': c.uid, 'use_cls': use_cls, 'use_gct': use_gct, 'gene': None, 'probe': None}

        job_id = Stemformatics_Job.create_job(db,job_details)

        if job_id is None:
            return redirect(url(controller='contents', action='index'), code=404)

        if not os.path.exists(base_path+str(job_id)):
            os.mkdir(base_path+str(job_id))

        ini_filename = base_path + str(job_id) + '/job.ini'

        # create ini file
        ini_file = open(ini_filename,"w")

        ini_file_list = ['[StemformaticsQueue]\n','analysis='+str(analysis)+'\n','uid='+str(c.uid)+'\n','gene_set_id='+str(gene_set_id)+'\n','dataset_id='+str(dataset_id)+'\n']

        ini_file.writelines(ini_file_list)
        ini_file.close()

        # call java code from command line
        command_line = "nice -n 15 " + self.FullJavaPath + " -jar "+ self.StemformaticsController +" " + str(job_id)+ " " + config['__file__']

        p = subprocess.Popen(command_line,shell=True)

        audit_dict = {'ref_type':'gene_set_id','ref_id':gene_set_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return redirect(h.url('/workbench/analysis_confirmation_message/'+str(job_id)))


    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_annotation_save(self,id): #CRITICAL-4

        job_id = int(id)

        # find the dataset id and gene set id from the job itself.
        # check which analysis the job_id has eg. HC, CMS etc
        job_detail = Stemformatics_Job.get_job_details(db,job_id)

        if job_detail is None:
            return redirect(url(controller='contents', action='index'), code=404)

        # check if this could be a shared resource if user not the job owner
        if c.uid != job_detail.uid:
            share_type = "Job"
            share_id = job_id
            check_shared_resource = Stemformatics_Shared_Resource.check_shared_resource(db,share_type,share_id,c.uid)
            if len(check_shared_resource) == 0:
                return redirect(url(controller='contents', action='index'), code=404)

            use_uid = check_shared_resource[0].from_uid
        else:
            use_uid = c.uid

        gene_set_id = job_detail.gene_set_id
        dataset_id = job_detail.dataset_id

        filter_gene_set_id = request.params.get('filter_gene_set_id')

        genes_selected = request.params.get('genes_selected')

        nice_gene_names_selected = request.params.get('nice_gene_names_selected')

        filter = {}
        tm_filter  = request.params.get('tm')


        if tm_filter == 'True':
            filter['tm_domain'] = True

        if tm_filter == 'False':
            filter['tm_domain'] = False


        sp_filter  = request.params.get('sp')

        if sp_filter == 'True':
            filter['signal_peptide'] = True

        if sp_filter == 'False':
            filter['signal_peptide'] = False


        # filter_id passed in overrides anything else
        filter_id = request.params.get('filter_id')

        if filter_id is not None:
            new_filter = Stemformatics_Transcript.loadFilter(db,filter_id,use_uid)

            if new_filter is not None:
                filter = new_filter

        c.filter = filter


        describe_filters = ""
        for name in filter:

            output = ""
            first_word_passed = False
            for word in name.split("_"):
                if not word:
                    output += "_"
                    continue
                else:
                    output += word.capitalize() + " "


            new_name = output[:-1]

            describe_filters = describe_filters + " " + new_name + ":" + str(filter[name])

            describe_filters = describe_filters.replace('Tm','Transmembrane')

        if filter_gene_set_id is not None:
            public_uid = 0
            result = Stemformatics_Gene_Set.getGeneSet(db,public_uid,int(filter_gene_set_id))
            describe_filters = describe_filters + ' filtered pathway/gene list: "' + result.gene_set_name + '"'

        gene_set_name = request.params.get('gene_set_name')
        gene_set_description = request.params.get('description')

        if gene_set_name is None:

            gene_set = Stemformatics_Gene_Set.getGeneSet(db,use_uid,gene_set_id)

            if gene_set is None:
                return redirect(url(controller='contents', action='index'), code=404)

            c.message = ""
            # get the list of ensemblIDs and then save this against the user

            this_time = datetime.now()
            format_time = this_time.strftime("%Y-%m-%d %H:%M")

            c.gene_set_name = "Annotated gene list \"" + gene_set.gene_set_name + "\" Job#"+ str(job_id) +" Created:" + format_time

            if describe_filters != "":
                describe_filters = "using filters " + describe_filters

            c.description = "From gene list annotation Job#"+ str(job_id) +"  using gene list: \"" + gene_set.gene_set_name + "\" " + describe_filters + " Created:" + format_time

            if genes_selected is not None:
                c.description = c.description + " with the following genes selected manually " + nice_gene_names_selected


            c.url = h.url(str(request.environ.get('PATH_INFO') + '?' + request.environ.get('QUERY_STRING')))

            return render('workbench/gene_set_annotation_save.mako')



        db_id = Stemformatics_Gene_Set.get_db_id(db,c.uid,gene_set_id)

        order_by = request.params.get('order_by')

        if order_by is None:
            order_by = 'gene_name'


        if genes_selected is not None:
            save_genes = genes_selected.split(',')
        else:

            filter_level = 'Gene'

            base_path = self.StemformaticsQueue + str(job_id) + '/'

            tx_dict = Stemformatics_Job.read_transcript_data_gene_set_annotation(db,job_id,base_path,filter_gene_set_id)

            result = Stemformatics_Transcript.get_statistics(tx_dict,filter,order_by,filter_level)
            new_genes = result[0]

            save_genes = []

            for gene in new_genes:
                save_genes.append(gene)

        result = Stemformatics_Gene_Set.addGeneSet(db,c.uid,gene_set_name,gene_set_description,db_id,save_genes)

        return redirect(url('/workbench/gene_set_index'))

    """

    This is now where the display happens

    """
    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_annotation_view(self,id): #CRITICAL-4

        job_id = int(id)


        analysis  = 4
        transcripts_per_page = request.params.get('transcripts_per_page')
        sp_filter  = request.params.get('sp')
        tm_filter  = request.params.get('tm')
        filter_name = request.params.get('filter_name')
        order_by = request.params.get('order_by')
        descending = request.params.get('descending')
        filter_gene_set_id = request.params.get('filter_gene_set_id')
        remove_pagination = request.params.get('remove_pagination')
        page = request.params.get('page')

        if transcripts_per_page is None:
            transcripts_per_page = 50
        else:
            transcripts_per_page = int(transcripts_per_page)

        c.analysis = analysis


        # check which analysis the job_id has eg. HC, CMS etc
        job_detail = Stemformatics_Job.get_job_details(db,job_id)

        if job_detail is None:
            return redirect(url(controller='contents', action='index'), code=404)

        # check if this could be a shared resource if user not the job owner
        if c.uid != job_detail.uid:
            share_type = "Job"
            share_id = job_id
            check_shared_resource = Stemformatics_Shared_Resource.check_shared_resource(db,share_type,share_id,c.uid)
            if len(check_shared_resource) == 0:
                return redirect(url(controller='contents', action='index'), code=404)

            use_uid = check_shared_resource[0].from_uid
            c.job_shared = True
            c.shared_user = Stemformatics_Auth.get_user_from_uid(db,use_uid)

        else:
            use_uid = c.uid
            c.job_shared = False
            c.shared_user = None




        # if dataset is not 0, find out if user can still access this dataset
        if job_detail.dataset_id != 0:
            # now check if dataset is available
            available = Stemformatics_Dataset.check_dataset_availability(db,use_uid,job_detail.dataset_id)

            if not available:
                c.title = "You no longer have access to this dataset"
                c.message = "This dataset is private and you no longer have access to it. Please contact "+c.site_name+" for further details."
                return render('workbench/error_message.mako')


        c.job_id = job_id
        c.title = c.site_name+' Analyses  - View Result for Job #' + str(c.job_id)
        # get gene_set_id from job
        gene_set_id = job_detail.gene_set_id
        dataset_id = job_detail.dataset_id

        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/gene_set_annotation_wizard'),'Gene List Annotation - Choose Gene List'],[h.url('/workbench/gene_set_annotation_wizard?gene_set_id=')+str(gene_set_id),'Gene List Annotation - Choose Dataset'],['','Gene List Annotation']]


        result = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db,use_uid,gene_set_id)
        c.gene_set = result[0]
        gene_set_genes = result[1]

        genes = []
        gene_dictionary = {}


        filter = {}


        if tm_filter == 'True':
            filter['tm_domain'] = True
        if tm_filter == 'False':
            filter['tm_domain'] = False



        if sp_filter == 'True':
            filter['signal_peptide'] = True
        if sp_filter == 'False':
            filter['signal_peptide'] = False

        # filter_id passed in overrides anything else
        filter_id = request.params.get('filter_id')

        if filter_id is not None:
            new_filter = Stemformatics_Transcript.loadFilter(db,filter_id,c.uid)

            if new_filter is not None:
                filter = new_filter



        c.filter = filter


        # save filter if filter name is not none
        if filter_name is not None:
            new_filter_id = Stemformatics_Transcript.saveFilter(db,use_uid,filter_name,filter)


        c.filter_list = Stemformatics_Transcript.getFilters(db,use_uid)

        db_id = Stemformatics_Gene_Set.get_db_id(db,c.uid,gene_set_id)


        # filter_level = 'Transcript'

        # if order_by is None:
          #  order_by = 'transcript_name'
          #  descending = False

        filter_level = "Gene"
        if order_by is None:
            order_by = 'gene_name'
            descending = False

        if descending is None:
            descending = False
        else:
            if descending == 'True':
                descending = True
            else:
                descending = False

        base_path = self.StemformaticsQueue + str(job_id) + '/'

        tx_dict = Stemformatics_Job.read_transcript_data_gene_set_annotation(db,job_id,base_path,filter_gene_set_id)

        result = Stemformatics_Transcript.get_statistics(tx_dict,filter,order_by,filter_level)

        new_genes = result[0]
        new_tx = result[1]
        statistics = result[2]
        ordered_list = result[3]

        gene_pathways_file = base_path + 'pathways.tsv'

        # now get the gene pathways details if gene pathway not specified
        gene_pathways_list = Stemformatics_Job.read_gene_pathways_gene_set_annotation(gene_pathways_file,new_genes)

        c.gene_pathways_list = gene_pathways_list

        # get the Fisher exact pvalues from the export file
        gene_pathway_export_file = base_path + 'pathway_export.tsv'

        # now get the gene pathway fisher exact pvalues two tailed
        pathway_statistics = Stemformatics_Job.read_gene_pathways_export_gene_set_annotation(gene_pathway_export_file)
        c.pathway_statistics = pathway_statistics


        public_uid = 0
        gene_set_details = Stemformatics_Gene_Set.get_gene_set_details(db,public_uid,gene_pathways_list)

        # order by type eventually, at the moment just order by name
        c.gene_set_details = {}

        # default values
        c.filter_gene_set_id = 0
        c.filter_gene_set_name = "None"

        for gs in gene_set_details:

            if gs.gene_set_type not in c.gene_set_details:
                c.gene_set_details[gs.gene_set_type] = []

            fisher_exact_pvalue = pathway_statistics[str(gs.id)]['fisher_exact_pvalue']

            c.gene_set_details[gs.gene_set_type].append((float(fisher_exact_pvalue),gs))

            if filter_gene_set_id is not None and int(filter_gene_set_id) == gs.id:
                c.filter_gene_set_id = int(filter_gene_set_id)
                c.filter_gene_set_name = gs.gene_set_name



        ordered_list.sort(reverse=descending)

        # Pagination details
        if remove_pagination != 'True':
            if page is None:
                page = 1
            else:
                page = int(page)


            # pagination details
            total = len(new_genes)
            start = ((page - 1) * transcripts_per_page)
            end = page * transcripts_per_page

            if end > total:
                end = total

            c.paginate = {}

            c.paginate['page'] = c.page = page
            c.paginate['start_page'] = 1

            if page == 1:
                c.paginate['prev_page'] = page
            else:
                c.paginate['prev_page'] = page - 1

            c.paginate['end_page'] = end_page = int(math.floor(total / transcripts_per_page) + 1)


            if page == end_page:
                c.paginate['next_page'] = page
            else:
                c.paginate['next_page'] = page + 1

            c.paginate['start'] = start
            c.paginate['end'] = end
            c.paginate['total'] = total


            c.genes = ordered_list[start:end]
            c.paginate_on = True
        else:
            c.genes = ordered_list
            c.paginate_on = False



        tx_list = {}
        for gene in c.genes:
            gene_name = gene[0]
            gene_id = gene[1]['gene_id']

            tx_list[gene_id] = new_tx[gene_id]

        c.tx_list = tx_list

        c.statistics = statistics

        # for filtering
        # job=true is just to add an ? it doesn't actually do anything :)

        c.url = h.url('/workbench/gene_set_annotation_view/')+str(job_id)+'?run=true'



        c.url_pagination = '&remove_pagination='+str(not c.paginate_on)

        c.url_filter_id = ""
        if filter_id is not None:
            c.url_filter_id = "&filter_id=" + str(filter_id)

        c.url_sp_filter = ""
        if sp_filter is not None:
            c.url_sp_filter = '&sp=' + sp_filter

        c.url_tm_filter = ""
        if tm_filter is not None:
            c.url_tm_filter = '&tm=' + tm_filter

        c.url_filter_gene_set_id = ""
        if filter_gene_set_id is not None:
            c.url_filter_gene_set_id = '&filter_gene_set_id=' + str(filter_gene_set_id)

        c.url_order_by = "&order_by="+order_by+"&descending="+str(descending)

        if c.paginate_on == True:
            c.paginate['base_url'] = c.url + c.url_filter_id + c.url_tm_filter + c.url_sp_filter + c.url_order_by + c.url_filter_gene_set_id
            c.paginate['order_by'] = order_by

        return render('workbench/gene_set_annotation.mako')



    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_annotation_export_pathways(self,id):

        job_id = int(id)

        # find the dataset id and gene set id from the job itself.
        job_detail = Stemformatics_Job.get_job_details_check_user(db,job_id,c.uid)

        if job_detail is None:
            return redirect(url(controller='contents', action='index'), code=404)

        base_path = self.StemformaticsQueue + str(job_id) + '/'
        gene_pathways_export = base_path + 'pathway_export.tsv'


        response.headers['Content-type'] = 'text/tab-separated-values'
        stemformatics_version = config['stemformatics_version']
        response.headers['Content-Disposition'] = 'attachment;filename=export_gene_set_annotation_pathways_'+stemformatics_version+'.tsv'
        response.charset= "utf8"

        printout = Stemformatics_Job.read_gene_pathways_export_gene_set_annotation_raw(gene_pathways_export)
        return printout



    @Stemformatics_Auth.authorise()
    #---------------------NOT MIGRATED--------------------------------
    def gene_set_annotation_export_tx(self,id): #CRITICAL-4

        job_id = int(id)

        # find the dataset id and gene set id from the job itself.
        job_detail = Stemformatics_Job.get_job_details_check_user(db,job_id,c.uid)

        if job_detail is None:
            return redirect(url(controller='contents', action='index'), code=404)

        gene_set_id = job_detail.gene_set_id
        dataset_id = job_detail.dataset_id

        filter_gene_set_id = request.params.get('filter_gene_set_id')

        genes_selected = request.params.get('genes_selected')

        nice_gene_names_selected = request.params.get('nice_gene_names_selected')

        filter = {}
        tm_filter  = request.params.get('tm')


        if tm_filter == 'True':
            filter['tm_domain'] = True

        if tm_filter == 'False':
            filter['tm_domain'] = False


        sp_filter  = request.params.get('sp')

        if sp_filter == 'True':
            filter['signal_peptide'] = True

        if sp_filter == 'False':
            filter['signal_peptide'] = False


        # filter_id passed in overrides anything else
        filter_id = request.params.get('filter_id')

        if filter_id is not None:
            new_filter = Stemformatics_Transcript.loadFilter(db,filter_id,c.uid)

            if new_filter is not None:
                filter = new_filter

        c.filter = filter


        describe_filters = "using filters "
        for name in filter:

            output = ""
            first_word_passed = False
            for word in name.split("_"):
                if not word:
                    output += "_"
                    continue
                else:
                    output += word.capitalize() + " "


            new_name = output[:-1]

            describe_filters = describe_filters + " " + new_name + ":" + str(filter[name])

            describe_filters = describe_filters.replace('Tm','Transmembrane')

        if filter_gene_set_id is not None:
            public_uid = 0
            result = Stemformatics_Gene_Set.getGeneSet(db,public_uid,int(filter_gene_set_id))
            describe_filters = describe_filters + ' filtered pathway/gene list: "' + result.gene_set_name + '"'



        order_by = request.params.get('order_by')

        if order_by is None:
            order_by = 'gene_name'


        filter_level = 'Gene'

        base_path = self.StemformaticsQueue + str(job_id) + '/'

        #tx_dict = self._return_tx_dict_for_gene_set_annotations_job(db,job_id,base_path,filter_gene_set_id)
        tx_dict = Stemformatics_Job.read_transcript_data_gene_set_annotation(db,job_id,base_path,filter_gene_set_id)

        result = Stemformatics_Transcript.get_statistics(tx_dict,filter,order_by,filter_level)
        new_tx = result[1]

        print_tx = {}

        if genes_selected is not None:

            gene_list = genes_selected.split(',')

            for gene in new_tx:
                if gene in gene_list:
                    print_tx[gene] = new_tx[gene]
        else:
            print_tx = new_tx

        response.headers['Content-type'] = 'text/tab-separated-values'
        stemformatics_version = config['stemformatics_version']
        response.headers['Content-Disposition'] = 'attachment;filename=export_gene_set_annotation_'+stemformatics_version+'.tsv'
        response.charset= "utf8"

        printout = ''
        firstLine = True
        header = ''

        for gene in print_tx:
            transcripts = new_tx[gene]

            for transcript in transcripts:
                details = transcript[1]
                for data in details:
                    if firstLine == True:
                        header = header + data + "\t"
                    printout = printout + unicode(details[data]) + "\t"

                printout = printout + "\n"
                firstLine = False

        printout = header + "\n" + printout

        return printout






    #---------------------NOT MIGRATED--------------------------------
    def download_gct_file_for_gene_set_wizard(self): #CRITICAL-5

        c.analysis = 6

        gene_set_id  = request.params.get('gene_set_id')
        file_type  = request.params.get('file_type')

        #~ if file_type is None:
            #~ file_type = 'gct'
            #~
        #~ if file_type != 'gct' and file_type != 'txt':
            #~ raise Error
        #~
        c.title = c.site_name+' Analyses - Download Expression Profile Wizard'
        if gene_set_id is None:
            # call a gene list chooser for
            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)

            c.public_result = Stemformatics_Gene_Set.getGeneSets(db,0)

            c.result = result
            c.url = h.url('/workbench/download_gct_file_for_gene_set_wizard')
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/download_gct_file_for_gene_set_wizard'),'Download Expression Profile - Choose Gene List (Step 1 of 3)']]
            return render('workbench/choose_gene_set.mako')

        else:
            gene_set_id = int(gene_set_id)
            species = Stemformatics_Gene_Set.get_species(db,c.uid,gene_set_id)
            gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db,c.uid,gene_set_id)



        dataset_id  = request.params.get('datasetID')

        if dataset_id is None:
            #now get the dataset ID
            c.species = species
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)

            c.url = h.url('/workbench/download_gct_file_for_gene_set_wizard?gene_set_id=')+str(gene_set_id)
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/download_gct_file_for_gene_set_wizard'),'Download Expression Profile - Choose Gene List'],[h.url('/workbench/download_gct_file_for_gene_set_wizard?gene_set_id=')+str(gene_set_id),'Download Expression Profile - Choose Dataset  (Step 2 of 3)']]
            return render('workbench/choose_dataset.mako')
        ds_id = dataset_id

        if file_type is None:

            c.purple_title = 'Choose File Type'
            c.help_text = 'Choose file type to download. You can choose GenePattern file type gct or a simple text file with columns as samples and rows as probes.'
            c.options = {'GCT (GenePattern)':'gct','TXT':'txt'}

            c.url = h.url('/workbench/download_gct_file_for_gene_set_wizard?gene_set_id=')+str(gene_set_id)+'&datasetID='+str(dataset_id)+'&file_type='
            c.breadcrumbs = [[h.url('/genes/search'),'Genes'],[h.url('/workbench/download_gct_file_for_gene_set_wizard'),'Choose Gene List'],[h.url('/workbench/download_gct_file_for_gene_set_wizard?gene_set_id=')+str(gene_set_id),'Choose Dataset '],[h.url('/workbench/download_gct_file_for_gene_set_wizard'),'Download Expression Profile - Choose File Type (Step 3 of 3)']]
            return render('workbench/generic_choose.mako')


        base_path = self.StemformaticsQueue

        chip_type = Stemformatics_Dataset.getChipType(db,dataset_id)

        db_id = Stemformatics_Dataset.get_db_id(db,dataset_id)

        # set some variables
        self.DatasetGCTFiles = config['DatasetGCTFiles']
        d = datetime.now()
        date_string = d.strftime("%Y%m%d%H%M%S%f")
        temp_directory = config['temp_directory_for_download_expression_profile_for_gene_set']

        handle = Stemformatics_Dataset.getHandle(db,dataset_id)

        temp_gct_filename = temp_directory + 'download_expression_profile_gene_set_'+str(gene_set_id)+'_dataset_'+str(dataset_id)+'_'+date_string+'.gct'

        options = []

        if file_type == 'gct':
            download_gct_filename = 'download_expression_profile_gene_set_'+str(gene_set_id)+'_dataset_'+handle+'.gct'

        if file_type == 'txt':
            download_gct_filename = 'download_expression_profile_gene_set_'+str(gene_set_id)+'_dataset_'+handle+'.txt'
            options = ['no_gct_header']


        read_gct_file_name = self.DatasetGCTFiles + 'dataset'+str(dataset_id)+'.gct'


        ref_type = 'gene_set_id'
        ref_id = gene_set_id

        gct_text = Stemformatics_Dataset.build_gct_from_redis(db,ref_type,ref_id,ds_id,c.uid,options)

        response.headers['Content-type'] = 'text/plain'
        stemformatics_version = config['stemformatics_version']
        response.headers['Content-Disposition'] = 'attachment;filename='+download_gct_filename
        response.charset= "utf8"

        return gct_text



    #---------------------NOT MIGRATED--------------------------------
    def _get_inputs_for_gene_neighbour_graph(self):
        geneSearch = FTS_SEARCH_EXPRESSION.to_python(request.params.get('gene'))
        try:
            first_check = request.params.get('ds_id')
            second_check = request.params.get('datasetID')
            if first_check is not None:
                ds_id = int(first_check)
            else:
                ds_id = int(second_check)
        except:
            ds_id = None

        if ds_id is None:
            return redirect(url(controller='contents', action='index'), code=404)


        choose_dataset_immediately = False

        sortBy = request.params.get('sortBy')
        self._temp.geneSearch = geneSearch
        self._temp.graphType = "scatter"
        self._temp.sortBy = "Sample Type"
        self._temp.ds_id = ds_id
        self._temp.choose_dataset_immediately  = choose_dataset_immediately
        self._temp.url = request.environ.get('PATH_INFO')

        self._temp.original_temp_datasets = []
        self._temp.force_choose = False

        if request.environ.get('QUERY_STRING'):
            self._temp.url += '?' + request.environ['QUERY_STRING']
        self._temp.large = request.params.get('size') == "large"


    #---------------------NOT MIGRATED--------------------------------
    def _set_outputs_for_graph(self):
        c.choose_dataset_immediately = self._temp.choose_dataset_immediately
        c.allow_genePattern_analysis = Stemformatics_Dataset.allow_genePattern_analysis(db,self._temp.ds_id)
        c.geneSearch = self._temp.geneSearch
        c.ds_id = self._temp.ds_id
        c.db_id = self._temp.db_id
        if self._temp.ref_type == 'ensemblID':
            c.ensemblID = self._temp.ensemblID
            c.ucsc_links = Stemformatics_Auth.get_ucsc_links_for_uid(db,c.uid,c.db_id)
            c.ucsc_data = Stemformatics_Gene.get_ucsc_data_for_a_gene(db,c.db_id,c.ensemblID)
            c.data = Stemformatics_Gene.get_genes(db,c.species_dict,self._temp.geneSearch,c.db_id,True,None)
            c.symbol = self._temp.symbol
        c.large = self._temp.large
        c.human_db = config['human_db']
        c.mouse_db = config['mouse_db']

        if hasattr(self._temp,'this_view'):
            c.json_view_data = self._temp.this_view.get_json_data()
            c.view_data = self._temp.this_view.view_data

        c.species = Stemformatics_Dataset.returnSpecies(c.db_id)
        c.url = self._temp.url
        c.dataset_status = self._temp.dataset_status
        show_limited = True
        c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited,c.db_id)

    #---------------------NOT MIGRATED--------------------------------
    def fold_change_viewer_wizard(self): #CRITICAL-5

        analysis  = 5
        c.analysis = analysis

        gene_set_id  = 0

        self._temp.ds_id = c.datasetID = ds_id  = request.params.get('datasetID')

        self._temp.gene = c.gene = gene = request.params.get('gene')
        c.title = c.site_name+' Analyses  - Fold Change Viewer Wizard'
        db_id = request.params.get('db_id')
        c.db_id = db_id

        if gene is None:
            # get db_id of dataset
            c.url = h.url('/workbench/fold_change_viewer_wizard')
            c.message = request.params.get('message')
            c.breadcrumb_title = 'Choose Gene for Fold Change Viewer - please enter in a HGNC gene symbol, Ensembl ID, Entrez ID or RefSeq ID in the search provided'
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/fold_change_viewer_wizard'),'Fold Change Viewer - Choose Gene (Step 1 of 2)']]
            return render('workbench/choose_gene.mako')


        select_all_ambiguous = True
        gene_list = []
        gene_list.append(gene)
        get_description = True
        chip_type = None


        result = Stemformatics_Gene.get_genes(db, c.species_dict, gene, db_id, False, None)

        if len(result) ==1 :
            temp_gene = result.itervalues().next()
            c.ensemblID = ensembl_gene_id = temp_gene['EnsemblID']
            c.gene = symbol = temp_gene['symbol']

            c.db_id = db_id = temp_gene['db_id']
        else:
            # get a list together with some more details
            # and then choose
            c.db_id = db_id
            c.analysis = None
            c.show_probes_in_dataset = False
            c.multiple_genes = result

            c.url = h.url('/workbench/fold_change_viewer_wizard?use=')
            c.breadcrumbs = [[h.url('/genes/search'),'Gene Search']]
            return render('workbench/choose_from_multiple_genes.mako')

        if ds_id is None:
            #now get the dataset ID
            c.species = Stemformatics_Gene.get_species_from_db_id(db,db_id)
            show_limited = False
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited, db_id)
            c.breadcrumb_title = 'Choose Dataset for Fold Change Viewer'
            c.url = h.url('/workbench/fold_change_viewer_wizard?db_id='+str(db_id)+'&gene='+str(gene))
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/fold_change_viewer_wizard?datasetID='+str(ds_id)),'Fold Change Viewer - Choose Gene'],[h.url('/workbench/fold_change_viewer_wizard'),'Fold Change Viewer - Choose Dataset (Step 2 of 2)']]
            return render('workbench/choose_dataset.mako')

        c.dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,c.uid)
        if c.dataset_status != "Available":
            return redirect(url(controller='contents', action='index'), code=404)


        available = Stemformatics_Dataset.check_dataset_availability(db,c.uid,ds_id)

        if not available:
            return redirect(url(controller='contents', action='index'), code=404)




        base_path = self.StemformaticsQueue

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # Using bar graph technology to get values back
        self._temp.db_id = db_id
        choose_dataset_immediately = False
        sortBy = request.params.get('sortBy')
        self._temp.geneSearch = gene
        self._temp.graphType = "bar"
        self._temp.sortBy = "Sample Type"
        self._temp.symbol = symbol
        self._temp.ds_id = ds_id
        self._temp.choose_dataset_immediately  = choose_dataset_immediately
        self._temp.url = request.environ.get('PATH_INFO')
        self._temp.original_temp_datasets = []
        self._temp.force_choose = False
        self._temp.large = False
        if request.environ.get('QUERY_STRING'):
            self._temp.url += '?' + request.environ['QUERY_STRING']

        self._temp.dataset_status = available

        self._temp.ref_type = 'ensemblID'
        self._temp.ref_id = self._temp.ensemblID = ensembl_gene_id
        self._temp.line_graph_available = False
        self._temp.this_view = self._setup_graphs(self._temp)
        self._set_outputs_for_graph()


        c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/fold_change_viewer_wizard'),'Fold Change Viewer - Choose Gene'],[h.url('/workbench/fold_change_viewer_wizard?gene='+str(ensembl_gene_id)+'&db_id='+str(db_id)),'Fold Change Viewer - Choose Dataset'],['/','Fold Change Viewer']]

        audit_dict = {'ref_type':'gene_id','ref_id':gene,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)



        return render('workbench/fold_change_viewer.mako')






    @Stemformatics_Auth.authorise(db)
    def gene_neighbour_wizard(self): #CRITICAL-5
        c = self.request.c
        request = self.request
        analysis  = 2
        c.analysis = analysis

        gene_set_id  = 0

        ds_id = dataset_id  = request.params.get('datasetID')
        gene = request.params.get('gene')
        probe = request.params.get('probe')
        c.title = c.site_name+' Analyses  - Gene Neighbourhood Wizard'
        c.use_galaxy_server = use_galaxy = config['use_galaxy_server']

        db_id = request.params.get('db_id')
        c.db_id = db_id

        if gene is None:
            # get db_id of dataset

            c.datasetID = dataset_id
            c.url = h.url('/workbench/gene_neighbour_wizard')
            c.analysis = analysis
            c.message = request.params.get('message')
            c.breadcrumb_title = 'Choose Gene for Gene Neighbourhood - please enter in a HGNC gene symbol, Ensembl ID, Entrez ID or RefSeq ID in the search provided'
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/gene_neighbour_wizard'),'Gene Neighbour - Choose Gene (Step 1 of 2)']]
            return render_to_response('S4M_pyramid:templates/workbench/choose_gene.mako',self.deprecated_pylons_data_for_view,request=self.request)


        select_all_ambiguous = True
        gene_list = []
        gene_list.append(gene)
        get_description = True


        result = Stemformatics_Gene.get_genes(db, c.species_dict, gene, db_id, False, None)

        if len(result) ==1 :
            temp_gene = next(iter(result.values()))
            ensemblID = gene = temp_gene['EnsemblID']
            c.db_id = db_id = temp_gene['db_id']

            # to get name of gene
            for symbol in result:
                c.symbol = result[symbol]['symbol']
        else:
            # get a list together with some more details
            # and then choose
            c.db_id = db_id
            c.analysis = None
            c.show_probes_in_dataset = False
            c.multiple_genes = result

            c.url = h.url('/workbench/gene_neighbour_wizard?use=')
            c.breadcrumbs = [[h.url('/genes/search'),'Gene Search']]
            return render_to_response('S4M_pyramid:templates/workbench/choose_from_multiple_genes.mako',self.deprecated_pylons_data_for_view,request=self.request)





        if dataset_id is None:
            #now get the dataset ID
            c.species = Stemformatics_Gene.get_species_from_db_id(db,db_id)
            show_limited = False
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid,show_limited,db_id)
            c.breadcrumb_title = 'Choose Dataset for Gene Neighbourhood'
            c.url = h.url('/workbench/gene_neighbour_wizard?gene='+str(gene)+'&db_id='+str(db_id))
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/gene_neighbour_wizard'),'Gene Neighbour - Choose Gene '],[h.url('/workbench/gene_neighbour_wizard'),'Gene Neighbour - Choose Dataset (Step 2 of 2)']]
            return render_to_response('S4M_pyramid:templates/workbench/choose_dataset.mako',self.deprecated_pylons_data_for_view,request=self.request)

        c.dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,c.uid)
        if c.dataset_status != "Available":
            return redirect(url(controller='contents', action='index'), code=404)



        chip_type = Stemformatics_Dataset.getChipType(db,dataset_id)

        result = Stemformatics_Gene.get_unique_gene_fast(db,gene_list,db_id,'all',select_all_ambiguous,get_description,chip_type)





        if probe is None:


            # now check that the gene has only one probe
            probes = Stemformatics_Probe.return_probe_information(db,ensemblID,db_id,ds_id)
            len_probes = len(probes)

            if len_probes == 0:
                #now get the dataset ID
                c.error_message = "The dataset you chose does not have a probe that maps to this gene. Please select another dataset."
                c.species = Stemformatics_Gene.get_species_from_db_id(db,db_id)
                show_limited = False
                c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid, show_limited,db_id)
                c.breadcrumb_title = 'Choose Dataset for Gene Neighbourhood'
                c.url = h.url('/workbench/gene_neighbour_wizard?gene='+str(gene)+'&db_id='+str(db_id))
                c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/gene_neighbour_wizard'),'Gene Neighbour - Choose Gene '],[h.url('/workbench/gene_neighbour_wizard'),'Gene Neighbour - Choose Dataset (Step 2 of 2)']]
                return render_to_response('S4M_pyramid:templates/workbench/choose_dataset.mako',
                                          self.deprecated_pylons_data_for_view, request=self.request)

            if len_probes == 1:
                # now go to the next one
                probe = probes[0]['to_id']

            else:
                self._temp.db_id = db_id
                self._get_inputs_for_gene_neighbour_graph()
                self._check_dataset_status()
                self._check_gene_status()

                self._temp.ref_type = 'ensemblID'
                self._temp.ref_id = self._temp.ensemblID
                self._temp.line_graph_available = False
                gene_annotation_names_required = "no"
                chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
                data = Stemformatics_Gene_Set.get_probes_from_genes(db_id,ds_id,[self._temp.ensemblID],gene_annotation_names_required)
                probe_list = data[0]

                c.probe_list = [probe.encode('UTF8') for probe in probe_list]
                c.sorted_probe_list = sorted(c.probe_list)
                # self._temp.this_view = self._setup_graphs(self._temp)
                self._set_outputs_for_graph()

                return render_to_response('S4M_pyramid:templates/workbench/choose_probe_new.mako',
                                          self.deprecated_pylons_data_for_view, request=self.request)



        base_path = self.StemformaticsQueue

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        use_cls = False
        use_gct = True

        # create job here
        options = {}
        options['galaxy_server_url'] = config['galaxy_server_url']

        job_details = { 'analysis': analysis, 'status': 0, 'dataset_id': dataset_id, 'gene_set_id': gene_set_id, 'uid': c.uid, 'use_cls': use_cls, 'use_gct': use_gct, 'gene': gene, 'probe': probe,'options':json.dumps(options)}

        job_id = Stemformatics_Job.create_job(db,job_details)
        if job_id is None:
            return redirect(url(controller='contents', action='index'), code=404)

        if not os.path.exists(base_path+str(job_id)):
            os.mkdir(base_path+str(job_id))

        # create gct_file_path
        gct_file_path = self.StemformaticsQueue + str(job_id) + '/' +'job.gct'
        chip_type= None
        # copy gct file to job directory
        Stemformatics_Expression.create_gct_file_for_analysis(dataset_id,analysis,gct_file_path,chip_type,options,probe)
        datasetGCTFile = config['DatasetGCTFiles']+"dataset"+str(dataset_id)+".gct"
        command = "cp "+datasetGCTFile+ " " +gct_file_path
        p = subprocess.call(command,shell=True)

        # connect to galaxy
        from S4M_pyramid.model.stemformatics.stemformatics_galaxy import Stemformatics_Galaxy
        galaxyInstance = Stemformatics_Galaxy.connect_to_galaxy()

        # run tool
        Stemformatics_Galaxy.run_GN_tool(galaxyInstance,job_id,gct_file_path,c.uid,probe,analysis)

        audit_dict = {'ref_type':'gene_id','ref_id':gene,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        audit_dict = {'ref_type':'ds_id','ref_id':dataset_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return redirect(h.url('/workbench/analysis_confirmation_message/'+str(job_id)))


    #---------------------NOT MIGRATED--------------------------------
    def user_defined_expression_profile(self):
        # CHoose a dataset
        ds_id = request.params.get('datasetID')
        c.analysis=7
        c.species = None
        c.use_galaxy_server = use_galaxy = config['use_galaxy_server']
        if ds_id is None:
            #now get the dataset ID
            c.datasets = Stemformatics_Dataset.getChooseDatasetDetails(db,c.uid)

            c.url = h.url('/workbench/user_defined_expression_profile')
            c.breadcrumbs = [[h.url('/workbench/index'),'Analyses'],[h.url('/workbench/user_defined_expression_profile'),'User Defined Expression Profile - Choose Dataset  (Step 1 of 2)']]
            return render('workbench/choose_dataset.mako')

        c.dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,c.uid)
        if c.dataset_status != "Available":
            return redirect(url(controller='contents', action='index'), code=404)

        show_limited = False
        c.result = Stemformatics_Dataset.getExpressionDatasetMetadata(db,ds_id,c.uid,show_limited)
        try:
            float(c.result['detection_threshold'])
        except:
            c.result['detection_threshold'] = 0

        input_0 = request.params.get('input_0')
        if input_0 is None:

            #might need to get the max and min range for this dataset?
            # choose the profile
            #create the values and store them in the stemformatics.jobs_metadata table
            #might move the values from jobs into the stemformatics.jobs_metadata table from now on.
            # fix remove samples help
            c.url = h.url('/workbench/user_defined_expression_profile?datasetID='+str(ds_id))
            return render('workbench/user_defined_expression_profile.mako')

        options = {}
        options['galaxy_server_url'] = config['galaxy_server_url']

        options['expression_values'] = {}
        sample_type_display_order = c.result['sampleTypeDisplayOrder'].split(',')
        for variable in request.params:
            if 'input' in variable:
                position = int(variable.replace('input_',''))
                sample_type = sample_type_display_order[position]
                options['expression_values'][sample_type] = float(request.params[variable])

        json_options = json.dumps(options)


        gene_set_id = 0
        use_cls = False
        use_gct = True
        gene = 'User'
        probe = 'User'
        job_details = { 'analysis': c.analysis, 'status': 0, 'dataset_id': ds_id, 'gene_set_id': gene_set_id, 'uid': c.uid, 'use_cls': use_cls, 'use_gct': use_gct, 'gene': gene, 'probe': probe, 'options':json_options}
        job_id = Stemformatics_Job.create_job(db,job_details)

        if job_id is None:
            return redirect(url(controller='contents', action='index'), code=404)

        base_path = self.StemformaticsQueue

        if not os.path.exists(base_path+str(job_id)):
            os.mkdir(base_path+str(job_id))

        chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
        # create gct_file_path
        gct_file_path = self.StemformaticsQueue + str(job_id) + '/' +'job.gct'

        # now create gct file
        try:
            Stemformatics_Expression.create_gct_file_for_analysis(ds_id,c.analysis,gct_file_path,chip_type,options,probe)
        except: # this will catch excpetion when GCT file is not created dues to some exception like for dataset 6461 where in sample type column multiple sample types are present
            status = '2'
            reference_id = 'None'
            reference_type = "Galaxy UDEP unable to create GCT file"
            Stemformatics_Job.update_job_status(db,job_id,status, reference_id, reference_type)

            # redirect to 404 as something went wrong and job is not submiteed to galaxy
            return redirect(url(controller='contents', action='index'), code=404)

        # connect to galaxy
        from guide.model.stemformatics.stemformatics_galaxy import Stemformatics_Galaxy
        galaxyInstance = Stemformatics_Galaxy.connect_to_galaxy()

        # run tool
        Stemformatics_Galaxy.run_GN_tool(galaxyInstance,job_id,gct_file_path,c.uid,probe,c.analysis)

        audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return redirect(h.url('/workbench/analysis_confirmation_message/'+str(job_id)))


    @Stemformatics_Auth.authorise(db)
    @action(renderer="templates/workbench/choose_gene_expression_profile.mako")
    def gene_expression_profile_wizard(self):
        c = self.request.c
        c.analysis = 7
        c.title = c.site_name+' Analyses  - Gene Expression Profile Wizard'
        c.url = h.url('/workbench/gene_expression_profile_wizard')
        return self.deprecated_pylons_data_for_view


    #---------------------NOT MIGRATED--------------------------------
    def ucsc(self):
        return render('workbench/ucsc.mako')


    #---------------------NOT MIGRATED--------------------------------
    def download_multiple_datasets(self):
        search= request.params.get('filter')
        export= request.params.get('export')
        ds_ids= request.params.get('ds_ids')
        c.search = search


        if search is not None and search != '':
            get_samples = True
            temp_result = Stemformatics_Dataset.find_datasets_and_samples(search,get_samples,c.uid,g.all_sample_metadata)
            c.datasets = temp_result['datasets']
            c.all_samples = temp_result['all_samples']
            c.all_samples_by_ds_id = temp_result['all_samples_by_ds_id']
            c.all_sample_metadata = g.all_sample_metadata
        else:
            temp_result = None
            c.datasets = None
            c.all_samples = None
            c.all_samples_by_ds_id = None


        if export is not None and c.datasets is not None:
            del response.headers['Cache-Control']
            del response.headers['Pragma']
            stemformatics_version = config['stemformatics_version']
            if export == 'download_script':
                response.headers['Content-type'] = 'text/plain'
                response.headers['Content-Disposition'] = 'attachment;filename=multi_'+export+'.sh'
            else:
                response.headers['Content-type'] = 'text/tab-separated-values'
                response.headers['Content-Disposition'] = 'attachment;filename=export_metadata_'+export+'_'+stemformatics_version+'.tsv'
            response.charset= "utf8"
            data = Stemformatics_Dataset.export_download_dataset_metadata(temp_result,export,ds_ids,g.all_sample_metadata,c.uid,c.user)

            return data


        else:
            if search is not None and search != '':
                audit_dict = {'ref_type':'search_term','ref_id':search,'uid':c.uid,'url':url,'request':request}
                result = Stemformatics_Audit.add_audit_log(audit_dict)

            return render('workbench/download_multiple_datasets.mako')

    #---------------------NOT MIGRATED--------------------------------
    def rohart_msc_test(self):
        return render('workbench/rohart_msc_landing_page.mako')

    #---------------------NOT MIGRATED--------------------------------
    def rohart_msc_graph(self):
        show_limited = False
        c.msc_values_access = config['msc_values_access']
        ds_id  = request.params.get('ds_id',None)
        values = ""
        if ds_id is not None:
            try:
                ds_id = int(ds_id)
                available = Stemformatics_Msc_Signature.get_dataset_msc_access(db,ds_id,c.uid)
                if not available:
                    error_subject = c.title = "Error with accessing MSC Test"
                    error_body = c.message = "There has been an error accessing the dataset it is either unavailable or not an MSC dataset. Please contact the "+c.site_name+" Team."
                    ip_address = request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])
                    error_body += " User was " + c.user + "("+str(c.uid)+") IP:" + ip_address
                    error_subject += " "+str(ds_id)
                    Stemformatics_Notification.send_error_email(error_subject,error_body)
                    return render ('workbench/error_message.mako')

                # check the file exists and error out if not found
                file_name = Stemformatics_Msc_Signature.get_file_name_of_msc_values(ds_id,True)
                if not os.path.isfile(file_name):
                    error_subject = c.title = "Error with accessing MSC Test"
                    error_body = c.message = "There has been an error accessing the file for this dataset. Please contact the "+c.site_name+" Team."
                    ip_address = request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])
                    error_body += " User was " + c.user + "("+str(c.uid)+") IP:" + ip_address
                    error_subject += " "+str(ds_id)
                    Stemformatics_Notification.send_error_email(error_subject,error_body)
                    return render ('workbench/error_message.mako')
            except:
                return redirect(url(controller='contents', action='index'), code=404)
        else:
            ds_id = 6037 # default to an interesting dataset


        c.dataset = Stemformatics_Dataset.getDatasetDetails(db,ds_id,c.uid)

        c.dataset_json = json.dumps(c.dataset)
        c.ds_id = ds_id

        audit_dict = {'ref_type':'ds_id','ref_id':ds_id,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return render('workbench/rohart_msc_graph.mako')
