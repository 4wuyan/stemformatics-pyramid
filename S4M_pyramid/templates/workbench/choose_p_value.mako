<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/choose_gene_set.css')}" >

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

                                % if c.analysis == 2:
                                   Gene Neighbourhood- Choose Score >> <div class="hidden_url"></div>
                                % endif
                                % if c.analysis == 7:
                                   User Defined Expression Profile - Choose Score >> <div class="hidden_url"></div>
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

                                <p>Please select a score value. The closer to 0 the more stringent the filter becomes and the less genes will appear in the list.</p>


                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>




            <form action="${c.url}" method="post">
                <table id="choose_p_value">
                    <thead>
                        <tr>
                            <th id="original">Information</th>
                            <th id="status">Score</th>
                        </tr>
                    </thead>
                    <tbody>
                            <tr>
                                <td>The lower the score the more stringent the test and less  genes will appear in the list.</td>
                                <td>
                                    <select name="p_value">
                                            <option value="0.01" >0.01 (Most stringent)</option>
                                            <option selected value="0.05" >0.05 (Default)</option>
                                            <option value="0.1" >0.10</option>
                                            <option value="0.2" >0.20 (Least stringent)</option>
                                    </select>
                                </td>
                            </tr>




                    </tbody>
                </table>

                <div class="clear" > </div>
                <input class="smallMarginTop" name="p_value_submit" type="Submit" value="Submit"/>
            </form>


        </div>

        <div class="clear" > </div>

</div>
