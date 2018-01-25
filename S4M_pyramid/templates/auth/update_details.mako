<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/auth/auth_default.css')}" >
</%def>


    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            ${Base.wb_breadcrumbs()}


            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                My Account
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>Update your account details or password here.</p>
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>



            <div id=form class=tables>
                <div class="innerDiv">
                    <div class="title">Update Your Account</div>
                    <form action="${h.url('/auth/update_details')}" method="post">
                      <dl>
                        % if c.error_message != "":
                            <dt><div class="error_message" style="font-size:16px">${c.error_message}</div></dt> <dd></dd>
                        % else:
                            <dt>${c.error_message}</dt> <dd></dd>
                        % endif
                        <dt>${c.this_user.username}</dt> <dd><input type="hidden" name="update" value="1"></dd>

                        <dt>Full Name:</dt>
                        <dd><input type="text" name="name" value="${c.this_user.full_name.strip()}"></dd>
                        <dt>Organisational Affiliation:</dt>
                        <dd><input type="text" name="organisation" value="${c.this_user.organisation.strip()}"></dd>
                        <dt>Allow general email notifications:</dt>
                        <dd>
                            <input type="checkbox" name="send_email_marketing"
                                %if c.this_user.send_email_marketing:
                                    checked
                                %endif
                            >
                        </dd>
                        <dt>Allow emails on job completion:</dt>
                        <dd>
                            <input type="checkbox" name="send_email_job_notifications"
                                %if c.this_user.send_email_job_notifications:
                                    checked
                                %endif
                            >
                        </dd>


                        <dt>Leave pass phrases blank to keep current pass phrase</dt><dd></dd>
                        <dt>Pass phrase:</dt>
                        <dd><input type="password" name="password" value="" autocomplete="off"></dd>
                        <dt>Confirm pass phrase:</dt>
                        <dd><input type="password" name="password_confirm" value="" autocomplete="off"></dd>
                      </dl>

                      % if c.guest_username != c.this_user.username:
                      <input type="submit" name="authform" value="Update" />
                      % endif
                      <div class="clear"></div>
                    </form>
                </div>
            </div>
        </div>
    </div>
