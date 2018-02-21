<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/admin/config_index.js')}"></script>
</%def>

    
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Config Admin interface
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>Configs for this instance</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>
        
        
            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="long">Type</th>
                        <th class="long">Task</th>
                        <th class="long">Action</th>
                        
                    </tr>
                </thead>
                <tbody>
                    %for key in c.configs: 
                        <% value = c.configs[key] %>
                        <tr> <td>${key}</td> <td id="${key}_value">${value}</td><td><a data-ref-type="${key}" class="edit_config" href="#!">Edit</a></td> </tr>
                    %endfor 
                </tbody>
            </table>
        
        </div>
    </div>
    
