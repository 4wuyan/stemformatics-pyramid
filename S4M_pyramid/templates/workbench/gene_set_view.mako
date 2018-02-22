<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_view.css')}" >
    <script type="text/javascript" src="${h.url('/js/popups.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_view.js')}"></script>
</%def>



    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            ${Base.wb_breadcrumbs()}


            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">


                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">Gene List View - ${c.gene_set.gene_set_name}</div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>Genes in your gene list are listed here.</p>
                                <p>From this view, you may send your gene list to Analysis or view the expression of your geneset in a Multi-Gene Expression Graph.</p>
                            </div>
                        </div>


                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <div id="form">
                <div class="innerDiv">

                    <div class="hidden" id="gene_set_id">${c.gene_set.id}</div>
                    <div class="hidden" id="db_id">${c.gene_set.db_id}</div>
                    <div class="hidden" id="gene_set_name">${c.gene_set.gene_set_name}</div>

                    <div class="genesetmenu">
                        <ul class="buttonMenus">
                            <li id="exportMenu">
                                <a class="button dropdown"><span><span class="icon go"></span>Export &amp; Share</span><span class="arrow down"></span></a>
                                <ul class="submenu">
                                    <li><a href="#" id="exportTableCSVButton">Export Gene List</a></li>
                                    <li><a href="${h.url('/workbench/download_gct_file_for_gene_set_wizard?gene_set_id=')}${c.gene_set.id}">Download Expression Profile</a></li>
                                    <li><a href="#" data-id='${c.gene_set.id}' data-name='${c.gene_set.gene_set_name}' data-description='${c.gene_set.description}'  class="share_gene_list_link">Share</a></li>
                                    % if not c.public:
                                        <li><a href="#" data-email='${c.publish_gene_set_email_address}' data-id='${c.gene_set.id}' data-name='${c.gene_set.gene_set_name}' data-description='${c.gene_set.description}'  class="publish_gene_list_link">Publish</a></li>
                                    % endif
                                </ul>
                            </li>
                            <li id="analysisMenu">
                                <a class="button dropdown"><span><span class="icon glass"></span>Analysis</span><span class="arrow down"></span></a>
                                <ul class="submenu">
                                    <li><a href="${h.url('/workbench/hierarchical_cluster_wizard?gene_set_id=')}${c.gene_set.id}">Hierarchical Cluster</a></li>
                                    <li><a id="histogram" href="${h.url('/workbench/histogram_wizard?db_id='+str(c.gene_set.db_id)+'&gene_set_id=')}${c.gene_set.id}">Multi-Gene Expression Graph</a></li>
                                    <li><a href="${h.url('/workbench/gene_set_annotation_wizard?gene_set_id=')}${c.gene_set.id}">Gene List Annotation</a></li>
                                        <!-- This is setup in base.py. Search for c.innate_db_object -->
                                        <% dict_of_types = c.innate_db_object.return_dict_of_types() %>
                                        <% list_of_types_in_order = c.innate_db_object.return_list_of_types_in_order() %>
                                        %for analysis in list_of_types_in_order:
                                            <% type = dict_of_types[analysis] %>
                                            <li><a href="#" class="innate_db" data_type="${type}">Innate DB ${analysis}</a></li>

                                        %endfor
                                </ul>
                            </li>
                            % if not c.public or (c.public and c.role =="admin"):
                                <li id="maintenanceMenu">
                                    <a class="button dropdown"><span><span class="icon fix"></span>Maintenance</span><span class="arrow down"></span></a>
                                    <ul class="submenu">
                                        <li><a href="${h.url('/workbench/gene_set_bulk_import_manager?gene_set_id=')}${c.gene_set.id}" id="add_gene_new">Add Gene</a></li>
                                        <li><a href="#" data-email='${c.publish_gene_set_email_address}' data-id='${c.gene_set.id}' data-name='${c.gene_set.gene_set_name}' data-description='${c.gene_set.description}'  class="edit_gene_list_link">Update Name and Description</a></li>
                                        <li><a href="${h.url('/workbench/gene_set_delete/')}${c.gene_set.id}" data-id='${c.gene_set.id}' data-name='${c.gene_set.gene_set_name}' data-description='${c.gene_set.description}'  class="delete_gene_list_link">Delete Gene List</a></li>
                                        <li><a href="${h.url('/workbench/merge_gene_sets?gene_set_id1=')}${c.gene_set.id}" id="mergeGeneSets">Merge Gene Lists</a></li>
                                    </ul>
                                </li>
                            % endif
                            <li id="helpMenu"> <a href="#" class="button help wb_open_help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li>
                        </ul>
                    </div>

                    <div class=message>${c.message}</div>

                    <div class="clear"></div>
                    <div id="description" class="description">
                        <div class="innerDiv">
                                <%
if c.public and (c.gene_set.description == '' or c.gene_set.description is None):
    descriptionText = c.gene_set.gene_set_name +" ("+str(len(c.result)) + " genes)"
elif c.gene_set.description == '' or c.gene_set.description is None:
    descriptionText = "No description (" + str(len(c.result)) + " genes)"
else:
    descriptionText = c.gene_set.description + " ("+str(len(c.result))+" genes)"
endif
%>
                            <div id="descriptionText">${descriptionText}</div>
                        </div>
                    </div>

                    <table id="gene_set_items">
                        <thead>
                            <tr>
                                <th id="symbol">Gene Name</th>
                                <th id="aliases">Aliases</th>
                                <th id="ensemblID">Ensembl ID</th>
                                <th>Description</th>
                                <th id="status">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                        % if c.result == [] or c.result is None:
                            <tr><td style="text-align:center;"> No Genes were found. </td><td></td><td></td>
                        % else:
                            <% count = 0 %>

                            % for genes in c.result:

                                <%
                                    name = genes.associated_gene_name
                                    aliases = genes.associated_gene_synonym
                                    ensemblID = genes.stemformatics_gene_set_items_gene_id
                                    description = genes.description
                                    gene_set_list_id = genes.stemformatics_gene_set_items_id
                                %>



                                <tr>
                                    <td><a target="_blank" href="${h.url('/genes/search?gene=')}${ensemblID.strip()}">${name}</a></td>
                                    <td>${aliases}</td>
                                    <td>${ensemblID}</td>
                                    <td>${description.replace('<br />','')}</td>
                                    <td>

                                        % if not c.public or (c.public and c.role=="admin"):
                                        <a class="delete" href="${h.url('/workbench/delete_gene_from_set/')}${gene_set_list_id}">Delete</a>
                                        %else:
                                        No actions available
                                        %endif
                                    </td>


                                </tr>


                            % endfor
                        % endif
                        </tbody>
                    </table>
                    <div class="clear" > </div>
                </div>
                <div class="clear" > </div>
            </div>
        </div>
        <div class="clear" > </div>
    </div>

    <div class="hidden">
        <table id="gene_set_items_download">
                <thead>
                    <tr>
                        <th id="symbol">Gene Names for ${c.gene_set.gene_set_name}</th>
                        <th id="aliases">Aliases</th>
                        <th id="ensemblID">Ensembl ID</th>
                        <th>Description</th>
                        <th>Chromosome</th>
                        <th>Chr Start</th>
                        <th>Chr End</th>
                        <th>Chr Strand</th>


                    </tr>
                </thead>
                <tbody>

                % if c.result == [] or c.result is None:
                    <tr><td style="text-align:center;"> No Genes were found. </td>
                % else:
                    % for genes in c.result:

                        <%
                            name = genes.associated_gene_name.strip()
                            ensemblID = genes.gene_id.strip()
                            aliases = genes.associated_gene_synonym.strip()
                            description = genes.description.strip()
                            chr = genes.chromosome_name
                            start = genes.gene_start
                            end = genes.gene_end
                            strand = genes.strand

                        %>

                        <tr>
                            <td>${name}</td>
                            <td>${aliases}</td>
                            <td>${ensemblID}</td>
                            <td>${description.replace('<br />','')}</td>
                            <td>${chr}</td>
                            <td>${start}</td>
                            <td>${end}</td>
                            <td>${strand}</td>
                        </tr>


                    % endfor
                % endif
                </tbody>
            </table>



    </div>
    <div class="hidden innatedb">
            <!-- this is for innatedb -->
            % if c.result != [] or c.result is not None:
                <%
                list_of_ensembl_ids = []
                for genes in c.result:
                    ensemblID = genes.gene_id.strip()
                    list_of_ensembl_ids.append(ensemblID)
               %>
               ${c.innate_db_object.create_form_to_post(list_of_ensembl_ids)| n}



            %endif

    </div>
