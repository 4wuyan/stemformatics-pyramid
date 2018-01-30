#TODO-1
import logging
log = logging.getLogger(__name__)

import sqlalchemy as SA
from sqlalchemy import or_, and_, desc

import re
import string
import json
import redis
import psycopg2
import psycopg2.extras
from S4M_pyramid.model import s4m_psycopg2
from S4M_pyramid.model.stemformatics.stemformatics_gene_set import Stemformatics_Gene_Set # wouldn't work otherwise??
from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset # wouldn't work otherwise??
from S4M_pyramid.lib.deprecated_pylons_globals import config
import subprocess


__all__ = ['Stemformatics_Gene']

import formencode.validators as fe

SUBSCRIBER_NAME = fe.Regex("[\w ]*", not_empty=False, if_empty="Anonymous User")
SUBSCRIBER_STATE = fe.Regex("[\w ]*", not_empty=False, if_empty="PENDING")
DESCRIPTIVE_TEXT = fe.Regex("[\w ]*", not_empty=False, if_empty="")
POS_INT = fe.Int(min=1, not_empty=True)
NUMBER = fe.Number(not_empty=True)
IDENTIFIER = fe.PlainText(not_empty=True)
URL = fe.URL(not_empty=True)
VQ = re.compile(r"[^\'\"\`\$\\]*")


class Stemformatics_Gene(object):
    """\
    Stemformatics_Gene Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for gene data

    Please note for most of these functions you will have to pass in the db object

    All functions have a try that will return None if errors are found

    """

    def __init__ (self):
        pass


    @staticmethod
    def get_species(db):
        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from annotation_databases;")
        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        species_dict =  {}

        for row in result:
            db_id = row['an_database_id']
            sci_name = row['genome_version']
            name = row['model_id']
            species_dict[db_id] = {'sci_name': sci_name, 'name': name}

            #from S4M_pyramid.model.stemformatics.stemformatics_gene_set import *
            result = Stemformatics_Gene_Set.get_first_kegg_gene_list(db_id)
            if result != []:
                default_kegg_gene_list_id = result[0]['id']
            else:
                default_kegg_gene_list_id = None
            species_dict[db_id]['default_kegg_gene_list_id'] = default_kegg_gene_list_id

            #from S4M_pyramid.model.stemformatics.stemformatics_dataset import *
            ds_id = Stemformatics_Dataset.get_default_dataset(db_id)
            species_dict[db_id]['default_ds_id'] = ds_id


        return species_dict



    @staticmethod
    def get_total_number_genes(db,db_id): #CRITICAL-2
        return db.genome_annotations.filter(db.genome_annotations.db_id == db_id).count()

    """
    This takes a genome_annotation row from psycopg2 and turns it into the right format
    """
    @staticmethod
    def _encode_gene(row_result,species_dict):
        returnDict = {}
        samples_detected = ''
        samples = ''
        # entrez gene ID not in use anymore
        official_symbol = ''
        official_name = ''
        aliases = ''
        map_location = ''
        entrez_description = ''
        tax_id = ''
        locus_tag = ''
        dbXrefs = ''
        gene_type = ''
        nomenclature_status = ''
        other_designations = ''
        modification_date = ''

        returnDict[row_result['gene_id']] = {
            'symbol': row_result['associated_gene_name'],
            'id': row_result['gene_id'],
            'location': {
                "direction": row_result['strand'],
                "end": row_result['gene_end'],
                "orientation": row_result['strand'],
                "start": row_result['gene_start'],
                "chr": row_result['chromosome_name'],
                "chromosome": row_result['chromosome_name'],
                "strand": row_result['strand']
                },
            'description': row_result['description'],
            'EnsemblID': row_result['gene_id'],
            'EntrezID': row_result['entrezgene_id'],
            'biotype': row_result['gene_biotype'],
            'associated_db': row_result['associated_gene_db'],
            'source': row_result['source'],
            'status': row_result['gene_status'],
            'refseq_dna_id': row_result['refseq_dna_id'],
            'db_id': row_result['db_id'],
            'species': species_dict[row_result['db_id']]['sci_name'],
            'official_symbol': row_result['associated_gene_name'],
            'aliases': row_result['associated_gene_synonym'],
            # 'entrez_description': entrez_description,
            #'tax_id': tax_id,
            # 'locus_tag': locus_tag,
            # 'dbXrefs': dbXrefs,
            # 'gene_type': gene_type,
            # 'nomenclature_status': nomenclature_status,
            # 'other_designations': other_designations,
            # 'modification_date': modification_date,
            'samples_detected': samples_detected, 'samples': samples,
            'diseases': 'diseases go here (not included in genome_annotations)',
            'alt_splicing': '',
            'cage_data': '',
            'Pathways': '',
            # Also, add a few synonyms here (e.g. aliases <--> synonyms)
            'name': row_result['associated_gene_name'],
            'Synonyms': row_result['associated_gene_synonym'],
            'Location': {
                "direction": row_result['strand'],
                "end": row_result['gene_end'],
                "orientation": row_result['strand'],
                "start": row_result['gene_start'],
                "chr": row_result['chromosome_name'],
                "chromosome": row_result['chromosome_name'],
                "strand": row_result['strand']
            }
        }



        return returnDict

    """
        Input a generic gene search and return a dictionary of genes that are found.
        As of 3/11/2015 used in 9 places
        geneSearch allows for a | to be divide it out to be an OR search term
        species_dict is to show if it's human etc in the _encode_gene

        always explicit search on gene_id and db_id if not None
        if not definitively found
            lexemes search and associated gene name including db_id
            if not results found for either gene_id, lexemes search and associated gene_name
                then can use feature_mapping search with db_id


        It then goes and gets the metadata for all the genes found.

        Sometimes it is called twice - eg. in Gene Expression Graph etc - we need to stop this!

        Note that explicitSearch is no longer used
    """
    @staticmethod
    def get_genes(db,species_dict,geneSearch,db_id,explicitSearch,maxNumber): #CRITICAL-2 #CRITICAL-4

       # geneSearch = geneSearch.encode('utf-8') #the encode step is unnesssary in python3
       # and it causes error when the encoded string is used in re
        geneSearchFinal = Stemformatics_Gene._preGeneSearch(geneSearch)
        if geneSearchFinal == None:
           return None

        # explicit search on gene id
        conn_string = config['psycopg2_conn_string']

        if db_id == None:
            sql = "select * from genome_annotations where gene_id = (%(geneSearchFinal)s) limit 1;"
            data = {"geneSearchFinal":geneSearchFinal}
        else:
            sql = "select * from genome_annotations where gene_id = (%(geneSearchFinal)s) and db_id = (%(db_id)s) limit 1;"
            data = {"geneSearchFinal":geneSearchFinal,"db_id":db_id}


        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql,data)

        # retrieve the records from the database
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        # Always return if we get an exact match. No need to go into more searches
        if len(result) == 1:
            row_result = result[0]
            return_dict =  Stemformatics_Gene._encode_gene(row_result,species_dict)
            return return_dict

        # Search based on the fts_lexemes tsvector
        if db_id == None:
            sql = "select * from genome_annotations where fts_lexemes @@ to_tsquery(%(geneSearchFinal)s) order by gene_id;"
            data = {"geneSearchFinal":geneSearchFinal}
        else:
            sql = "select * from genome_annotations where fts_lexemes @@ to_tsquery(%(geneSearchFinal)s) and db_id = %(db_id)s order by gene_id;"
            data = {"geneSearchFinal":geneSearchFinal,"db_id":db_id}


        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql,data)

        # retrieve the records from the database
        result = cursor.fetchall()

        # if we get any results lets return them
        if len(result) > 0:

            """
            This is from getAutoComplete
            """

            returnListFirst = []
            returnListSecond = []

            return_dict = {}
            temp_dict = {}
            # get and order the result first
            for row_result in result:
                tempGeneName = row_result['associated_gene_name'].split(' ')
                ensembl_id = row_result['gene_id']
                showSymbol = tempGeneName[0] + ':'+ensembl_id
                for symbol in tempGeneName[1:]:
                    m = re.search('LOC[0-9]{1,10}?',symbol)
                    if m==None:
                        showSymbol = showSymbol + ' ' + symbol

                if showSymbol.lower().startswith(geneSearch.lower()):
                    returnListFirst.append(showSymbol)
                else:
                    returnListSecond.append(showSymbol)

                temp_dict[showSymbol] = row_result

            returnListFirst = sorted(returnListFirst,key=str.lower)
            returnListSecond = sorted(returnListSecond,key=str.lower)
            ordered_list = returnListFirst + returnListSecond

            if maxNumber is not None:
                ordered_list = ordered_list[0:maxNumber]

            # old code
            for showSymbol in ordered_list:
                row_result = temp_dict[showSymbol]
                gene_id = row_result['gene_id']
                gene_return_dict =  Stemformatics_Gene._encode_gene(row_result,species_dict)
                return_dict[gene_id] = gene_return_dict[gene_id]

            cursor.close()
            conn.close()

            return return_dict

        # Search based on feature mappings (just in case they search on a probe)
        if db_id == None:
            sql = "select distinct(from_id) as from_id from stemformatics.feature_mappings where to_id = %(geneSearchFinal)s and from_type = 'Gene' and to_type='Probe' order by from_id limit %(maxNumber)s;"
            data = {"geneSearchFinal":geneSearchFinal,'maxNumber':maxNumber}
        else:
            sql = "select distinct(from_id) as from_id from stemformatics.feature_mappings where to_id = %(geneSearchFinal)s and from_type = 'Gene' and to_type='Probe' and db_id = %(db_id)s order by from_id limit %(maxNumber)s;"
            data = {"geneSearchFinal":geneSearchFinal,'maxNumber':maxNumber,"db_id":db_id}


        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql,data)

        # retrieve the records from the database
        result = cursor.fetchall()

        list_of_gene_ids = []
        for row_result in result:
            gene_id = row_result['from_id']
            list_of_gene_ids.append(gene_id)


        sql = "select * from genome_annotations where gene_id = ANY(%(list_of_gene_ids)s);"
        data = {"list_of_gene_ids":list_of_gene_ids}

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql,data)

        # retrieve the records from the database
        result = cursor.fetchall()

        # if we get any results lets return them
        if len(result) > 0:
            return_dict = {}
            for row_result in result:
                gene_id = row_result['gene_id']
                gene_return_dict =  Stemformatics_Gene._encode_gene(row_result,species_dict)
                return_dict[gene_id] = gene_return_dict[gene_id]

            cursor.close()
            conn.close()

            return return_dict

    """
    This function gets all the probe mappings for a single gene for multiple datasets. This is mainly used
    for YuGene graphs. It uses the chip_type in the datasets_dict
    returns a two dictionaries - one to map chip_type to mapping id and another to map mapping_id to probes

    example:
        result = Stemformatics_Gene.get_probe_mappings_for_datasets(db_id,datasets_dict,ensemblID)
        chip_type_mapping_id_dict = result['chip_type_mapping_id_dict']
        mapping_id_probe_list = result['mapping_id_probe_list']

        mapping_id = chip_type_mapping_id_dict[chip_type]
        probe_list = mapping_id_probe_list[mapping_id]
    """
    @staticmethod
    def get_probe_mappings_for_datasets(db_id,datasets_dict,ensemblID):
        chip_type_probe_lists = {}


        # get a list of chip_types and then get the mappping ids
        # then get all the probe details via feature_mappings

        chip_type_list = []
        ds_set = set()
        for row_result in datasets_dict:
            chip_type = datasets_dict[row_result]['chip_type']
            chip_type_list.append(chip_type)
            chip_type_list.append(chip_type)
            ds_set.add(row_result)

        chip_type_list = list(set(chip_type_list)) # make unique

        ds_list = list(ds_set)


        sql = "select id,mapping_id from datasets where id = ANY (%(ds_list)s) ;"
        data = {"ds_list":ds_list}
        result = s4m_psycopg2._get_psycopg2_sql(sql,data)

        ds_id_mapping_id_dict = {}
        mapping_id_list = []
        for row_result in result:
            mapping_id = row_result['mapping_id']
            ds_id = row_result['id']
            mapping_id_list.append(mapping_id)
            ds_id_mapping_id_dict[ds_id] = mapping_id


        mapping_id_list = list(set(mapping_id_list))
        sql = "select mapping_id,to_id from stemformatics.feature_mappings where db_id = %(db_id)s and from_type = 'Gene' and from_id = %(ensemblID)s and mapping_id = ANY (%(mapping_id_list)s) ;"
        data = {"db_id":db_id,'ensemblID':ensemblID,'mapping_id_list':mapping_id_list}
        result = s4m_psycopg2._get_psycopg2_sql(sql,data)

        mapping_id_probe_list = {}
        for row_result in result:
            mapping_id = row_result['mapping_id']
            probe_id = row_result['to_id']

            if mapping_id not in mapping_id_probe_list:
                mapping_id_probe_list[mapping_id] = [] #make it a list

            mapping_id_probe_list[mapping_id].append(probe_id)

        return {'ds_id_mapping_id_dict':ds_id_mapping_id_dict,'mapping_id_probe_list':mapping_id_probe_list}



    @staticmethod
    def getAutoComplete(db,species_dict,geneSearch,db_id,explicitSearch,maxNumber): #CRITICAL-2

        #set spaces in geneSearch to be and if there are spaces in it.
        geneSearchFinal = Stemformatics_Gene._preGeneSearch(geneSearch)
        if geneSearchFinal == None:
            return None

        if db_id != None:
            db_id = POS_INT.to_python(db_id)

        result = Stemformatics_Gene.get_genes(db,species_dict,geneSearchFinal,db_id,explicitSearch,maxNumber)
        if result is None:
            return []

        returnListFirst = []
        returnListSecond = []

        gene_details = {}
        return_data = []
        # make sure the match on gene name with the gene search is shown first
        for ensembl_id in result:
            tempGeneName = result[ensembl_id]['symbol'].split(' ')
            db_id = result[ensembl_id]['db_id']
            aliases = result[ensembl_id]['Synonyms']
            species = result[ensembl_id]['species']
            symbol = result[ensembl_id]['symbol']
            showSymbol = tempGeneName[0] + ':'+ensembl_id
            description = result[ensembl_id]['description']
            for symbol in tempGeneName[1:]:
                m = re.search('LOC[0-9]{1,10}?',symbol)
                if m==None:
                    showSymbol = showSymbol + ' ' + symbol

            if showSymbol.lower().startswith(geneSearch.lower()):
                returnListFirst.append(showSymbol)
            else:
                returnListSecond.append(showSymbol)

            gene_details[showSymbol] = {'description':description,'ensembl_id':ensembl_id,'symbol':symbol,'db_id':db_id,'aliases':aliases,'species':species}

        returnListFirst = sorted(returnListFirst,key=str.lower)
        returnListSecond = sorted(returnListSecond,key=str.lower)
        returnList = returnListFirst + returnListSecond

        for symbol in returnList:
            return_data.append(gene_details[symbol])

        return return_data


    # gene could be an ensembl gene or a gene symbol. has to return first ensemble gene that matches
    @staticmethod
    def getGene(db,useSqlSoup,gene,db_id): #CRITICAL-2

        try:
            #set spaces in geneSearch to be and if there are spaces in it.

            human_db = int(config['human_db'])

            geneFinal = Stemformatics_Gene._preGeneSearch(gene)

            if geneFinal == None:
                return None

            # do fts query via sqlsoup via match function
            db.schema = 'public'
            fts_filter = db.genome_annotations.fts_lexemes.match(geneFinal)

            if db_id == human_db:
                geneFinal = geneFinal.upper()
            else:
                geneFinal = geneFinal.capitalize()

            search_gene_name = db.genome_annotations.associated_gene_name == geneFinal

            where = and_(search_gene_name,db.genome_annotations.gene_id.like('ENS%'),db.genome_annotations.db_id == db_id)

            geneFound = db.genome_annotations.filter(where).order_by(db.genome_annotations.associated_gene_name).all()

            if len(geneFound) != 1:
                where = and_(fts_filter,db.genome_annotations.gene_id.like('ENS%'),db.genome_annotations.db_id == db_id)
                geneFound = db.genome_annotations.filter(where).order_by(db.genome_annotations.associated_gene_name).all()


            gene_dict = []
            for gene in geneFound:
                ensemblID = geneFound[0].gene_id
                symbol = geneFound[0].associated_gene_name
                chromosome_name = geneFound[0].chromosome_name
                gene_start = geneFound[0].gene_start
                gene_end = geneFound[0].gene_end
                strand = geneFound[0].strand
                gene_dict.append({ 'ensemblID': ensemblID, 'symbol': symbol, 'chr': chromosome_name, 'start': gene_start, 'end': gene_end, 'strand': strand  })

            return gene_dict

        except:
            return None


    @staticmethod
    def _preGeneSearch(geneSearch):

            geneSearch = geneSearch.strip()

            genes = re.findall("[\/\w\.\-\@]{1,}",geneSearch)

            geneSearchFinal = ''

            for i in range(len(genes)):

                try:
                    m = re.search('('+genes[i]+')(.*?)('+genes[i+1]+')',geneSearch)

                    if ' ' in m.group(0) or '&' in m.group(0):
                        geneSearchFinal = geneSearchFinal + genes[i] + '&'
                    else:
                        geneSearchFinal = geneSearchFinal + genes[i] + '|'


                except IndexError:
                    geneSearchFinal = geneSearchFinal + genes[i]

            return geneSearchFinal


    @staticmethod
    def get_ensembl_from_probe(db,probe_list,db_id):
        ensembl_list = []
        r_server = redis.Redis(unix_socket_path=config['redis_server'])

        db_id = int(db_id)

        for probe in probe_list:

            if probe != '':

                try:
                    label_name = 'probe_mappings_'+str(db_id)+'_'+probe
                    found = json.loads(r_server.get(label_name))
                except:
                    continue

                for gene in found:
                    ensembl_list.append(gene)

        return list(set(ensembl_list))



    """
        seach_type options are all, ensembl_id symbol, fts and probe
    """
    @staticmethod
    def get_unique_gene(db,geneSet,db_id,search_type = 'all'): #CRITICAL-2

        # try:
        human_db = int(config['human_db'])
        db_id = int(db_id)

        returnDict = {}

        # geneSet is a list of genes
        for geneSearch in geneSet:

            geneSearchFinal = Stemformatics_Gene._preGeneSearch(geneSearch)
            if geneSearchFinal == None:
                return None


            # firstly, try to find an exact match on the gene_id   (ensembl)
            # firstly, try to find an exact match on the associated gene Id - noting for human it's STAT1 for mouse it's Stat1
            # if that returns nothing, then try the full text search
            # then if that returns nothing, then search on probes


            db.schema = 'public'
            ga = db.genome_annotations

            # set this for testing
            length_gr = 100


            # Check gene_id always regardless
            fts_filter = (ga.gene_id == geneSearchFinal)
            where = and_(fts_filter,ga.db_id == db_id)
            gr = [ (r.gene_id,r) for r in ga.filter(where).order_by(ga.gene_id).all()]
            length_gr = len(gr)



            # search on exact associated gene name (symbol) if ensembl ID not found
            if (search_type == 'symbol' or search_type == 'all') and length_gr == 0:

                # dodgy, but human is all upper case and mouse is capitalized
                if db_id == 56:
                    tempGeneSearchFinal = geneSearchFinal.upper()
                else:
                    tempGeneSearchFinal = geneSearchFinal.capitalize()

                fts_filter = (ga.associated_gene_name == tempGeneSearchFinal)
                where = and_(fts_filter,ga.db_id == db_id)
                gr = [ (r.gene_id,r) for r in ga.filter(where).order_by(ga.gene_id).all()]

                length_gr = len(gr)

            # search on full text search if no exact ensembl or symbol
            if (search_type == 'fts' or search_type == 'all') and length_gr == 0:
                fts_filter = ga.fts_lexemes.match(geneSearchFinal)
                where = and_(fts_filter,ga.db_id == db_id)
                gr = [ (r.gene_id,r) for r in ga.filter(where).order_by(ga.gene_id).all()]
                length_gr = len(gr)


            if (search_type == 'probe' or search_type == 'all') and length_gr == 0:
                # just search as if probe ids using explicit search of term
                # Might have to use perl and prebuild this?
                db.schema = 'stemformatics'
                fm = db.feature_mappings

                join1 = db.join(ga, fm,and_(ga.gene_id==fm.from_id,fm.from_type=="Gene"))
                where = and_(fm.to_id==geneSearchFinal,fm.db_id == db_id,fm.to_type =="Probe")
                gr = [ (r.gene_id,r) for r in join1.filter(where).all() ]



            grDict = dict(gr)

            length = len(grDict)

            if length == 1:
                status = 'OK'
                symbol = gr[0][1].associated_gene_name
                ensemblID = gr[0][0]
            elif length == 0:
                status = 'Not found'
                symbol = ''
                ensemblID = ''
            elif length > 1:
                status = 'Ambiguous'
                symbol = [ row[1].associated_gene_name for row in gr]
                ensemblID = ''
            returnDict[geneSearch] = {'status': status, 'original': geneSearch, 'symbol': symbol, 'ensemblID': ensemblID, 'object': gr}

        return returnDict
        '''except:
            return None'''




    """
        seach_type options are all, ensembl_id symbol, fts and probe
    """
    @staticmethod
    def get_unique_gene_fast(db,geneSet,db_id,search_type,select_all_ambiguous,get_description = True,chip_type = 0,one_search_term = False): #CRITICAL-4 #CRITICAL-6
        r_server = redis.Redis(unix_socket_path=config['redis_server'])

        # try:
        human_db = int(config['human_db'])
        db_id = int(db_id)

        returnDict = {}

        # geneSet is a list of genes
        for geneSearch in geneSet:

            if search_type != 'probes_using_chromosomal_locations' and one_search_term == False:
                geneSearchFinal = Stemformatics_Gene._preGeneSearch(geneSearch)
                if geneSearchFinal == None:
                    return None
            else:
                geneSearchFinal = geneSearch


            # firstly, try to find an exact match on the gene_id   (ensembl)
            # firstly, try to find an exact match on the associated gene Id - noting for human it's STAT1 for mouse it's Stat1
            # if that returns nothing, then try the full text search
            # then if that returns nothing, then search on probes


            db.schema = 'public'
            ga = db.genome_annotations

            # set this for testing
            length_gr = 100

#            if geneSearchFinal in gene_mappings[db_id]:
#                found = gene_mappings[db_id][geneSearchFinal]
#
#                gr = [ (geneSearchFinal,found,geneSearchFinal) ]
#                length_gr = len(gr)
#            else:
#                gr = []
#                length_gr = 0
#
             # check for ensembl gene id always
            try:
                label_name = 'gene_mappings_'+str(db_id)+'_'+geneSearchFinal
                found = r_server.get(label_name)
                if found is not None:
                    gr = [ (geneSearchFinal,found,geneSearchFinal) ]
                    length_gr = len(gr)
                else:
                    gr = []
                    length_gr = 0
            except:
                gr = []
                length_gr = 0



            # check for symbols if applicable in lower case
            if (search_type == 'symbol' or search_type == 'all') and length_gr == 0:

                lowercase_geneSearchFinal = geneSearchFinal.lower()
                try:
                    label_name = 'symbol_mappings_'+str(db_id)+'_'+lowercase_geneSearchFinal
                    found = json.loads(r_server.get(label_name))
                    gr = [ (gene,found[gene],gene,geneSearchFinal) for gene in found]
                    length_gr = len(gr)
                except:
                    gr = []
                    length_gr = 0

            # check for aliases if applicable in lowercase
            if (search_type == 'alias' or search_type == 'all') and length_gr == 0:

                lowercase_geneSearchFinal = geneSearchFinal.lower()

                try:
                    label_name = 'alias_mappings_'+str(db_id)+'_'+lowercase_geneSearchFinal
                    found = json.loads(r_server.get(label_name))
                    gr = [ (gene,found[gene],gene,geneSearchFinal) for gene in found]
                    length_gr = len(gr)
                except:
                    gr = []
                    length_gr = 0

            # check for entrez if applicable
            if (search_type == 'entrez' or search_type == 'all') and length_gr == 0:

                try:
                    label_name = 'entrez_mappings_'+str(db_id)+'_'+geneSearchFinal
                    found = json.loads(r_server.get(label_name))
                    gr = [ (gene,found[gene],gene,geneSearchFinal) for gene in found]
                    length_gr = len(gr)
                except:
                    gr = []
                    length_gr = 0

            # check for refseq if applicable
            if (search_type == 'refseq' or search_type == 'all') and length_gr == 0:


                try:
                    label_name = 'refseq_mappings_'+str(db_id)+'_'+geneSearchFinal
                    found = json.loads(r_server.get(label_name))
                    gr = [ (gene,found[gene],gene,geneSearchFinal) for gene in found]
                    length_gr = len(gr)
                except:
                    gr = []
                    length_gr = 0


            # check for probes if applicable
            if (search_type == 'probe' or search_type == 'all' or search_type == 'probes_using_chromosomal_locations') and length_gr == 0:

                try:
                    label_name = 'probe_mappings_'+str(db_id)+'_'+geneSearchFinal
                    found = json.loads(r_server.get(label_name))
                    gr = [ (gene,found[gene],gene,geneSearchFinal) for gene in found]
                    length_gr = len(gr)
                except:
                    gr = []
                    length_gr = 0




            length = len(gr)

            # print length
            create_single_dict_entry = True
            if length == 1:
                status = 'OK'
                symbol = gr[0][1]
                ensemblID = gr[0][0]
            elif length == 0:
                status = 'Not found'
                symbol = ''
                ensemblID = ''
            elif length > 1:

                if select_all_ambiguous:
                    create_single_dict_entry = False

                    for row in gr:
                        status = 'OK'
                        symbol = row[1]
                        ensemblID = row[0]

                        if chip_type != 0:
                            from S4M_pyramid.model.stemformatics.stemformatics_gene_set import Stemformatics_Gene_Set
                            # changes for task#2527, now ensemblID will be a list of ensemblIDs
                            ensemblID_list = [ensemblID]
                            gene_annotation_names_required = "yes"
                            result = Stemformatics_Gene_Set.get_probes_from_genes(db_id,chip_type,ensemblID_list,gene_annotation_names_required)
                            number_of_probes = len(result[0])
                        else:
                            number_of_probes = ''
                        if get_description == True:
                            # get the description
                            db.schema = "public"
                            ga = db.genome_annotations
                            where = and_(ga.db_id == db_id,ga.gene_id == ensemblID)
                            gene_annotation = ga.filter(where).one()
                            returnDict[ensemblID] = {'number_of_probes': number_of_probes,'status': status, 'original': geneSearch, 'symbol': symbol, 'ensemblID': ensemblID, 'description':gene_annotation.description, 'aliases': gene_annotation.associated_gene_synonym,'EntrezID': gene_annotation.entrezgene_id}
                        else:
                            returnDict[ensemblID] = {'number_of_probes': number_of_probes,'status': status, 'original': geneSearch, 'symbol': symbol, 'ensemblID': ensemblID}
                else:
                    status = 'Ambiguous'
                    symbol = [ row[1] for row in gr]
                    ensemblID = ''

            if create_single_dict_entry:
                returnDict[geneSearch] = {'status': status, 'original': geneSearch, 'symbol': symbol, 'ensemblID': ensemblID}


        return returnDict
        '''except:
            return None'''


    @staticmethod
    def setup_bulk_import_manager_mappings(gene_mapping_raw_file_base_name,feature_mapping_raw_file_base_name): #CRITICAL-4
        r_server = redis.Redis(unix_socket_path=config['redis_server'])



        # Feature mapping is really probe mapping

        # Do the gene mapping via genome_annotation table first
        f = open(gene_mapping_raw_file_base_name,'r')

        gene_mappings = {}
        symbol_mappings = {}
        alias_mappings = {}
        entrez_mappings = {}
        refseq_mappings = {}

        for raw_line in f:
            line = raw_line.replace('\n','')

            temp = line.split("\t")

            db_id = int(temp[0])
            ensembl_gene_id = temp[1]
            symbol = temp[2]
            aliases_raw = temp[3]
            aliases = aliases_raw.split(' ')
            entrez_id = temp[4]
            refseq_ids_raw = temp[5]
            refseq_ids = refseq_ids_raw.split(' ')
            gene_description = temp[6].replace('<br />','').strip()
            lower_gene_description = gene_description.lower()

            lower_symbol = symbol.lower()


            # Gene mapping
            if db_id not in gene_mappings:
                gene_mappings[db_id] = {}

            gene_mappings[db_id][ensembl_gene_id] = symbol
            label_name = 'gene_mappings_'+str(db_id)+'_'+ensembl_gene_id
            result = r_server.set(label_name,symbol)

            # symbol mapping
            if db_id not in symbol_mappings:
                symbol_mappings[db_id] = {}

            if lower_symbol not in symbol_mappings[db_id]:
                symbol_mappings[db_id][lower_symbol] = {}

            symbol_mappings[db_id][lower_symbol][ensembl_gene_id] = symbol

            if lower_gene_description not in symbol_mappings[db_id]:
                symbol_mappings[db_id][lower_gene_description] = {}

            symbol_mappings[db_id][lower_gene_description][ensembl_gene_id] = symbol

            # alias mapping
            if db_id not in alias_mappings:
                alias_mappings[db_id] = {}

            for alias in aliases:

                if alias != '':
                    lower_alias = alias.lower()

                    if alias not in alias_mappings[db_id]:
                        alias_mappings[db_id][lower_alias] = {}

                    alias_mappings[db_id][lower_alias][ensembl_gene_id] = symbol

            # entrez mapping
            if db_id not in entrez_mappings:
                entrez_mappings[db_id] = {}

            if entrez_id != '':
                if entrez_id not in entrez_mappings[db_id]:
                    entrez_mappings[db_id][entrez_id] = {}

                entrez_mappings[db_id][entrez_id][ensembl_gene_id] = symbol

            # refseq mapping
            if db_id not in refseq_mappings:
                refseq_mappings[db_id] = {}

            for refseq_id in refseq_ids:

                if refseq_id != '':

                    if refseq_id not in refseq_mappings[db_id]:
                        refseq_mappings[db_id][refseq_id] = {}

                    refseq_mappings[db_id][refseq_id][ensembl_gene_id] = symbol




        f.close()



        probe_mappings = {}


        f = open(feature_mapping_raw_file_base_name,'r')

        probe_mappings = {}


        for raw_line in f:
            line = raw_line.replace('\n','')

            temp = line.split("\t")

            db_id = int(temp[0])
            chip_type = temp[1]
            map_from_type = temp[2] # usually gene
            map_from_id = temp[3]
            map_to_type = temp[4] # usually probe
            map_to_id = temp[5] #probe ID

            if map_from_type == "Gene" and map_to_type == "Probe":

                probe_id = map_to_id
                ensembl_gene_id = map_from_id

                if db_id not in probe_mappings:
                    probe_mappings[db_id] = {}

                if probe_id not in probe_mappings[db_id]:
                    probe_mappings[db_id][probe_id] = {}

                try:
                    symbol = gene_mappings[db_id][ensembl_gene_id]
                except:
                    symbol = ''

                if symbol != '':
                    probe_mappings[db_id][probe_id][ensembl_gene_id] = symbol


        for db_id in symbol_mappings:
            for text in symbol_mappings[db_id]:
                json_result = json.dumps(symbol_mappings[db_id][text])
                label_name = 'symbol_mappings_'+str(db_id)+'_'+text
                result = r_server.set(label_name,json_result)

        for db_id in alias_mappings:
            for text in alias_mappings[db_id]:
                json_result = json.dumps(alias_mappings[db_id][text])
                label_name = 'alias_mappings_'+str(db_id)+'_'+text
                result = r_server.set(label_name,json_result)

        for db_id in entrez_mappings:
            for text in entrez_mappings[db_id]:
                json_result = json.dumps(entrez_mappings[db_id][text])
                label_name = 'entrez_mappings_'+str(db_id)+'_'+text
                result = r_server.set(label_name,json_result)

        for db_id in refseq_mappings:
            for text in refseq_mappings[db_id]:
                json_result = json.dumps(refseq_mappings[db_id][text])
                label_name = 'refseq_mappings_'+str(db_id)+'_'+text
                result = r_server.set(label_name,json_result)

        for db_id in probe_mappings:
            for text in probe_mappings[db_id]:
                json_result = json.dumps(probe_mappings[db_id][text])
                label_name = 'probe_mappings_'+str(db_id)+'_'+text
                result = r_server.set(label_name,json_result)

        return [gene_mappings,symbol_mappings,alias_mappings,entrez_mappings,probe_mappings,refseq_mappings]




    @staticmethod
    def get_species_from_db_id(db,db_id): #CRITICAL-2
        db.schema = 'public'
        ad = db.annotation_databases
        result = ad.filter(ad.an_database_id == db_id).one()
        return result.genome_version


    @staticmethod
    def get_ucsc_db_id_from_db_id(db,db_id): #CRITICAL-2
        db.schema = 'public'
        ad = db.annotation_databases
        result = ad.filter(ad.an_database_id == db_id).one()
        species = result.model_id # eg. Mouse or Human

        if species == 'Mouse':
            ucsc_db_id = config['ucsc_mouse_db_id']
        if species == 'Human':
            ucsc_db_id = config['ucsc_human_db_id']
        return ucsc_db_id

    @staticmethod
    def get_ucsc_data_for_a_gene(db,db_id,ensemblID): #CRITICAL-2
        db.schema = 'public'
        ga = db.genome_annotations
        where = and_(ga.gene_id == ensemblID,ga.db_id == db_id)
        result = ga.filter(where).one()
        ucsc_data = {}
        ucsc_data["strand"] = result.strand
        ucsc_data["end"]= result.gene_end
        ucsc_data["start"]= result.gene_start
        ucsc_data["chr"]= result.chromosome_name
        ucsc_data["ucsc_db_id"] = Stemformatics_Gene.get_ucsc_db_id_from_db_id(db,db_id)

        ucsc_data['base_url'] = config['ucsc_base_url']
        return ucsc_data

    @staticmethod
    def find_feature_search_items(feature_search_term,species,feature_type,use_json):

        if feature_search_term == None or feature_search_term == '':
            if use_json:
                return json.dumps(["No features found. Please try again"])
            else:
                return None

        feature_search_items = {}
        feature_annotation_file = config['feature_annotation_file']
        output = subprocess.check_output("grep -i \""+feature_search_term+"\" "+feature_annotation_file+"; exit 0",shell=True).decode("utf-8")
        if output == "":
            if use_json:
                return json.dumps(["No features found. Please try again"])
            else:
                return None

        else:
            temp_output_list = output.split("\n")
            if temp_output_list is not None:
                if len(temp_output_list) > 100:
                    temp_output_list = temp_output_list[0:100]

            last_position = len(temp_output_list) - 1
            if temp_output_list[last_position] == "":
                temp_output_list.pop(-1)

            output_list = []
            for row in temp_output_list:
                array_row_items = row.split("\t")
                row_dict = {}
                row_dict['feature_type'] = array_row_items[2]
                row_dict['feature_id']  = array_row_items[0]
                row_dict['species']  = array_row_items[1]
                if species == None  or (species != None and species == row_dict['species']):
                    row_dict['symbol'] = array_row_items[3]
                    row_dict['aliases'] = array_row_items[4]
                    row_dict['description'] = array_row_items[5]
                    row_dict['sequence'] = array_row_items[6]
                    output_list.append(row_dict)

        #return temp_output_list
        if use_json:
            result = json.dumps(output_list)
        else:
            result = output_list

        return result


    @staticmethod
    def autocomplete_feature_search_items(feature_search_term,species,feature_type):
        use_json = False
        temp_result = Stemformatics_Gene.find_feature_search_items(feature_search_term,species,feature_type,use_json)
        result = []
        if temp_result is not None:
            for item in temp_result:
                del item['sequence']
                result.append(item)

        else:
            result = []
        return json.dumps(result)


    @staticmethod
    def get_search_return_order(geneSearch, search_results):
        returnListFirst = []
        returnListSecond = []
        returnListThird = []
        delimiter = '::'
        for gene in search_results:
            if gene['symbol'].lower().startswith(geneSearch.lower()):
                returnListFirst.append(str(gene['symbol']+delimiter+gene['EnsemblID']))
            else:
                if gene['aliases'].lower().find(geneSearch.lower()) != -1:
                    returnListSecond.append(str(gene['symbol']+delimiter+gene['EnsemblID']))
                else:
                    returnListThird.append(str(gene['symbol']+delimiter+gene['EnsemblID']))

        # turn into a set, then a list, then sorted. turning it into a set removes duplicates
        returnListFirst  = sorted(list(set(returnListFirst)),  key=str.lower)
        returnListSecond = sorted(list(set(returnListSecond)), key=str.lower)
        returnListThird  = sorted(list(set(returnListThird)),  key=str.lower)

        returnList = returnListFirst + returnListSecond + returnListThird

        order = []
        for composite_gene in returnList:
            temp = composite_gene.split(delimiter)
            symbol = temp[0]
            ensembl_id = temp[1]
            order.append(ensembl_id)
        return order




    @staticmethod
    def get_last_gene_list(uid,gene_list_type):
        try:
            uid = int(uid)
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            if gene_list_type == 'public':
                sql = "select id from stemformatics.gene_sets where gene_set_type = 'Public' order by id desc limit 1;"
                cursor.execute(sql)

            if gene_list_type == 'private':
                sql = "select id from stemformatics.gene_sets where uid = %s order by id desc limit 1;"
                data = (uid,)
                cursor.execute(sql,data)

            # retrieve the records from the database
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            return result[0][0]



        except:
            return None


    @staticmethod
    def search_and_choose_genes(db,species_dict,gene_search,db_id,max_number):
        explicit_search = True
        result  =  Stemformatics_Gene.getAutoComplete(db,species_dict,gene_search,db_id,explicit_search,max_number)
        final_dict = {}
        final_dict['filter'] = gene_search
        final_dict['genes'] = result
        final_dict['order'] = []
        return final_dict

    @staticmethod
    def check_number_of_gene_id_found(db_id,species_dict,geneSearch):
        if (geneSearch is None) or (len(geneSearch) < 1):
            return "0"

        select_all_ambiguous = True
        from S4M_pyramid.model.stemformatics.stemformatics_dataset import Stemformatics_Dataset
        # chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
        gene_list = []
        gene_list.append(geneSearch)
        get_description = True
        result = Stemformatics_Gene.get_genes(None, species_dict, geneSearch, db_id, False, None)

        if result is None:
            return "0"

        if len(result) == 1:
            temp_gene = next(iter(result.values()))#result.itervalues().next()
            ensemblID = temp_gene['EnsemblID']
            return "1"

        else:
            return "many"

    @staticmethod
    def get_mapping_for_genes(gene_list,ds_id,db_id):
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        # setting db = None as we don't use it when getting chip Type
        db = None
        unique_gene_list = set(gene_list)
        r_server = redis.Redis(unix_socket_path=config['redis_server'])

        # get the mapping id for ds_id
        result = r_server.get("dataset_mapping_data")
        if not result:
            # get the mapping id from db if mapping id not available
            mapping_id = Stemformatics_Dataset.get_dataset_mapping_id(ds_id)
            # now refresh redis
            Stemformatics_Dataset.set_datasets_mapping_id_into_redis()
        else:
            mapping_id = Stemformatics_Expression.unpickle_expression_data(result)

        # check if mapping id for that dataset is available, if not means it is new datast and we should update redis
        if ds_id not in mapping_id:
            mapping_id = Stemformatics_Dataset.get_dataset_mapping_id(ds_id)
            Stemformatics_Dataset.set_datasets_mapping_id_into_redis()

        delimiter = config['redis_delimiter']
        ref_type = 'ensemblID'
        genes_not_in_redis = []
        probe_list = []
        gene_mapping_redis = {}

        # first get the gene mapping from redis
        for gene in unique_gene_list:
            gene_mapping_redis[gene] = []
            label_name = "gene_mapping_data"+ delimiter + str(mapping_id[ds_id]) + delimiter + str(gene) + delimiter + str(ref_type) + delimiter + str(db_id)
            result = r_server.get(label_name)
            if result is not None:
                unpickled_data = Stemformatics_Expression.unpickle_expression_data(result)
                gene_mapping_redis[gene].extend(unpickled_data)
            else:
                genes_not_in_redis.append(gene)

        # now check gene not found in redis list
        if not genes_not_in_redis:
            for gene in gene_list:
                probes = gene_mapping_redis[gene]
                probe_list.extend(probes)
            return [probe_list,gene_mapping_redis]
        else:
            # get mapping for genes from database for all genes mapping not in redis
            gene_annotation_names_required = "no"
            result = Stemformatics_Gene_Set.get_probes_from_genes(db_id,ds_id,genes_not_in_redis,gene_annotation_names_required)
            probe_to_gene_dict = result[1]

            # create a gene to probe mapping from probe to gene mapping
            gene_mapping_database = {}
            for gene in genes_not_in_redis:
                gene_mapping_database[gene] = []
            for probe in probe_to_gene_dict:
                gene = probe_to_gene_dict[probe]
                gene_mapping_database[gene].append(probe)

            # now for all genes store the data into redis
            data_result = Stemformatics_Gene.set_mapping_data_in_redis("ensemblID",ds_id,db_id,gene_mapping_database,genes_not_in_redis)
            if data_result == True:
                # now combine this data with redis data for each gene
                for gene in genes_not_in_redis:
                    gene_mapping_redis[gene] = gene_mapping_database[gene]
            else:
                return "Something went worng Try again"

            # create a full probe list
            for gene in gene_list:
                probes = gene_mapping_redis[gene]
                probe_list.extend(probes)

            return [probe_list,gene_mapping_redis]

    @staticmethod
    def set_mapping_data_in_redis(ref_type,ds_id,db_id,mapping_data,ref_id_not_in_redis):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??

        # get the mapping id for ds_id
        result = r_server.get("dataset_mapping_data")
        mapping_id = Stemformatics_Expression.unpickle_expression_data(result)

        delimiter = config['redis_delimiter']
        expiry_time = config['expiry_time']
        for ref_id in ref_id_not_in_redis:
            if ref_type == "ensemblID":
                label_name = "gene_mapping_data"+ delimiter + str(mapping_id[ds_id]) + delimiter + str(ref_id) + delimiter + str(ref_type) + delimiter + str(db_id)

            elif ref_type == "gene_set_id":
                label_name = "gene_set_mapping_data"+ delimiter + str(mapping_id[ds_id]) + delimiter + str(ref_id) + delimiter + str(ref_type) + delimiter + str(db_id)

            data = Stemformatics_Expression.pickle_expression_data(mapping_data[ref_id])
            result = r_server.set(label_name,data)
            if result == True:
                expiry = r_server.expire(label_name,expiry_time)
                # if expiry == False:
                #     return False

        return True

    @staticmethod
    def get_mapping_for_gene_set(ref_id,db_id,ds_id):
        # setting db = None as we don't use it when getting chip Type
        db = None
        from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression # wouldn't work otherwise??
        # first check the mapping for each gene set in redis
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']

        # get the mapping id for ds_id
        result = r_server.get("dataset_mapping_data")
        if not result:
            resut = Stemformatics_Dataset.set_datasets_mapping_id_into_redis()
            mapping_id = Stemformatics_Expression.unpickle_expression_data(result)
        else:
            mapping_id = Stemformatics_Expression.unpickle_expression_data(result)

        # check if mapping id for that dataset is available, if not means it is new datast and we should update redis
        if ds_id not in mapping_id:
            Stemformatics_Dataset.set_datasets_mapping_id_into_redis()

        ref_type = 'gene_set_id'
        gene_set_mapping_data_from_redis = {}
        gene_set_mapping_data_from_database = {}
        gene_set_not_in_redis = []
        for gene_set_id in ref_id:
            label_name = "gene_set_mapping_data"+ delimiter + str(mapping_id[ds_id]) + delimiter + str(gene_set_id) + delimiter + str(ref_type) + delimiter + str(db_id)
            result = r_server.get(label_name)
            if result is not None:
                unpickled_data = Stemformatics_Expression.unpickle_expression_data(result)
                gene_set_mapping_data_from_redis[gene_set_id] = (unpickled_data)
            else:
                gene_set_not_in_redis.append(gene_set_id)

        # now check if gene_set_not_in_redis is empty or not
        if not gene_set_not_in_redis:
            return gene_set_mapping_data_from_redis
        else:
            # get the mapping for gene_set_ids not in redis
            chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
            for gene_set_id in gene_set_not_in_redis:
                # it will be executed only once as we always have 1 gene_set_id in our list
                gene_set_mapping_data = Stemformatics_Gene_Set.get_probes_from_gene_set_id(db,db_id,ds_id,gene_set_id)
                dict_of_probe_to_gene_id = gene_set_mapping_data[2]
                probe_list = gene_set_mapping_data[0]

                gene_set_mapping_data_from_database[gene_set_id] = dict_of_probe_to_gene_id.values()

                # combine the database data with redis data
                gene_set_mapping_data_from_redis[gene_set_id] = gene_set_mapping_data_from_database[gene_set_id]

            # save the mapping in redis for all gene set id
            data_result = Stemformatics_Gene.set_mapping_data_in_redis("gene_set_id",ds_id,db_id,gene_set_mapping_data_from_database,gene_set_not_in_redis)
            return gene_set_mapping_data_from_redis
            # if data_result == True:
            #     return gene_set_mapping_data_from_redis
            # else:
            #     return "Something went wrong"
