from S4M_pyramid.lib.base import BaseController
from pyramid_handlers import action
import json

class StatisticsController(BaseController):
    __name__ = 'StatisticsController'

    @action(renderer='templates/statistics/index.mako')
    def index(self):
        return self.deprecated_pylons_data_for_view

    # api create for RDS Monitoring of when we moved the HC processing to Galaxy
    @action(renderer='string')
    def get_galaxy_hc_stats(self):
        request = self.request
        start_date  = request.params.get('start_date')
        end_date  = request.params.get('end_date')
        from S4M_pyramid.model.stemformatics.stemformatics_job import Stemformatics_Job
        hc_stats = Stemformatics_Job.get_hc_stats_from_s4m_db(start_date,end_date)
        hc_stats_json = json.dumps(hc_stats)
        return hc_stats_json
