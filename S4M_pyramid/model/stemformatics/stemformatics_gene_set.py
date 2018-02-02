#TODO-1
import logging
log = logging.getLogger(__name__)


import re
from S4M_pyramid.model import redis_server as r_server
import datetime
from datetime import timedelta


from sqlalchemy import or_, and_, desc

from S4M_pyramid.lib.deprecated_pylons_globals import config

__all__ = ['Stemformatics_Gene_Set']


import psycopg2
import psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


#CRITICAL-6
from S4M_pyramid.model.stemformatics.stemformatics_gene import * #wouldn't work with Stemformatics_Gene
from S4M_pyramid.model.stemformatics.stemformatics_admin import Stemformatics_Admin

# check strong password
# (?=^.{8,20}$)(?=.*\d)(?=.*\W+)(?!.*\s)(?=.*[A-Z])(?=.*[a-z]).*$
#  1 upper case letter, 1 lower case letter, 1 number, 1 special char, 8 to 20 characters, no spaces
# based off here http://hspinfo.wordpress.com/2008/07/05/a-regular-expression-for-a-strong-password/
password_regex = re.compile('(?=^.{8,20}$)(?=.*\d)(?=.*\W+)(?!.*\s)(?=.*[A-Z])(?=.*[a-z]).*$')


class Stemformatics_Gene_Set(object):
    """\
    Stemformatics_Auth Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for login controller

    Please note for most of these functions you will have to pass in the db object

    All functions have a try that will return None if errors are found

    """

    def __init__ (self):
        pass

    @staticmethod
    def check_gene_set_availability(gene_set_id,uid):
        uid = int(uid)
        uids = [0,uid]
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select id from stemformatics.gene_sets where id = %s and uid  = ANY (%s) order by id asc limit 1;"
        data = (gene_set_id,uids,)
        cursor.execute(sql, data)

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        try:
            if result[0][0] == gene_set_id:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def addGeneSet(db,uid,gene_set_name,gene_set_description,db_id,list_of_genes): #CRITICAL-2
        try:
            # firstly, you have to successfully save the gene_set
            list_of_genes = list(set(list_of_genes))
            db.schema = 'stemformatics'
            gene_sets = db.gene_sets
            gene_set_items = db.gene_set_items
            result = gene_sets.insert(gene_set_name=gene_set_name ,description = gene_set_description, db_id=db_id, uid = uid)

            db.commit()
            db.flush()

            gene_set_id = int(result.id)

            for ensemblID in list_of_genes:
                gene_set_items.insert(gene_id = ensemblID, gene_set_id = gene_set_id)



            db.commit()
            db.flush()
            return gene_set_id
        except:
            return None


    @staticmethod
    def replace_gene_set_items(db,uid,gene_set_id,list_of_genes): #CRITICAL-2
        try:
            # firstly, you have to successfully save the gene_set
            list_of_genes = list(set(list_of_genes))
            db.schema = 'stemformatics'
            gene_sets = db.gene_sets
            gene_set_items = db.gene_set_items
            result = gene_set_items.filter(gene_set_items.gene_set_id == gene_set_id).delete()
            db.commit()
            db.flush()

            for ensemblID in list_of_genes:
                gene_set_items.insert(gene_id = ensemblID, gene_set_id = gene_set_id)



            db.commit()
            db.flush()

            return True
        except:
            return None

    """
    Returns a SQLSoup object with the count of the gene set items for a user

    find . -type f -name "*.py" -exec grep -sHin "getGeneSets(" {} \;
    ./controllers/workbench.py:97:        geneSetResult = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
    ./controllers/workbench.py:224:        result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
    ./controllers/workbench.py:235:        result = Stemformatics_Gene_Set.getGeneSets(db,0)
    ./controllers/workbench.py:527:            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
    ./controllers/workbench.py:598:            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
    ./controllers/workbench.py:1227:            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
    ./controllers/workbench.py:1456:            result = Stemformatics_Gene_Set.getGeneSets(db,c.uid)
    """
    @staticmethod
    def getGeneSets(db,uid): #CRITICAL-2
        returnGeneSets = {}

        db.schema = 'stemformatics'
        gene_sets = db.gene_sets
        sql = "select gene_set_id,count(*) as n from stemformatics.gene_set_items group by gene_set_id;"
        rp  = db.execute(sql)
        gene_set_count = {}

        for gene_set_id,n in rp.fetchall(): gene_set_count[gene_set_id] = n

        result = gene_sets.filter(gene_sets.uid==uid).all()

        for gene_set in result:
            gene_set_id = gene_set.id
            try:
                count = gene_set_count[gene_set_id]
            except:
                count = 0
            gene_set.count = count

        return result


    """
    Returns an array of SQL Soup objects for the gene set and it's gene set items. Validates against user id
    Returns None if there is an error



     find . -type f -name "*.py" -exec grep -sHin "getGeneSetData("
    ./controllers/workbench.py:259:        result = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
    ./controllers/workbench.py:1320:        getData = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
    ./controllers/workbench.py:1365:        result = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
    ./controllers/workbench.py:1382:        result = Stemformatics_Gene_Set.getGeneSetData(db,0,gene_set_id)
    ./controllers/workbench.py:1527:        result = Stemformatics_Gene_Set.getGeneSetData(db,c.uid,gene_set_id)
    ./controllers/api.py:230:        result = Stemformatics_Gene_Set.getGeneSetData(db,uid,gene_set_id)
    ./model/stemformatics/stemformatics_gene_set.py:101:    def getGeneSetData(db,uid,gene_set_id):
    ./model/stemformatics/stemformatics_gene_set.py:286:            result = Stemformatics_Gene_Set.getGeneSetData(db,uid,gene_set_id)
    """
    @staticmethod
    def getGeneSetData(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets
            gsi = db.gene_set_items
            db.schema = 'public'
            ga = db.genome_annotations

            or_clause = or_(gs.uid == uid,gs.uid ==0)

            where = and_(or_clause, gs.id==gene_set_id)

            resultGeneSet = gs.filter(where).one()

            if resultGeneSet is not None:

                join1 = db.join(gsi,ga,and_(ga.gene_id==gsi.gene_id,ga.db_id == resultGeneSet.db_id))
                where = and_(gsi.gene_set_id==gene_set_id)
                resultGeneSetData = join1.filter(where).order_by(gsi.gene_id).all()

                result = [resultGeneSet,resultGeneSetData]
            else:
                return None

            return result
        except:
            return None






    """
    Returns a SQLSoup result for an individual gene set and checks the user id is valid
    Returns None if there is an error

    find . -type f -name "*.py" -exec grep -sHin "getGeneSet(" {} \;
    ./controllers/workbench.py:1736:            result = Stemformatics_Gene_Set.getGeneSet(db,public_uid,int(filter_gene_set_id))
    ./controllers/workbench.py:1744:            gene_set = Stemformatics_Gene_Set.getGeneSet(db,c.uid,gene_set_id)
    ./controllers/workbench.py:2247:            result = Stemformatics_Gene_Set.getGeneSet(db,public_uid,int(filter_gene_set_id))
    """

    @staticmethod
    def getGeneSet(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets
            or_clause = or_(gs.uid == uid,gs.uid ==0)

            where = and_(or_clause, gs.id==gene_set_id)

            result = gs.filter(where).one()

            return result
        except:
            return None

    @staticmethod
    def delete_gene_set_item(db,uid,gene_set_item_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets
            gsi = db.gene_set_items

            # first find the gene_set_item_id and the gene_set record
            join1 = db.join(gsi,gs,gsi.gene_set_id==gs.id)
            result = join1.filter(gsi.id==gene_set_item_id).one()

            if result is None:
                raise ValueError
                return None

            # check that this user owns this gene_set record
            if result.uid != uid:
                raise ValueError
                return None

            # save gene_set_id
            gene_set_id = result.gene_set_id

            # delete gene_set_item
            gsi.filter(gsi.id==gene_set_item_id).delete()

            if result is None:
                return None

            db.commit()
            db.flush()

            # return gene_set_id
            return gene_set_id
        except:
            return None

    @staticmethod
    def add_gene_to_set(db,uid,gene_set_id,db_id,gene): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets
            gsi = db.gene_set_items

            # find unique gene for db_id and gene
            geneList = [gene]
            uniqueGeneResult = Stemformatics_Gene.get_unique_gene(db,geneList,db_id)

            if uniqueGeneResult is None:
                return None

            # should only be one brought back
            for gene_found in uniqueGeneResult:
                if uniqueGeneResult[gene_found]['ensemblID'] != '':
                    geneID = uniqueGeneResult[gene_found]['ensemblID']
                else:
                    return None

            # ensure this gene_set_id belongs to this uid
            where = and_(gs.id == gene_set_id, gs.uid == uid)
            result = gs.filter(where).one()

            if result is None:
                return None


            # check it isn't already in there
            where = and_(gsi.gene_set_id==gene_set_id,gsi.gene_id== geneID)
            result = gsi.filter(where).all()

            if len(result) != 0:
                return None

            # add to this gene set
            result = gsi.insert(gene_set_id=gene_set_id,gene_id=geneID)

            if result is None:
                return None

            db.commit()
            db.flush()

            return True
        except:
            return None


    @staticmethod
    def update_gene_set_name(db,uid,gene_set_id,gene_set_name): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets

            # check uid, geneset id are valid
            is_admin = Stemformatics_Admin.is_user_admin(db,uid)
            if is_admin:
                where = and_(gs.id==gene_set_id)
            else:
                where = and_(gs.uid == uid, gs.id==gene_set_id)
            result = gs.filter(where).one()

            if result is None:
                return None

            # update gene name
            result = gs.filter(gs.id == gene_set_id).update({'gene_set_name': gene_set_name})

            if result is None:
                return None

            db.commit()


            return True
        except:
            return None

    @staticmethod
    def delete_gene_set(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets
            gsi = db.gene_set_items


            # check uid, geneset id are valid
            where = and_(gs.uid == uid, gs.id==gene_set_id)
            query = gs.filter(where)

            result = query.one()

            if result is None:
                return None

            query_gsi = gsi.filter(gsi.gene_set_id == gene_set_id)
            query_gsi.delete()

            query.delete()
            db.commit()
            db.flush()
            return True
        except:
            return None



    @staticmethod
    def get_db_id(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets

            # check uid, geneset id are valid
            or_clause = or_(gs.uid == uid,gs.uid ==0)

            where = and_(or_clause, gs.id==gene_set_id)

            query = gs.filter(where)

            result = query.one()

            return result.db_id
        except:
            return None

    # no check for uid now
    @staticmethod
    def get_gene_set_name(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets

            where = and_(gs.id==gene_set_id)

            query = gs.filter(where)

            result = query.one()

            return result.gene_set_name
        except:
            return None


    @staticmethod
    def get_species(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets

            # check uid, geneset id are valid
            or_clause = or_(gs.uid == uid,gs.uid ==0)

            where = and_(or_clause, gs.id==gene_set_id)
            query = gs.filter(where)

            result = query.one()

            db_id = result.db_id

            db.schema = 'public'
            ad = db.annotation_databases

            result = ad.filter(ad.an_database_id == db_id).one()

            return result.genome_version

        except:
            return None



    @staticmethod
    def update_gene_set_description(db,uid,gene_set_id,gene_set_description): #CRITICAL-2
        #try:
            db.schema = 'stemformatics'
            gs = db.gene_sets

            # check uid, geneset id are valid
            is_admin = Stemformatics_Admin.is_user_admin(db,uid)
            if not is_admin:
                where = and_(gs.uid == uid, gs.id==gene_set_id)
            else:
                where = and_(gs.id==gene_set_id)

            result = gs.filter(where).one()

            if result is None:
                return None

            # update gene description
            result = gs.filter(gs.id == gene_set_id).update({'description': gene_set_description})

            if result is None:
                return None

            db.commit()


            return True
        #except:
        #    return None


    @staticmethod
    def get_gene_set_details(db,uid,gene_sets): #CRITICAL-2

        db.schema = 'stemformatics'
        gs = db.gene_sets

        # check uid, geneset id are valid
        where = and_(gs.uid == uid, gs.id.in_(gene_sets))
        query = gs.filter(where)

        result = query.all()

        return result

    @staticmethod
    def get_gene_set_count(db,gene_set_id):

        sql = "select count(*) as total FROM stemformatics.gene_set_items where gene_set_items.gene_set_id = "+str(gene_set_id)+";"
        sql_result = db.execute(sql)
        values = sql_result.fetchall()
        result = int(values[0][0])
        return result


    @staticmethod
    def get_gene_set_counts(db,uid,gene_sets): #CRITICAL-2

        db.schema = 'stemformatics'
        gs = db.gene_sets
        gsi = db.gene_set_items

        # check uid, geneset id are valid
        where = and_(gs.uid == uid, gs.id.in_(gene_sets))


        join1 = db.join(gsi,gs,gsi.gene_set_id==gs.id)

        result = join1.filter(where).order_by(gs.id).all()

        pathway_count_result = {}
        for gene in result:
            gene.gene_set_id = str(gene.gene_set_id)

            if gene.gene_set_id not in pathway_count_result:
                pathway_count_result[gene.gene_set_id] = 0

            pathway_count_result[gene.gene_set_id] = pathway_count_result[gene.gene_set_id] + 1

        return pathway_count_result



    """
    Returns an array of SQL Soup objects for the gene set and it's gene set items. Validates against user id
    Does not get the genome_annotations for speed
    Returns None if there is an error


    find . -type f -name "*.py" -exec grep -sHin "getGeneSetData_with" {} \;
    ./controllers/workbench.py:1846:        result = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db,c.uid,gene_set_id)
    ./controllers/workbench.py:2114:            result = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db,public_uid,filter_gene_set_id)
    """
    @staticmethod
    def getGeneSetData_without_genome_annotations(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets
            gsi = db.gene_set_items
            db.schema = 'public'

            or_clause = or_(gs.uid == uid,gs.uid ==0)

            where = and_(or_clause, gs.id==gene_set_id)
            resultGeneSet = gs.filter(where).one()

            if resultGeneSet is not None:

                where = and_(gsi.gene_set_id==gene_set_id)
                resultGeneSetData = gsi.filter(where).order_by(gsi.gene_id).all()

                result = [resultGeneSet,resultGeneSetData]
            else:
                return None

            return result
        except:
            return None



    """
        Get the list of all the gene sets that are matched to a gene on a per gene basis
    """
    @staticmethod
    def read_db_all_genes(filename,filter_genes):

        gene_list = {};
        f_gs = open(filename,'r')
        for line in f_gs:
            line = line.replace('\n','')
            row_list = line.split('\t')
            gene_id = row_list[0]

            if gene_id in filter_genes:

                # print gene_id
                gene_list[gene_id] = row_list[1:]

        f_gs.close()

        return gene_list

    # rewrite to use psycopg2 and less joins
    @staticmethod
    def get_probes_from_gene_set_id(db,db_id,ds_id,gene_set_id):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select mapping_id from datasets where id = %s"
        data = (ds_id,)
        cursor.execute(sql, data)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        mapping_id = result[0][0]

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from stemformatics.feature_mappings as fm where db_id = %s and mapping_id = %s and from_type = 'Gene' and from_id in (select gene_id from stemformatics.gene_set_items as gsi where gene_set_id = %s);"
        data = (db_id,mapping_id,gene_set_id)
        cursor.execute(sql, data,)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()


        probes_to_genes = result
        list_of_probes = []
        list_of_genes = []
        dict_of_probe_to_gene = {}
        # added thsi for task 2527, to create a dict with probe and gene_id
        dict_of_probe_to_gene_id = {}
        for row in result:
            probe_id = row['to_id']
            gene_id = row['from_id']
            list_of_probes.append(probe_id)
            list_of_genes.append(gene_id)

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select gene_id,associated_gene_name from genome_annotations where db_id = %s and gene_id =ANY(%s);"
        data = (db_id,list_of_genes)
        cursor.execute(sql, data,)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        dict_of_gene_to_name = {}
        for row in result:
            gene_id = row['gene_id']
            gene_name = row['associated_gene_name']
            dict_of_gene_to_name[gene_id] = gene_name

        for row in probes_to_genes:
            probe_id = row['to_id']
            gene_id = row['from_id']
            dict_of_probe_to_gene[probe_id] = dict_of_gene_to_name[gene_id]

        for row in probes_to_genes:
            probe_id = row['to_id']
            gene_id = row['from_id']
            dict_of_probe_to_gene_id[probe_id] = gene_id

        return [list_of_probes,dict_of_probe_to_gene,dict_of_probe_to_gene_id]

    # gene must be ensemblID
    # rewriting to use pyscopg2 and incorporate list of genes instead of a single gene
    @staticmethod
    def get_probes_from_genes(db_id,ds_id,gene_list,gene_annotation_names_required): #CRITICAL-2
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select mapping_id from datasets where id = %s"
        data = (ds_id,)
        cursor.execute(sql, data,)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        mapping_id = result[0][0]

        probe_mappings = {}

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from stemformatics.feature_mappings as fm where db_id = %(db_id)s and mapping_id = %(mapping_id)s and from_type = 'Gene' and from_id in %(genes)s;"
        cursor.execute(sql, {"db_id":db_id,"mapping_id":mapping_id,"genes":tuple(gene_list)})
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        probes_to_genes = result
        list_of_probes = []
        list_of_genes = []

        for row in result:
            probe_id = row['to_id']
            gene_id = row['from_id']
            list_of_probes.append(probe_id)
            list_of_genes.append(gene_id)

        list_of_probes = list(set(list_of_probes))

        if gene_annotation_names_required == "yes":
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select gene_id,associated_gene_name from genome_annotations where db_id = %s and gene_id =ANY(%s);"
            data = (db_id,list_of_genes)
            cursor.execute(sql, data,)
            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            dict_of_gene_to_name = {}
            probe_mappings_to_gene_name = {}

            for row in result:
                gene_id = row['gene_id']
                gene_name = row['associated_gene_name']
                dict_of_gene_to_name[gene_id] = gene_name

            for row in probes_to_genes:
                probe_id = row['to_id']
                gene_id = row['from_id']
                probe_mappings_to_gene_name[probe_id] = dict_of_gene_to_name[gene_id]

            return [list_of_probes,probe_mappings_to_gene_name]

        else:
            probe_mappings_to_gene_id = {}

            for row in probes_to_genes:
                probe_id = row['to_id']
                gene_id = row['from_id']
                probe_mappings_to_gene_id[probe_id] = gene_id

            return [list_of_probes,probe_mappings_to_gene_id]




    @staticmethod
    def copy_gene_set(db,gene_set_id,from_uid,to_uid):

        db.schema = 'stemformatics'
        gs = db.gene_sets

        result = Stemformatics_Gene_Set.getGeneSetData_without_genome_annotations(db,from_uid,gene_set_id)

        return result


    @staticmethod
    def set_needs_attention_to_false(db,uid,gene_set_id): #CRITICAL-2
        try:
            db.schema = 'stemformatics'
            gs = db.gene_sets
            result = gs.filter(and_(gs.uid == uid,gs.id==gene_set_id)).update({'needs_attention':False})
            db.commit()
            db.flush()
        except:
            return False

    @staticmethod
    def get_numbers_for_gene_lists_for_gene(db,uid,gene_id):
        result = Stemformatics_Gene_Set.get_gene_lists_for_gene(db,uid,gene_id)
        result_dict = {}
        result_list = []
        for gene_set in result:
            temp_uid = gene_set['uid']
            gene_set_id = gene_set['gene_set_id']
            result_list.append(gene_set_id)
            if temp_uid == 0:
                gene_set_type = gene_set['gene_set_type']
                if gene_set_type not in result_dict:
                    result_dict[gene_set_type] = []
                result_dict[gene_set_type].append(gene_set_id)

            else:
                if 'uid' not in result_dict:
                    result_dict['uid'] = []
                result_dict['uid'].append(gene_set_id)
        return [result,result_dict,result_list]


    """ Note that shared gene lists are actually copies of the original gene lists saved
        under the real sharee's uid """
    @staticmethod
    def get_gene_lists_for_gene(db,uid,gene_id):
        uid = int(uid)
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select gene_set_id,uid,gene_set_type,gene_set_name,db_id from stemformatics.gene_set_items as gsi left join  stemformatics.gene_sets as gs on gs.id = gsi.gene_set_id where gene_id = %s and uid in (%s,0) order by uid,gene_set_type,gene_set_id"
        data = (gene_id,uid)
        cursor.execute(sql, data)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result


    @staticmethod
    def get_first_kegg_gene_list(db_id):
        try:
            db_id = int(db_id)
        except:
            db_id = None
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from stemformatics.gene_sets where gene_set_type = 'Kegg' and db_id = %s order by id asc limit 1;"
        data = (db_id,)
        cursor.execute(sql, data)
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        # if not found, value is []
        return result

    """
    This is used to delete keys everytime a gene list is updated
    """
    @staticmethod
    def delete_short_term_redis_keys_for_a_gene_list(gene_set_id):
        expiry_amplifier = 2
        days_to_subtract = (config['expiry_time']/86400) * expiry_amplifier
        d = datetime.today() - timedelta(days=days_to_subtract)
        date_formatted = d.strftime('%Y-%m-%d')
        delimiter = config['delimiter']

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select ref_id from stemformatics.audit_log where extra_ref_type = 'gene_set_id' and action = 'histogram_wizard' and extra_ref_id = %(gene_set_id)s and date_created >= %(date)s;",{"date":date_formatted,"gene_set_id":str(gene_set_id)})

        result = cursor.fetchall()

        gene_set_mapping_keys = []
        ds_id_list = []
        for row in result:
            ds_id = row['ref_id']
            ds_id_list.append(ds_id)
        if ds_id_list != []:
            cursor.execute("select id,mapping_id,db_id from datasets where id in %(ds_id_list)s ;",{"ds_id_list":tuple(ds_id_list)})

            ds_id_info_list = cursor.fetchall()

            cursor.close()
            conn.close()

            for row in ds_id_info_list:
                ds_id = row['id']
                mapping_id = row['mapping_id']
                db_id = row['db_id']
                gene_set_mapping_keys.append("gene_set_mapping_data"+delimiter+str(mapping_id)+delimiter+str(gene_set_id)+delimiter+'gene_set_id'+delimiter+str(db_id))

            delimiter = config['redis_delimiter']

            for key in gene_set_mapping_keys:
                r_server.delete(key)

        return True
