#TODO-1
import logging
log = logging.getLogger(__name__)

from sqlalchemy import and_

import json

__all__ = ['Stemformatics_Transcript']

import formencode.validators as fe

class Stemformatics_Transcript(object):
    """\
    Stemformatics_Transcript Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for transcript data

    Please note for most of these functions you will have to pass in the db object

    All functions have a try that will return None if errors are found

    """

    def __init__ (self):
        pass

    @staticmethod
    def get_gene_id_transcript_annotations(db,db_id,gene_id): #CRITICAL-2
        #try:

        db.schema = 'stemformatics'
        tx_ann = db.transcript_annotations
        where = and_(tx_ann.gene_id == gene_id,tx_ann.db_id == db_id)
        result = tx_ann.filter(where).order_by(tx_ann.transcript_name).all()

        return result

        #except:
            #return None


    """
        This is the old way of calculating statistics etc for filtering at a transcript level
        Keep this to add a secondary test for now. 22/07/2011
        Using database to filter

    """
    @staticmethod
    def get_filtered_transcript_annotations(db,db_id,genes,filters,order_by): #CRITICAL-2

        #try:

        base_where = None

        db.schema = 'stemformatics'
        tx_ann = db.transcript_annotations


        for filter in filters:

                value = filters[filter]

                if filter == 'signal_peptide' and base_where is None:
                    base_where = tx_ann.signal_peptide == value
                elif filter == 'signal_peptide' and base_where is not None:
                    base_where = and_(base_where,tx_ann.signal_peptide == Value)

                if filter == 'tm_domain' and base_where is None:
                    base_where = tx_ann.tm_domain == value
                elif filter == 'tm_domain' and base_where is not None:
                    base_where = and_(base_where,tx_ann.tm_domain == value)


                if filter == 'targeted_mirna' and base_where is None:
                    base_where = tx_ann.targeted_mirna == value
                elif filter == 'targeted_mirna' and base_where is not None:
                    base_where = and_(base_where,tx_ann.targeted_mirna == value)


        where = and_(base_where,tx_ann.db_id == db_id,tx_ann.gene_id.in_(genes))

        tx_result = tx_ann.filter(where).order_by(order_by).all()


        count_sp = 0
        count_tm = 0
        count_mirna = 0
        new_genes = {}

        for transcript in tx_result:

            # setup the gene dictionary
            if transcript.gene_id not in new_genes:
                new_genes[transcript.gene_id] = {'count_tx': 1, 'count_sp': 0, 'count_tm': 0, 'count_mirna': 0}
            else:
                new_genes[transcript.gene_id]['count_tx'] = new_genes[transcript.gene_id]['count_tx'] + 1


            if transcript.signal_peptide:
                count_sp = count_sp + 1
                new_genes[transcript.gene_id]['count_sp'] = new_genes[transcript.gene_id]['count_sp'] + 1

            if transcript.tm_domain:
                count_tm = count_tm + 1
                new_genes[transcript.gene_id]['count_tm'] = new_genes[transcript.gene_id]['count_tm'] + 1

            if transcript.targeted_mirna:
                count_mirna = count_mirna + 1
                new_genes[transcript.gene_id]['count_mirna'] = new_genes[transcript.gene_id]['count_mirna'] + 1




        statistics = {}
        statistics['count_sp'] = count_sp
        statistics['count_tm'] = count_tm
        statistics['count_mirna'] = count_mirna
        statistics['count_transcripts'] = len(tx_result)
        statistics['count_genes'] = len(new_genes)

        return [tx_result,statistics,new_genes]

        #except:
            #return None



    @staticmethod
    def saveFilter(db,uid,name,filter): #CRITICAL-2
        json_filter = json.dumps(filter)
        db.schema = 'stemformatics'
        af = db.annotation_filters
        result = af.insert(uid=uid ,json_filter = json_filter, name = name)

        db.commit()
        db.flush()

        return int(result.id)


    @staticmethod
    def loadFilter(db,filter_id,uid): #CRITICAL-2

        db.schema = 'stemformatics'
        af = db.annotation_filters
        where = and_(af.id==filter_id,af.uid == uid)
        result = af.filter(where).one()

        dict_result = json.loads(result.json_filter)

        return dict_result


    @staticmethod
    def getFilters(db,uid): #CRITICAL-2

        db.schema = 'stemformatics'
        af = db.annotation_filters
        where = af.uid == uid
        result = af.filter(where).all()

        for filter in result:
            filter.dict_filter = json.loads(filter.json_filter)

        return result


    @staticmethod
    def deleteFilter(db,filter_id,uid): #CRITICAL-2

        db.schema = 'stemformatics'
        af = db.annotation_filters
        where = and_(af.id==filter_id,af.uid == uid)
        result = af.filter(where).one()

        db.delete(result)
        db.commit()
        db.flush()
        return True



    @staticmethod
    def get_transcript_annotations(db,db_id,genes): #CRITICAL-2

        #try:

        db.schema = 'stemformatics'
        tx_ann = db.transcript_annotations

        db.schema = 'public'

        ga = db.with_labels(db.genome_annotations)


        where = and_(tx_ann.db_id == db_id,tx_ann.gene_id.in_(genes))

        join1 = db.join(ga,tx_ann,tx_ann.gene_id==ga.public_genome_annotations_gene_id)

        tx_result = join1.filter(where).all()

        tx_dict = {}
        for transcript in tx_result:
            tx_dict[transcript.transcript_id] = {'gene_name': transcript.public_genome_annotations_associated_gene_name, 'gene_id': transcript.gene_id, 'tm_domain': transcript.tm_domain, 'signal_peptide': transcript.signal_peptide, 'transcript_name': transcript.transcript_name, 'protein_length': transcript.protein_length, 'targeted_mirna': transcript.targeted_mirna}


        return tx_dict

        #except:
            #return None

    """
        get_statistics expects a dictionary of transcripts with

            this_gene_id = tx_dict[transcript]['gene_id']
            this_sp = tx_dict[transcript]['signal_peptide']
            this_tm = tx_dict[transcript]['tm_domain']
            this_mirna = tx_dict[transcript]['targeted_mirna']

        also order_by being the name of the field in the dictionary eg. transcript_name



        It will return both the gene centric and transcription centric filtering provided

        return [new_genes,gene_statistics,new_tx,tx_statistics]

    """
    @staticmethod
    def get_statistics(tx_dict,filters,order_by,filter_level): #CRITICAL-4



        # filter_level of transcript
        tx_count_sp = 0
        tx_count_tm = 0
        tx_count_mirna = 0
        tx_count_tx = 0
        tx_gene_list = []

        new_genes = {}
        ordered_list = []
        new_tx = {}

        for transcript in tx_dict:

            this_gene_id = tx_dict[transcript]['gene_id']
            this_sp = tx_dict[transcript]['signal_peptide']
            this_tm = tx_dict[transcript]['tm_domain']
            this_mirna = tx_dict[transcript]['targeted_mirna']
            this_gene_name = tx_dict[transcript]['gene_name']

            # setup the gene dictionary
            if filter_level == 'Gene':
                if this_gene_id not in new_genes:
                    new_genes[this_gene_id] = {'gene_id': this_gene_id,'gene_name': this_gene_name, 'count_tx': 1, 'count_sp': 0, 'count_tm': 0, 'count_mirna': 0}
                else:
                    new_genes[this_gene_id]['count_tx'] = new_genes[this_gene_id]['count_tx'] + 1


                # make this a two dimensional list for ordering later
                if this_gene_id not in new_tx:
                    new_tx[this_gene_id] = []


                transcript_name = tx_dict[transcript]['transcript_name']
                new_tx[this_gene_id].append((transcript_name,tx_dict[transcript]))


                # new_tx[this_gene_id][transcript] = tx_dict[transcript]



                if this_sp:
                    new_genes[this_gene_id]['count_sp'] = new_genes[this_gene_id]['count_sp'] + 1

                if this_tm:
                    new_genes[this_gene_id]['count_tm'] = new_genes[this_gene_id]['count_tm'] + 1

                if this_mirna:
                    new_genes[this_gene_id]['count_mirna'] = new_genes[this_gene_id]['count_mirna'] + 1


            # do some filtering based off transcriptions
            if filter_level == 'Transcript':
                ignore_tx = False
                if 'signal_peptide' in filters:
                    if filters['signal_peptide'] and this_sp == 0:
                        ignore_tx = True

                    if not filters['signal_peptide'] and this_sp > 0:
                        ignore_tx = True


                if 'tm_domain' in filters:
                    if filters['tm_domain'] and this_tm == 0:
                        ignore_tx = True

                    if not filters['tm_domain'] and this_tm > 0:
                        ignore_tx = True



                if 'targeted_mirna' in filters:
                    if filters['targeted_mirna'] and this_mirna == 0:
                        ignore_tx = True
                    if not filters['targeted_mirna'] and this_mirna > 0:
                        ignore_tx = True



                if not ignore_tx:
                    tx_count_sp = tx_count_sp + this_sp
                    tx_count_tm = tx_count_tm + this_tm
                    tx_count_mirna = tx_count_mirna + this_mirna
                    tx_count_tx = tx_count_tx + 1

                    #store this info for later
                    new_tx[transcript] = tx_dict[transcript]

                    # store this info to calculate genes in tx based filtering
                    if this_gene_id not in new_genes:
                        new_genes[this_gene_id] = {'gene_id': this_gene_id,'gene_name': this_gene_name,'count_tx': 1, 'count_sp': 0, 'count_tm': 0, 'count_mirna': 0}
                    else:
                        new_genes[this_gene_id]['count_tx'] = new_genes[this_gene_id]['count_tx'] + 1

                    if this_sp:
                        new_genes[this_gene_id]['count_sp'] = new_genes[this_gene_id]['count_sp'] + 1

                    if this_tm:
                        new_genes[this_gene_id]['count_tm'] = new_genes[this_gene_id]['count_tm'] + 1

                    if this_mirna:
                        new_genes[this_gene_id]['count_mirna'] = new_genes[this_gene_id]['count_mirna'] + 1

                    ordered_field_value = tx_dict[transcript][order_by]
                    ordered_list.append((ordered_field_value,new_tx[transcript]))




                statistics = {}
                statistics['count_sp'] = tx_count_sp
                statistics['count_tm'] = tx_count_tm
                statistics['count_mirna'] = tx_count_mirna
                statistics['count_transcripts'] = tx_count_tx

                # ensure no duplicate genes
                statistics['count_genes'] = len(new_genes)



        if filter_level == 'Gene':
            gene_count_sp = 0
            gene_count_tm = 0
            gene_count_mirna = 0
            gene_count_tx = 0
            delete_genes = []


            genes_count_sp_yes = 0
            genes_count_sp_no = 0
            genes_count_sp_either = 0

            genes_count_tm_yes = 0
            genes_count_tm_no = 0
            genes_count_tm_either = 0


            for gene in new_genes:

                this_sp = new_genes[gene]['count_sp']
                this_mirna = new_genes[gene]['count_mirna']
                this_tm = new_genes[gene]['count_tm']
                this_tx = new_genes[gene]['count_tx']

                ignore_gene = False
                if 'signal_peptide' in filters:
                    if filters['signal_peptide'] and this_sp == 0:
                        ignore_gene = True

                    if not filters['signal_peptide'] and this_sp > 0:
                        ignore_gene = True


                if 'tm_domain' in filters:
                    if filters['tm_domain'] and this_tm == 0:
                        ignore_gene = True

                    if not filters['tm_domain'] and this_tm > 0:
                        ignore_gene = True



                if 'targeted_mirna' in filters:
                    if filters['targeted_mirna'] and this_mirna == 0:
                        ignore_gene = True
                    if not filters['targeted_mirna'] and this_mirna > 0:
                        ignore_gene = True


                if not ignore_gene:
                    gene_count_sp = gene_count_sp + this_sp
                    gene_count_tm = gene_count_tm + this_tm
                    gene_count_mirna = gene_count_mirna + this_mirna
                    gene_count_tx = gene_count_tx + this_tx

                    if this_sp > 0:
                        genes_count_sp_yes = genes_count_sp_yes +  1
                    else:
                        genes_count_sp_no = genes_count_sp_no +  1

                    genes_count_sp_either = genes_count_sp_either + 1

                    if this_tm > 0:
                        genes_count_tm_yes = genes_count_tm_yes +  1
                    else:
                        genes_count_tm_no = genes_count_tm_no +  1

                    genes_count_tm_either = genes_count_tm_either + 1



                    ordered_field_value = new_genes[gene][order_by]
                    ordered_list.append((ordered_field_value,new_genes[gene]))

                else:
                    delete_genes.append(gene)


            for gene in delete_genes:
                del new_genes[gene]

            statistics = {}
            statistics['count_sp'] = gene_count_sp
            statistics['count_tm'] = gene_count_tm
            statistics['count_mirna'] = gene_count_mirna
            statistics['count_transcripts'] = gene_count_tx
            statistics['count_genes'] = len(new_genes)

            statistics['count_sp_yes'] = genes_count_sp_yes
            statistics['count_sp_no'] = genes_count_sp_no
            statistics['count_sp_either'] = genes_count_sp_either
            statistics['count_tm_yes'] = genes_count_tm_yes
            statistics['count_tm_no'] = genes_count_tm_no
            statistics['count_tm_either'] = genes_count_tm_either


        return [new_genes,new_tx,statistics,ordered_list]

