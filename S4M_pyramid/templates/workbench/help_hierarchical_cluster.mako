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
                                Hierarchical Cluster Analysis Help
                            </div>
                        </div>
                        <div class="wb_help_bar_showing wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Hide help information <img class="help" src="/images/workbench/minus.png" "="">
                            </div>
                        </div>
                        <div class="wb_help_showing wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>This analysis groups genes and samples to highlight co-regulated gene sets.</p>
                                
                                <p>It uses the analysis provided by <a target="_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/">GenePattern</a> from MIT. Two separate Gene Pattern modules are used, one to do the analysis and one to create an image.</p>
                                <p> To see more detail about the underlying analysis that is provided by Gene Pattern, please <a target="_blank" href="http://gepetto.qfab.org:8080/gp/module/doc/urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00009:5">click here</a>.</p>
                                <p>To see more detail about the image creation provided by Gene Pattern, please <a target="_blank" href="http://gepetto.qfab.org:8080/gp/module/doc/urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00009:5">click here</a>.</p>
                                <p>The default settings for the ${c.site_name} Gene Pattern Hierarchical Cluster analysis are shown below.</p>
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
                        <td>column distance measure</td>
                        <td>Analysis type for sample clustering</td>
                        <td>Pearson correlation</td>
                        <td>The Pearson correlation is a widely used and accepted measure of the strength of linear dependence.</td>
                    </tr>
                    <tr>
                        <td>row distance measure</td>
                        <td>Analysis type for gene/probe clustering</td>
                        <td>Pearson correlation</td>
                        <td>The Pearson correlation is a widely used and accepted measure of the strength of linear dependence.</td>
                    </tr>
                    <tr>
                        <td>clustering method</td>
                        <td>Hierarchical clustering method</td>
                        <td>Pairwise average-linking</td>
                        <td>This was chosen arbitrarily</td>
                    </tr>
                    <tr>
                        <td>log transform</td>
                        <td>Log transform data before clustering</td>
                        <td>no</td>
                        <td>All ${c.site_name} expression data is already logged</td>
                    </tr>
                    <tr>
                        <td>row center</td>
                        <td>Center each gene/probe</td>
                        <td>no</td>
                        <td>This was chosen arbitrarily</td>
                    </tr>
                    <tr>
                        <td>row normalize</td>
                        <td>Normalize each gene/probe</td>
                        <td>no</td>
                        <td>All ${c.site_name} expression data is already normalized</td>
                    </tr>
                    <tr>
                        <td>column center</td>
                        <td>Center each sample</td>
                        <td>no</td>
                        <td>This was chosen arbitrarily</td>
                    </tr>
                    <tr>
                        <td>column normalize</td>
                        <td>Normalize each sample</td>
                        <td>no</td>
                        <td>All ${c.site_name} expression data is already normalized</td>
                    </tr>
                    
                    <!-- 
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    -->
                </table>
                <!-- <img src="${h.url('/images/workbench/gn-1.png')}" style="width:100%;border: 1px solid #5a5a5a;" /> -->
            </div>
        
            <div class="clear" > </div>
        </div>
    </div>
