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
                                   Hierarchical cluster - Choose Cluster Type >> <div class="hidden_url"><a href="${h.url('workbench/hierarchical_cluster_wizard')}">link</a></div>
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

                                <p>Please choose a cluster type. If you choose both, you will get clustering for both the samples along the top and the genes/probes along the side. Choosing samples will reorder the samples and cluster them across the top but will keep the genes/probes in order. Choosing genes/probes will reorder the genes but keep the samples in order along the top.</p>


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
                            <th id="status">Value</th>
                        </tr>
                    </thead>
                    <tbody>
                            <tr>
                                <td>Cluster Options</td>
                                <td>
                                    <select name="cluster_type">
                                            <option value="pearson_both" >Cluster by Samples and Probes using Pearson Correlation</option>
                                            <option value="pearson_row" >Cluster by Genes/Probes only using Pearson Correlation</option>
                                            <option value="pearson_column" >Cluster by Samples only using Pearson Correlation</option>
                                            <option value="euclidean_both" >Cluster by Samples and Probes using Euclidean Correlation</option>
                                            <option value="euclidean_row" >Cluster by Genes/Probes only using Euclidean Correlation</option>
                                            <option value="euclidean_column" >Cluster by Samples only using Euclidean Correlation</option>
                                    </select>
                                </td>
                            </tr>




                    </tbody>
                </table>

                <div class="clear" > </div>
                <input name="cluster_type_submit" class="smallMarginTop" type="Submit" value="Submit"/>
            </form>


        </div>

        <div class="clear" > </div>

</div>
