<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/choose_gene_set.css')}" >


    <script type="text/javascript" src="${h.url('/js/workbench/choose_gene_set.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/remove_samples.js')}"></script>

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
                                   Hierarchical cluster - Select Samples >> <div class="hidden_url"><a href="${h.url('workbench/hierarchical_cluster_wizard')}">link</a></div>
                                % endif

                                % if c.analysis == 1:
                                   Comparative marker selection - Select Samples >><div class="hidden_url"><a href="${h.url('workbench/comparative_marker_selection_wizard')}">link</a></div>
                                % endif

                                % if c.analysis == 3:
                                    Histogram display - Select Samples
                                % endif

                                % if c.analysis == 4:
                                    Gene List Annotation - Select Samples
                                % endif

                                % if c.analysis == 6:
                                    Download Expression Profile for a Gene List - Select Samples
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

                                <p>Please choose the sample that you want to select</p>

                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>




            <form action="${c.url}" method="post">
                <input name="remove_chip_ids" type="Submit" value="Submit"/>
                <table id="remove_samples_table">
                    <thead>
                        <tr>
                            <th id="original">Select</th>
                            <th id="status">Sample ID</th>
                        </tr>
                    </thead>
                    <tbody>
                        % if c.chip_id_details == [] or c.chip_id_details is None:
                            <tr><td style="text-align:center;"> No Samples found. </td><td></td><td></td><td></td><td></td></tr>
                        % else:
                            % for chip_id in c.sample_chip_ids_in_order:

                                <%
                                    chip = c.chip_id_details[chip_id]
                                    sample_id = chip['replicate_group_id']
                                %>


                                <tr>
                                    <td>
                                        <input class = "choose_samples" type="checkbox" checked value="${chip_id}"/>
                                        <input class = "hidden" id="remove_chip_ids_${chip_id}" name="remove_chip_ids_${chip_id}" type="checkbox" value="${chip_id}"/>
                                    </td>
                                    <td>${sample_id}</td>


                                </tr>


                            % endfor
                        % endif




                    </tbody>
                </table>

                <div class="clear" > </div>
                <input name="remove_chip_ids" class="smallMarginTop" type="Submit" value="Submit"/>
            </form>


        </div>

        <div class="clear" > </div>

</div>

