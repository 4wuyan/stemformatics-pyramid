<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link type="text/css" href="${h.url('/css/workbench/index.css')}" rel="stylesheet" />
    <script type="text/javascript" src="${h.url('/js/workbench/view_gn_job.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/share_job_link.js')}"></script>
    %if c.analysis == 7:
        <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/user_defined_expression_profile.css')}" >
        <script type="text/javascript" src="${h.url('/js/workbench/user_defined_expression_profile.js')}"></script>
    %endif
</%def>



    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">


            ${Base.wb_breadcrumbs()}


            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                % if c.analysis ==2:
                                    Gene Neighbourhood Result
                                % endif
                                % if c.analysis ==7:
                                    User Defined Expression Profile
                                % endif
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>The genes most similar to your gene of interest/expression profile are displayed here in rank order. You may save this gene list for further use by clicking the “Save” button, or you can Export (download) them.  The closer the score is to 0 the more similar the gene is. Only genes that have a score of less than 0.05 are shown in the table.</p>
                                <p>For more details on the underlying analysis methods, <a href="${h.url('/workbench/help_gene_neighbourhood')}">click here</a> </p>
                            </div>

                        </div>


                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <div id="form">
                <div class="innerDiv">

                    <table id="job_titles" class="job_titles">
                        <tbody>
                            <tr>
                                <td>Job#</td>
                                <td>${str(c.job_detail.job_id) + ' [Shared by '+ c.shared_user.username +']' if c.job_shared else str(c.job_detail.job_id)}</td>
                            </tr>
                            <tr>
                                <td>Gene</td>
                                <td>${c.gene}</td>
                            </tr>
                            <tr>
                                <td>Probe</td>
                                <td>${c.probe}</td>
                            </tr>
                            <tr>
                                <td>Dataset</td>
                                <td><a href="${h.url('/datasets/search?ds_id='+str(c.job_detail.dataset_id))}">${c.handle}</a></td>
                            </tr>
                            <tr>
                                <td>Probes Returned</td>
                                %if c.analysis == 2:
                                    <td>${len(c.listProbesInOrderODF)}</td>
                                %else:
                                    <td>${len(c.listProbesInOrderODF)-1}</td>

                                %endif
                            </tr>

                        </tbody>
                    </table>
                    <form action="${c.url}" method="post">
                        <table id="choose_p_value">
                            <thead>
                                <tr>
                                    <th id="original">Information</th>
                                    <th id="status">Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                    <tr>
                                        <td>The lower the p-value the more stringent the test and less genes will appear in the list.</td>
                                        <td>
                                            <select name="p_value">
                                                    <option value="0.01" ${ "selected" if c.p_value == 0.01 else ""} >0.01 (Most stringent)</option>
                                                    <option value="0.05" ${ "selected" if c.p_value == 0.05 else ""} >0.05</option>
                                                    <option value="0.1" ${ "selected" if c.p_value == 0.1 else ""} >0.10</option>
                                                    <option value="0.2" ${ "selected" if c.p_value == 0.2 else ""} >0.20 (Least stringent)</option>
                                            </select>
                                        </td>
                                    </tr>




                            </tbody>
                        </table>

                        <div class="clear" > </div>
                        <input class="smallMarginTop" name="p_value_submit" type="Submit" value="Submit"/>
                    </form>
                    <div class="clear"></div>
                    <a name="table"></a>

                    <div class="result_title">Results table</div>
                    <ul class="buttonMenus">
                        <li id="exportMenu">
                            <a class="button dropdown"><span><span class="icon go"></span>Export &amp; Share</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                                <li><a href="#" id="submitSaveAsGeneSetButton">Save Result as Gene List</a></li>
                                <li><a href="#" id="exportTableCSVButton">Export Genes</a></li>
                                % if not c.job_shared:
                                    <li><a href="#" id="share_link">Share</a></li>
                                % endif
                            </ul>
                        </li>
                        <li id="helpMenu"> <a href="#" class="button help wb_open_help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li>
                    </ul>
                    <div class="clear"></div>

                    %if c.analysis == 7:
                        <table class="udep_overview">
                            <thead>
                                <tr>
                                    <th >Detection Threshold</th>
                                    <th >Median</th>
                                    <th >Min Value</th>
                                    <th >Max Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td id="detection_threshold">${c.dataset_metadata['detection_threshold']}</td>
                                    <td id="median">${c.dataset_metadata['median_dataset_expression']}</td>
                                    <td id="min_value_for_dataset">0</td>
                                    <td id="max_value_for_dataset">${c.dataset_metadata['maxGraphValue']}</td>
                                </tr>

                            </tbody>
                        </table>

                        <div id="initialise_slider" class="hidden">${c.options}</div>
                        <div id="sample_type_display_order" class="hidden">${c.dataset_metadata['sampleTypeDisplayOrder']}</div>

                        <% sample_type_display_order = c.dataset_metadata['sampleTypeDisplayOrder'].split(',') %>
                        <% position = 0 %>
                        % for sample_type in sample_type_display_order:
                            <div class="details">
                                <div id="slider_${position}" class="slider" ></div>
                                <div id="name_${position}" class="view_value">${sample_type}</div>
                                <input type="hidden" id="input_${position}" name="input_${position}" value="${c.dataset_metadata['detection_threshold']}" >
                                <div id="value_${position}" class="view_value"></div>
                                <div class="clear"></div>
                            </div>
                            <% position +=1 %>
                        %endfor

                    %endif



                    <table id="showGNOutput" class="show_job_output">
                        <thead>



                            <tr>
                                    <th>Gene</th>
                                    <th>Probe</th>
                                    <th>Score</th>
                            </tr>
                            </thead>
                            <tbody>
                                <% revalidateText = "" %>

                                % for probe in c.listProbesInOrderODF:

                                    <%
                                        if isinstance(c.geneList[probe]['symbol'],list):
                                            symbol = ' '.join(c.geneList[probe]['symbol'])
                                            ambiguous = True
                                        else:
                                            symbol = c.geneList[probe]['symbol']
                                            ambiguous = False

                                        revalidateText = revalidateText + probe + '\n'

                                        score = float(c.result[probe]['score'])

                                        score = "%.2E" % score
                                        # score = round(c.result[probe]['score'],2)

                                        ensemblID = c.geneList[probe]['ensemblID']
                                    %>

                                    % if symbol != '':
                                    <tr>
                                        <td>${symbol}</td>
                                        % if not ambiguous:
                                            <td><a href="${h.url('/expressions/result?graphType=box&gene='+str(ensemblID)+'&db_id='+str(c.db_id)+'&datasetID='+str(c.job_detail.dataset_id))}">${probe}</a></td>
                                        % else:
                                            <td><a href="${h.url('/expressions/probe_result?graphType=box&db_id='+str(c.db_id)+'&datasetID='+str(c.job_detail.dataset_id)+'&probe=')}${str(probe)| u }">${probe}</a></td>
                                        % endif
                                        <td>${score}</td>
                                    </tr>
                                    %else:
                                        % if probe != 'User':
                                            <tr>
                                                <td>Probe not mapped</td>
                                                    <td><a href="${h.url('/expressions/probe_result?graphType=box&db_id='+str(c.db_id)+'&datasetID='+str(c.job_detail.dataset_id)+'&probe=')}${str(probe)| u }">${probe}</a></td>
                                                <td>${score}</td>
                                            </tr>
                                        %endif

                                    % endif

                                % endfor


                        </tbody>
                    </table>


                    <div class="clear"></div>

                    <form id="saveAsGeneSet" action="${h.url('/workbench/save_gene_set')}" method="post">

                        <input name="probe_list" type="hidden" value = "${revalidateText}" />
                        <input name="db_id" type="hidden" value="${c.db_id}" />
                        <input name="job_id" type="hidden" value="${c.job_id}" />

                        %if c.analysis==2:
                        <input name="gene_set_name" type="hidden" value="From Gene Neighbourhood job# ${c.job_detail.job_id}">
                        %endif
                        %if c.analysis==7:
                        <input name="gene_set_name" type="hidden" value="From User Defined Expression Profile job# ${c.job_detail.job_id}">
                        %endif
                        %if c.analysis==2:
                        <input name="description" type="hidden" value="Genes similar to Gene ${c.gene} and Probe ${c.probe} with dataset ${c.handle} from Gene Neighbourhood Job# ${c.job_detail.job_id}">
                        %endif
                        %if c.analysis==7:
                        <input name="description" type="hidden" value="Genes similar to the user defined expression profile with dataset ${c.handle} from User Defined Expression Profile Job# ${c.job_detail.job_id}">
                        %endif
                        <input class=hidden id=submitSaveAsGeneSetButton type="submit" value="Save"/>
                        <div class="clear"></div>
                    </form>
                    <div class="clear"></div>
                </div>
            </div>

        </div>
    </div>
