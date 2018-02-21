<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
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
This is the ${c.site_name} Browser Compatibility page.
            </div>
            <div class="text">
<p>Unfortunately, we can no longer continue to support Safari 5 and 6, Internet Explorer 6,7,8,9 and 10, Firefox versions 33 and below and Google Chrome versions 38 and below.</p>

<p>All of these browsers have default security options that are too low and therefore they have been removed from the list of browsers that ${c.site_name} supports.</p>

<p>However, Internet Explorer 11+, Safari 7+  and the latest Google Chrome and up to date Mozilla Firefox are 100% supported. Google Chrome and Mozilla Firefox are also free.</p>


<p>You can download Firefox for free at <a class="underline large" target = "_blank" href="http://www.mozilla.org/">Mozilla.org</a>. </p><p>You can download Google Chrome for free at <a class="large underline" target="_blank" href="http://www.google.com/chrome">Google.com</a>.</p>
<p>We apologise for any inconvenience this may cause.<p>

            </div>
        </div>

    </div>
</div>
