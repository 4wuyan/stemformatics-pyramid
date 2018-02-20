#TODO-1
import logging
log = logging.getLogger(__name__)
import sqlalchemy as SA
import re
import string
import json
from guide.lib.state import *
from pylons import config
from decorator import decorator
import sys
__all__ = ['Stemformatics_Ensembl_Upgrade']
from guide.model.stemformatics.stemformatics_gene_set import Stemformatics_Gene_Set  #CRITICAL-6


class Stemformatics_Ensembl_Upgrade(object):
    
    def __init__ (self):
        pass


    """
    usage of returned data: return_gene_sets[1451][ENSG000415155].ens_id_status
    """ 
    @staticmethod
    def get_private_gene_sets_archive(db,uid): #CRITICAL-2
        return_gene_sets = {}
        
        db.schema = 'stemformatics'
        pa = db.private_gene_sets_update_archive
        
        result = pa.filter(pa.user_id==uid).all()
        for old_gene in result:
            gs_id = old_gene.gene_set_id
            old_gene_id = old_gene.old_ens_id
            db_id = old_gene.species_db_id
           
            if gs_id not in return_gene_sets:
                return_gene_sets[gs_id] = {}  
                return_gene_sets[gs_id]['retired'] = 0  
                return_gene_sets[gs_id]['remapped'] = 0  
                return_gene_sets[gs_id]['db_id'] = db_id  

            if 'genes' not in return_gene_sets[gs_id]:
                return_gene_sets[gs_id]['genes'] = {} 

            return_gene_sets[gs_id]['genes'][old_gene_id] = old_gene 
            if old_gene.ens_id_status =="retired":
                return_gene_sets[gs_id]['retired'] += 1  
            if old_gene.ens_id_status =="remapped":
                return_gene_sets[gs_id]['remapped'] += 1  

            return_gene_sets[gs_id]['gene_set_name'] = old_gene.gene_set_name
            return_gene_sets[gs_id]['description'] = ""
 
        for gs_id in return_gene_sets:
            gs_result = Stemformatics_Gene_Set.get_gene_set_details(db,uid,[gs_id])
            gs_count = Stemformatics_Gene_Set.get_gene_set_count(db,gs_id)
            number_of_genes = gs_count
            return_gene_sets[gs_id]['number_of_current_genes'] = number_of_genes

            if gs_result is None or gs_result == []:
                return_gene_sets[gs_id]['status'] = "Deleted"
            else:    
                for row in gs_result:
                    return_gene_sets[gs_id]['status'] = "Needs Attention" if row.needs_attention else "OK"
        return return_gene_sets

