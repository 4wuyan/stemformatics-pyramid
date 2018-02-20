<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_view.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_view.js')}"></script>
</%def>

    
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            ${Base.wb_breadcrumbs()}  
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">
                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">Changes in Gene List since Ensembl upgrade - ${c.data['gene_set_name']}</div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>Genes in your gene list that have been changed are listed here.</p>
                                <p>Genes that are in your gene list currently are not listed here.</p>
                            </div>
                        </div>

                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>    
            <div id="form">
                <div class="innerDiv">
                
                    <div class="hidden" id="gene_set_id">${c.gene_set_id}</div>
                    <div class="hidden" id="db_id">${c.data['db_id']}</div>
                    <div class="hidden" id="gene_set_name">${c.data['gene_set_name']}</div>
                                <% status = c.data['status'] %>

                    <div class="genesetmenu">
                        <ul class="buttonMenus">
                            <!-- <li id="exportMenu">
                                <a class="button dropdown"><span><span class="icon go"></span>Export</span><span class="arrow down"></span></a>
                                <ul class="submenu">
                                    <li><a href="#" id="exportTableCSVButton">Export Gene List</a></li>
                                </ul>
                            </li>
                            -->
                                %if status != "Deleted":
                               <li id="maintenanceMenu">
                                    <a class="button dropdown"><span><span class="icon fix"></span>Maintenance</span><span class="arrow down"></span></a>
                                    <ul class="submenu">
                                        <li><a id="setok" href="${h.url('/ensembl_upgrade/update_gene_set/')}${c.gene_set_id}?update=OK">Mark as OK</a></li>
                                        <li><a id="add_using_ogs" href="${h.url('/ensembl_upgrade/update_gene_set/')}${c.gene_set_id}?update=all">Add to Gene List using Gene Name and Entrez ID</a></li>
                                        <li><a id="add_using_ogs" href="${h.url('/ensembl_upgrade/update_gene_set/')}${c.gene_set_id}?update=ogs">Add to Gene List using Gene Name (official gene symbol)</a></li>
                                        <li><a id="add_using_ogs" href="${h.url('/ensembl_upgrade/update_gene_set/')}${c.gene_set_id}?update=entrez">Add to Gene List using Entrez ID</a></li>
                                        <li><a id="deleteGeneSet" href="${h.url('/workbench/gene_set_delete/')}${c.gene_set_id}">Delete Gene List</a></li>
                                    </ul>
                                </li>
                                % endif
                            <!-- <li id="helpMenu"> <a href="#" class="button help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li> -->
                        </ul>
                    </div>
                    
                    <div class=message>${c.message}</div>
                    
                    <div class="clear"></div>
                    <div id="description"> 
                        <div class="innerDiv">
                                <% 
                                number_of_current_genes = c.data['number_of_current_genes']
if c.data['description'] == '' or c.data['description'] is None:
    descriptionText = "No description (Only retired and remapped genes shown here. "+str(number_of_current_genes)+" current genes,"+ str(c.data['remapped']) + " remapped genes and "+str(c.data['retired'])+" retired genes)"
else:
    descriptionText = c.data['description'] + " (Only retired and remapped genes shown here. "+str(number_of_current_genes)+" current genes,"+str(c.data['remapped']) +" remapped genes and "+str(c.data['retired'])+" retired genes)"
endif 
%>
                            <div id="descriptionText">${descriptionText}</div>
                        </div>
                    </div>
                            
                    <table id="gene_set_items">
                        <thead>
                            <tr>
                                <th>Upgrade Status</th>
                                <th id="symbol">Pre-upgrade Gene Name</th>
                                <th id="ensemblID">Pre-upgrade Ensembl ID</th>
                                <th id="entrez">Pre-upgrade Entrez ID</th>
                            </tr>
                        </thead>
                        <tbody>
                        % if c.data['genes'] == [] or c.data['genes'] is None:
                            <tr><td style="text-align:center;"> No Genes were found. </td><td></td><td></td>
                        % else: 
                            <% count = 0 %>
                        
                            % for old_ens_gene_id in c.data['genes']:
                                
                                <% 
                                    genes = c.data['genes'][old_ens_gene_id]
                                    name = genes.old_ogs
                                    entrez = genes.old_entrez_id
                                    status = genes.ens_id_status
                                    ensemblID = old_ens_gene_id
                                    db_id = c.data['db_id']
                                    gene_set_list_id = c.gene_set_id
                                    if db_id == int(c.human_db): 
                                        ensemblLink = c.url_human_old_ensembl_archive+"/Homo_sapiens/Gene/Summary?g="+str(ensemblID)            
                                    else:
                                        ensemblLink = c.url_mouse_old_ensembl_archive+"/Mus_musculus/Gene/Summary?g="+str(ensemblID)
                                %>
                                
                                <tr>
                                    <td>${status}</td>
                                    <td>${name}</td>
                                    <td><a target="_blank" href="${ensemblLink}">${ensemblID}</a></td>
                                    <td>${entrez}</td>
                                   
                                    
                                </tr>
                                
                                
                            % endfor
                        % endif
                        </tbody>
                    </table>
                    <div class="clear" > </div>
                </div>
                <div class="clear" > </div>
            </div>
        </div>
        <div class="clear" > </div>
    </div>
    

