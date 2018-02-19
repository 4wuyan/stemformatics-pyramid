from pylons import config, request, response, session, tmpl_context as c, url

from pylons.controllers.util import abort, redirect
import guide.lib.helpers as h
from guide.lib.base import BaseController, render
from guide.model.stemformatics import *
import json, os


class MscSignatureController(BaseController):
    def __before__(self):
        super(MscSignatureController, self).__before__()

        if request.path_info not in ('/msc_signature/get_msc_signature_values', '/msc_signature/rohart_msc_test'):
            access = Stemformatics_Msc_Signature.get_user_access(db, c.uid)
            if not access:
                redirect(url(controller='contents', action='index'), code=404)

    def index(self):

        project_msc_set = 'All'
        c.msc_samples_summary = Stemformatics_Msc_Signature.get_msc_samples_summary_by_ds_id(db, project_msc_set)
        return render('msc_signature/index.mako')

    def get_msc_signature_values(self):

        ds_id = request.params.get('ds_id', None)
        values = ""

        del response.headers['Cache-Control']
        del response.headers['Pragma']
        response.charset = "utf8"

        try:
            ds_id = int(ds_id)
        except:
            response.headers['Content-type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment;filename=error.txt'
            values = "Error with dataset id."
            return values

        values = Stemformatics_Msc_Signature.get_msc_values(db, ds_id, c.uid)
        if isinstance(values, dict):
            response.headers['Content-type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment;filename=error.txt'
            values = values['error']
            return values

        file_name = Stemformatics_Msc_Signature.get_file_name_of_msc_values(ds_id, False)
        response.headers['Content-type'] = 'text/tab-separated-values'
        # Content-Disposition: by convention the filename ends in ".rohart.MSC.txt" - see Stemformatics_Msc_Signature.get_file_name_of_msc_values
        response.headers['Content-Disposition'] = 'attachment;filename=' + file_name

        return values

    def export(self):

        # Task #396 - error with ie8 downloading with these on SSL
        del response.headers['Cache-Control']
        del response.headers['Pragma']

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



