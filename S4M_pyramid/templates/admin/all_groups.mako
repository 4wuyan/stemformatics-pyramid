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
            <a class="linkButtons" href="${h.url('/admin/add_users_to_groups_wizard')}">Add Group Users</a>
            <a class="linkButtons" href="${h.url('/admin/add_objects_to_datasets')}">Add Objects to Datasets</a>
            <div class="clear"></div>
            <br/>
        
        
            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="long">Group Name</th>
                        <th class="long">Users</th>
                        <th class="long">Action</th>
                        
                    </tr>
                </thead>
                <tbody>
                        %for row in c.result: 
                            <% 
                                gid = row['gid']
                                uid = row['uid']
                                group_name = c.groups_dict[gid]
                                username = row['username']
                                status = c.user_status_dict[row['status']]
                            %>
                            <tr> <td>${group_name} </td><td>${username} [${status}] [uid:${uid}]</td><td></td></tr>
                        %endfor 
                </tbody>
            </table>
        
        </div>
    </div>
    
