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

                               Gene Expression Profile - Choose Type


                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">

                                <p>Please choose a type.</p>


                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>




            <form action="${c.url}" method="post">
                <table id="choose_cluster_type">
                    <thead>
                        <tr>
                            <th id="original">Type</th>
                            <th id="status">Details</th>
                        </tr>
                    </thead>
                    <tbody>
                            <tr>
                                <td><a class="large_font" href="${h.url('/workbench/gene_neighbour_wizard')}">Gene Neighbourhood</a></td>
                                <td>The Gene Neighbourhood allows you to select a gene expression profile based on an existing gene in a dataset and search for any other gens with a similar profile.</td>
                            </tr>
                            <tr>
                                <td><a class="large_font" href="${h.url('/workbench/user_defined_expression_profile')}">User Defined Expression Profile</a></td>
                                <td>The User Defined Expression Profile allows you to define your own theoretical gene expression profile and search a dataset for any genes with a similar profile. </td>
                            </tr>


                    </tbody>
                </table>

                <div class="clear" > </div>
            </form>



        <div class="clear" > </div>

    </div>
</div>

