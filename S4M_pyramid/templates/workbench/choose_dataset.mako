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

                                % if c.analysis == 0:
                                    Hierarchical cluster - Choose Dataset >> <div class="hidden_url"><a href="${h.url('workbench/hierarchical_cluster_wizard')}">link</a></div>
                                % endif

                                % if c.analysis == 1:
                                    Comparative marker selection - Choose Dataset >><div class="hidden_url"><a href="${h.url('workbench/comparative_marker_selection_wizard')}">link</a></div>
                                % endif

                                % if c.analysis == 2:
                                    Gene Neighbourhood - Choose Dataset >><div class="hidden_url"><a href="${h.url('workbench/gene_neighbour_wizard')}">link</a></div>
                                % endif

                                % if c.analysis == 3:
                                    MultiGene display - Choose Dataset >><div class="hidden_url"><a href="${h.url('workbench/histogram')}">link</a></div>
                                % endif


                                % if c.analysis == 5:
                                    Fold Change Viewer - Choose Dataset >>
                                % endif

                                % if c.analysis == 6:
                                    Download Gene List Expression Profile - Choose Dataset >>
                                % endif

                                % if c.analysis == 7:
                                    User Defined Expression Profile  - Choose Dataset >>
                                % endif


                                % if c.analysis is None:
                                    Choose Dataset >>
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

                                % if c.analysis == 0:
                                <p>Hierarchical clustering groups genes and samples to highlight co-regulated gene lists.</p>
                                <p>Please choose the dataset for which you wish to perform this analysis.  Once all the options are selected, the clustering will begin (this may take several minutes as computation is required to produce your result). When completed, your analysis status will be updated in your analysis jobs view.  Periodically refresh the jobs page to check on progress.</p>
                                <p>When complete, you'll be able to view the resulting Hierarchical Cluster for your chosen genes and study.</p>
                                <p>Please note that some datasets are greyed out because they have not been certified to work with GenePattern Analyses.  If you think that this is in error please email us via the contact page</p>
                                % endif

                                % if c.analysis == 7:
                                <p>This analysis will find genes that share a similar expression profile that you create across all samples within a given study.</p>
                                <p>Now, please choose the study for which you wish to perform this analysis.</p>
                                <p>Please note that some datasets are greyed out because they have not been certified to work with GenePattern Analyses.  If you think that this is in error please email us via the contact page</p>
% endif

                                % if c.analysis == 2:
                                <p>This analysis will find genes that share a similar expression profile for your gene of interest across samples within a given study.</p>
                                <p>Now, please choose the study for which you wish to perform this analysis.</p>
                                <p>Please note that some datasets are greyed out because they have not been certified to work with GenePattern Analyses.  If you think that this is in error please email us via the contact page</p>
                                % endif

                                % if c.analysis == 3:
                                <p>Displays gene list as a histogram (bar plot) of gene expression.</p>
                                <p>Now, please choose the study for which you wish to perform this analysis.</p>
                                % endif

                                % if c.analysis == 5:
                                <p>This analysis will show you the fold change for the genes of a particular dataset.</p>
                                <p>Now, please choose the study for which you wish to perform this analysis.</p>
                                % endif

                                % if c.analysis == 6:
                                <p>This wizard will allow you to download the txt or gct (GenePattern) expression profile file for the gene list chosen of a particular dataset.</p>
                                <p>Now, please left mouse on the study for which you wish to perform this download. It will allow you to download the file straight away.</p>
                                <p>This txt or gct GenePattern file can also be used as the base expression profile for other systems with some simple formatting.</p>
                                <p>For more details on how a gct file is formatted, please click <a target="_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/tutorial/gp_fileformats#gct">here</a>
                                % endif

                                % if c.analysis is None:
                                <p>Please choose a dataset</p>
                                % endif

                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <%
                try:
                    if c.error_message is None:
                        c.error_message = ""
                except:
                    c.error_message = ""

            %>
            <div class="error_message ${'hidden' if c.error_message == "" else ''}">${c.error_message}</div>

            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="th1">Name</th>
                        <th>Title</th>
                        <th>Sample/Cell Types</th>
                        <th>Contact</th>

                    </tr>
                </thead>
                <tbody>
                    % for dataset in c.datasets:

                        % if not c.datasets[dataset].has_key('has_data') or c.datasets[dataset]['has_data'] == 'yes':
                        <%
                            # HC (analysis 0) cannot be run on any dataset anymore T#2270
                            gene_pattern_analysis = [0,1,2,7]
                            gene_pattern_analysis_access = c.datasets[dataset]['gene_pattern_analysis_access']



                            organism = c.datasets[dataset]['organism']
                            datasetID = dataset
                            name = c.datasets[dataset]['handle']
                            title = c.datasets[dataset]['title']
                            cells_samples_assayed = c.datasets[dataset]['cells_samples_assayed']
                            contact = c.datasets[dataset]['name']
                            url_link = "&datasetID=" if c.url.find('?') != -1 else "?datasetID="
                        %>

                        % if (organism == c.species or c.species is None) :
                            % if c.analysis in gene_pattern_analysis and gene_pattern_analysis_access =='Disable':
                                % if hasattr(c,'use_galaxy_server'):
                                <!-- this code will run only if analysis is 0 (Hierarchical Cluster) -->
                                    % if c.use_galaxy_server == "no" and c.analysis == 0:
                                        <tr class="disabled">
                                        <td>${name}</td>
                                    % else:
                                        <tr>
                                            <td><a href="${c.url}${url_link}${datasetID}">${name}</a></td>
                                    % endif
                                % else:
                                    <tr class="disabled">
                                    <td>${name}</td>
                                % endif
                            % else:
                            <tr >
                                <td><a href="${c.url}${url_link}${datasetID}">${name}</a></td>

                            % endif
                                <td>${title}</td>
                                <td>${cells_samples_assayed}</td>
                                <td>${contact}</td>

                        </tr>
                        % endif
                      % endif
                    % endfor

                </tbody>
            </table>
            <div class="clear" > </div>


        <div class="clear" > </div>

    </div>
</div>
