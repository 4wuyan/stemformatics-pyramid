<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

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
                                   Hierarchical cluster - Choose Cluster Size >> <div class="hidden_url"><a href="${h.url('workbench/hierarchical_cluster_wizard')}">link</a></div>
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
                                
                                
                                <p>Increase the size of the rows and columns to improve the viewing quality of the image. Please note that the large size might not be able to be processed on a large dataset using a big gene list (over 1000 genes in a gene list). Tiny is the original size pre v4.1 on ${c.site_name}.</p>
                               
                            </div>
                        </div>
                        
                        

                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>
        
            
            

            <form action="${c.url}" method="post">
                <table id="choose_cluster_size">
                    <thead>
                        <tr>
                            <th id="original">Details</th>
                            <th id="status">Size</th> 
                        </tr>
                    </thead>
                    <tbody>
                            <tr>
                                <td>Cluster Size Options</td>
                                <td>
                                    <select name="cluster_size">
                                            <option value="tiny" >Tiny (original size - suitable for large gene lists)</option>
                                            <option value="small" >Small </option>
                                            <option value="medium" selected>Medium (Default)</option>
                                            <option value="large" >Large (not suitable for large gene lists of over 1000 genes)</option>
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

