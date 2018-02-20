<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/jobs_index.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/admin/update_datasets.js')}"></script>
    <style>
        #main_body { width: 1400px !important; }
        #chooseDatasetTable { width: 1400px !important; }
    </style>

</%def>

    
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Dataset made Public 
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>Please check carefully.</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>
            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="long">ID</th>
                        <th class="long">Title</th>
                        <th class="long">Handle</th>
                        <th class="long">Private</th>
                        <th class="long">Published</th>
                        <th class="long">Yugene</th>
                        <th class="long">Limited</th>
                        <th class="long">GenePattern Access</th>
                        <th class="long">Platform Type</th>
                        <th class="long">Actions</th>
                        
                    </tr>
                </thead>
                <tbody>
                       % for ds_id in c.dataset: 

                            <% 
db_id = c.dataset[ds_id]['db_id']
gene_set_id = c.species_dict[db_id]['default_kegg_gene_list_id']
mgeg_url = h.url('/workbench/histogram_wizard?graphType=default&db_id='+str(db_id)+'&gene_set_id='+str(gene_set_id)+'&datasetID='+str(ds_id)) 

                            %>



                        <tr>    
                            <td>${ds_id}</td> 
                            <td id="${ds_id}title">${c.dataset[ds_id]['title']}</td> 
                            <td id="${ds_id}handle">${c.dataset[ds_id]['handle']}</td> 
                            <td id="${ds_id}private">${'Private' if c.dataset[ds_id]['private'] else 'Public'}</td> 
                            <td id="${ds_id}published">${'Published' if c.dataset[ds_id]['published'] else 'Not Published'}</td> 
                            <td id="${ds_id}yugene">${'Show Yugene' if c.dataset[ds_id]['show_yugene'] else 'Hide Yugene'}</td> 
                            <td id="${ds_id}limited">${'Show Limited' if c.dataset[ds_id]['show_limited'] else 'Hide Limited'}</td> 
                            <td id="${ds_id}genepattern_access">${c.dataset[ds_id]['gene_pattern_analysis_access']}</td> 
                            <td id="${ds_id}platform_type">${c.dataset[ds_id]['platform']}</td> 
                            <td>
                                <ul class="buttonMenus">
                                    <li id="updateMenu">
                                        <a class="button dropdown"><span>...</span><span class="arrow down"></span></a>
                                        <ul class="submenu">
                                            <li><a target="_blank" href="${h.url('/datasets/search?ds_id='+str(ds_id))}" class="annotate" ds_id="${ds_id}">View Dataset</a></li>
                                            <li><a target="_blank" href="${mgeg_url}" class="annotate" ds_id="${ds_id}">View Graph</a></li>
                                            <li><a target="_blank" href="${h.url('/admin/annotate_dataset?ds_id='+str(ds_id))}" class="annotate" ds_id="${ds_id}">Annotate Dataset</a></li>
                                            <li><a href="#" class="updateHandle" ds_id="${ds_id}">Update Handle</a></li>
%if not c.dataset[ds_id]['private']:
                                            <li><a href="#" class="makePrivate" ds_id="${ds_id}">Make Private</a></li>
%else:
                                            <li><a href="#" class="makePublic" ds_id="${ds_id}">Make Public</a></li>
%endif
                                            <li><a href="#" class="togglePublished" ds_id="${ds_id}">Toggle Published</a></li> 
                                            <li><a href="#" class="toggleYugene" ds_id="${ds_id}">Toggle Yugene</a></li> 
                                            <li><a href="#" class="toggleLimited" ds_id="${ds_id}">Toggle Limited</a></li> 
                                        </ul>
                                    </li>
                                </ul> 
                            </td>
                        </tr>
               
                       % endfor
                </tbody>
            </table>
            <div>
                <div class="text">
                    <p>
                        <br/><br/>
                        ${h.setup_email_to_contributing_author(c.dataset[c.ds_id],c.ds_id,c.full_name,c.external_base_url)  | n }

                    </p>
                </div> 
            </div>
        </div>
    </div>
    <div id="update_handle" class="modal">
        
        <div class="wb_modal_title">
            Dataset Handle Update
        </div>
        <form id="form_dataset_handle" method="post">
            <label>New Dataset Handle:</label><input name="handle" id="handle" type="text" value="" />
            <br />
            <button class="submit" id="submit_gene_set_name">Submit</button>
            
        </form>
        
    </div>

 
