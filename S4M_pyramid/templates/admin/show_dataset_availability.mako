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
            <table id="view_datasets">
                <thead>
                    <tr>
                        <th class="long">uid</th>
                        <th class="long">ds_id</th>
                        <th class="long">status</th>
                        
                    </tr>
                </thead>
                <tbody>
                        %for uid in c.output: 
                            %for ds_id in c.output[uid]:
                                <% status = c.output[uid][ds_id] %>
                                <tr><td>${uid}</td> <td>${ds_id}</td><td>${status}</td></tr>
                            %endfor
                        %endfor 
                </tbody>
            </table>
        
        </div>
    </div>
    
