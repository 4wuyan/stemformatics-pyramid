#TODO-1
import sqlalchemy as SA
from sqlalchemy import or_, and_, desc
import json,re,logging,redis,numpy
log = logging.getLogger(__name__)

from pylons import config
from guide.model.stemformatics import *

""" if ref_type == 'ensemblID':
            if ref_type == 'probeID':
            if ref_type == 'miRNA':
            if ref_type == 'gene_set_id':

"""

# http://code.activestate.com/recipes/135435-sort-a-string-using-numeric-order/
def stringSplitByNumbers(x):
    regex = re.compile('(\d+)')
    split_name = regex.split(x)
    return_list = [int(piece) if piece.isdigit() else piece for piece in split_name]
    return return_list

class Graph_Data(object):
    def __init__ (self,db,ds_id,ref_type,ref_id,db_id,list_of_samples_to_remove,species_dict,select_probes = None):
        self.delimiter = config['delimiter']
        self.ds_id = int(ds_id)
        self.ref_type = ref_type
        self.ref_id = ref_id
        self.db_id = int(db_id)
        self.chip_type = Stemformatics_Dataset.getChipType(db,ds_id)
        self.list_of_samples_to_remove = list_of_samples_to_remove
        self.species_dict = species_dict
        self.species = species_dict[self.db_id]['sci_name']
        self.header = Stemformatics_Notification.get_header_name_from_datasetId(self.ds_id)
        self.select_probes = select_probes

        if self.select_probes is not None:
            try:
                filter_probes = re.sub('\s{1,}',self.delimiter,self.select_probes)
                temp_probes = filter_probes.split(self.delimiter)
                self.select_probes = [ probe.strip() for probe in temp_probes]
            except:
                self.select_probes = None

        # initialise the database calls
        self.set_initial_data(db)

    def set_initial_data(self,db):

        if self.ref_type == 'ensemblID':
            ref_id_list = []
            get_probes_from_genes = "no"
            ref_id_list.append(self.ref_id)
            result = Stemformatics_Gene_Set.get_probes_from_genes(self.db_id,self.ds_id,ref_id_list,get_probes_from_genes)
            probe_list = result[0]
            self.probe_to_gene_dict = result[1]
            self.gene_data = Stemformatics_Gene.getGene(db,True,self.ref_id,self.db_id)[0]
            self.gene_to_probe_dict = {}
            self.gene_to_probe_dict[self.ref_id] = probe_list

        if self.ref_type == 'probeID':
            probe_list = []
            probe_list.append(self.ref_id)
            if self.select_probes is None:
                self.select_probes = [self.ref_id]
            self.gene_to_probe_dict = None

        if self.ref_type == 'miRNA':
            probe_list = []
            use_json = False
            result = Stemformatics_Gene.find_feature_search_items(self.ref_id,self.species,self.ref_type,use_json)
            for feature in result:
                aliases_array = feature['aliases'].split(",")
                probe_list = probe_list + aliases_array
                probe_list.append(feature['feature_id'])

            self.mirna_data = result
            self.gene_to_probe_dict = None

            lower_case_probe_list = []
            for probe in probe_list:
                lower_case_probe_list.append(probe.lower())

            probe_list = list(set(lower_case_probe_list))

        if self.ref_type == 'gene_set_id':
            result = Stemformatics_Gene_Set.get_probes_from_gene_set_id(db,self.db_id,self.chip_type,self.ref_id)
            probe_list = result[0]
            self.probe_to_gene_dict = result[1]
            # changes for task 2527, generating a dict with gene-probe mapping_dict
            self.probe_to_gene_id_dict = result[2]
            self.gene_to_probe_dict = {}
            gene_list = []
            for gene in self.probe_to_gene_id_dict.values():
                if gene in gene_list:
                    continue
                else:
                    gene_list.append(gene)

            # now converting the gene names to gene ids
            for gene in gene_list:
                self.gene_to_probe_dict[gene] = []

            # now create a dict for mapping
            for probe in self.probe_to_gene_id_dict:
                gene_name = self.probe_to_gene_id_dict[probe]
                self.gene_to_probe_dict[gene_name].append(probe)

            self.gene_data = None
            # 0 used as uid is not used anymore
            self.gene_set_name = Stemformatics_Gene_Set.get_gene_set_name(db,0,self.ref_id)

        new_probe_list = []
        if self.select_probes is not None:
            for temp_probe in self.select_probes:
                if temp_probe not in new_probe_list:
                    new_probe_list.append(temp_probe)
            probe_list = new_probe_list

            # want to change the title of the graph if multiple selected
            if self.ref_type == 'probeID':
                self.ref_id = 'Selected'

        probe_list = list(set(probe_list))
        self.raw_probe_list = probe_list
        self.probe_list = probe_list
        self.probe_dict = Stemformatics_Probe.get_gene_mappings_for_probe(probe_list,self.db_id,self.chip_type)

        self.probe_expression_rows = self.__get_expression_rows()
        self.number_of_probes = len(self.probe_expression_rows)
        self.sample_labels = self.__get_sample_labels()



        # remove any samples
        self.remove_samples(self.list_of_samples_to_remove)

        # work out the rest of the limitSortBy
        # sampleTypes , dataset metadata things needed
        # min_y_axis should override platform
        # do this first as we need to set self.mapping_id 
        # before running __set_probe_and_platform_information
        self.__set_dataset_metadata_information(db)

        # Calculate if the probes are multi-mapping and
        self.__set_probe_and_platform_information(db)
        self.__set_probe_display_names(db)


    def __return_renamed_probe(self,raw_probe_id):
        position = self.raw_probe_list.index(raw_probe_id)
        renamed_probe_id = self.probe_list[position]
        return renamed_probe_id

    def __get_cumulative_sample_labels(self):
        return Stemformatics_Expression.get_cumulative_sample_labels(self.ds_id)

    def __get_sample_labels(self):
        return Stemformatics_Expression.get_sample_labels(self.ds_id)

    def __get_expression_rows(self):
        raw_expression_rows = Stemformatics_Expression.get_expression_rows(self.ds_id,self.raw_probe_list)
        expression_rows = {}
        for raw_probe_id in raw_expression_rows:
            renamed_probe_id = self.__return_renamed_probe(raw_probe_id)
            expression_rows[renamed_probe_id] = raw_expression_rows[raw_probe_id]
        return expression_rows

    def __get_cumulative_rows(self):
        raw_cumulative_rows = Stemformatics_Expression.get_cumulative_rows(self.ds_id,self.raw_probe_list)
        cumulative_rows = {}
        for raw_probe_id in raw_cumulative_rows:
            renamed_probe_id = self.__return_renamed_probe(raw_probe_id)
            cumulative_rows[renamed_probe_id] = raw_cumulative_rows[raw_probe_id]
        return cumulative_rows

    def remove_samples(self,list_of_samples_to_remove):
        if list_of_samples_to_remove == [] or list_of_samples_to_remove is None:
            return

        result = {}
        for sample in list_of_samples_to_remove:
            index = self.sample_labels.index(sample)
            self.sample_labels.pop(index)
            for probe in self.probe_expression_rows:
                row = self.probe_expression_rows[probe]
                row.pop(index)
                result[probe] = row

        self.probe_expression_rows = result

    def __set_dataset_metadata_information(self,db):
        db.schema = 'public'
        ds = db.datasets
        result_ds = ds.filter(ds.id==self.ds_id).one()
        self.handle = Stemformatics_Dataset.add_extra_to_handle(db,result_ds.handle,result_ds.private,result_ds.show_limited)

        self.min_y_axis = 0.0 if result_ds.min_y_axis == '' else result_ds.min_y_axis # should override the platform min_y_axis

        self.mapping_id = result_ds.mapping_id
        self.log_2 = result_ds.log_2

        ds_md = db.dataset_metadata
        result_ds_md = ds_md.filter(ds_md.ds_id == self.ds_id).all()
        ds_md = {}
        for row in result_ds_md:
            ds_name = row.ds_name
            ds_value = row.ds_value
            ds_md[ds_name] = ds_value
        self.ds_md = ds_md
        self.y_axis_label = ds_md['yAxisLabel']
        self.probe_name = ds_md['probeName']
    def __set_probe_and_platform_information(self,db):

        db.schema = 'public'
        ap = db.assay_platforms
        result_ap = ap.filter(ap.chip_type == self.chip_type).one()
        self.manufacturer = result_ap.manufacturer
        self.platform = result_ap.platform
        self.version = result_ap.version
        probe_information = {}
        db.schema = 'stemformatics'
        fm = db.feature_mappings

        for raw_probe_id in self.raw_probe_list:
            where = and_(fm.to_type=="Probe",fm.to_id == raw_probe_id,fm.db_id == self.db_id,fm.mapping_id == self.mapping_id)
            renamed_probe_id = self.__return_renamed_probe(raw_probe_id)

            probe_information[renamed_probe_id] = len(fm.filter(where).all())


        self.probe_information = probe_information

    def __change_probe_display_name_if_transcript(self,probe,gene):
        generic_probe_name = self.probe_name
        if generic_probe_name == 'Transcript':
            mouse_gene = 'ENSMUSG'
            human_gene = 'ENSG'
            if mouse_gene in probe or human_gene in probe:
                new_probe_name = gene + ' Gene Summary'
            else:
                new_probe_name = gene + ' ' + generic_probe_name
        else:
            new_probe_name = gene + ' ' + generic_probe_name

        return new_probe_name

    def __set_probe_display_names(self,db):
        # get the values file
        probe_list = self.probe_list
        if self.ref_type in ['gene_set_id','ensemblID']:
            temp_renamed_probe_list = []
            for probe in probe_list:
                gene_name = self.probe_to_gene_dict[probe]
                new_probe_name = gene_name + self.delimiter+probe
                temp_renamed_probe_list.append(new_probe_name)
            if self.select_probes is None:
                temp_renamed_probe_list = sorted(temp_renamed_probe_list, key = stringSplitByNumbers)

            probe_count = 1
            probe_list = []
            renamed_probe_list = []


            for gene_probe in temp_renamed_probe_list:
                temp_dict = gene_probe.split(self.delimiter)
                gene = temp_dict[0]
                probe = temp_dict[1]

                new_probe_name = self.__change_probe_display_name_if_transcript(probe,gene)

                renamed_probe_list.append(new_probe_name)
                probe_list.append(probe)
                probe_count += 1


        elif self.ref_type in ['miRNA']:
            if self.select_probes is None:
                probe_list = sorted(probe_list, key = stringSplitByNumbers)
            renamed_probe_list = []
            for probe in probe_list:
                new_probe_name = probe
                renamed_probe_list.append(new_probe_name)

        else:
            if self.select_probes is None:
                probe_list = sorted(probe_list, key = stringSplitByNumbers)
            renamed_probe_list = []
            for probe in probe_list:
                new_probe_name = self.__change_probe_display_name_if_transcript(probe,'')
                renamed_probe_list.append(new_probe_name)

        self.probe_list = self.raw_probe_list = probe_list
        self.display_probe_list = renamed_probe_list
        self.__raise_probe_errors()

    def __raise_probe_errors(self):
        a = self.probe_list
        b = self.display_probe_list
        #raise ErrorProbes
