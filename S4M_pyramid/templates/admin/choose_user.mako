<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/admin/choose_user.js')}"></script>
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
            <div class=hidden id="group_ids">${c.group_ids}</div> 
            <div class="hidden" id=base_url>${c.base_url}</div>
            <input type="button" class="submit" value="Submit"></input>
            <div class="clear"></div>
            <textarea id=user_emails style="height:150px;width:660px"></textarea>        
            <div class="clear"></div>
            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="long">Select</th>
                        <th class="long">Username</th>
                        <th class="long">Full Name</th>
                        <th class="long">Organisation</th>
                        <th class="long">Status</th>
                        <th class="long">Action</th>
                        
                    </tr>
                </thead>
                <tbody>
                        %for row in c.result: 
                            <% 
                                username = row['username']
                                uid = row['uid']
                                status = c.user_status_dict[row['status']]
                                full_name = row['full_name']
                                organisation = row['organisation']
                            %>
                            <tr><td><input id=${uid} type="checkbox"></input></td> <td>${username} [${uid}]</td><td>${full_name}</td><td>${organisation}</td><td>${status}</td><td></td></tr>
                        %endfor 
                </tbody>
            </table>
            <input type="button" class="submit" value="Submit"></input>
        
        </div>
    </div>
    
