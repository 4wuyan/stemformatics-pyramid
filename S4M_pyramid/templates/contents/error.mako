<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link href="${h.url('/css/contents/error.css')}" type="text/css" rel="stylesheet">
</%def>

        <div class="errorTextColumn">
            <div id="errorText" class="title">
                <div id=message>404 Not Found.<br/><br/> The resource could not be found</div>
                <div id=prompt>The page you are looking for cannot be found or has an error. It might have been removed, had its name changed, or be temporarily unavailable.
                    <br><br>
                    Please try the following:
                    <br><br>
                    - If you typed the page address in the Address bar, check the spelling and use of upper-case and lower-case letters.
                    <br><br>
                    - Click the Back button on your browser to try another link.
                    <br><br>
                    - Go to the Home page and look for links to the information you want
                </div>
            </div>
        </div>

