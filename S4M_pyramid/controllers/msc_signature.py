from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, app_globals as g, config
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect

from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Msc_Signature, db_deprecated_pylons_orm as db,Stemformatics_Dataset
from pyramid_handlers import action


class MscSignatureController(BaseController):

    def __init__(self,request):
        super().__init__(request)
        c = self.request.c
        if request.path_info not in ('/msc_signature/get_msc_signature_values', '/msc_signature/rohart_msc_test'):
            access = Stemformatics_Msc_Signature.get_user_access(db, c.uid)
            if not access:
                redirect(url(controller='contents', action='index'), code=404)

    @action(renderer="templates/msc_signature/index.mako")
    def index(self):
        request = self.request
        c = self.request.c
        project_msc_set = 'All'
        c.msc_samples_summary = Stemformatics_Msc_Signature.get_msc_samples_summary_by_ds_id(db, project_msc_set)
        return self.deprecated_pylons_data_for_view

    def get_msc_signature_values(self):
        request = self.request
        c = self.request.c
        response = self.request.response

        ds_id = request.params.get('ds_id', None)
        values = ""

        response.headers.pop('Cache-Control', None)
        response.headers.pop('Pragma', None)
        response.charset = "utf8"

        try:
            ds_id = int(ds_id)
        except:
            response.headers['Content-type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment;filename=error.txt'
            values = "Error with dataset id."
            response.text = values
            return response

        values = Stemformatics_Msc_Signature.get_msc_values(db, ds_id, c.uid)
        if isinstance(values, dict):
            response.headers['Content-type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment;filename=error.txt'
            values = values['error']
            response.text = values
            return response

        file_name = Stemformatics_Msc_Signature.get_file_name_of_msc_values(ds_id, False)
        response.headers['Content-type'] = 'text/tab-separated-values'
        # Content-Disposition: by convention the filename ends in ".rohart.MSC.txt" - see Stemformatics_Msc_Signature.get_file_name_of_msc_values
        response.headers['Content-Disposition'] = 'attachment;filename=' + file_name
        response.text = values
        return response

    def export(self):

        request = self.request
        c = self.request.c
        response = self.request.reponse

        # Task #396 - error with ie8 downloading with these on SSL
        response.headers.pop('Cache-Control', None)
        response.headers.pop('Pragma', None)

        project_msc_set = request.params.get('project_msc_set')
        if project_msc_set == 'download_script':
            # c.user is actually username eg. rowland.mosbergen@mailinator.com
            ds_ids = request.params.get('ds_ids')
            try:
                filter_ds_ids = []
                temp_filter_ds_ids = ds_ids.split(',')
                for ds_id in temp_filter_ds_ids:
                    filter_ds_ids.append(int(ds_id))
            except:
                filter_ds_ids = None

            file_types = ['yugene']
            datasets = Stemformatics_Msc_Signature.get_msc_samples_summary_by_ds_id(db, 'All')
            data = Stemformatics_Dataset.create_download_script_for_multiple_datasets(datasets, c.uid, c.user,
                                                                                      filter_ds_ids, file_types)

            response.headers['Content-type'] = 'text/plain'
            stemformatics_version = config['stemformatics_version']
            response.headers['Content-Disposition'] = 'attachment;filename=multi_' + project_msc_set + '.sh'
            response.charset = "utf8"


        else:
            msc_samples = Stemformatics_Dataset.get_msc_samples(db, project_msc_set)

            response.headers['Content-type'] = 'text/tab-separated-values'
            response.headers['Content-Disposition'] = 'attachment;pfilename=msc_' + project_msc_set + '.tsv'
            response.charset = "utf8"

            delimiter = "\t"

            headers = ["chip_id", "sample_id", "sample_type", "ds_id", "msc_flag", "msc_set", "msc_why"]
            data = delimiter.join(headers) + "\n"
            for ds_id in msc_samples:
                for chip_id in msc_samples[ds_id]:
                    row = msc_samples[ds_id][chip_id]
                    row_list = []
                    msc_set = row['project_msc_set']
                    msc_flag = row['project_msc_type']
                    msc_why = row['project_msc_why']
                    sample_id = row['Replicate Group ID']
                    sample_type = row['Sample Type']

                    data = data + chip_id + delimiter + sample_id + delimiter + sample_type + delimiter + str(
                        ds_id) + delimiter + msc_flag + delimiter + msc_set + delimiter + msc_why + "\n"

        return data



