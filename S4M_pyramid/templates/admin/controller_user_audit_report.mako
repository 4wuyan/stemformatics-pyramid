<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/jobs_index.js')}"></script>

    <script>
    $(document).ready(function() {
        $('div.export').click(function(){
            data_id = $(this).attr('data-id');
            $('#'+data_id+'_audit_report').table2CSV();	
        });          
    }); 
    </script>


</%def>

    
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Audit Reports
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>


            <form action="#" method="post" class="margin_bottom_large">

                <dl>
                    <div>Start Date</div><div class="margin_bottom_small"><input type="text" name="start_date" value="${c.start_date}"></div>
                    <div>End Date</div><div class="margin_bottom_small"><input type="text" name="end_date" value="${c.end_date}"></div>
                    <div>Limit rows</div><div class="margin_bottom_small"><input type="text" name="limit" value="${c.limit}"></div>
                    <input type="submit">
                </dl>
            </form>



            <div class="title margin_bottom_small">Controller User Audit Report <div data-id="controller_user" class="export margin_left_small generic_orange_button"><a href="#!">Export Controller User Audit Report</a></div></div> 
            <table id="controller_user_audit_report" class="margin_bottom_large">
                <thead>
                    <tr>
                        <th class="long">Controller</th>
                        <th class="long">Action</th>
                        <th class="long">Username</th>
                        <th class="long">Count</th>
                        
                    </tr>
                </thead>
                <tbody>
                    %for row in c.result['controller_user']: 
                        <tr>
                            <td>${row['controller']}</td>
                            <td>${row['action']}</td>
                            <td>${row['username']}</td>
                            <td>${row['c']}</td>
                        </tr>
                    %endfor
                </tbody>
            </table>
          
        </div>
    </div>
    
