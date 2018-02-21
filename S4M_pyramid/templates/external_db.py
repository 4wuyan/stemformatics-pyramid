__all__ = ['externalDB', 'innateDB', 'stringDB']


class externalDB(object):
    def __init__(self, single_gene_url=None, multiple_gene_url=None):
        self.single_gene_url = single_gene_url
        self.multiple_gene_url = multiple_gene_url

    def get_single_gene_url(self, ensembl_id):
        # check that ensembl_id is valid and url is valid
        if  isinstance(ensembl_id, str) and isinstance(self.single_gene_url, str):
            url = self.single_gene_url + ensembl_id
        else:
            url = "#"

        return url

    def create_form_to_post(self, list_of_ensembl_ids):

        # check that list of ensembl_id is valid and url is valid
        if isinstance(list_of_ensembl_ids, list) and isinstance(self.multiple_gene_url, str):
            html = '<form action="' + self.multiple_gene_url + '" method="post"> '
            html += '<input type="submit"></input>'
            html += '</form>'
        else:
            html = ""

        return html


class stringDB(externalDB):
    pass


class innateDB(externalDB):
    def return_list_of_types_in_order(self):
        list_of_types_in_order = ['Pathway Analysis', 'Gene Ontology Analysis', 'Network Analysis', 'Interactor Analysis', 'Transcription Factor Binding Site Analysis']
        return list_of_types_in_order

    def return_dict_of_types(self):
        dict_of_types = { \
            'Pathway Analysis': 'pathway', \
            'Gene Ontology Analysis': 'gene', \
            'Network Analysis': 'interaction', \
            'Interactor Analysis': 'interactor', \
            'Transcription Factor Binding Site Analysis': 'TFinteraction' \
            }
        return dict_of_types

    def create_form_to_post(self, list_of_ensembl_ids):

        # check that list of ensembl_id is valid and url is valid
        if isinstance(list_of_ensembl_ids, list) and isinstance(self.multiple_gene_url, str):

            """
                innate_db_type can be replaced by one of the following via javascript
                type = "interactor"
                type = "go"
                type = "pw"
                type = "intx"
                type = "tfbs"
            """

            try:
                text = "\n".join(list_of_ensembl_ids)
            except:
                text = ""

            html = ""
            html += '<form class="innate_db_form" action="' + self.multiple_gene_url + '" method="post" target="_blank"> '
            html += '<input type="hidden" name="inputType" value="textbox"></input>'
            html += '<input type="hidden" name="listType" id="listType" value="innate_db_type"></input>'
            html += '<input type="hidden" name="xrefColumn" value="0"/>'
            html += '<input type="hidden" name="xref_db" value="Ensembl"/>'
            html += '<input type="hidden" name="algorithm" value="Hypergeometric"/>'
            html += '<input type="hidden" name="correctionMethod" value="BenjaminiHochberg"/>'
            html += '<input type="hidden" name="skipSteps" value="true"/>'
            html += '<input type="hidden" name="numConditions" value="0"/>'

            html += '<textarea name="customText">' + text + '</textarea> '
            html += '<input type="submit"></input>'
            html += '</form>'


        else:
            html = ""

        return html


