<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link href="${h.url('/css/workbench/analysis_confirmation_message.css')}" type="text/css" rel="stylesheet">

</%def>

    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            <div id="confirmText">
                <div id="confirmText_inner_div">
                    <div id=message>${c.title}</div>
                    <div id=prompt> ${c.message.split('|')[0]}
                    <% temp = c.message.split('|') %>
                    %if len(temp) == 2:
                        <%
                            url = temp[1].split(':')[0]
                            text = temp[1].split(':')[1]
                        %>
                        <a id=extra_link href="${url}">${text}</a>
                    %endif
                    </div>
                    <div class="clear"></div>
                </div>
                <div class="clear"></div>
            </div>
            <div class="clear"></div>

        </div>
        <div class="clear"></div>

    </div>
    <div class="hidden" id="show_help_flag">NO</div>


