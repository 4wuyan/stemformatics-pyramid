<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">

</%def>



    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            ${Base.wb_breadcrumbs()}

            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                ${c.purple_title}
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>${c.help_text}</p>
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>

            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="th1">Select an option:</th>

                    </tr>
                </thead>
                <tbody>
                    % for option in c.options:





                        <tr>

                                <td><a href="${c.url}${c.options[option]}">${option}</a></td>


                            </tr>


                    % endfor

                </tbody>
            </table>

        </div>
    </div>
