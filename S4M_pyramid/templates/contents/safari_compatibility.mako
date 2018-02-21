<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    <link href="${h.url('/css/contents/privacy_policy.css')}" type="text/css" rel="stylesheet"> 
    <link href="${h.url('/css/sass/stylesheets/screen.css')}" type="text/css" rel="stylesheet"> 
</%def>


<div class="content">
    <div class="content_left_column">
        ${Base.content_menu(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column">
        <div class="content_box">
            <div class="header_1">
This is the Safari Compatibility page.
            </div>
            <div class="text">
<p>Unfortunately, we can no longer continue to support Safari 5 and 6 due to a security issue with these browsers. It is recommended that this browser should not be used to access secure websites. As of the start of 2015, about 1.31% of the traffic to ${c.site_name} has been Safari 6.</p><p>However, Safari 7 and above, the latest Google Chrome and up to date Mozilla Firefox are 100% supported. Google Chrome and Mozilla Firefox are also free.</p>
<p>You can download Firefox for free at <a class="underline large" target = "_blank" href="http://www.mozilla.org/">Mozilla.org</a>. </p><p>You can download Google Chrome for free at <a class="large underline" target="_blank" href="http://www.google.com/chrome">Google.com</a>.</p>
<p>We apologise for any inconvenience this may cause.<p>

            </div>
        </div>

    </div>
</div>


