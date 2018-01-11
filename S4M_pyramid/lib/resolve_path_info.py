import re

class path_resolver(object):
    def __init__(self, path_info_string):
        self.path = path_info_string
        self.result = {'controller': None, 'action': None, 'id': None}

    def _match(self, pattern):
        controller_regex = '(?P<controller>[^/]+)'
        action_regex = '(?P<action>[^/]+)'
        id_regex = '(?P<id>[^/]+)'
        regex_pattern = pattern.format(controller=controller_regex, action=action_regex, id=id_regex)
        m = re.fullmatch(regex_pattern, self.path)
        if m:
            self.result.update(m.groupdict())
            #print(pattern)
            return True
        else:
            return False

    def resolve_path_info(self):
        if self._match('/error/{action}'):
            self.result.update(dict(controller='error'))
        elif self._match('/error/{action}/{id}'):
            self.result.update(dict(controller='error'))
        elif self._match('/project_grandiose'):
            self.result.update(dict(controller='projects', action='project_grandiose'))
        elif self._match('/leukomics'):
            self.result.update(dict(controller='projects', action='leukomics'))
        elif self._match('/'):
            self.result.update(dict(controller='contents', action='index'))
        elif self._match('/hamlet/index'):
            self.result.update(dict(controller='contents', action='removal_of_hamlet'))
        elif self._match('/tests'):
            self.result.update(dict(controller='main', action='tests'))
        elif self._match('/genes'):
            self.result.update(dict(controller='genes', action='search'))
        elif self._match('/genes/'):
            self.result.update(dict(controller='genes', action='search'))
        elif self._match('/genes/summary'):
            self.result.update(dict(controller='expressions', action='yugene_graph'))
        elif self._match('/workbench/gene_set_index'):
            self.result.update(dict(controller='genes', action='gene_set_index'))
        elif self._match('/workbench/public_gene_set_index'):
            self.result.update(dict(controller='genes', action='public_gene_set_index'))
        elif self._match('/workbench/gene_set_view/{id}'):
            self.result.update(dict(controller='genes', action='gene_set_view'))
        elif self._match('/workbench/gene_set_bulk_import_manager'):
            self.result.update(dict(controller='genes', action='gene_set_bulk_import_manager'))
        elif self._match('/workbench/merge_gene_sets'):
            self.result.update(dict(controller='genes', action='merge_gene_sets'))
        elif self._match('/admin/check_redis_consistency_for_datasets'):
            self.result.update(dict(controller='api', action='check_redis_consistency_for_datasets'))
        elif self._match('/workbench/histogram_wizard'):
            self.result.update(dict(controller='expressions', action='histogram_wizard'))
        elif self._match('/expressions'):
            self.result.update(dict(controller='contents', action='index'))
        elif self._match('/expressions/'):
            self.result.update(dict(controller='contents', action='index'))
        elif self._match('/datasets'):
            self.result.update(dict(controller='datasets', action='search'))
        elif self._match('/datasets/'):
            self.result.update(dict(controller='datasets', action='search'))
        elif self._match('/{controller}/{action}'):
            pass
        elif self._match('/{controller}/{action}/{id}'):
            pass
        elif self._match('/{controller}'):
            self.result.update(dict(controller='DYNAMIC',action='index'))

