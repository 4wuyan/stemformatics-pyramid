<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
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
                                   Hierarchical cluster - Choose Colour By >> <div class="hidden_url"><a href="${h.url('workbench/hierarchical_cluster_wizard')}">link</a></div>
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

                                <p>Please choose the colour by option. If you choose colour by row z-scores, each value in the row of the heatmap will be coloured relative to the other values within that row. If you choose colour by entire dataset values, each value in the row will be coloured relative to all the values in the dataset.</p>

                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>

            <form action="${c.url}" method="post">
                <table id="choose_colour_by">
                    <thead>
                        <tr>
                            <th id="original">Type</th>
                            <th id="status">Value</th>
                        </tr>
                    </thead>
                    <tbody>
                            <tr>
                                <td>Colour By</td>
                                <td>
                                    <select name="colour_by">
                                            <option value="row" >Row z-scores</option>
                                            <option value="dataset" >Entire dataset values</option>
                                    </select>
                                </td>
                            </tr>




                    </tbody>
                </table>

                <div class="clear" > </div>
                <input name="cluster_size_submit" class="smallMarginTop" type="Submit" value="Submit"/>
            </form>


        </div>

        <div class="clear" > </div>

</div>
