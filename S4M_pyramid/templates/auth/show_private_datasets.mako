<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/jobs_index.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/js/workbench/jobs_index.js')}" >
    <script type="text/javascript" src="${h.url('/js/admin/config_index.js')}"></script>
</%def>

    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Show Private Dataset Privileges
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                The private datasets that you have been granted specific group or user access to are shown.
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>
            </div>
            <table id="chooseDatasetTable">
                <thead>
                    <tr>
                    <th class="long">ID</th>
                    <th class="long">Title</th>
                    <th class="long">Handle</th>
                    <th class="long">Species</th>
                    <th class="long">Dataset status</th>
                    <th class="long">Access Type</th>
                    <th class="extra_long">Privileges</th>
                    </tr>
                </thead>
                <tbody>

                % if c.user_datasets:
                    % for dset in c.user_datasets:
                            <tr>
                            <td>${dset}</td>
                            <td>
                                ${c.user_datasets[dset]["Title"]}
                            </td>
                            <td>
                                ${c.user_datasets[dset]["handle"]}
                            </td>
                            <td>
                                ${c.user_datasets[dset]["Organism"]}
                            </td>
                            <td>
                                % if c.user_datasets[dset]["private"] == False:
                                    Public
                                % else:
                                    Private
                                % endif
                            </td>
                            <td>
                                ${c.user_datasets[dset]["permissions"]}
                            </td>
                            <td>
                                % if c.user_datasets[dset]["status"] == "annotator":
                                    <div class="sidebyside">
                                        <a href=${h.url(str("/datasets/search?ds_id="
                                            + str(dset)))} >View</a>

                                    % if c.user_datasets[dset]["private"] != False:
                                        -
                                        <a href=${h.url(str("/admin/annotate_dataset?ds_id="
                                        + str(dset)))}  >Annotate</a>
                                    % else:
                                        - Annotated
                                    % endif
                                    </div>
                                % else:
                                    <a href=${h.url(str("/datasets/search?ds_id=" + str(dset)))} />View</a>
                                % endif
                            </td>
                        </tr>
                    % endfor
                % endif
                </tbody>
            </table>
        </div>
    </div>
