<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/popups.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_index.js')}"></script>
</%def>

    <div class="hidden" id="publish_gene_set_email_address">${c.publish_gene_set_email_address}</div>

    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">


            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                % if c.public == False:
                                    Manage Gene Lists
                                % else:
                                    Public Gene Lists
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

                                % if c.public == False:
                                    <p>Manage your personal gene lists here.</p>
                                % else:
                                    <p>View public gene lists here.</p>
                                % endif
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <div class="tables">
                <div>${c.message}</div>
                <div class="hidden" id="initial_filter">${c.initial_filter}</div>
                <ul class="buttonMenus">
                    <li id="exportMenu">
                        <a class="button dropdown"><span><span class="icon go"></span>Export</span><span class="arrow down"></span></a>
                        <ul class="submenu">
                            <li><a href="#" id="exportTableCSVButton">Export Gene List Names</a></li>
                        </ul>
                    </li>
                    % if not c.public:
                        <li id="maintenanceMenu">
                            <a class="button dropdown"><span><span class="icon fix"></span>Add a Gene List</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                                <li><a href="${h.url('/workbench/gene_set_bulk_import_manager')}" id="add_gene">Add Gene List</a></li>
                                <li><a href="${h.url('/workbench/gene_set_upload')}" id="upload_gene">Upload Gene List</a></li>
                            </ul>
                        </li>
                    % endif
                    <li id="helpMenu"> <a href="#" class="button help wb_open_help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li>
                </ul>
                <div class="height12px"></div>
                <table id="gene_set_items">
                    <thead>
                        <tr>
                            <th id="original">Gene List Name</th>
                            <th># genes</th>

                            % if c.public == False:
                                <th>Description</th>
                            % else:
                                <th>Type</th>
                            % endif
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
                                db_id = geneSet.db_id
                                id = geneSet.id
                                if c.gene_sets_in_search is not None:
                                    if id not in c.gene_sets_in_search:
                                        continue
                                name = geneSet.gene_set_name
                                if geneSet.db_id == int(c.human_db) :
                                    species = 'Human'
                                else:
                                    species = 'Mouse'
                            %>

                            <tr>
                                <td id="name${id}">${name.strip()}</td>
                                <td>${geneSet.count}</td>
                                % if c.public == False:
                                    <td id="description${id}">${geneSet.description}</td>
                                % else:
                                    <td>${geneSet.gene_set_type}</td>
                                % endif
                                <td>${species}</td>
                                <td class="action">
                                    <ul class="buttonMenus">
                                        <li id="exportMenu">
                                            <a class="button dropdown"><span>Actions .....</span><span class="arrow down"></span></a>
                                            <ul class="submenu">
                                            %if c.public == True:
                                                <li><a href="${h.url('/workbench/gene_set_view/')}${id}">View</a></li>
                                                %if c.role=="admin":
                                                    <li><a class="edit" href="#${id}" >Rename</a></li>

                                                %endif
                                            % else:
                                                <li><a href="${h.url('/workbench/gene_set_view/')}${id}">View</a></li>
                                                <li><a href="#" data-id='${id}' data-name='${name}' data-description='${geneSet.description}'  class="edit_gene_list_link">Rename</a></li>
                                                <li><a href="${h.url('/workbench/gene_set_delete/')}${id}" data-id='${id}' data-name='${name}' data-description='${geneSet.description}'  class="delete_gene_list_link">Delete</a></li>
                                                <li class="sep"></li>
                                                <li><a href="${h.url('/workbench/download_gct_file_for_gene_set_wizard?gene_set_id=')}${id}">Download Expression Profile</a></li>
                                                <li><a href="${h.url('/workbench/merge_gene_sets?gene_set_id1=')}${id}" id="mergeGeneSets">Merge Gene Lists</a></li>
                                                <li><a href="#" data-id='${id}' data-name='${name}' data-description='${geneSet.description}'  class="share_gene_list_link">Share</a></li>
                                                <li><a href="#" data-id='${id}'  data-email='${c.publish_gene_set_email_address}' data-name='${name}' data-description='${geneSet.description}'  class="publish_gene_list_link">Publish</a></li>
                                                <li class="sep"></li>
                                                <li><a href="${h.url('/workbench/hierarchical_cluster_wizard?gene_set_id=')}${id}">Hierarchical Cluster</a></li>
                                                <li><a id="histogram" href="${h.url('/workbench/histogram_wizard?db_id='+str(db_id)+'&gene_set_id=')}${id}">Multi-Gene Expression Graph</a></li>
                                                <li><a href="${h.url('/workbench/gene_set_annotation_wizard?gene_set_id=')}${id}">Gene List Annotation</a></li>
                                            % endif

                                           </ul>
                                        </li>
                                    </ul>
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

    <div class="hidden" id="downloadGeneSets">
        <table id="downloadGeneSetsTable">
                <thead>
                    <tr>
                        <th>Gene List Name</th>
                        <th># Genes</th>
                        <th>Description</th>
                        <th>Species</th>

                    </tr>
                </thead>
                <tbody>
                % if c.result == [] or c.result is None:
                    <tr><td style="text-align:center;"> No Gene Lists found. </td>
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

                        <tr>
                            <td id="name${id}">${name.strip()}</td>
                            <td>${geneSet.count}</td>
                            <td>${geneSet.description}</td>
                            <td>${species}</td>
                        </tr>


                    % endfor
                % endif
                </tbody>
        </table>
    </div>




