#-------Last synchronised with Pylons repo (master) on---------------#
#------------------------19 Feb 2018---------------------------------#
#-------------------------by WU Yan----------------------------------#
#TODO-1
import logging

log = logging.getLogger(__name__)
from pyramid_handlers import action
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, app_globals as g, config
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
from S4M_pyramid.lib.base import BaseController
from pyramid.renderers import render_to_response
import S4M_pyramid.lib.helpers as h

import json

# Live querying
from S4M_pyramid.model.stemformatics import *

import re,os.path,subprocess

from sqlalchemy.exc import *


class DatasetsController(BaseController):
    __name__ = 'DatasetsController'


    def __init__(self,request):
        super().__init__(request)
        c = self.request.c
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db


        self.default_human_dataset = int(config['default_human_dataset'])
        self.default_mouse_dataset = int(config['default_mouse_dataset'])

    #---------------------NOT MIGRATED--------------------------------
    def pca(self):
        c.ds_id = request.params.get("ds_id")
        pca_type = request.params.get("pca_type")
        c.title = pca_type.replace("_"," ")
        # check if user has access to dataset
        status = Stemformatics_Dataset.check_dataset_with_limitations(db,c.ds_id,c.uid)
        if status == "Available":
            c.pca_type = request.params.get("pca_type")
            c.all_pca_types = Stemformatics_Dataset.get_pca_types_for_dataset(c.ds_id)
            return render('/datasets/pca.mako')
        else:
            redirect(url(controller='contents', action='index'), code=404)

    #---------------------NOT MIGRATED--------------------------------
    def return_pca_data(self):
        file_name = request.params.get("file_name")
        c.ds_id =ds_id = request.params.get("ds_id") # check if user has access to data
        status = Stemformatics_Dataset.check_dataset_with_limitations(db,c.ds_id,c.uid)
        if status == "Available":
            pca_type = request.params.get("pca_type")
            data  = Stemformatics_Dataset.return_pca_data_files(ds_id,pca_type,file_name)
            return data
        else:
            redirect(url(controller='contents', action='index'), code=404)

    def search(self):
        c = self.request.c
        request = self.request
        response = self.request.response
        c.msc_values_access = config['msc_values_access']
        c.searchQuery = request.params.get("filter", None)

        if c.searchQuery:
            c.searchQuery = c.searchQuery.replace('<script>','').replace('</script>','')

        c.title = c.site_name+" - Dataset Search"
        ds_id = request.params.get("ds_id", None)
        c.selected_ds_id = False
        c.db_id = None
        c.dataset_status = ''

        if ds_id is not None and (c.searchQuery is None and c.searchQuery != ""):
            c.searchQuery = ds_id

        if ds_id is not None:
            db=None # this is not used at the moment
            dataset_status = Stemformatics_Dataset.check_dataset_with_limitations(db,ds_id,c.uid)
            if dataset_status == "Unavailable":
                return redirect(url(controller='contents', action='index'), code=404)
            if dataset_status == "Limited": # always show limited datasets
                pass

            ds_id = int(ds_id)
            c.ds_id = int(ds_id)
            dict_of_ds_ids = {}
            dict_of_ds_ids[ds_id] = {'dataset_status':dataset_status}
            format_type = 'front_end'
            c.dataset = Stemformatics_Dataset.get_dataset_metadata(dict_of_ds_ids,format_type)
            c.selected_ds_id = True
            # set the dataset data from the chosen ds_id into redis
            if c.dataset[ds_id]['has_data'] == 'yes':
                dataset_metadata = Stemformatics_Dataset.get_expression_dataset_metadata(ds_id)
            try:
                c.dataset_status = c.dataset[ds_id]['dataset_status']
            except:
                return redirect(url(controller='contents', action='index'), code=404)
            c.db_id = Stemformatics_Dataset.get_db_id(db,ds_id)
        else:
            c.ds_id = None
            c.datasets = None
            c.dataset = None
            c.selected_ds_id = False
        if c.selected_ds_id:
            c.header = Stemformatics_Notification.get_header_name_from_datasetId(c.ds_id)

        export = request.params.get("export",None)
        if export is None:
            if c.ds_id is not None:
                audit_dict = {'ref_type':'ds_id','ref_id':c.ds_id,'uid':c.uid,'url':url,'request':request}
                result = Stemformatics_Audit.add_audit_log(audit_dict)
            return render_to_response('S4M_pyramid:templates/datasets/search.mako',self.deprecated_pylons_data_for_view,request=self.request)
        else:
            # Task #396 - error with ie8 downloading with these on SSL
            response.headers.pop('Cache-Control', None)
            response.headers.pop('Pragma', None)

            response.headers['Content-type'] = 'text/tab-separated-values'
            stemformatics_version = config['stemformatics_version']
            response.headers['Content-Disposition'] = 'attachment;filename=export_stemformatics_'+stemformatics_version+'.tsv'
            response.charset= "utf8"
            ds_id = request.params.get("ds_id", None)

            if ds_id is not None:
                datasets = c.dataset
            else:
                filter_dict = {'show_limited':False,'rohart_msc_test':False}
                datasets = Stemformatics_Dataset.dataset_search(c.uid,c.searchQuery, filter_dict)

            data = self._convert_datasets_to_csv(ds_id,datasets)
            response.text = data
            return response

    #---------------------NOT MIGRATED--------------------------------
    def _convert_datasets_to_csv(self,ds_id,datasets):
        csv_text ="Title	Handle	Cells	Authors	PubmedID	Array Express	GEO	Genes of Interest	Contact Name	Contact Email	Affiliation	Platform	SRA	PXD	ENA\n"
        if datasets is None:
            return csv_text

        for temp_ds_id in datasets:
            if ds_id is not None and int(ds_id) != temp_ds_id:
               continue
            temp_row = datasets[temp_ds_id]
            title = temp_row['title']
            handle = temp_row['handle']
            cells_assayed = temp_row['cells_samples_assayed']
            authors =  temp_row['authors']
            description =  temp_row['description']
            pubmed_id =  temp_row['pub_med_id']
            AE =  temp_row['ae_accession_id']
            GEO =  temp_row['geo_accession_id']
            SRA =  temp_row['sra_accession_id']
            PXD =  temp_row['pxd_accession_id']
            ENA =  temp_row['ena_accession_id']
            genes_of_interest = temp_row['top_diff_exp_genes']
            if isinstance(genes_of_interest, dict):
                genes = []
                for symbol in genes_of_interest:
                    gene = genes_of_interest[symbol]['ensemblID']
                    genes.append(gene)
                genes_of_interest = ",".join(genes)

            contact_name = temp_row['name']
            contact_email =  temp_row['email']
            affiliation = temp_row['affiliation']
            platform =  temp_row['platform']
            probes_detected =  temp_row['probes detected']
            probes =  temp_row['probes']

            csv_text += title + "	" + handle + "	" + cells_assayed + "	" + authors + "	" + pubmed_id + "	" + AE + "	" + GEO + "	" + genes_of_interest + "	" + contact_name + "	" + contact_email + "	" + affiliation + "	" + platform + "	" + SRA + "	" + PXD    + "	" + ENA + "\n"
        return csv_text

    #---------------------NOT MIGRATED--------------------------------
    def view(self,id):
        c.title = c.site_name+" - Dataset Summary"
        ds_id = c.ds_id = int(id)
        redirect('/datasets/search?ds_id='+str(ds_id))


    #---------------------NOT MIGRATED--------------------------------
    def summary(self):
        c.title = c.site_name+" - Dataset Summary"
        try:
            ds_id = c.ds_id = int(request.params.get("datasetID", None))
        except:
            try:
                ds_id = c.ds_id = int(request.params.get("ds_id", None))
            except:
                redirect(url(controller='contents', action='index'), code=404)

        redirect('/datasets/search?ds_id='+str(ds_id))

   # Used in datasets/search for now
    #---------------------NOT MIGRATED--------------------------------
    def get_details(self):

        dataSets = Stemformatics_Dataset.getAllDatasetDetails(db,c.uid)
        if (dataSets == None): redirect(url(controller='contents', action='index'), code=404)
        return json.dumps(dataSets)

    #---------------------NOT MIGRATED--------------------------------
    def download_yugene(self,id):
        ds_id = int(id)

        export_key = request.params.get("export_key", None)
        username = request.params.get("username", None)
        if export_key is not None and username is not None and username is not u'':
            user = Stemformatics_Auth.get_user_from_username(db,username)
            uid = user.uid
            has_access = Stemformatics_Dataset.check_dataset_availability_by_export_key(db,uid,export_key,ds_id)
            if not has_access:
                redirect(url(controller='contents', action='index'), code=404)
            else:
                permission_used = 'export_key'
                log_uid = uid
        else:
            has_access = Stemformatics_Dataset.check_dataset_availability(db,c.uid,ds_id)
            if not has_access:
                redirect(url(controller='contents', action='index'), code=404)
            else:
                permission_used = 'logged_in'
                log_uid = c.uid




        download_type = 'Yugene'
        ip_address = request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])
        result = Stemformatics_Dataset.audit_download_dataset(log_uid,ds_id,download_type,ip_address,permission_used)

        # read in the file
        file_name = config['x_platform_base_dir'] + 'dataset'+str(ds_id)+'.cumulative.txt'
        temp_file_name = config['DatasetTempGCTFiles'] + 'dataset'+str(ds_id)+'.tmpyugene'

        if os.path.isfile(file_name):
            sample_labels = Stemformatics_Expression.get_cumulative_sample_labels(ds_id)
            initial_header="Probe ID"
            new_header = Stemformatics_Expression.return_gct_file_sample_headers_as_replicate_group_id(db,ds_id,sample_labels,[],initial_header)

            new_header = new_header.replace("\n","")
            # changes for task 2563
            # http://stackoverflow.com/questions/28714142/getting-error-sed-e-expression-1-char-5-unknown-command-0
            command_line = "sed '1s\#.*\#"+new_header+"\#' "+file_name+" > "+temp_file_name
            p = subprocess.call(command_line,shell=True)

            # Task #396 - error with ie8 downloading with these on SSL
            del response.headers['Cache-Control']
            del response.headers['Pragma']

            response.headers['Content-type'] = 'text/tab-separated-values'
            # Content-Disposition : leaving this as .txt as this is the default naming convention for YuGene files
            response.headers['Content-Disposition'] = 'attachment;filename=dataset'+str(id)+'.cumulative.txt'

            response.charset= "utf8"

            # returns a stream
            # http://stackoverflow.com/questions/3622675/returning-a-file-to-a-wsgi-get-request
            filelike = open(temp_file_name, "rb")
            block_size = 1024
            if 'wsgi.file_wrapper' in request.environ:
                return request.environ['wsgi.file_wrapper'](filelike, block_size)
            else:
                return iter(lambda: filelike.read(block_size), '')

        else:
            # Task #396 - error with ie8 downloading with these on SSL
            del response.headers['Cache-Control']
            del response.headers['Pragma']

            response.headers['Content-type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment;filename=dataset'+str(id)+'.cumulative_error.txt'
            response.charset= "utf8"

            # push the file
            contents = 'There was no file to download. Please contact the '+c.site_name+' Team.'

            return contents

    #---------------------NOT MIGRATED--------------------------------
    def download_gct(self,id):
        ds_id = int(id)
        export_key = request.params.get("export_key", None)
        username = request.params.get("username", None)
        if export_key is not None and username is not None and username is not u'':
            user = Stemformatics_Auth.get_user_from_username(db,username)
            uid = user.uid
            has_access = Stemformatics_Dataset.check_dataset_availability_by_export_key(db,uid,export_key,ds_id)
            if not has_access:
                redirect(url(controller='contents', action='index'), code=404)
            else:
                permission_used = 'export_key'
                log_uid = uid
        else:
            has_access = Stemformatics_Dataset.check_dataset_availability(db,c.uid,ds_id)
            if not has_access:
                redirect(url(controller='contents', action='index'), code=404)
            else:
                permission_used = 'logged_in'
                log_uid = c.uid


        download_type = 'Gct'
        ip_address = request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])
        result = Stemformatics_Dataset.audit_download_dataset(log_uid,ds_id,download_type,ip_address,permission_used)

        # read in the file
        file_name = config['DatasetGCTFiles'] + 'dataset'+str(ds_id)+'.gct'
        temp_file_name = config['DatasetTempGCTFiles'] + 'dataset'+str(ds_id)+'.tmpexpression'

        if os.path.isfile(file_name):

            sample_labels = Stemformatics_Expression.get_sample_labels(ds_id)
            new_gct_header = Stemformatics_Expression.return_gct_file_sample_headers_as_replicate_group_id(db,ds_id,sample_labels,[])

            new_gct_header = new_gct_header.replace("\n","")
            # changes for task 2563
            # http://stackoverflow.com/questions/28714142/getting-error-sed-e-expression-1-char-5-unknown-command-0
            command_line = "sed '3s\#.*\#"+new_gct_header+"\#' "+file_name+" > "+temp_file_name
            p = subprocess.call(command_line,shell=True)

            # Task #396 - error with ie8 downloading with these on SSL
            del response.headers['Cache-Control']
            del response.headers['Pragma']

            response.headers['Content-type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment;filename=dataset'+str(id)+'.gct'
            response.charset= "utf8"

            # returns a stream
            # http://stackoverflow.com/questions/3622675/returning-a-file-to-a-wsgi-get-request
            filelike = open(temp_file_name, "rb")
            block_size = 1024
            if 'wsgi.file_wrapper' in request.environ:
                return request.environ['wsgi.file_wrapper'](filelike, block_size)
            else:
                return iter(lambda: filelike.read(block_size), '')


        else:
            # Task #396 - error with ie8 downloading with these on SSL
            del response.headers['Cache-Control']
            del response.headers['Pragma']

            response.headers['Content-type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment;filename=dataset'+str(id)+'_error.gct'
            response.charset= "utf8"

            # push the file
            contents = 'There was no file to download. Please contact the '+c.site_name+' Team.'

            return contents



    #---------------------NOT MIGRATED--------------------------------
    def download_cls(self,id):
        has_access = Stemformatics_Dataset.check_dataset_availability(db,c.uid,id)
        if not has_access: redirect(url(controller='contents', action='index'), code=404)


        get_sortBy = request.params.get("sortBy")

        if get_sortBy is None:
            sort_by = ''
        else:
            sort_by = get_sortBy

        # read in the file
        file_name = config['DatasetCLSFiles'] + str(id)+sort_by+'.cls'
        f = open(file_name,'r')

        contents = f.read()

        # set the headers
        # Task #396 - error with ie8 downloading with these on SSL
        del response.headers['Cache-Control']
        del response.headers['Pragma']

        response.headers['Content-type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'attachment;filename=dataset'+str(id)+sort_by+'.cls'
        response.charset= "utf8"

        # push the file

        return contents


    #---------------------NOT MIGRATED--------------------------------
    def autocomplete_probes_for_dataset(self):
        search_term = request.params.get("term")
        ds_id = request.params.get("ds_id")

        use_json = True
        result_json = Stemformatics_Dataset.get_autocomplete_probes_for_dataset(search_term,ds_id,use_json)
        return result_json

    #---------------------NOT MIGRATED--------------------------------
    def download_ds_id_mapping_id_file(self):
        ds_id = 0
        result = Stemformatics_Dataset.get_dataset_mapping_id(ds_id)
        data = Stemformatics_Dataset.text_for_download_ds_id_mapping_id_file(result)

        del response.headers['Cache-Control']
        del response.headers['Pragma']
        response.headers['Content-type'] = 'text/tab-separated-values'
        stemformatics_version = config['stemformatics_version']
        response.headers['Content-Disposition'] = 'attachment;filename=ds_id_to_mapping_id.tsv'
        response.charset= "utf8"

        return data

    @action(renderer="string")
    def search_and_choose_datasets_ajax(self):
        c = self.request.c
        request = self.request
        temp_data = {}

        rohart_msc_test = request.params.get("rohart_msc_test", False)
        if rohart_msc_test == 'true':
            rohart_msc_test = True
        else:
            rohart_msc_test = False

        filter_dict = {'show_limited':False,'rohart_msc_test':rohart_msc_test}
        c.searchQuery = request.params.get("filter", None)

        temp_data = Stemformatics_Dataset.search_and_choose_datasets(c.uid,c.searchQuery,filter_dict)

        json_data = json.dumps(temp_data)

        audit_dict = {'ref_type':'search_term','ref_id':c.searchQuery,'uid':c.uid,'url':url,'request':request}
        result = Stemformatics_Audit.add_audit_log(audit_dict)

        return json_data
