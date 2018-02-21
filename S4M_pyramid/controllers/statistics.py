
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import url

from guide.lib.base import BaseController, render
import json


# Live querying
from guide.model.stemformatics import *
import re

from pylons import config

class StatisticsController(BaseController):
    __name__ = 'StatisticsController'

    #---------------------NOT MIGRATED--------------------------------
    def index(self):
        return render ('/statistics/index.mako')

    # api create for RDS Monitoring of when we moved the HC processing to Galaxy
    #---------------------NOT MIGRATED--------------------------------
    def get_galaxy_hc_stats(self):
        start_date  = request.params.get('start_date')
        end_date  = request.params.get('end_date')
        from guide.model.stemformatics.stemformatics_job import Stemformatics_Job
        hc_stats = Stemformatics_Job.get_hc_stats_from_s4m_db(start_date,end_date)
        hc_stats_json = json.dumps(hc_stats)
        return hc_stats_json
