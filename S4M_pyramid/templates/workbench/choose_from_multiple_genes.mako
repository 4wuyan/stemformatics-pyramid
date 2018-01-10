<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/choose_dataset.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/choose_dataset.js')}"></script>
</%def>



<div id="wb_background" class="wb_background_divs">
    <div id="wb_background_inner_div">

        ${Base.wb_breadcrumbs()}

        <div class="wb_question_groups_selected">


            <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">


                                % if c.analysis == 2:
                                    Gene Neighbourhood - Choose Gene >>
                                % endif


                                % if c.analysis == 5:
                                    Fold Change Viewer - Choose Gene >>
                                % endif

                                % if c.analysis == 'graphs':
                                    Expression Graphs - Choose Gene >>
                                % endif

                                % if c.analysis is None:
                                    Choose Gene >>
                                % endif


                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">


                                <p>You have chosen a gene that has the same symbol name but different underlying Ensembl gene id.</p>
                                <p>Clicking on "more info" will take you to the Ensembl website for more information about that gene.</p>
                                <p>Now, please choose the gene for which you wish to choose.</p>


                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>

            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="th1">Symbol</th>
                        <th>Ensembl Gene ID</th>
                        <th>Species</th>
                        <th>Description</th>
                        % if c.show_probes_in_dataset:
                            <th>Probes in dataset</th>
                        % endif

                        <th>Links</th>

                    </tr>
                </thead>
                <tbody>
                    % for ensembl_gene_id in c.multiple_genes:



                        <%
                            symbol = c.multiple_genes[ensembl_gene_id]['symbol']
                            description = c.multiple_genes[ensembl_gene_id]['symbol'].replace('<br />','')
                            db_id = c.multiple_genes[ensembl_gene_id]['db_id']
                            species = c.multiple_genes[ensembl_gene_id]['species']
                            try:
                                number_of_probes = c.multiple_genes[ensembl_gene_id]['number_of_probes']
                            except:
                                number_of_probes = 0
                        %>


                        <tr>

                                <td><a href="${c.url}&gene=${ensembl_gene_id}&db_id=${db_id}">${symbol}</a></td>
                                <td><a href="${c.url}&gene=${ensembl_gene_id}&db_id=${db_id}">${ensembl_gene_id}</a></td>
                                <td>${species}</td>
                                <td>${description}</td>

                                % if c.show_probes_in_dataset:
                                    <td>${number_of_probes}</td>
                                % endif

                                % if db_id == 46:
                                <td><a target="_blank" href="http://www.ensembl.org/Mus_musculus/Gene/Summary?g=${ensembl_gene_id}">More info</a></td>
                                % endif

                                % if db_id == 56:
                                <td><a target="_blank" href="http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=${ensembl_gene_id}">More info</a></td>
                                % endif
                                % if db_id is None:
                                <td></td>
                                % endif


                        </tr>


                    % endfor

                </tbody>
            </table>
            <div class="clear" > </div>

        </div>

        <div class="clear" > </div>

</div>
