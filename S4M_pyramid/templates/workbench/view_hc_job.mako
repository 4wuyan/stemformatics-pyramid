<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link type="text/css" href="${h.url('/css/workbench/index.css')}" rel="stylesheet" />
    <script type="text/javascript" src="${h.url('/js/workbench/view_hc_job.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/share_job_link.js')}"></script>
</%def>


    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">


            ${Base.wb_breadcrumbs()}

            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Hierarchical Cluster Result
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>This graphic is a clustered heatmap, showing samples on the X axis and genes on the Y axis. Genes and samples are grouped to highlight co-regulated gene lists.  Similar patterns of expression appear near to each other, letting us more intuitively see biologically interesting variation.</p>
                                <p>Red cells indicate that the gene for a given sample is highly expressed. Blue cells indicate low expression. The range of intermediate colours gives an idea as to relative expression levels in the mid-ranges.</p>
                                <p>The clustering “trees” (dendograms) show how samples and genes are related.</p>
                                <p>For more details on the underlying analysis methods, <a href="${h.url('/workbench/help_hierarchical_cluster')}">click here</a> </p>
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
                            <%
                            import json
                            options = json.loads(c.job_detail.options)
                            %>
                            %if 'select_probes' in options and options['select_probes'] != "":
                                <td>Individually selected probes</td>
                                <td>${len(filter(None,options['select_probes'].split(config['delimiter'])))} probes selected</td>
                            %else:
                                <td>Gene List</td>
                                %if c.job_detail.uid == c.uid:
                                <td><a href="${h.url('/workbench/gene_set_view/'+str(c.job_detail.gene_set_id))}">${c.gene_set_name}</a></td>
                                %else:
                                <td>${c.gene_set_name}</td>

                                %endif
                            %endif
                            </tr>
                            <tr>
                                <td>Dataset</td>
                                <td><a href="${h.url('/datasets/search?ds_id='+str(c.job_detail.dataset_id))}">${c.handle}</a></td>
                            </tr>
                            <tr>
                                <td>Cluster Type</td>
                                <% import json %>
                                <%
                                    try:
                                        options = json.loads(c.job_detail.options)
                                    except:
                                        options = {}
                                %>
                                <%
                                    cluster_type = options['cluster_type']
                                    if cluster_type == 'pearson_both':
                                        display_cluster_type = 'Cluster by Samples and Probes using Pearson Correlation'
                                    elif cluster_type == 'pearson_row':
                                        display_cluster_type = 'Cluster by Genes/Probes only using Pearson Correlation'
                                    elif cluster_type == 'pearson_column':
                                        display_cluster_type = 'Cluster by Samples only using Pearson Correlation'
                                    elif cluster_type == 'euclidean_both':
                                        display_cluster_type = 'Cluster by Samples and Probes using Euclidean Correlation'
                                    elif cluster_type == 'euclidean_row':
                                        display_cluster_type = 'Cluster by Genes/Probes only using Euclidean Correlation'
                                    elif cluster_type == 'euclidean_column':
                                        display_cluster_type = 'Cluster by Samples only using Euclidean Correlation'
                                 %>
                                <td>${display_cluster_type}</td>
                            </tr><tr>
                                <td>Cluster Size</td>
                                <td>${options['cluster_size'] if 'cluster_size' in options else 'small'}</td>
                            </tr>
                            <tr>
                                <td>Samples Removed</td>
                                <td>${c.text_remove_sample_ids}</td>
                            </tr>
                            % if c.HC_server != "GenePattern":
                            <tr>
                                <td>Colour Scale</td>
                                <td>${c.colour_by}</td>
                            </tr>
                            <tr>
                                <td>Genes Removed due to NA rows</td>
                                <td>${len(c.text["na_rows"])}</td>
                            </tr>
                            % endif
                         </tbody>
                    </table>

                    <a name="heatmap"></a>
                    <div class="result_title">Hierarchical Cluster Image</div>
                    <div class="bookmarks">
                        <a class="bookmark" href="#table">Table</a>
                    </div>
                    <ul class="buttonMenus">
                        <li id="exportMenu">
                            <a class="button dropdown"><span><span class="icon go"></span>Export &amp; Share</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                                <li><a href="#" id="exportTableCSVButton">Export Ranked Genes</a></li>
                                % if c.HC_server != "GenePattern":
                                <li><a href="#" id="exportTableCSVButton_for_na_rows">Export Probes with NA rows/ all values 0 </a></li>
                                <li><a href="#" id="exportTableCSVButton_for_na_columns">Export Samples with all values 0 </a></li>
                                % endif
                                % if not c.job_shared:
                                    <li><a href="#" id="share_link">Share</a></li>
                                % endif
                                <li><a href="#" id="save_image">Save Image</a></li>
                            </ul>
                        </li>
                        <li id="helpMenu"> <a href="#" class="button help wb_open_help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li>
                    </ul>
                    <div class="clear"></div>

                    <img class="hc_heatmap" src="${h.url('/workbench/view_image?src='+ str(c.gp_job_id) +'/hc.png'+ '&hc_server=' + str(c.HC_server))}"/>
                    <div class="clear"></div>

                    <a name="table"></a>
                    <div class="result_title">Hierarchical Cluster Ranked Genes</div>
                    <div class="bookmarks">
                        <a class="bookmark" href="#heatmap">Heatmap</a>
                        <div class="clear"/>
                    </div>
                    <div class="clear"></div>
                    % if c.HC_server == "GenePattern":
                        <table id="RankedGenes" class="show_job_output">
                            <thead>
                                <tr>
                                    <th>Gene</th>
                                    <th>Probe</th>
                                </tr>
                            </thead>
                            <tbody>
                                <%
                                    count = 0
                                %>
                                % for line in c.text:

                                    % if count > 2:

                                        <%

                                            splitTemp = line.split('\t')

                                            gene = "hello"
                                            probe = "hello"

                                            if c.cluster_type == 'pearson_column':
                                                gene_and_probe = splitTemp[0]
                                            else:
                                                gene_and_probe = splitTemp[1]
                                            splitTemp2 = gene_and_probe.split(' ')

                                            gene = splitTemp2[0]
                                            probe = splitTemp2[len(splitTemp2)-1]
                                        %>

                                        <tr>
                                            <td>${gene}</td>
                                            <td><a href="${h.url('/expressions/probe_result?graphType=default&datasetID='+str(c.job_detail.dataset_id)+'&db_id='+str(c.db_id)+'&probe=')}${probe | u }">${probe}</a></td>
                                        </tr>
                                    % endif

                                    <%
                                        count = count + 1
                                    %>
                                % endfor
                            </tbody>
                        </table>
                    % else:
                    <table id="RankedGenes" class="show_job_output">
                        <thead>
                            <tr>
                                <th>Gene</th>
                                <th>Probe</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for line in c.text['row_ids']:
                                <% splitTemp = line.split(' ') %>
                                <!-- this checks if mapped gene for probe id present or not-->
                                    % if len(splitTemp) > 1:
                                    <%
                                        gene = splitTemp[0]
                                        probe = splitTemp[1]
                                    %>
                                % else:
                                    <%
                                        gene = ''
                                        probe = line
                                    %>
                                % endif
                                <tr>
                                    <td>${gene}</td>
                                    <td><a href="${h.url('/expressions/probe_result?graphType=default&datasetID='+str(c.job_detail.dataset_id)+'&db_id='+str(c.db_id)+'&probe=')}${probe}">${probe}</a></td>
                                </tr>
                            % endfor

                        </tbody>
                    </table>
                    <table id="NaRows" class="show_job_output hidden">
                        <thead>
                            <tr>
                                <th>Gene</th>
                                <th>Probe</th>
                                <th>Type</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for line in c.text['na_rows']:
                            <% splitTemp = line.split(' ') %>
                            <!-- this checks if mapped gene for probe id present or not-->
                                % if len(splitTemp) > 1:
                                <%
                                    gene = splitTemp[0]
                                    probe = splitTemp[1]
                                    type = 'atleast 1 value was found as NA'
                                %>
                            % else:
                                <%
                                    gene = ''
                                    probe = line
                                    type = 'atleast 1 value was found as NA'
                                %>
                            % endif
                                <tr>
                                    <td>${gene}</td>
                                    <td>${probe}</td>
                                    <td>${type}</td>
                                </tr>
                            % endfor
                            <!-- create rows for rows will exp values as 0 -->
                            % if hasattr(c.text,'zero_var_rows'):
                                % for line in c.text['zero_var_rows']:
                                    <% splitTemp = line.split(' ') %>
                                    <!-- this checks if mapped gene for probe id present or not-->
                                        % if len(splitTemp) > 1:
                                        <%
                                            gene = splitTemp[0]
                                            probe = splitTemp[1]
                                            type = 'all values were found to be 0'
                                        %>
                                    % else:
                                        <%
                                            gene = ''
                                            probe = line
                                            type = 'all values were found to be 0'
                                        %>
                                    % endif
                                        <tr>
                                            <td>${gene}</td>
                                            <td>${probe}</td>
                                            <td>${type}</td>
                                        </tr>
                                % endfor
                            % endif
                        </tbody>
                    </table>
                    <table id="NaColumns" class="show_job_output hidden">
                      <thead>
                        <tr>
                            <th>Sample</th>
                            <th>Type</th>
                        </tr>
                      </thead>
                      <tbody>
                        <!-- create columns for columns will exp values as 0 -->
                          % if hasattr(c.text,'zero_var_columns'):
                              % for line in c.text['zero_var_columns']:
                                  <%
                                      sample = line
                                      type = 'all sample values were found to be 0'
                                  %>
                                      <tr>
                                          <td>${sample}</td>
                                          <td>${type}</td>
                                      </tr>
                              % endfor
                          % endif
                      </tbody>

                    </table>
                    % endif
                    <div class="bookmarks">
                        <a class="bookmark" href="#heatmap">Heatmap</a>
                        <a class="bookmark" href="#table">Table</a>
                        <div class="clear"/>
                    </div>
                    <div class="clear"></div>
                </div>
            </div>
        </div>
    </div>
    </div>
    </div>
