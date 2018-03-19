<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/choose_gene_set.css')}" >

    <script type="text/javascript" src="${h.url('/js/workbench/choose_gene_set.js')}"></script>

</%def>




<div id="wb_background" class="wb_background_divs">
    <div id="wb_background_inner_div">

        ${Base.wb_breadcrumbs()}


        <div class="wb_question_groups_selected">
            <div class="hidden" id="analysis">${c.analysis}</div>


            <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">

                                % if c.analysis == 0:
                                   Hierarchical cluster - Choose Gene List >> <div class="hidden_url"><a href="${h.url('workbench/hierarchical_cluster_wizard')}">link</a></div>
                                % endif

                                % if c.analysis == 1:
                                   Comparative marker selection - Choose Gene List >><div class="hidden_url"><a href="${h.url('workbench/comparative_marker_selection_wizard')}">link</a></div>
                                % endif

                                % if c.analysis == 3:
                                    MultiGene Expression Graph display - Choose Gene List
                                % endif

                                % if c.analysis == 4:
                                    Gene List Annotation - Choose Gene List
                                % endif

                                % if c.analysis == 6:
                                    Download Expression Profile for a Gene List - Choose Gene List
                                % endif

                                % if c.analysis == 8:
                                     Merge Gene Lists - Choose Gene List
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

                                <p>Please choose a gene list to continue. You may choose one of your own or a public gene list. Simply click on the title or the plus button.</p>

                                % if c.analysis == 0:
                                <p>Hierarchical clustering groups genes and samples to highlight co-regulated gene lists.</p>
                                <p>To begin, please select a gene list on which to perform this analysis. If you have not yet created any gene lists, please copy/paste or upload a gene list first, and return to this analysis.</p>
                                % endif

                                % if c.analysis == 1:
                                <p>Comparative marker selection shows you which of your genes of interest are most differentially expressed in distinct phenotypes within a study.</p>
                                <p>To begin, please select a gene list on which to perform this analysis. If you have not yet created any gene lists, please copy/paste or upload a gene list first, and return to this analysis.</p>
                                % endif

                                % if c.analysis == 3:
                                <p>Displays gene list as a graph of gene expression.</p>
                                <p>To begin, please select a gene list to visualise. If you have not yet created any gene lists, please copy/paste or upload a gene list first, and return to this analysis.</p>
                                % endif

                                % if c.analysis == 4:
                                <p>To begin, please select a gene list to annotate. If you want to create your own gene lists, please copy/paste or upload a gene list first, and return to this analysis.</p>
                                % endif

                                % if c.analysis == 6:
                                <p>To begin, please select a gene list to download the txt or gct file (for GenePattern). If you want to created your own gene list, please copy/paste or upload a gene list first, and return to this download.</p>
                                <p>This txt or gct GenePattern file can also be used as the base expression profile for other systems with some simple formatting.</p>
                                <p>For more details on how a gct file is formatted, please click <a target="_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/tutorial/gp_fileformats#gct">here</a>
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


           <% if not hasattr(c,'filter_by_db_id') : c.filter_by_db_id = None %>
           <% if not hasattr(c,'filter_out_gene_sets') : c.filter_out_gene_sets = [] %>
           <% delimiter = '&' if '?' in c.url else '?' %>
            % if c.uid != 0:
            <h2 id=gene_set_items_header>My Gene Lists <img class="expand" src="/images/workbench/plus.png" ></h2>
            <div id="gene_set_items_div" class="display_gene_sets">
                <table id="gene_set_items">
                    <thead>
                        <tr>
                            <th id="original">Gene List Name</th>
                            <th># genes</th>
                            <th>Description</th>
                            <th id="symbol">Species</th>
                            <th id="status">Action</th>
                        </tr>
                    </thead>
                    <tbody>

                        % if c.result == [] or c.result is None:
                            <tr><td style="text-align:center;"> No Gene Lists found. </td><td></td><td></td><td></td><td></td></tr>
                        % else:
                            % for geneSet in c.result:

                                <%
                                    id = geneSet.id
                                    name = geneSet.gene_set_name
                                    if geneSet.db_id == int(c.human_db) :
                                        species = 'Human'
                                    else:
                                        species = 'Mouse'
                                %>
                                % if id not in c.filter_out_gene_sets and (c.filter_by_db_id is None or  geneSet.db_id in c.filter_by_db_id):
                                <tr>
                                    <td id="name${id}"><a class="gene_set_link" href="${c.url}${delimiter}gene_set_id=${id}">${name.strip()}</a><div class="hidden">${geneSet.count}</div></td>
                                    <td>${geneSet.count}</td>
                                    <td>${geneSet.description}</td>
                                    <td>${species}</td>
                                    <td>

                                    <ul class="buttonMenus">
                                        <li id="exportMenu">
                                            <a class="button dropdown"><span>Action</span><span class="arrow down"></span></a>
                                            <ul class="submenu">
                                                        <li><a class="popup" href="${h.url('/workbench/gene_set_gene_preview/')}${id}" >Preview</a></li>
                                            <li><a class="gene_set_link" href="${c.url}${delimiter}gene_set_id=${id}">Select</a> </li>
                                            </ul>
                                        </li>
                                    </ul>


                                    </td>


                                </tr>
                                % endif

                            % endfor
                        % endif




                    </tbody>
                </table>

                <div class="clear" > </div>
            </div>

            %endif

            <h2 id=public_gene_set_items_header>Public Gene Lists <img class="expand" src="/images/workbench/plus.png" ></h2>
            <div id="public_gene_set_items_div" class="display_gene_sets">
                <table id="public_gene_set_items">
                    <thead>
                        <tr>
                            <th id="original">Gene List Name</th>
                            <th># genes</th>
                            <th>Description</th>
                            <th id="symbol">Species</th>
                            <th id="status">Action</th>
                        </tr>
                    </thead>
                    <tbody>

                        % if c.public_result == [] or c.public_result is None:
                            <tr><td style="text-align:center;"> No Gene Lists found. </td><td></td><td></td><td></td><td></td></tr>
                        % else:
                            % for geneSet in c.public_result:

                                <%
                                    id = geneSet.id
                                    name = geneSet.gene_set_name
                                    if geneSet.db_id == int(c.human_db) :
                                        species = 'Human'
                                    else:
                                        species = 'Mouse'
                                %>
                                % if id not in c.filter_out_gene_sets and (c.filter_by_db_id is None or geneSet.db_id in  c.filter_by_db_id):
                                <tr>
                                    <td id="name${id}"><a class="gene_set_link" href="${c.url}${delimiter}gene_set_id=${id}">${name.strip()}</a><div class="hidden">${geneSet.count}</div></td>
                                    <td>${geneSet.count}</td>
                                    <td>${geneSet.gene_set_type}</td>
                                    <td>${species}</td>
                                    <td>
                                    <ul class="buttonMenus">
                                        <li id="exportMenu">
                                            <a class="button dropdown"><span>Action</span><span class="arrow down"></span></a>
                                            <ul class="submenu">
                                                        <li><a class="popup" href="${h.url('/workbench/gene_set_gene_preview/')}${id}" >Preview</a></li>
                                            <li><a class="gene_set_link" href="${c.url}${delimiter}gene_set_id=${id}">Select</a> </li>
                                            </ul>
                                        </li>
                                    </ul>

                                   </td>


                                </tr>
                                % endif

                            % endfor
                        % endif




                    </tbody>
                </table>

                <div class="clear" > </div>
            </div>
        % if c.analysis == 0:
            <h2 id="select_probes_for_hc_header">Enter in a list of probes <img class="expand" src="/images/workbench/plus.png" ></h2>
            <div id="select_probes_for_hc_div">
                <form action="${c.url}" method="post">
                    <textarea name="select_probes" placeholder="Enter probes with spaces eg. probeA probeB" ></textarea>
                    <input type="submit"></submit>
                </form>
            </div>
        %endif

        <div class="clear" > </div>

    </div>
</div>
