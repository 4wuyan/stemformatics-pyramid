<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link type="text/css" href="${h.url('/css/workbench/index.css')}" rel="stylesheet" />
    <link type="text/css" href="${h.url('/css/workbench/fold_change_viewer.css')}" rel="stylesheet" />
    <script type="text/javascript" src="${h.url('/js/workbench/fold_change_viewer.js')}"></script>
</%def>



    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">


            ${Base.wb_breadcrumbs()}


            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Fold Change Viewer
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>The details for the fold change can be shown below. Simply select two samples and the values will automatically change</p>
                                <p>Please note that the values shown are normalized by ${c.site_name} and a log2 is performed. See more <a href="${h.url('/'+str(c.site_name)+'_data_methods.pdf')}" target="_blank">details here</a>.</p>
                                <p>The fold change is calculated as 2 to the power of (Sample 2 value (which is a log 2) - Sample 1 value) </p>
                                <p>eg. Sample 1 is 8 and Sample 2 is 10. The fold change is calculated as 2 to the power of (10-8) which is a fold change of 4.</p>
                            </div>

                        </div>


                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <div id="form">
                <div class="hidden" id="json_view_data">${c.json_view_data}</div>
                <div class="innerDiv">

                    <table id="job_titles" class="job_titles">
                        <tbody>
                            <tr>
                                <td>Gene</td>
                                <td>${c.gene}</td>
                            </tr>
                            <tr>
                                <td>Dataset</td>
                                <td><a href="${h.url('/datasets/search?ds_id='+str(c.view_data.ds_id))}">${c.view_data.handle}</a></td>
                            </tr>
                        </tbody>
                    </table>

                    <a name="table"></a>
                    <div class="result_title">Results table</div>
                    <ul class="buttonMenus">
                        <li id="exportMenu">
                            <a class="button dropdown"><span><span class="icon go"></span>Export</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                                <li><a href="#" id="exportTableCSVButton">Export Fold Change</a></li>
                            </ul>
                        </li>
                        <li id="viewMenu">
                            <a class="button dropdown"><span><span class="icon bargraph"></span>View Expression</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                                <li><a id="gene_expression_view_button" href="${h.url('/expressions/result?datasetID='+ str(c.view_data.ds_id) + '&gene='+ str(c.ensemblID) + '&db_id='+str(c.db_id)+'&graphType=box')}" >View Gene Expression</a></li>
                            </ul>
                        </li>
                        <li id="helpMenu"> <a href="#" class="button help wb_open_help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li>
                    </ul>
                    <div class="clear"></div>

                    <table id="fold_change_output_table" class="show_job_output">
                    % if hasattr(c.view_data,'raw_probe_list'):
                        <thead>



                            <tr>
                                    <th class="short"></th>
                                    <th>Sample 1 value</th>
                                    <th class="short"></th>
                                    <th>Sample 2 value</th>
                            </tr>
                            </thead>
                            <tbody>
                                <% c.sample_data = c.view_data.sample_type_display_order %>
                                <% revalidateText = "" %>
                                <tr>
                                    <th>Probe</th>
                                    <td>${h.select("sample_type_1",'' , c.sample_data)}</td>
                                    <td>Fold Change</td>
                                    <td>${h.select("sample_type_2",'' , c.sample_data)}</td>
                                </tr>
                                    % for i in c.view_data.raw_probe_list:

                                        <tr>
                                            <td>${i}</td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>

                                    % endfor

                        </tbody>
                    </table>


                    %else :

                    <tr><td>No probes found for this gene and dataset.</td></tr>
                    </table>
                    %endif

                    <a name="save"></a>
                    <div class="clear"></div>

                    <a name="export"></a>
                    <div class="clear"></div>
                </div>
            </div>

        </div>
    </div>
