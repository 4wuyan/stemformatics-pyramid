<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/jobs_index.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/download_multiple_datasets.js')}"></script>
</%def>
 
    
        
    <div id="wb_background" class="wb_background_divs dataset_results">    
        <div id="wb_background_inner_div">
            
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                     
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                MSC Signature home
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>Coming soon</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>


                   <% 
                        totals={}
                        totals['Total'] = 0 
                        totals['MSC'] = 0 
                        totals['Non-MSC'] = 0 
                        totals['Training'] = 0 
                        totals['Testing'] = 0 
                        totals['Excluded'] = 0 
                        totals['MSC Training'] = 0 
                        totals['Non-MSC Training'] = 0 
                        totals['MSC Testing'] = 0 
                        totals['Non-MSC Testing'] = 0 
                        for ds_id in c.msc_samples_summary:
                            row = c.msc_samples_summary[ds_id]
                            totals['Total'] +=row['Total'] 
                            totals['MSC'] +=row['MSC'] 
                            totals['Non-MSC'] +=row['Non-MSC'] 
                            totals['Training'] +=row['Training'] 
                            totals['Testing'] +=row['Testing'] 
                            totals['Excluded'] +=row['Excluded'] 
                            totals['MSC Training'] +=row['MSC Training']
                            totals['Non-MSC Training'] +=row['Non-MSC Training'] 
                            totals['MSC Testing'] +=row['MSC Testing'] 
                            totals['Non-MSC Testing'] +=row['Non-MSC Testing'] 
                     

                    %> 
 
            <div class="export_buttons">

                <% 
                    url_training=h.url('/msc_signature/export?project_msc_set=Training') 
                    url_testing=h.url('/msc_signature/export?project_msc_set=Testing') 
                    url_all=h.url('/msc_signature/export?project_msc_set=All') 
                    url_rejected=h.url('/msc_signature/export?project_msc_set=Excluded') 
                    url_download=h.url('/msc_signature/export?project_msc_set=download_script') 
                %>

                <!-- 
                <div class="generic_orange_button "><a class="" href="${url_training}">Export Training Samples</a></div>
                <div class="generic_orange_button margin_bottom_large"><a class="" href="${url_testing}">Export Testing Samples</a></div>
                <div class="generic_orange_button "><a class="" href="${url_all}">Export All Samples</a></div>
                <div class="generic_orange_button "><a class="" href="${url_rejected}">Export Excluded Samples</a></div>
                -->
                <div class="margin_bottom_large generic_orange_button script_to_download"><a class="export" href="${url_download}">Export download script for selected datasets</a></div>
                <div class="generic_orange_button "><a href="${h.url('/contents/download_mappings')}">Link to probe mappings</a></div>
            </div>

            <table >
                <thead>
                    <tr>
                        <th class="long">Totals</th>
                        <th class="long">Total</th>
                        <th class="long">Training</th>
                        <th class="long">Testing</th>
                        <th class="long">Excluded</th>
                        <th class="long">Training MSC/Non-MSC</th>
                        <th class="long">Testing MSC/Non-MSC</th>
                        <th class="long" colspan="4">Downloads</th>
                    </tr>
                </thead>
                <tbody>
                  <tr> 
                            <td>Totals</td>
                            <td>${totals['Total']}</td>
                            <td>${totals['Training']}</td>
                            <td>${totals['Testing']}</td>
                            <td>${totals['Excluded']}</td>
                            <td>${totals['MSC Training']}/${totals['Non-MSC Training']}</td>
                            <td>${totals['MSC Testing']}/${totals['Non-MSC Testing']}</td>
                            <td>
                            <a href="${h.url('/msc_signature/export?project_msc_set=Training')}">Training</a>
                            </td>
                            <td>
                            <a href="${h.url('/msc_signature/export?project_msc_set=Testing')}">Testing</a>
                            </td>
                            <td>
                            <a href="${h.url('/msc_signature/export?project_msc_set=All')}">All</a>
                            </td>
                            <td>
                            <a href="${h.url('/msc_signature/export?project_msc_set=Excluded')}">Excluded</a>
                            </td>
                                
                        </tr>
                     

                </tbody>
            </table>
  
            <table id="chooseDatasetTable" class="msc">
                <thead>
                    <tr>
                        <th class="toggle_select_all">Click to toggle</th>
                        <th class="long">Dataset ID</th>
                        <th class="long">Handle</th>
                        <th class="long">Total</th>
                        <th class="long">Training</th>
                        <th class="long">Testing</th>
                        <th class="long">Excluded</th>
                        <th class="long">Training MSC/Non-MSC</th>
                        <th class="long">Testing MSC/Non-MSC</th>
                        <th class="long actions_header">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    %for ds_id in c.msc_samples_summary:
                        <%
                            row = c.msc_samples_summary[ds_id]
                            handle = row['handle']
                        %>
                        <tr> 
                            <td><input name="${ds_id}" type="checkbox" checked></input></td>
                            <td>${ds_id}</td>
                            <td> <a target="_blank" href="${h.url('/datasets/search?filter='+str(ds_id)+'&ds_id='+str(ds_id))}">${handle}</a></td>
                            <td>${row['Total']}</td>
                            <td>${row['Training']}</td>
                            <td>${row['Testing']}</td>
                            <td>${row['Excluded']}</td>
                            <td>${row['MSC Training']}/${row['Non-MSC Training']}</td>
                            <td>${row['MSC Testing']}/${row['Non-MSC Testing']}</td>
                            <td class="actions">
                                <ul class="buttonMenus">
                                    <li id="exportMenu">
                                        <a class="button dropdown"><span>Actions .....</span><span class="arrow down"></span></a>
                                        <ul class="submenu">
                                        <% 
                                        url_summary = h.url('/datasets/search?ds_id='+str(ds_id))
                                        url_yugene = h.url('/datasets/download_yugene/'+str(ds_id))
                                        url_gct = h.url('/datasets/download_gct/'+str(ds_id))
                                        url_annotate = h.url('/admin/annotate_dataset?ds_id='+str(ds_id))
                                        %>
                                           <li><a target="_blank" href="${url_summary}">View Dataset Summary</a></li>
                                           <li><a target="_blank" href="${url_annotate}">Annotate</a></li>
                                           <li><a href="${url_yugene}">Download Yugene</a></li>
                                       </ul>
                                    </li>
                                </ul>

                            </td>
                        </tr>
                    %endfor 


                </tbody>
            </table>
            
        </div>
    </div>
    
