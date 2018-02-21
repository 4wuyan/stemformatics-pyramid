<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/jobs_index.js')}"></script>
</%def>

    
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Admin interface
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>Admin Tasks</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>
            <a class="linkButtons" href="${h.url('/admin/add_objects_to_datasets')}">Add Objects to Datasets</a>
            <div class="clear"></div>
            <br/>
        
        
            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="long">Username</th>
                        <th class="long">Dataset</th>
                        <th class="long">Role</th>
                        <th class="long">Check</th>
                        
                    </tr>
                </thead>
                <tbody>
                        %for row in c.result: 
                            <% 
                                object_type = row['object_type']
                                object_name = row['object_name']
                                handle = row['handle']
                                role = row['role']
                                object_id = row['object_id']
                                ds_id = row['ds_id']
                                status = c.user_status_dict[row['object_status']]
                            %>
                            <tr> <td>${object_type} ${object_name} [${status}] [id:${object_id}]</td><td>${handle} [${ds_id}]</td><td>${role}</td>
                            <td>
                                <a href="${h.url('/admin/check_uid_ds_id?user_ids='+str(object_id)+'&datasetID='+str(ds_id))}">Check Access</a> | 
                                <a href="${h.url('/admin/create_letter_for_annotator?uid='+str(object_id)+'&ds_id='+str(ds_id))}">Template</a> 
                            </td>
                            </tr>
                        %endfor 
                </tbody>
            </table>
        
        </div>
    </div>
    
