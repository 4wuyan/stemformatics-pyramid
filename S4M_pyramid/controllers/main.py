from pyramid_handlers import action
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Auth, Stemformatics_Dataset, Stemformatics_Admin, Stemformatics_Audit, Stemformatics_Export,db_deprecated_pylons_orm as db
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals, url, app_globals as g, config
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import redirect
import json
import formencode.validators as fe
import re
from pyramid.renderers import render_to_response
import S4M_pyramid.lib.helpers as h

class MainController(BaseController):
    __name__ = 'MainController'

    def __init__(self,request): #CRITICAL-3
        super().__init__ (request)

    def health_check(self):
        result = Stemformatics_Admin.health_check(db)
        return result

    #---------------------NOT MIGRATED--------------------------------
    def tests(self):
        return render('tests.mako')

    def suggest_dataset(self):
        redirect(config['agile_org_base_url']+'datasets/external_add')

    def export(self):
        request = self.request
        response = self.request.response
        # Task #396 - error with ie8 downloading with these on SSL
        response.headers.pop('Cache-Control', None)
        response.headers.pop('Pragma', None)

        response.headers['Content-type'] = 'text/csv'
        stemformatics_version = config['stemformatics_version']
        format = request.params.get("format")
        if format == None:
            format = "csv"
        #This Content-Disposition is from teh table2CSV file so am leaving this as csv. Might change to tsv later
        response.headers['Content-Disposition'] = 'attachment;filename=export_stemformatics_'+stemformatics_version+'.'+format
        response.charset= "utf8"
        data = request.params['exportdata']
        response.text = data
        return response

    """
        must be logged in to use this

        data - always in svg_xml as show in javascript below:

        example: Portal/guide/public/js/msc_signature/rohart_msc_test.js
        var tmp = document.getElementById(this_div);
        var svg = tmp.getElementsByTagName("svg")[0];
        // Extract the data as SVG text string
        var svg_xml = (new XMLSerializer).serializeToString(svg);

        file_name: filename of the download file without the extension (calculated by output_format)
        output_format: restrict to svg/pdf/png


        NOTE: not sure about allowing download if you are registered only
    """
    #@Stemformatics_Auth.authorise(db)
    def export_d3(self):
        request = self.request
        response = self.request.response
        """
        available = Stemformatics_Auth.check_real_user(c.uid)
        if not available:
            return_message = "This could not be downloaded. You need to be logged in with your own email address to be able to use this feature."
            return return_message
        """

        data = request.params['data']
        file_name = request.params['file_name']
        output_format = request.params['output_format']

        export_data = Stemformatics_Export.get_export_data_for_d3(data,file_name,output_format)

        response.headers.pop('Cache-Control', None)
        response.headers.pop('Pragma', None)

        response.headers['Content-type'] = export_data.content_type
        response.headers['Content-Disposition'] = 'attachment;filename='+export_data.file_name
        response.charset= "utf8"
        response.body = export_data.data

        return response


    def send_email(self):

        sender  = config['from_email']
        recipient = request.params.get('to_email')
        subject = request.params.get('subject')
        body = request.params.get('body')

        available = Stemformatics_Auth.check_real_user(c.uid)
        if not available:
            return_message = "This email could not be sent. You need to be logged in with your own email address to be able to share links."
            return return_message

        success =  Stemformatics_Notification.send_email(sender,recipient,subject,body)
        try:
            if success:
                result = "This email was sent successfully."
            else:
                result = "This email was not sent."

        except:
            result = "This email was not sent."

        return result


    # Trying to fix issues with ie9 and downloading canvas2image files
    def save_image(self):
        response.headers.pop('Cache-Control', None)
        response.headers.pop('Pragma', None)

        response.headers['Content-type'] = 'image/png'
        response.headers['Content-Disposition'] = 'attachment;filename=download_image.png'
        encoded = request.params.get('imgdata')
        encoded = encoded.replace(' ','+')
        decoded = base64.b64decode(encoded)
        return decoded

    def download_thomson_reuters_xml_file(self):
        result = Stemformatics_Dataset.get_thomson_reuters_feed()

        file_text = Stemformatics_Dataset.create_thomson_reuters_xml_file(result)

        response.headers['Content-type'] = 'text/xml'
        response.headers['Content-Disposition'] = 'filename=stemformatics_thomson_reuters_feed.xml'
        response.charset= "utf8"
        return file_text

    def audit_help_log(self):
        ref_type = request.params.get("ref_type")
        ref_id = request.params.get("ref_id")
        controller = request.params.get("controller")
        action = request.params.get("action")
        audit_dict = {'ref_type':ref_type,'ref_id':ref_id,'uid':c.uid,'url':url,'request':request, "controller": controller, "action": action}
        result = Stemformatics_Audit.add_audit_log(audit_dict)
        return str(result)
