<%inherit file="../default.html"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/probes/multi_map_summary.js')}"></script>
    <link type="text/css" href="${h.url('/css/probes/multi_map_summary.css')}" rel="stylesheet" />
</%def>


    <div class="content">
        <div class="breadcrumbs"><span class="current">Multi Mapping Probe Summary<span></div>
        <div id="displayGenes" class="showDetail searchDiv" >
            <div id="multi_probe_map_summary">
                
                <div class="innerDiv">
                    <div class="title">Multi Mapping Probe Summary for Probe ${c.probe_id}</div>
                    <div class="description">
                        <div class="innerDiv">${c.message}</div>
                    </div>
                    <table class="display" id="genesTable">
                        <thead>
                        <tr>
                            <th class="name">Gene Name</th>
                            <th class="name">Ensembl ID</th>
                            <th>Chromosome</th>
                            <th>Strand</th>
                            <th>Start</th>
                            <th>End</th>
                        </tr>
                        </thead>
                        <tbody>
                        
                        % if c.unique_genes == [] or c.unique_genes is None:
                            <tr><td colspan=6 style="text-align:center;"> No genes in the database maps to this probe. </td>
                        % else: 
                            % for genes in c.unique_genes:
                                    <% 
                                        ensemblGeneID = genes[1]
                                        symbol = genes['associated_gene_name']
                                    %>
                                    <tr>
                                        <td><a href="${h.url('/genes/summary?gene=')}${ensemblGeneID}&db_id=${c.db_id}">${symbol}</a></td>
                                        <td><a href="${h.url('/genes/summary?gene=')}${ensemblGeneID}&db_id=${c.db_id}">${ensemblGeneID}</a></td>
                                        <td>
                                            <% chr = c.geneDetails[ensemblGeneID]['location']['chromosome'] %>
                                            
                                            
                                            % if chr.isdigit():
                                                chr${chr}
                                            % else:
                                                ${chr}
                                            %endif
                                        
                                        
                                        </td>   
                                        <td>
                                            <%
                                                if c.geneDetails[ensemblGeneID]['location']['strand'] == 1:
                                                    context.write('+')
                                                else:
                                                    context.write('-')
                                            %>
                                        
                                        </td>   
                                        <td>${c.geneDetails[ensemblGeneID]['location']['start']}</td>   
                                        <td>${c.geneDetails[ensemblGeneID]['location']['end']}</td>   
                                    </tr>
                            % endfor
                        % endif
                        </tbody>
                    </table>
                    <div class="clear"></div>
                </div>
            </div>
                    
        </div>
        <div id=downloadData class="hidden">
        </div>
        <div class=clear></div>
    </div>
