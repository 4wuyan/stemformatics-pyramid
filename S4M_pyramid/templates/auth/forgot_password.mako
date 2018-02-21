<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
</%def>


    <div id="wb_background" class="wb_background_divs">

        <div id=form>
            <div class="innerDiv modal display">
                <div class="title">Forgot pass phrase</div>
                <div class="error_message ${'hidden' if c.error_message == "" else ''}">${c.error_message}</div>
                <form action="${h.url('/auth/forgot_password')}" method="post">
                  <dl>
                    <dt>Email address (used as your username):</dt>
                    <dd><input type="text" name="username" value="${c.username}"></dd>
                    % if hasattr(c,'recaptcha'):
                    <dt>${c.recaptcha}</dt>
                    % endif
                  </dl>
                  <input type="submit" name="authform" value="Submit" />
                  <div class="clear"></div>
                </form>
            </div>
        </div>
    </div>

    <div class="hidden" id="show_help_flag">NO</div>

    <!-- <div class="hidden" id="show_help_flag"></div> -->
    <!-- <div class="hidden" id="help_flag_message">Pass phrase is 15 characters with at least one space</div> -->
    <!-- <div class="hidden" id="help_flag_top_position">300px</div>  -->
    <!-- <div class="hidden" id="help_flag_left_position">482px</div> -->
