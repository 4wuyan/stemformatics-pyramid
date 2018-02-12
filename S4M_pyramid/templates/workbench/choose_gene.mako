<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">

    <script type="text/javascript" src="${h.url('/js/workbench/choose_gene.js')}"></script>
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
                                Which of my genes share a similar expression pattern to my gene of interest? [Gene Neighbourhood] >><div class="hidden_url"><a href="${h.url('workbench/gene_neighbour_wizard')}">link</a></div>
                            % endif

                            % if c.analysis == 5:
                                    Fold Change Viewer - Choose Gene >>
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

                            % if c.analysis == 2:
                            <p>Now, please select your gene of interest. Search for your gene by symbol or annotation ID (e.g. Ensembl ID).</p>
                            <p>If your selected gene has multiple matching probes, you will be prompted to select one of these probes in order to proceed with the Gene Neighbourhood analysis. Otherwise, the Gene Neighbourhood analysis will begin (this may take several minutes because computation is required to produce your result). When completed, your analysis status will be updated in your analysis jobs view.  Periodically refresh the analysis screen to check on progress.</p>
                            <p>When complete, you'll be able to view genes that are behaving similarly to your gene of interest, i.e. those genes having a similar expression profile across the set of samples in your chosen study.</p>

                            % endif

                            % if c.analysis == 5:
                            <p>Now, please select the gene you would like to view the fold change for. Search for your gene by symbol or annotation ID (e.g. Ensembl ID).</p>
                            <p>When complete, you'll be able to view the fold change of the probes that match the gene you selected in your chosen study.</p>

                            % endif

                        </div>
                    </div>



                </div>
                <div class="clear"></div>
            </div>

        </div>




        <div id="geneSearchDiv" class="searchDiv">
            <div class="hidden" id="datasetID">${c.datasetID}</div>
            <div class="hidden" id="db_id">${c.db_id}</div>
            <div class="hidden" ><a id="url_to_post" href="${c.url}"></a></div>
           <%
            text.input_id = "geneSearch"
            text.search_button_id = "viewGenes"
            text.search_action = "#"
            text.search_value = ""
            text.input_name = "gene"
            text.input_class = ""

            %>
            ${Base.search_box(text)}

            <div class="showSearchTerms"></div>

            <div id="displayGeneResults" class="showResults searchDiv"></div>

            <div class="clear"></div>

        </div>

        <div class="clear"></div>
    </div>

</div>



<div class="hidden" id="datasetID">${c.datasetID}</div>
