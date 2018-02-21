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
                                Redis Check - DB vs GCT Files vs Redis
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
        
            <%
            header_1 = 'Total datasets OK: ' + str(len(c.ok_list))
            header_2 = 'Total datasets with at least one problem: ' + str(len(c.problem_list))
            %>
            
            <h1>${header_1}</h1>
            <h1>${header_2}</h1>
 
            <table id="chooseDatasetTable">



                <thead>
                    <tr>
                        <th class="long">ds_id</th>
                        <th class="long">in_db</th>
                        <th class="long">in_gct</th>
                        <th class="long">in_redis</th>
                        
                    </tr>
                </thead>
                <tbody>
                    %for ds_id in c.problem_list:

                        <%
                        details = c.result_dict[ds_id]
                        in_db = details['in_db']
                        in_gct = details['in_gct']
                        in_redis = details['in_redis']
                        ds_id_html = "<a target=\"_blank\" href=\"/datasets/search?ds_id="+str(ds_id)+"\" >"+str(ds_id)+"</a>"
                        row_list = [ds_id_html,str(in_db),str(in_gct),str(in_redis)] 
                        row_html = "<tr><td>" + "</td><td>".join(row_list) + "</td></tr>"
                        %>
             
                        ${row_html | n } 
                    
                    %endfor
                </tbody>
            </table>
        
        </div>
    </div>
    
