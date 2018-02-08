<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <meta http-equiv="refresh" content="60">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/jobs_index.js')}"></script>
</%def>

<%!
    import datetime,json
%>


    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            ${Base.wb_breadcrumbs()}


            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Manage Analysis Jobs
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>Your analysis jobs are displayed here. You may view results for completed analysis tasks and delete analysis tasks as you wish.</p>
                                <p>Refresh this page to see the latest status of your analysis tasks.</p>
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>


            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="th1">#</th>
                        <th class="long">Analysis</th>
                        <th class="finished">Finished</th>
                        <th class="short">Status</th>
                        <th class="expiry">Expires In</th>
                        <!-- <th class="long">Dataset</th>
                        <th class="long">Gene List</th> -->
                        <th class="actions">Actions</th>

                    </tr>
                </thead>
                <tbody>
                    % if c.jobs is not None:
                        % for job in c.jobs:
                            %if job['job_id'] is not None:
                                % if job['status'] == 1:
                                    <tr>
                                % else:
                                    <tr class="pending">
                                %endif


                                        <td>${job['job_id']}</td>

                                        %if 'share_type' in job:
                                            <td id="job_name_${job['job_id']}">${c.analysis[job['analysis']]['name']} [Shared by ${job['username']}]</td>
                                        % else:
                                            <td id="job_name_${job['job_id']}">${c.analysis[job['analysis']]['name']}</td>
                                        %endif

                                        % if job['finished'] is not None:
                                            <td>${job['finished'].strftime("%d/%m/%y %H:%M")}</td>
                                        % else:
                                            <td></td>
                                        % endif
<%
if job['analysis'] ==2: #GN
    first_part = job['gene'] + ' ' + job['probe']
    second_part = ""
elif job['analysis'] == 0: #HC

    if job['options'] is not None:
        options = json.loads(str(job['options']))
        if 'select_probes' in job['options'] and options['select_probes'] != "":
            first_part = str(len(filter(None,options['select_probes'].split(config['delimiter']))))
            second_part = ' individually selected probes '
        else:
            first_part = 'Gene List '
            second_part = job['gene_set_name']
            if second_part is None:
                second_part = "Unknown"
    else:
        first_part = 'Unknown'
        secon_part = ''

else:
    first_part = 'Gene List '
    if job['gene_set_name'] is None:
        second_part = 'Unknown'
    else:
        second_part = job['gene_set_name']
%>
<%
try:
    parameters_text =  first_part + second_part
except:
    parameters_text = "Error working out parameters"
%>
                                        <% dataset_comment = 'with dataset '+job['handle'] if job['handle'] != None else '' %>
                                        % if job['status'] == 1:
                                            <td id="job_status_${job['job_id']}" class="td_status">
        ${c.status[job['status']]} ${dataset_comment} <br/>
        with parameters:
        ${ parameters_text}</td>
                                        % elif job['status'] == 0:
                                            <td class="td_status"><img src="${h.url('/images/spinner.gif')}"></td>
                                        % elif job['status'] == 2:
                                            <td class="td_status"><span class="error">Error</span></td>
                                        % endif

                                        <%
                                            if job['finished'] is not None:
                                                expiry_date = job['finished'] + datetime.timedelta(days=30)
                                                time_difference = expiry_date - datetime.datetime.now()

                                                if time_difference.days < 0:
                                                    expires_in = "expired"
                                                elif time_difference.days >= 1:
                                                    expires_in = str(time_difference.days) + " days"
                                                elif time_difference.seconds >= 60*60:
                                                    expires_in = str(time_difference.seconds/60/60) + " hours"
                                                else:
                                                    expires_in = str(time_difference.seconds/60) + " minutes"
                                            else:
                                                expires_in = ""
                                        %>
                                        <td>${expires_in}</td>

                                        <!-- <td id="job_handle_${job['job_id']}">${job['handle']}</td>
                                        <td id="job_parameters_${job['job_id']}">${ job['gene'] + ' ' + job['probe'] if job['analysis'] ==2 else 'Gene List: ' + str(job['gene_set_name']) if job['gene_set_name'] is None else job['gene_set_name'] }</td>
                                       -->
                                        <td class="action">
                                            <ul class="buttonMenus">
                                                <li id="exportMenu">
                                                    <a class="button dropdown"><span>Actions</span><span class="arrow down"></span></a>
                                                    <ul class="submenu">
                                                        % if job['status'] == 1:
                                                                <li><a href="${h.url('/workbench/job_view_result/'+ str(job['job_id']))}" id="exportDataCSVButton">View</a></li>
                                                        % endif
                                                        %if hasattr(job,'share_type'):
                                                            <li><a class="remove" id="rem_${job['job_id']}"href="${h.url('/workbench/job_remove_shared/'+ str(job['job_id']))}">Remove</a></li>
                                                        %else:
                                                            <li><a class="delete" id="del_${job['job_id']}"href="${h.url('/workbench/job_delete/'+ str(job['job_id']))}">Delete</a></li>
                                                        %endif
                                                    </ul>
                                                </li>
                                            </ul>
                                        </td>


                                </tr>
                            %endif


                        % endfor
                    %endif
                </tbody>
            </table>

        </div>
    </div>

