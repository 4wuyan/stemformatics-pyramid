<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_index.js')}"></script>
</%def>

    <div id="help_flag_message" class="hidden">Click the grey help bar to hide. Click again to expand.</div>
    <div id="help_flag_top_position" class="hidden">230px</div>
    
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            
            ${Base.wb_breadcrumbs()}  
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Gene Neighbourhood Analysis Help
                            </div>
                        </div>
                        <div class="wb_help_bar_showing wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Hide help information <img class="help" src="/images/workbench/minus.png" "="">
                            </div>
                        </div>
                        <div class="wb_help_showing wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>This analysis searches a given study for genes with expression profiles similar to that of your gene of interest.</p>
                                <p>It utilizes analysis tools provided by <a target="_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/">GenePattern (MIT)</a>. For more detail about the specific GenePattern tools used for this analysis, please <a target="_blank" href="http://gepetto.qfab.org:8080/gp/module/doc/urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00007:3">click here</a>.</p>
                                <!-- <p>It uses the analysis provided by <a target="_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/">GenePattern</a> from MIT. To see more detail about the underlying analysis that is provided by Gene Pattern, please <a target="_blank" href="http://gepetto.qfab.org:8080/gp/module/doc/urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00007:3">click here</a>.</p> -->
                                <p>The default settings for the ${c.site_name} Gene Neighbourhood analysis are shown below.</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>    
            <div class="tables">
                <table>
                    <tr>
                        <th>Field name</th>
                        <th>Description</th>
                        <th>${c.site_name} Default</th>
                        <th>Reason for Default</th>
                    </tr>
                    <tr>
                        <td>num neighbors</td>
                        <td>Number of neighbours to return</td>
                        <td>10</td>
                        <td>This was chosen arbirtrarily</td>
                    </tr>
                    <tr>
                        <td>distance metric</td>
                        <td>Analysis type for calculation</td>
                        <td>Pearson distance</td>
                        <td>The Pearson correlation is a widely used and accepted measure of the strength of linear dependence.</td>
                    </tr>
                    <tr>
                        <td>filter data</td>
                        <td></td>
                        <td>no</td>
                        <td>This was chosen to always return 10 results</td>
                    </tr>
                    <tr>
                        <td>min threshold</td>
                        <td>Minimum threshold when using filter</td>
                        <td>N/A</td>
                        <td>No filtering was used</td>
                    </tr>
                    <tr>
                        <td>max threshold</td>
                        <td>Maximum threshold when using filter</td>
                        <td>N/A</td>
                        <td>No filtering was used</td>
                    </tr>
                    <tr>
                        <td>min fold diff</td>
                        <td>Minimum fold difference when using filter</td>
                        <td>N/A</td>
                        <td>No filtering was used</td>
                    </tr>
                    <tr>
                        <td>max fold diff</td>
                        <td>Maximum fold difference when using filter</td>
                        <td>N/A</td>
                        <td>No filtering was used</td>
                    </tr>
                </table>
                <!-- <img src="${h.url('/images/workbench/gn-1.png')}" style="width:100%;border: 1px solid #5a5a5a;" /> -->
            </div>
        
            <div class="clear" > </div>
        </div>
    </div>
