<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
</%def>


    <div id="wb_background" class="wb_background_divs">

        <div id="form" class="tables">
            <div class="innerDiv">
                <div class="title">Please Sign In</div>
                <div class="error_message ${'hidden' if c.error_message == "" else ''}">${c.error_message}</div>
                <div class="sign_in">
                    <form action="${h.url('/auth/submit')}" method="post">
                      <dl>
                        <dt>Username/Email address:</dt>
                        <dd><input type="text" name="username" value="${c.username}"></dd>
                        <dt>Pass phrase:</dt>
                        <dd><input type="password" name="password"></dd>
                        <dt>Stay signed in:</dt>
                        <dd><input type="checkbox" name="stay_signed_in" checked></dd>

                      </dl>

                      <INPUT TYPE="submit" value="Submit">

                      <a href="${h.url('/auth/register')}">Register an account now</a>
                      <a href="${h.url('/auth/forgot_password')}">Reset your pass phrase here</a>

                      <div class="clear"></div>
                    </form>
                </div>
                <div id="register">
                        <% hover_text = "The guest account allows you to automatically sign in as a public user. This allows you to do analyses but it is public. If you want to keep your analyses private, please register for free." %>
                    ${Base.large_icon('analyses','user_logo','Guest Account','Click for automatic sign in',hover_text,h.url('/auth/guest'))}
                </div>
                <div class="clear"></div>
            </div>

        </div>
    </div>

    <!-- <div class="hidden" id="show_help_flag"></div> -->
    <div class="hidden" id="help_flag_message">No account? Please register below the sign in button</div>
    <div class="hidden" id="help_flag_top_position">295px</div>
    <div class="hidden" id="help_flag_left_position">512px</div>



