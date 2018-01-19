<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
</%def>

    <div id="wb_background" class="wb_background_divs">

        <div id=form>
            <div class="innerDiv">
                <div class="title">Please Reset your password.</div>
                <div class="error_message ${'hidden' if c.error_message == "" else ''}">${c.error_message}</div>
                <form action="${h.url('/auth/confirm_new_password/')}${c.id}" method="post">
                  <dl>
                    <dt>${c.username}</dt> <dd></dd>
                    <dt>Pass phrase*:</dt>
                    <dd><input type="password" name="password"></dd>
                    <dt>Confirm pass phrase:</dt>
                    <dd><input type="password" name="password_confirm"></dd>
                  </dl>
                  <input type="submit" name="authform" value="Reset" />
                  <div class="clear"></div>
                </form>
                <div class="innerDiv"> <small>* ${config['validation_warning']}</small></div>
            </div>
        </div>
    </div>
