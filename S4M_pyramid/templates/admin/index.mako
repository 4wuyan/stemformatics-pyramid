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


            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                        <th class="long">Type</th>
                        <th class="long">Task</th>

                    </tr>
                </thead>
                <tbody>

                        <tr> <td>Reports</td> <td><a href="${h.url('/admin/audit_reports')}">Audit reports</a></td> </tr>
                        <tr> <td>Reports</td> <td><a href="${h.url('/admin/controller_user_audit_report')}">Controller User Audit reports</a></td> </tr>
                        <tr> <td>Reports</td> <td><a href="${h.url('/admin/check_redis_consistency_for_datasets')}">Unsync Datasets Report</a></td> </tr>
                        <tr> <td>Configs</td> <td><a href="${h.url('/admin/config_index')}">All configs from database</a></td> </tr>
                        <tr> <td>Configs</td> <td><a href="${h.url('/admin/trigger_config_update')}">Update configs from database</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/redis_check')}">Check Redis vs DB vs GCT files</a></td> </tr>
                        <tr> <td>User</td> <td><a href="${h.url('/admin/show_dataset_availability')}">Show Dataset Availability</a></td> </tr>
                        <tr> <td>MSC Signature</td> <td><a href="${h.url('/msc_signature/index')}">MSC Signature Home page</a></td> </tr>
                        <tr> <td>Twitter</td> <td><a href="${h.url('/admin/get_raw_twitter_response?force_refresh=false')}">Get reponse values for twitter force refresh false</a></td> </tr>
                        <tr> <td>Twitter</td> <td><a href="${h.url('/admin/get_raw_twitter_response?force_refresh=true')}">Get reponse values for twitter force refresh true</a></td> </tr>
                        <tr> <td>User</td> <td><a href="${h.url('/admin/triggers_for_change_in_user')}">Update redis after user change</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/triggers_for_change_in_dataset')}">Update redis after dataset change</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/setup_cls_files/2000')}">Update cls for dataset (defaults to 2000)</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/update_datasets')}">Update datasets</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/setup_all_sample_metadata')}">Setup all sample metadata for redis</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/annotate_dataset?ds_id=1000')}">Annotate a dataset (defaults to 1000)</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/setup_redis_gct/0')}">Setup gct for redis for a dataset</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/setup_redis_sd')}">Setup Standard Deviation for redis for a dataset</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/setup_new_dataset/0')}">Setup new dataset with redis </a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/setup_redis_cumulative/0')}">Setup yugene for redis for a dataset</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/validation_replicate_group_id/bgc')}">Validate all replicate group ids</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/show_all_user_emails_critical_outage')}">Show All User Emails for a critical outage</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/email_pending_users')}">Email Pending Users</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/show_subscriber_lists')}">Show Subscribers Emails</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/dataset_override_users')}">Show Private Dataset Override Objects</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/add_objects_to_datasets')}">Add Objects to Datasets</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/all_users')}">Show All Users</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/add_users_to_groups_wizard')}">Add Users to Groups</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/all_groups')}">Show All Group Users</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/check_uid_ds_id')}">Check access for a user and a dataset</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/view_add_group')}">View/Add a Group</a></td> </tr>
                        <tr> <td>Jobs</td> <td><a href="${h.url('/api/kill_pending_jobs')}">Kill Pending Jobs</a></td> </tr>
                        <tr> <td>Jobs</td> <td><a href="${h.url('/api/remove_old_jobs')}">Remove Old Jobs</a></td> </tr>
                        <tr> <td>Help</td> <td><a href="${h.url('/contents/speed_test')}">Speed Test</a></td> </tr>
                        <tr> <td>Help</td> <td><a href="${h.url('/admin/help')}">Manage Help Data</a></td> </tr>
                        <tr> <td>Jobs</td> <td><a href="${h.url('/admin/re_run_job?job_id=0')}">Re-run Job</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/email_users')}">Email Users</a></td> </tr>
                        <tr> <td>Genes</td> <td><a href="${h.url('/admin/setup_bulk_import_manager')}">Setup Bulk Import Manager with redis</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/change_user_to_annotator_for_dataset')}">Change Users to be Annotators for a dataset</a></td> </tr>
                        <tr> <td>Log</td> <td><a href="${h.url('/admin/read_logfile?number_of_lines=500')}">Read Logfile</a></td> </tr>
                        <tr> <td>Log</td> <td><a href="${h.url('/admin/check_jar_processes')}">Check Jar job processes running </a></td> </tr>
                        <tr> <td>Log</td> <td><a href="${h.url('/admin/delete_job_files?job_id=0')}">Delete job files from disk</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/add_line_graph?ds_id=0')}">Add Line Graph</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/add_project_banner?ds_id=0')}">Add Project Banner for dataset</a></td> </tr>
                        <tr> <td>MSC Signature</td> <td><a href="${h.url('/admin/add_msc_project?ds_id=0')}">Add MSC Project</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/unsubscribe_users_from_outage_critical_notifications')}">Unsubscribe Users from Outage Critical Notifications (From MailChimp)</a></td> </tr>
                        <tr> <td>Users</td> <td><a href="${h.url('/admin/set_users_to_inactive')}">Set Users to Inactive (From MailChimp)</a></td> </tr>
                        <tr> <td>Log</td> <td><a href="${h.url('/admin/view_resident_memory')}">View Resident Paster Memory</a></td> </tr>
                        <tr> <td>User</td> <td><a href="${h.url('/admin/refresh_base_export_keys')}">Refresh Base Export Keys</a></td> </tr>
                        <tr> <td>Tests</td> <td><a href="${h.url('/admin/run_regression_nosetests')}">Run Regression Nosetests</a></td> </tr>
                        <tr> <td>User</td> <td><a href="${h.url('/admin/login_as_user')}">Login as another user</a></td> </tr>
                        <tr> <td>Feeds</td> <td><a href="${h.url('/main/download_thomson_reuters_xml_file')}">Download Thomson Reuters XML feed</a></td> </tr>
                        <tr> <td>Dataset</td> <td><a href="${h.url('/admin/refresh_probe_mappings_to_download')}">Refresh probe mappings for users to download</a></td> </tr>
                        <tr> <td>Error</td> <td><a href="${h.url('/admin/check_error_response')}">Check error response for debug set to ${config['debug']}</a></td> </tr>
<tr><td>Delete dataset</td><td><a href="${h.url('/admin/delete_dataset/0')}" >Delete Dataset</a></td></tr>
                </tbody>
            </table>

        </div>
    </div>
