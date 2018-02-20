<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_view.js')}"></script>
</%def>
    
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            
            ${Base.wb_breadcrumbs()}  
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                    Manage Gene Lists that have differences since the upgrade
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                                    <p>Manage Gene Lists that have differences since the upgrade from Mouse ${c.old_mouse_ensembl_version} to ${c.current_mouse_ensembl_version} and from Human ${c.old_human_ensembl_version} to ${c.current_human_ensembl_version} . You can view, delete, try and add them to your gene lists by using the old ogs or entrez id,  or set them to OK. </p>
                                    <p>You can find more information here - <a href="${h.url('/User_information_about_'+c.site_name+'_Ensembl_upgrade_v4.pdf')}">User Information about ${c.site_name} Ensembl Upgrade</a>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>    
            <div class="tables">
                <div>${c.message}</div>
                <ul class="buttonMenus">
                    <!-- <li id="exportMenu">
                        <a class="button dropdown"><span><span class="icon go"></span>Export</span><span class="arrow down"></span></a>
                        <ul class="submenu">
                            <li><a href="#" id="exportTableCSVButton">Export Gene List Names</a></li>
                        </ul>
                    </li> 
                        <li id="maintenanceMenu">
                            <a class="button dropdown"><span><span class="icon fix"></span>Maintenance</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                                <li><a href="${h.url('/workbench/gene_set_bulk_import_manager')}" id="add_gene">Add Gene List</a></li>
                            </ul>
                        </li>
                    -->
                    <li id="helpMenu"> <a href="#" class="button help wb_open_help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li>
                </ul>
                <div class="height12px"></div> 
                <table id="gene_set_items">
                    <thead>
                        <tr>
                            <th id="original">Gene List Name</th>
                            <th>Status</th>
                            <th># current genes</th>
                            <th># genes remapped</th>
                            <th># genes retired</th>
                            <th id="symbol">Species</th> 
                            <th id="status">Action</th> 
                        </tr>
                    </thead>
                    <tbody>
                    % if c.data == [] or c.data is None:
                        <tr><td style="text-align:center;"> No Gene Lists found. </td><td></td><td></td><td></td><td></td></tr>
                    % else: 
                        % for gene_set_id in c.data:
                            <% 
                                gene_set = c.data[gene_set_id]
                                db_id = gene_set['db_id']
                                name = gene_set['gene_set_name']
                                if db_id == int(c.human_db) :
                                    species = 'Human'
                                else:
                                    species = 'Mouse'
                                num_remapped = gene_set['remapped']
                                num_retired = gene_set['retired']
                                status = gene_set['status']
                                number_of_current_genes = gene_set['number_of_current_genes']
                             %>
                           
                            <tr>
                                <td gene_set_id="name${gene_set_id}">${name.strip()}</td>
                                <td>${status}</td>
                                <td>${number_of_current_genes}</td>
                                <td>${num_remapped}</td>
                                <td>${num_retired}</td>
                                <td>${species}</td>
                                <td class="action">
                                    <ul class="buttonMenus">
                                        <li gene_set_id="exportMenu">
                                            <a class="button dropdown"><span>Actions .....</span><span class="arrow down"></span></a>
                                            <ul class="submenu">
                                                <li><a class="view" href="${h.url('/ensembl_upgrade/view/')}${gene_set_id}">View</a></li>
                                                %if status != "Deleted":
                                                <li><a id="setok" href="${h.url('/ensembl_upgrade/update_gene_set/')}${gene_set_id}?update=OK">Mark as OK</a></li>
                                                <li><a id="add_using_ogs" href="${h.url('/ensembl_upgrade/update_gene_set/')}${gene_set_id}?update=all">Add to Gene List using Gene Name and Entrez ID</a></li>
                                                <li><a id="add_using_ogs" href="${h.url('/ensembl_upgrade/update_gene_set/')}${gene_set_id}?update=ogs">Add to Gene List using Gene Name (official gene symbol)</a></li>
                                                <li><a id="add_using_ogs" href="${h.url('/ensembl_upgrade/update_gene_set/')}${gene_set_id}?update=entrez">Add to Gene List using Entrez ID</a></li>
                                                <li><a id="deleteGeneSet" href="${h.url('/workbench/gene_set_delete/')}${gene_set_id}">Delete Gene List</a></li>
                                                % endif
         
                                           </ul>
                                        </li>
                                    </ul>
                                </td>
                                
                                
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
    
   
