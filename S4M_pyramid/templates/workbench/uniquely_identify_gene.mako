<%inherit file="/popup.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/popup.css')}" > 
    <script type="text/javascript" src="${h.url('/js/workbench/uniquely_identify_gene.js')}"></script>
</%def>
    



    <div class="content">
        
        <div id=form>
        
            <div class="hidden" id="original">${c.original}</div>
            <div class="innerDiv">
            
                <div class="title">Uniquely Identify Gene : ${c.original} </div> 

                    <table class="display" id="gene_set_items">
                            <thead>
                                <tr>
                                    
                                    <th>Ensembl</th> 
                                    <th>Symbol</th>
                                    <th>Name</th> 
                                    <th>Aliases</th> 
                                    <th>Entrez</th> 
                                    
                                </tr>
                            </thead>
                            <tbody>
                         
                                <tr>
                                    <td colspan=5><a id="selectAll" href="#all">Select All</a></td>
                                    
                                </tr>
                                

                            % for gene in c.data:
                                
                                
                                
                                <%
                                    ensemblID = c.data[gene]['ensemblID']
                                    name = c.data[gene]['description'].replace('<br />','')
                                    aliases = c.data[gene]['aliases']
                                    entrezID = c.data[gene]['EntrezID']
                                    symbol = c.data[gene]['symbol']
                                %>
                                
                                <tr>
                                    <td><a class="choose" href="#${ensemblID}">${ensemblID}</a></td>
                                    <td>${symbol}</td>
                                    <td>${name}</td>
                                    <td>${aliases}</td>
                                    <td>${entrezID}</td>
                                </tr>
                                
                            % endfor
                              
                              
                            </tbody>
                        </table>
                <div class="clear"></div>
            </div>
            <div class="clear"></div>
        </div>

    </div>
