<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/choose_probe.css')}" >

    <script src="${h.external_dependency_url('cdn.jsdelivr.net/kineticjs/4.5.4/kinetic.min.js','/js/external_asset_dependencies/kinetic-4.5.4.min.js')}" ></script>
    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.min.js','/js/external_asset_dependencies/jquery-0.8.2.flot.min.js')}"></script>
    % if c.production != 'true' or c.debug is not None:
        <script type="text/javascript" src="${h.url('/js/expressions/gene_expression_graph_triggers.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/gene_expression_graphs.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph.js')}"  ></script>
    % else:
        <script type="text/javascript" src="${h.url('/js/expressions/geg.min.js')}"  ></script>
    % endif

    <script type="text/javascript" src="${h.url('/js/workbench/choose_probe.js')}"></script>
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
                            <p>Your selected gene is represented by more than one probe in this dataset.</p>
                            <p>Please select a probe from this list - we've provided expression previews for each probe as an aid to your selection.</p>
                            <p>Once selected, the Gene Neighbourhood analysis will begin (this may take several minutes because computation is required to produce your result). When completed, your analysis status will be updated in your analysis jobs view.  Periodically refresh the jobs page to check on progress.</p>
                            <p>When complete, you'll be able to view genes that are behaving similarly to your gene of interest, i.e. those genes having a similar expression profile across the set of samples in your chosen study.</p>
                            % endif

                        </div>
                    </div>



                </div>
                <div class="clear"></div>
            </div>

        </div>


        <div id="probe_selection">
            <div id="db_id" class="hidden">${c.db_id}</div>
            <div id="choose_dataset_immediately" class="hidden">${c.choose_dataset_immediately}</div>
            <div id="ds_id" class="hidden">${c.ds_id}</div>
            <div id="json_view_data${c.ds_id}"} class="hidden">${c.json_view_data}</div>
            <div id="graphTypeOptions"><input type="radio" checked value="scatter"></div>
            <div id="kinetic_legend"></div>
            <table id="probe_graph_table">
                <thead>
                    <tr>
                        <th id="symbol">Select Probe</th>
                        <th>Graph</th>
                    </tr>

                </thead>
                <tbody>
                    <% probe_count = 0 %>
                    % for probe in c.view_data.probe_list:
                        <%
                            raw_probe = c.view_data.raw_probe_list[probe_count]
                        %>
                        <tr>
                            <td><a href="${h.url('/workbench/gene_neighbour_wizard?datasetID='+str(c.ds_id)+'&gene='+str(c.ensemblID)+'&probe=')}${str(raw_probe) | u}">${probe}</a></td>
                            <td class="td_graph">
                                <a href="${h.url('/workbench/gene_neighbour_wizard?datasetID='+str(c.ds_id)+'&gene='+str(c.ensemblID)+'&probe=')}${str(raw_probe) | u}">
                                    <div id="displayGeneDetail${probe_count}" class="showDetail searchDiv" >
                                            <div class="innerDiv">
                                                <div id="xaxis_labels${c.ds_id}" class="xaxis_labels"></div>
                                                <div id='graph${probe_count}' class="graph" style='width:100px;height:100px'>

                                                </div>
                                            </div>
                                    </div>
                                </a>
                            </td>
                            <div class="clear"></div>
                        </tr>
                        <%
                            probe_count += 1
                        %>
                    % endfor

                </tbody>
            </table>

        </div>
        <div class="clear" > </div>
    </div>
</div>
