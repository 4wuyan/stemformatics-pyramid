<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/admin/choose_group.js')}"></script>
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
            <div class="hidden" id=base_url>${c.base_url}</div>
            <input type="button" class="submit" value="Submit"></input>
        
            <div class="clear"></div>
        
            <table id="choose_group_table">
                <thead>
                    <tr>
                        <th class="long">Select</th>
                        <th class="long">Group Name</th>
                        
                    </tr>
                </thead>
                <tbody>
                        %for gid in c.groups_dict: 
                            <% 
                                group_name = c.groups_dict[gid]
                            %>
                            <tr><td><input id=${gid} type="checkbox"></input></td> <td>${group_name}</td></tr>
                        %endfor 
                </tbody>
            </table>
            <div class="clear"></div>
            <input type="button" class="submit" value="Submit"></input>
             
        </div>
    </div>
    
