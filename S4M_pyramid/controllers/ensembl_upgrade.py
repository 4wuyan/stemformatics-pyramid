#TODO-1
import logging
log = logging.getLogger(__name__)
from pylons import request, response, session, url, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g
#from guide import model
from guide.lib.base import BaseController, render
from sqlalchemy import or_, and_, desc
from sqlalchemy.exceptions import *
from paste.deploy.converters import asbool
# Live querying
from guide.model.stemformatics import *
from pylons import config
connection = db.engine.connect()
# for some reason it is not applied in guide/lib/base.py
import guide.lib.helpers as h
import re



class EnsemblUpgradeController(BaseController):
    __name__ = 'EnsemblUpgradeController'
    
    
    def __before__(self): #CRITICAL-3
        super(EnsemblUpgradeController, self).__before__ ()
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
  
    @Stemformatics_Auth.authorise(db)
    def index(self):
        uid = c.uid 
        c.title = c.site_name+'  - List of Gene Lists that have changed since the upgrade'
        c.data = Stemformatics_Ensembl_Upgrade.get_private_gene_sets_archive(db,uid)        
        Stemformatics_Auth.set_smart_redirect(h.url('/ensembl_upgrade/index'))
        if request.params.get('debug') == "yes":
            raise Error
        return render('ensembl_upgrade/private_gene_sets_archive.mako')

    @Stemformatics_Auth.authorise(db)
    def view(self,id):
        c.breadcrumbs = [[h.url('/workbench/index'),'Workbench'],[h.url('/ensembl_upgrade/index'),'Manage Gene Lists that have changed since the Ensembl Upgrade'],['','Changes in this Gene List']]
        uid = c.uid 
        c.gene_set_id = int(id)
        c.title = c.site_name+'  - List of Gene Lists that have changed since the upgrade'
        result = Stemformatics_Ensembl_Upgrade.get_private_gene_sets_archive(db,uid)        
        c.data = result[c.gene_set_id]
        Stemformatics_Auth.set_smart_redirect(h.url('/ensembl_upgrade/view/'+str(c.gene_set_id)))
        if request.params.get('debug') == "yes":
            raise Error
        return render('ensembl_upgrade/gene_set_changed.mako')




    @Stemformatics_Auth.authorise(db)
    def update_gene_set(self,id): #CRITICAL-4
        
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
            return render('workbench/error_message.mako')
            
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
        return render('workbench/gene_set_manage_bulk_import.mako')
  
