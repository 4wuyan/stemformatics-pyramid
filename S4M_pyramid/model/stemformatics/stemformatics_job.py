#TODO-1
import logging
log = logging.getLogger(__name__)

from sqlalchemy import or_, and_, desc

import json
from datetime import datetime, timedelta



from S4M_pyramid.lib.deprecated_pylons_globals import config,url,magic_globals
from S4M_pyramid.model.stemformatics import Stemformatics_Dataset,Stemformatics_Gene_Set
import formencode.validators as fe
import os, subprocess
import psycopg2
import psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

SUBSCRIBER_NAME = fe.Regex("[\w ]*", not_empty=False, if_empty="Anonymous User")
SUBSCRIBER_STATE = fe.Regex("[\w ]*", not_empty=False, if_empty="PENDING")
DESCRIPTIVE_TEXT = fe.Regex("[\w ]*", not_empty=False, if_empty="")
POS_INT = fe.Int(min=1, not_empty=True)
NUMBER = fe.Number(not_empty=True)
IDENTIFIER = fe.PlainText(not_empty=True)
URL = fe.URL(not_empty=True)

analysis = {0: {'name': 'Hierarchical Cluster' , 'description': 'Hierarchical clustering groups genes and samples to highlight co-regulated gene lists.'},
            1: {'name': 'Comparative Marker Selection' , 'description':'Comparative marker selection shows you which of your genes of interest are most differentially expressed in distinct phenotypes within a study.'},
            2: {'name': 'Gene Neighbourhood' ,'description':'This analysis will find genes that share a similar expression profile for your gene of interest across samples within a given study.'},
            4: {'name': 'Gene List Annotation' , 'description':'This will annotate your gene list.'},
            5: {'name': 'Fold Change Viewer' , 'description':'This will view your fold change.'},
            6: {'name': 'Download Gene List Expression Profile' , 'description':'Download the expression profile for a gene list and dataset.'},
            7: {'name': 'User Defined Expression Profile' , 'description':'Find your own expression profile for a dataset.'}
            }


status = {0: 'Pending', 1: 'Finished', 2: 'Error',3:'Deleted'}

# have to easy_install numpy and fisher
from fisher import pvalue

def get_status_by_name(status):
    status_by_name = {}
    for status_id in status:
        name = status[status_id]
        status_by_name[name]=status_id
    return status_by_name

status_by_name = get_status_by_name(status)

class Stemformatics_Job(object):
    """\
    Stemformatics_Job Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for job related data

    Please note for most of these functions you will have to pass in the db object

    All functions have a try that will return None if errors are found

    """

    def __init__ (self):
        pass


    @staticmethod
    def return_all_analysis():
        return analysis

    @staticmethod
    def return_all_analysis_by_name():
        analysis_by_name = {}
        for analysis_id in analysis:
            name = analysis[analysis_id]['name']
            description = analysis[analysis_id]['description']
            analysis_by_name[name] = {'analysis_id': analysis_id,'description':description}
        return analysis_by_name

    @staticmethod
    def return_all_status():
        return status

    @staticmethod
    # job_details = { 'analysis': analysis, 'status': 0, 'dataset_id': dataset_id, 'gene_set_id': gene_set_id, 'uid': c.uid, 'use_cls': True, 'use_gct': True}
    def create_job(db,job_details): #CRITICAL-2
        try:
            db.schema = 'stemformatics'

            if 'comparison_type' not in job_details:
                job_details['comparison_type'] = ''

            if 'options' not in job_details:
                job_details['options'] = ''
                temp_job_options = {}
            else:
                temp_job_options = json.loads(job_details['options'])

            base_url = url("/", qualified=True)
            temp_job_options['base_url'] = base_url
            job_details['options'] = json.dumps(temp_job_options)


            result = db.jobs.insert(analysis=job_details['analysis'],status=job_details['status'],dataset_id=job_details['dataset_id'],gene_set_id=job_details['gene_set_id'],uid=job_details['uid'],use_cls=job_details['use_cls'],use_gct=job_details['use_gct'],gene=job_details['gene'], probe=job_details['probe'], comparison_type = job_details['comparison_type'], options=job_details['options'])

            db.commit()
            db.flush()
            return result.job_id
        except:
            return None
    @staticmethod
    def get_GN_data_from_output_file(text, p_value, analysis_server):
        result = {}
        return_data = {}
        data = False
        zScoreInputMean = []
        zScoreInputFoldChange = []
        listProbesInOrderODF = []
        fdr_bh_limit = p_value

        if analysis_server == "GenePattern":
            for line in text:
        # because this is in order, as soon as you have something that doesn't have the cut off then break out of the loop
                if data:
                    splitTemp = line.split('\t')
                    probeName = splitTemp[0]
                    score = splitTemp[2]
                    temp_score = score.split('\n')

                    score = float(temp_score[0])

                    if score <= fdr_bh_limit and temp_score[0] != '-Infinity':
                        listProbesInOrderODF.append(probeName)
                        result[probeName] = {'score': score}


                if line.find('DataLines') != -1:
                    data = True
        # for Galaxy
        else:
            firstline = True
            for line in text:
                if firstline:    #skip first line
                    firstline = False
                    continue
                splitTemp = line.split('\t')
                probeName = splitTemp[0]
                temp_score = splitTemp[1]
                # when empty value found
                if temp_score != "":
                    score = float(temp_score)
                    score = 1- score # need to substract coorelation value from 1 to match gene pattern result
                    if score <= fdr_bh_limit and temp_score != '-Infinity':
                        listProbesInOrderODF.append(probeName)
                        result[probeName] = {'score': score}

        return_data["listProbesInOrderODF"] = listProbesInOrderODF
        return_data["result"] = result
        return return_data

    @staticmethod
    def get_job_view_result_for_HC(job_details):
        result = {} #this will store all the results taht needs to be returned
        HC_server = job_details.reference_type
        StemformaticsQueue = config['StemformaticsQueue']
        GPQueue = config['GPQueue']
        db= None

        if HC_server != "GenePattern":
            path = StemformaticsQueue +str(job_details.job_id) + "/"
            dirList = os.listdir(path)
            openFile = path + "na_rows.txt"
        else:
            path = GPQueue+str(job_details.reference_id) + "/"
            dirList = os.listdir(path)
            openFile = path + "hc.cdt"

        pngFile = path + "hc.png"

        if not os.path.isfile(pngFile) or not os.path.isfile(openFile):
            return "Files not found"

        f = open(openFile,'r')
        text = f.readlines()
        if HC_server != "GenePattern":
            text = json.loads(text[0]) # converts the string to python dict that can be used in mako
        result["text"] = text
        f.close()

        try:
            options = json.loads(job_details.options)
        except:
            options = {}

        text_remove_sample_ids = "No Samples Removed"
        if 'remove_chip_ids' in options:
            remove_chip_ids = options['remove_chip_ids']
            if remove_chip_ids != []:
                chip_type = Stemformatics_Dataset.getChipType(job_details.dataset_id)
                text_remove_sample_ids = []
                for chip_id in remove_chip_ids:
                    text_remove_sample_ids.append(g.all_sample_metadata[chip_type][chip_id][job_details.dataset_id]['Replicate Group ID'])
                text_remove_sample_ids = ",".join(text_remove_sample_ids)

        cluster_type = "None"
        if 'cluster_type' in options:
            cluster_type  = options['cluster_type']


        if 'colour_by' in options:
            colour_by = options['colour_by']
            if colour_by == 'row':
                colour_by = 'Row z-scores'
            else:
                colour_by = 'Entire dataset values'

        db = None
        result["db_id"] = db_id = Stemformatics_Dataset.get_db_id(job_details.dataset_id)
        result["colour_by"] = colour_by
        result["cluster_type"] = cluster_type
        result["text_remove_sample_ids"] = text_remove_sample_ids
        return result

    @staticmethod
    def get_job_details_check_user(db,job_id,uid): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            where = and_(db.jobs.job_id == job_id,db.jobs.uid == uid,db.jobs.status != 3)
            result = db.jobs.filter(where).one()
            return result
        except:
            return None

    @staticmethod
    def get_job_details(db,job_id): #CRITICAL-2
        db.schema = 'stemformatics'
        try:
            result = db.jobs.filter(and_(db.jobs.job_id == job_id,db.jobs.status!=3)).one()
            return result
        except:
            return None


    @staticmethod
    def get_job_details_with_gene_set(db,job_id): #CRITICAL-2
        try:
            db.schema = 'public'
            ds = db.datasets

            db.schema = 'stemformatics'
            # wrap the db so that column with the same name can be distinguished
            gs = db.with_labels(db.gene_sets)
            initial_result = db.jobs.filter(db.jobs.job_id == job_id).one()
            if initial_result.dataset_id != 0:
                #note that gs.id now needs to be gs.stemformatics_gene_sets_id,because of the prefix
                join1 = db.join(db.jobs,gs,gs.stemformatics_gene_sets_id==db.jobs.gene_set_id,True)

                join2 = db.join(join1,ds,ds.id==db.jobs.dataset_id)

                result = join2.filter(db.jobs.job_id == job_id).one()
            else:
                join1 = db.join(db.jobs,gs,gs.id==db.jobs.gene_set_id,True)
                result = join1.filter(db.jobs.job_id == job_id).one()

            return result
        except:
            return None

    # changed to psycopg2
    @staticmethod
    def update_job(db,job_id,job_details): #CRITICAL-2
        try:
            if 'reference_type' not in job_details:
                job_details['reference_type'] = None
            if 'reference_id' not in job_details:
                job_details['reference_id'] = None
            if 'finished' not in job_details:
                job_details['finished'] = None

            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "update stemformatics.jobs set reference_type = %s , reference_id = %s , finished = %s , status = %s where job_id = %s;"
            cursor.execute(sql, (job_details['reference_type'], job_details['reference_id'], job_details['finished'], job_details['status'], job_id))

            # retrieve the records from the database
            cursor.close()
            conn.commit()
            conn.close()

            return True
        except:
            return None

    """ api/update_job controller action is being moved under this method
        so that it can be called from workbench controller when job status is to be updated
    """
    @staticmethod
    def update_job_status(db,job_id, status, reference_id, reference_type):
        magic_globals.fetch()
        c = magic_globals.c

        job_details = {}
        if status is not None:
            job_details['status'] = status
            job_details['finished'] = datetime.now()

        if reference_type is not None:
            job_details['reference_type'] = reference_type
            job_details['reference_id'] = reference_id
        if job_details != {}:
            from S4M_pyramid.model.stemformatics.stemformatics_notification import Stemformatics_Notification
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



                        body = "Congratulations, your job #%s has been completed, you have 30 days until it expires and is removed from the system.\n\n Click here to view result: %s \n\n To stop receiving these emails click here: %s" % (str(job_id),new_url,external_base_url+url('auth/unsubscribe_job_notification/'+str(user.uid)) )

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
                    subject = c.site_name+" - Job Error #%s" % (str(job_id)) + " on " + hostname


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
    @staticmethod
    def get_pending_jobs_in_s4m():
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from stemformatics.jobs where status = %(status)s;",{"status":0})
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result
    # the output of get_old_jobs gets passed into here  - it is a list of psycopg2 objects/dicts
    # jobs = Stemformatics_Job.get_old_jobs(db,before_cutoff_time)
    @staticmethod
    def bulk_delete_job(jobs): #CRITICAL-2
        job_deletion_list = []
        galax_job_list = []
        for job in jobs:

            job_id = job['job_id']
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from stemformatics.jobs where job_id = %(job_id)s;",{"job_id":job_id})
            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            if len(result) == 1:
                ref_type = result[0]['reference_type']
                ref_id = result[0]['reference_id']
                if ref_type == "GenePattern":
                    gene_pattern_dir = config['GPQueue']
                    gene_pattern_id = ref_id
                    command_line = "rm -fR " + gene_pattern_dir + gene_pattern_id + "/"
                    p = subprocess.Popen(command_line,shell=True)
                elif ref_type == "Galaxy HC":
                    # create job list for galaxy jobs
                    galax_job_list.append(job_id)

                job_dir = config['StemformaticsQueue']
                command_line = "rm -fR " + job_dir + str(job_id) + "/"
                p = subprocess.Popen(command_line,shell=True)
                job_deletion_list.append(job_id)

            else:
                return None
        # now clean up files for the galaxy jobs in galaxy
        from S4M_pyramid.model.stemformatics.stemformatics_galaxy import Stemformatics_Galaxy
        galaxyInstance = Stemformatics_Galaxy.connect_to_galaxy()
        import socket
        server_name = socket.gethostname()
        Stemformatics_Galaxy.delete_bulk_jobs(galaxyInstance, galax_job_list, server_name)

        log.debug('finished the append')

        if len(job_deletion_list) != 0:
            job_deletion_list_string = ",".join(map(str,job_deletion_list))
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("update stemformatics.jobs set status = 3 where job_id in ("+job_deletion_list_string+");")
            cursor.close()
            conn.commit()
            conn.close()
            return "OK"
        else:
            return None

    @staticmethod
    def delete_job(db,job_id,uid): #CRITICAL-2
        try:
            job_id = int(job_id)
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from stemformatics.jobs where job_id = %(job_id)s;",{"job_id":job_id})
            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            if len(result) == 1:
                if "reference_type" in result:
                    if result.reference_type == "GenePattern":
                        gene_pattern_dir = config['GPQueue']
                        gene_pattern_id = result.reference_id
                        command_line = "rm -fR " + gene_pattern_dir + gene_pattern_id + "/"
                        p = subprocess.Popen(command_line,shell=True)

                job_dir = config['StemformaticsQueue']
                command_line = "rm -fR " + job_dir + str(job_id) + "/"
                p = subprocess.Popen(command_line,shell=True)

                conn_string = config['psycopg2_conn_string']
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("update stemformatics.jobs set status = 3 where job_id = %(job_id)s;",{"job_id":job_id})
                # retrieve the records from the database
                cursor.close()
                conn.commit()
                conn.close()
                return result
            else:
                return None
        except Exception as e:
            return None

    @staticmethod
    def get_user_from_job_id(db,job_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'

            result = db.jobs.filter(db.jobs.job_id == job_id).one()

            from S4M_pyramid.model.stemformatics.stemformatics_auth import Stemformatics_Auth # wouldn't work otherwise??
            user = Stemformatics_Auth.get_user_from_uid(db,result.uid)

            return user
        except:
            return None

    @staticmethod
    def get_datasetId_from_job_id(db,job_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'

            result = db.jobs.filter(db.jobs.job_id == job_id).one()

            return result.dataset_id
        except:
            return None

    @staticmethod
    def write_transcript_data_gene_set_annotation(db,file_name,tx_dict):

        f = open(file_name, 'w')

        for gene_id,row in tx_dict.iteritems():
            row_array = []
            for key_details,value in row.iteritems():
                row_array.append(str(value))

            raw_line = gene_id + "\t" + "\t".join(row_array)+"\n"

            f.write(raw_line)

        f.close()
        return True



    """
        The filter gene list id is needed as you want to build the tx_dict with only limited genes from the gene list
    """
    @staticmethod
    def read_transcript_data_gene_set_annotation(db,job_id,base_path,filter_gene_set_id):

        file_name = base_path + 'job.tsv'

        f = open(file_name,'r')

        """
            Want back in this format
            {u'ENST00000001008': {'gene_id': u'ENSG00000004478', 'gene_name': u'FKBP4', 'protein_length': 459, ' signal_peptide': False, 'targeted_mirna': False, 'tm_domain': False, 'transcript_name': u'FKBP4-001'}
            from this format
            ENST    SP  MiRNA  ProteinLength   GeneID  TranscriptName   TM  GeneName
            ENST00000265631 False   False   675     ENSG00000004864 SLC25A13-001    False   SLC25A13
            ENST00000457146 False   False   62      ENSG00000010626 LRRC23-007      False   LRRC23
            ENST00000007516 False   False   156     ENSG00000004779 NDUFAB1-001     False   NDUFAB1
            ENST00000455230 True    False   137     ENSG00000003509 C2orf56-011     False   C2orf56


        """

        # have to check if there is a gene pathways specified as a filter
        if filter_gene_set_id is not None:
            public_uid = 0
            filter_gene_set_id = int(filter_gene_set_id)
            result = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db,public_uid,filter_gene_set_id)

            raw_genes = result[1]
            filter_gene_set_id_genes = [ gene.gene_id for gene in raw_genes]




        tx_dict = {}
        for line in f:
            line = line.replace('\n','')
            row = line.split('\t')
            tx_id = row[0]
            sp = row[1] == 'True'
            mirna = row[2] == 'True'
            protein_length = int(row[3])
            gene_id = row[4]
            tx_name = row[5]
            tm = row[6] == 'True'
            gene_name = row[7]

            if filter_gene_set_id is not None:
                if gene_id not in filter_gene_set_id_genes:
                    continue

            tx_dict[tx_id] = {'gene_id': gene_id, 'gene_name': gene_name, 'protein_length': protein_length, 'signal_peptide': sp, 'targeted_mirna': mirna, 'tm_domain': tm, 'transcript_name': tx_name}

        return tx_dict




    @staticmethod
    def write_gene_pathways_gene_set_annotation(file_name,gene_list,dict_gene_names):

        f = open(file_name, 'w')
        dict_pathway = {}
        gene_pathways_list = []
        for gene_id in gene_list:

            gene_sets = gene_list[gene_id]

            raw_line = gene_id + "\t" + "\t".join(gene_sets)+"\n"
            f.write(raw_line)

            for gene_set in gene_sets:

                if gene_set not in dict_pathway:
                    dict_pathway[gene_set] = []
                    gene_pathways_list.append(gene_set)

                dict_pathway[gene_set].append(dict_gene_names[gene_id])


        f.close()
        return [dict_pathway,gene_pathways_list]


    @staticmethod
    def write_gene_pathways_export_gene_set_annotation(file_name,dict_pathway,dict_gene_set_details,gene_set_counts,genes_in_gene_set_count,total_number_genes):

        f = open(file_name,'w')
        header = "InternalID\tPathway Name\t#Genes\tFisher Exact Test\tIndividual Genes\n"
        f.write(header)
        for pathway in dict_pathway:

            pathway_name = dict_gene_set_details[pathway].gene_set_name

            # genes_in_gene_set_count already calculated
            # total_number_genes already calculated
            genes_found_in_pathway = len(dict_pathway[pathway])
            genes_count_in_pathway = gene_set_counts[pathway]

            genes_not_found_in_pathway = genes_in_gene_set_count - genes_found_in_pathway
            genes_in_genome_not_in_pathway = total_number_genes - genes_count_in_pathway

            # test_string = str(genes_found_in_pathway) + "\t" + str(genes_count_in_pathway) + "\t" +str(genes_not_found_in_pathway) + "\t" +str(genes_in_genome_not_in_pathway) + "\t"

            p_value_fisher = pvalue(genes_found_in_pathway,genes_count_in_pathway,genes_not_found_in_pathway,genes_in_genome_not_in_pathway)

            raw_line = str(pathway)+ "\t" + pathway_name + "\t" + str(genes_found_in_pathway)+ "\t" + str(p_value_fisher.right_tail)+ "\t" + "\t".join(dict_pathway[pathway])+"\n"
            f.write(raw_line)

        f.close()


    @staticmethod
    def read_gene_pathways_gene_set_annotation(file_name,new_genes):
        f = open(file_name,'r')

        gene_pathways_list = []
        for line in f:
            line = line.replace('\n','')
            row_list = line.split('\t')
            gene_id = row_list[0]

            if gene_id in new_genes:
                for temp_gene_set_id in row_list[1:]:
                    if temp_gene_set_id not in gene_pathways_list:
                        gene_pathways_list.append(temp_gene_set_id)

        f.close()

        return gene_pathways_list


    @staticmethod
    def read_gene_pathways_export_gene_set_annotation(file_name):
        f = open(file_name,'r')

        pathway_statistics = {}
        header = True

        for line in f:
            if header == True:
                header = False
                continue
            line_values = line.split("\t")
            temp_gene_set_id = line_values[0]
            genes_found_in_pathway = line_values[2]
            fisher_exact_pvalue = line_values[3]
            pathway_statistics[temp_gene_set_id] = {'genes_found_in_pathway': genes_found_in_pathway, 'fisher_exact_pvalue': fisher_exact_pvalue }

        f.close()
        return pathway_statistics

    @staticmethod
    def read_gene_pathways_export_gene_set_annotation_raw(file_name):
        f = open(file_name,'r')
        printout = ""
        for line in f:
            printout = printout + line

        return printout


    @staticmethod
    def get_pending_jobs(db): #CRITICAL-2
        db.schema = 'stemformatics'
        jobs = db.jobs

        result = jobs.filter(jobs.status==0).all()

        return result

    @staticmethod
    def get_old_jobs(db,before_cutoff_time): #CRITICAL-2

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from stemformatics.jobs where status != 3 and created <= %(before_cutoff_time)s;",{"before_cutoff_time":before_cutoff_time})
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        #result = jobs.filter(jobs.created <= before_cutoff_time).all()

        return result

    @staticmethod
    def get_new_jobs(db,after_cutoff_time): #CRITICAL-2
        db.schema = 'stemformatics'
        jobs = db.jobs
        user = db.users
        join1 = db.join(jobs,user,jobs.uid == user.uid)

        result = join1.filter(jobs.created >= after_cutoff_time).all()

        return result

    @staticmethod
    def get_jobs_created_between(db, begin_date, end_date): #CRITICAL-2
        db.schema = 'stemformatics'
        jobs = db.jobs

        result = jobs.filter(and_(jobs.created >= begin_date, jobs.created < end_date)).all()

        return result

    @staticmethod
    def get_jobs_for_user(db,uid):
        try:
            uid = int(uid)
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            sql = "select * from stemformatics.jobs as j left join stemformatics.gene_sets as g on g.id = j.gene_set_id left join datasets as d on d.id = j.dataset_id where j.uid = %s and j.status != 3"
            data = (uid,)
            cursor.execute(sql,data)

            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            return result



        except:
            return None

    @staticmethod
    def get_shared_jobs_for_user(db,uid):
        try:
            uid = int(uid)
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select * from stemformatics.shared_resources as sr left join stemformatics.users as u on u.uid = sr.from_uid left join stemformatics.jobs as j on j.job_id = sr.share_id left join stemformatics.gene_sets as g on g.id = j.gene_set_id left join datasets as d on d.id = j.dataset_id where j.status != 3 and sr.share_type = 'Job' and sr.to_uid = %s"
            data = (uid,)
            cursor.execute(sql,data)

            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            return result
        except:
            return None

    @staticmethod
    def get_job(db,job_id): #CRITICAL-2
        db.schema = 'stemformatics'
        jobs = db.jobs
        result = jobs.filter(jobs.job_id == job_id).one()
        return result

    @staticmethod
    def check_shared_user_can_access_dataset(db,job_id,uid): #CRITICAL-2
        db.schema = 'stemformatics'
        jobs = db.jobs



        result = jobs.filter(jobs.job_id == job_id).all()
        if len(result) != 1:
            return False
        else:
            ds_id = result[0].dataset_id
            if ds_id != 0:
                return Stemformatics_Dataset.check_dataset_availability(db,uid,ds_id)
            else:
                return True

    @staticmethod
    def get_last_job_for_user(uid,analysis_id):
        try:
            uid = int(uid)
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            sql = "select job_id from stemformatics.jobs where analysis = %s and uid = %s and status = %s order by job_id desc limit 1;"
            data = (analysis_id,uid,status_by_name['Finished'],)
            cursor.execute(sql,data)

            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            return result[0][0]



        except:
            return None

    # method used by api created for RDS Monitoring of when we moved the HC processing to Galaxy
    @staticmethod
    def get_hc_stats_from_s4m_db(start_date,end_date):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select count(job_id),count(distinct uid),count(distinct dataset_id) from stemformatics.jobs where created >=%(start_date)s and finished <= %(end_date)s and reference_type = 'Galaxy HC' and analysis = 0;",{"start_date":start_date,"end_date":end_date})
        # retrieve the records from the database
        result_selected = cursor.fetchall()
        cursor.close()
        conn.close()
        stats = {}
        # data returned for selected date criteria
        stats['selected'] = {}
        stats['selected']['start_date'] =start_date
        stats['selected']['end_date'] =end_date
        stats['selected']['jobs'] = {}
        stats['selected']['datasets'] = result_selected[0][2]
        stats['selected']['jobs']['microarray'] = 0
        stats['selected']['jobs']['non_microarray'] = 0
        stats['selected']['jobs']['total'] = result_selected[0][0]
        stats['selected']['users'] = result_selected[0][1]

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select j.job_id, p.platform_type from stemformatics.jobs as j join datasets as d on d.id = j.dataset_id join assay_platforms as p on p.chip_type = d.chip_type where j.reference_type = 'Galaxy HC' and j.analysis = 0 and j.created >=%(start_date)s and j.finished <= %(end_date)s;",{"start_date":start_date,"end_date":end_date})
        # retrieve the records from the database
        dataset_breakdown_result = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in dataset_breakdown_result:
            platform_type = row['platform_type']
            if platform_type == 'microarray':
                stats['selected']['jobs']['microarray'] += 1
            else:
                stats['selected']['jobs']['non_microarray'] += 1

        return stats
