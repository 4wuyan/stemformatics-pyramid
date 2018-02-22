import logging
log = logging.getLogger(__name__)

from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import redirect
from pyramid_handlers import action
from S4M_pyramid.lib.base import BaseController
from pyramid.renderers import render_to_response
from S4M_pyramid.model.stemformatics import Stemformatics_Job, Stemformatics_Gene

class TestsController(BaseController):

    @action(renderer='templates/tests.mako')
    def static_tests(self):
        return self.deprecated_pylons_data_for_view

    def last_job_result(self):
        id = self.request.matchdict['id']
        c = self.request.c

        # first get the uid and find the last successful hc job
        # then redirect to that account
        analysis_id = int(id)
        job_id = Stemformatics_Job.get_last_job_for_user(c.uid,analysis_id)
        return redirect('/workbench/job_view_result/'+str(job_id))

    def last_gene_list(self):
        id = self.request.matchdict['id']
        c = self.request.c

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
            text = "No gene list found. "
            return render_to_response('string', text)

