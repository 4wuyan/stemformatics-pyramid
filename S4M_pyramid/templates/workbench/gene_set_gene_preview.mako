<%inherit file="/popup.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/popup.css')}" > 
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/wb_default.css')}" > 
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_gene_preview.js')}"></script>
</%def>

    
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            
            ${Base.wb_breadcrumbs()}  
                
    
            <div id="form">
                <div class="innerDiv">
                        
                    <div class="title">Gene List Preview: ${c.gene_set.gene_set_name}</div> 


                    <div class="tables">
                        <div class="hidden" id="gene_set_id">${c.gene_set.id}</div>
                        <div class="hidden" id="db_id">${c.gene_set.db_id}</div>
                                
                                
                        <table class="display" id="gene_set_items">
                            <thead>
                                <tr>
                                    <th id="symbol">Gene Name</th>
                                    <th id="ensemblID">Ensembl ID</th>
                                </tr>
                            </thead>
                            <tbody>
                            % if c.result == [] or c.result is None:
                                <tr><td style="text-align:center;"> No Genes were found. </td><td></td><td></td>
                            % else: 
                                % for genes in c.result:
                                    
                                    <% 
                                        name = genes.associated_gene_name
                                        ensemblID = genes.gene_id
                                        gene_set_list_id = genes.id
                                    %>
                                    
                                    <tr>
                                        <td>
                                            <a target="_blank" href="${h.url('/genes/summary?gene=')}${ensemblID.strip()}&db_id=${c.db_id}">${name}</a>
                                        </td>
                                        <td>
                                            ${ensemblID}
                                        </td>
                                        
                                    </tr>
                                    
                                    
                                % endfor
                            % endif
                            </tbody>
                        </table>
                        
                    </div>
                    <div class="clear" > </div>
                </div>
            </div>
        </div>
    </div>    
    
    <div class="hidden">
        <table id="gene_set_items_download">
                <thead>
                    <tr>
                        <th id="symbol">Gene Names for ${c.gene_set.gene_set_name}</th>
                        <th id="ensemblID">Ensembl ID</th>
                        
                    </tr>
                </thead>
                <tbody>
                    
                % if c.result == [] or c.result is None:
                    <tr><td style="text-align:center;"> No Genes were found. </td>
                % else: 
                    % for genes in c.result:
                        
                        <% 
                            name = genes.associated_gene_name.strip()
                            ensemblID = genes.gene_id.strip()
                            
                        %>
                        
                        <tr>
                            <td>${name}</td>
                            <td>${ensemblID}</td>
                            
                            
                        </tr>
                        
                        
                    % endfor
                % endif
                </tbody>
            </table>
    </div>
    
    
