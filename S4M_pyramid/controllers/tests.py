import logging,base64
log = logging.getLogger(__name__)
from pylons import config,request, response, session, tmpl_context as c, url

from pylons.controllers.util import abort, redirect

from guide.lib.base import BaseController, render

from guide.model.stemformatics import *

class TestsController(BaseController):

    #---------------------NOT MIGRATED--------------------------------
    def static_tests(self):
        return render('tests.mako')

    #---------------------NOT MIGRATED--------------------------------
    def last_job_result(self,id):

        # first get the uid and find the last successful hc job
        # then redirect to that account
        analysis_id = int(id)
        job_id = Stemformatics_Job.get_last_job_for_user(c.uid,analysis_id)
        return redirect('/workbench/job_view_result/'+str(job_id))

    #---------------------NOT MIGRATED--------------------------------
    def last_gene_list(self,id):

        # first get the uid and find the last successful hc job
        # then redirect to that account
        if id == 'public':
            gene_list_type = 'public'
        if id == 'private':
            gene_list_type = 'private'


        gene_list_id = Stemformatics_Gene.get_last_gene_list(c.uid,gene_list_type)
        if gene_list_id is not None:
            return redirect('/workbench/gene_set_view/'+str(gene_list_id))
        else:
            return "No gene list found. "

