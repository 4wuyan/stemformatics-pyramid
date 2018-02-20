#TODO-1
import logging
log = logging.getLogger(__name__)
from S4M_pyramid.lib.deprecated_pylons_globals import  url, config
from S4M_pyramid.lib.base import BaseController
from S4M_pyramid.model.stemformatics import Stemformatics_Ensembl_Upgrade,Stemformatics_Auth,Stemformatics_Gene_Set,Stemformatics_Gene,db_deprecated_pylons_orm as db
from S4M_pyramid.lib.deprecated_pylons_abort_and_redirect import abort,redirect
import S4M_pyramid.lib.helpers as h
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from sqlalchemy.exc import *
# Live querying
import re



class EnsemblUpgradeController(BaseController):
    __name__ = 'EnsemblUpgradeController'

    def __init__(self, request):
        super().__init__(request)
        c = self.request.c
        self.human_db = config['human_db']
        self.mouse_db = config['mouse_db']
        c.human_db = self.human_db
        c.mouse_db = self.mouse_db
        c.url_human_old_ensembl_archive = config['url_human_old_ensembl_archive']
        c.url_mouse_old_ensembl_archive = config['url_mouse_old_ensembl_archive']
        c.current_mouse_ensembl_version = config['current_mouse_ensembl_version_text']
        c.current_human_ensembl_version = config['current_human_ensembl_version_text']
        c.old_mouse_ensembl_version = config['old_mouse_ensembl_version_text']
        c.old_human_ensembl_version = config['old_human_ensembl_version_text']
  
    @Stemformatics_Auth.authorise()
    @action(renderer="templates/ensembl_upgrade/private_gene_sets_archive.mako")
    def index(self):
        request = self.request
        c = self.request.c
        uid = c.uid 
        c.title = c.site_name+'  - List of Gene Lists that have changed since the upgrade'
        c.data = Stemformatics_Ensembl_Upgrade.get_private_gene_sets_archive(db,uid)        
        Stemformatics_Auth.set_smart_redirect(h.url('/ensembl_upgrade/index'))
        if request.params.get('debug') == "yes":
            raise Exception
        return self.deprecated_pylons_data_for_view

    @Stemformatics_Auth.authorise()
    @action(renderer="templates/ensembl_upgrade/gene_set_changed.mako")
    def view(self,id):
        request = self.request
        c = self.request.c
        c.breadcrumbs = [[h.url('/workbench/index'),'Workbench'],[h.url('/ensembl_upgrade/index'),'Manage Gene Lists that have changed since the Ensembl Upgrade'],['','Changes in this Gene List']]
        uid = c.uid 
        c.gene_set_id = int(id)
        c.title = c.site_name+'  - List of Gene Lists that have changed since the upgrade'
        result = Stemformatics_Ensembl_Upgrade.get_private_gene_sets_archive(db,uid)        
        c.data = result[c.gene_set_id]
        Stemformatics_Auth.set_smart_redirect(h.url('/ensembl_upgrade/view/'+str(c.gene_set_id)))
        if request.params.get('debug') == "yes":
            raise Exception
        return self.deprecated_pylons_data_for_view




    @Stemformatics_Auth.authorise()
    def update_gene_set(self,id): #CRITICAL-4
        request = self.request
        c = self.request.c
        c.title = c.site_name+' Workbench - Upload New Gene List'
        try:
            gene_set_id = c.gene_set_id = int(id) 
        except:
            redirect(url(controller='contents', action='index'), code=404)

        uid = c.uid
        result = Stemformatics_Ensembl_Upgrade.get_private_gene_sets_archive(db,uid)        
        data = result[c.gene_set_id]

        posted  = request.params.get('posted')
        gene_set_name  = data['gene_set_name']
        c.db_id =  db_id = data['db_id']
        update = request.params.get('update')
        
        if update =="OK":
            result = Stemformatics_Gene_Set.set_needs_attention_to_false(db,c.uid,gene_set_id)
            default_url =h.url('/ensembl_upgrade/index') 
            redirect_url = Stemformatics_Auth.get_smart_redirect(default_url)
            redirect(redirect_url) 

        if update is None:
            c.title = "You must provide an update option."
            c.message = "You must provide an update option to update your gene set."
            return render_to_response("S4M_pyramid:templates/workbench/error_message.mako",
                                      self.deprecated_pylons_data_for_view, request=self.request)

        if gene_set_id is not None:
            gene_set_result = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
            gene_set = gene_set_result[0]
            gene_set_items = gene_set_result[1]

        gene_set_raw = ""
        for gene_archived in data['genes']:
            mapped_gene = data['genes'][gene_archived]
            gene_id = gene_archived
            ogs = mapped_gene.old_ogs
            entrezid = str(mapped_gene.old_entrez_id) if mapped_gene.old_entrez_id is not None else ""
            if update == 'ogs':
                gene_set_raw_line = ogs 
            if update == 'entrez':
                gene_set_raw_line= entrezid
            if update == 'all':
                gene_set_raw_line = ogs+ " "+ entrezid
            if gene_set_raw_line != "" and gene_set_raw_line != " ":
                gene_set_raw += gene_set_raw_line +"\n"
        for gene in gene_set_items:
            gene_set_raw += gene.gene_id+"\n" 
        
       
        m = re.findall('[\w\.\-\@]{1,}',gene_set_raw)
        
        # now input this list into a gene function that will return a dictionary
        # { 'ILMN_2174394' : { 'original' : 'ILMN_2174394', 'symbol' : 'STAT1', 'status' : 'OK' } }
        # If we make it a list of objects then we can sort, we cannot sort on a dictionary
        search_type = 'all'
        select_all_ambiguous = False
        c.select_all_ambiguous = select_all_ambiguous
        resultData = Stemformatics_Gene.get_unique_gene_fast(db,m,db_id,search_type,select_all_ambiguous)            
        c.gene_set_raw = gene_set_raw
        c.gene_set_raw_list = m
        c.gene_set_name = gene_set_name
        c.gene_set_processed = resultData
        c.db_id = db_id
        c.error_message = ""
        c.hide_save = False
        c.search_type = search_type
        # return 'Successfully uploaded: %s, size: %i rows' % (myfile.filename, len(m))
        c.title = c.site_name+' Workbench  - New Gene List'
        c.breadcrumbs = [[h.url('/workbench/index'),'Workbench'],[h.url('/workbench/gene_set_upload'),'Upload New Gene List'],['','Bulk Import Manager']]
        c.description = ''
        return render_to_response("S4M_pyramid:templates/workbench/gene_set_manage_bulk_import.mako",self.deprecated_pylons_data_for_view,request=self.request)

  
