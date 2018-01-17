<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/auth/auth_default.css')}" >
</%def>



        <div id="wb_background" class="wb_background_divs">

            <div id="form" class="modal display">
                <div class="innerDiv">

                    <div class="title">Please Register</div>
                    <div class="error_message ${'hidden' if c.error_message == "" else ''}">${c.error_message}</div>
                    <div class="sign_in">
                        <form action="${h.url('/auth/register')}" method="post">
                          <dl>
                            <dt>Email address (used as your username):</dt>
                            <dd><input type="text" name="username" value="${c.username}"></dd>
                            <dt>Full Name:</dt>
                            <dd><input type="text" name="name" value="${c.name}"></dd>
                            <dt>Organisational Affiliation:</dt>
                            <dd><input type="text" name="organisation" value="${c.org}"></dd>
                            <dt>Allow general email notifications:</dt>
                            <dd><input type="checkbox" name="send_email_marketing" checked></dd>
                            <dt>Allow emails on job completion:</dt>
                            <dd><input type="checkbox" name="send_email_job_notifications" checked></dd>

                            <dt>Pass phrase*:</dt>
                            <dd><input type="password" name="password"></dd>
                            <dt>Confirm pass phrase:</dt>
                            <dd><input type="password" name="password_confirm"></dd>
                            % if hasattr(c,'recaptcha'):
                            <dt>${c.recaptcha}</dt>
                            % endif

                          </dl>
                          <input type="submit" name="authform" value="Register" />
                          <div class="clear"></div>
                            <div class="innerDiv limit_register">* <small>${config['validation_warning']}</small></div>
                        </form>
                    </div>
                    <div id="register">
                        <% hover_text = "The guest account allows you to automatically sign in as a public user. This allows you to do analyses but it is public. If you want to keep your analyses private, please register for free." %>
                        ${Base.large_icon('analyses','ucsc_logo','Guest Account','Click for automatic sign in',hover_text,h.url('/auth/guest'))}
                    </div>
                    <div class="clear"></div>
                </div>

            </div>
        </div>
