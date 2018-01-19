<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/auth/history.js')}"></script>
    <link rel="stylesheet" type="text/css" href="${h.url('/css/auth/auth_default.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/auth/history.css')}" >
</%def>



    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">


            ${Base.wb_breadcrumbs()}


            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Show History
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>Your recent site history is displayed here. This is useful if you'd like to return to a particular analysis or feature, or to keep a record of how you arrived at a particular result.</p>
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>


            <ul class="buttonMenus">
                <li id="exportMenu">
                    <a class="button dropdown"><span><span class="icon go"></span>Export</span><span class="arrow down"></span></a>
                    <ul class="submenu">
                        <li><a href="#" id="exportTableCSVButton">Export History</a></li>
                    </ul>
                </li>
            </ul>
            <div class="height12px"></div>
            <table id="pageHistoryTable">
                <tr>
                    <th class="name">Page Title <a class="clear_history" href="${h.url('/auth/history/clear')}">(Clear History)</a></th>
                </tr>

                % if c.page_history == []:
                    <tr><td style="text-align:center;"> No history. </td>
                % else:
                    % for page in c.page_history:
                        % if page['title'] != c.site_name:
                        <tr>
                            <td>
                                <a href="${h.url(str(page['path']))}" />${page['title']}</a>
                            </td>

                        </tr>
                        % endif

                    % endfor
                % endif

            </table>



            <div class="hidden">

                <table class="display" id="downloadPageHistoryTable">
                    <tr>
                        <th>Page Title</th>
                        <th>URL</th>
                    </tr>

                    % if c.page_history == []:
                        <tr><td> No history.</td>
                    % else:
                        % for page in c.page_history:
                            % if page['title'] != c.site_name:
                            <tr>
                                <td>${page['title']}</td>
                                <td>http://${request.environ['HTTP_HOST']}${h.url(str(page['path']))}</td>
                            </tr>
                            % endif

                        % endfor
                    % endif

                </table>
            </div>
        </div>
    </div>
