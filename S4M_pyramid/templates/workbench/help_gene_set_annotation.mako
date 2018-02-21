<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <!-- <script type="text/javascript" src="${h.url('/js/workbench/gene_set_index.js')}"></script> -->
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
                                Gene Set Annotation Help
                            </div>
                        </div>
                        <div class="wb_help_bar_showing wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Hide help information <img class="help" src="/images/workbench/minus.png" "="">
                            </div>
                        </div>
                        <div class="wb_help_showing wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>This annotation provides a summary for the gene set allowing you to filter by Signal Peptide, Transmembrane Domain and Kegg Pathways. It also gives you the ability to see transcript level information.</p>
                                <p>It utilizes the Python package fisher 0.1.4  - <a target="_blank" href="http://pypi.python.org/pypi/fisher">click here for more details</a>.</p>
                                
                                <p>The numbers for the calculation of the 2x2 Fisher Exact Test are shown below, based on an <a target="_blank" href="http://david.abcc.ncifcrf.gov/content.jsp?file=functional_annotation.html">example from David</a> of human genome backround of 30,000 genes, and 40 genes involved in an example pathway. A given gene set has found 3 out of 300 belong to this pathway.</p>
                                
                                <p>The p-value for this example is 8.85E-3. Please note that the right tail is used for display and the lower the p-value the more likely this gene set is enriched in this pathway.</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>    
            <div id="help_gene_set_annotation" class="tables">
            
                <table>
                    <tr>
                        <th class="first"></th>
                        <th class="second">In the Gene Set</th>
                        <th class="third">In the genome</th>
                        
                    </tr>
                    <tr>
                        <td class="row_header">In the Kegg Pathway</td>
                        <td># genes in the gene set that were found in the Kegg pathway</td>
                        <td># genes in the Kegg pathway</td>

                    </tr>
                    <tr>
                        <td class="row_header">Outside the Kegg Pathway</td>
                        <td># genes in the gene set minus the # of genes found in the Kegg pathway</td>
                        <td># genes in the human genome that are not found in the Kegg pathway</td>
                    
                    </tr>
                    
                </table>
            
                <br/>
            
                <table>
                    <tr>
                        <th class="first"></th>
                        <th class="second">In the Gene Set</th>
                        <th class="third">In the genome</th>
                        
                    </tr>
                    <tr>
                        <td class="row_header">In the Kegg Pathway</td>
                        <td>3</td>
                        <td>40</td>

                    </tr>
                    <tr>
                        <td class="row_header">Outside the Kegg Pathway</td>
                        <td>297</td>
                        <td>29960</td>
                    
                    </tr>
                    
                </table>
                
            </div>
        
            <div class="clear" > </div>
        </div>
    </div>
