<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/user_defined_expression_profile.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/user_defined_expression_profile.js')}"></script>
</%def>


<div id="wb_background" class="wb_background_divs">
    <div id="wb_background_inner_div">

        ${Base.wb_breadcrumbs()}


        <div class="wb_question_groups_selected">


            <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                User Defined Expression Profile
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">

                                <p>Please choose an expression profile for these samples</p>
                                <p>Initial value is set to the detection threshold. If no detection threshold then it will be set to 0.</p>

                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <table class="summary">
                    <thead>
                        <tr>
                            <th >Detection Threshold</th>
                            <th >Median</th>
                            <th >Min Value</th>
                            <th >Max Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td id="detection_threshold">${c.result['detection_threshold']}</td>
                            <td id="median">${c.result['median_dataset_expression']}</td>
                            <td id="min_value_for_dataset">0</td>
                            <td id="max_value_for_dataset">${round(float(c.result['maxGraphValue']),2)}</td>
                        </tr>

                    </tbody>
            </table>

            <form action="${c.url}" method="post" id="user_defined_expression_profile_form">
                <% sample_type_display_order = c.result['sampleTypeDisplayOrder'].split(',') %>
                <% position = 0 %>
                % for sample_type in sample_type_display_order:
                    <div class="details">
                        <div id="slider_${position}" class="slider" ></div>
                        <div id="name_${position}" class="view_value">${sample_type}</div>
                        <input type="hidden" id="input_${position}" name="input_${position}" value="${c.result['detection_threshold']}" >
                        <div id="value_${position}" class="view_value">${c.result['detection_threshold']}</div>
                        <div class="clear"></div>
                    </div>
                    <% position +=1 %>
                %endfor
                <div class="clear" > </div>
                <input name="Submit" type="Submit" value="Submit"/>
            </form>


        </div>

        <div class="clear" > </div>

    </div>
</div>

