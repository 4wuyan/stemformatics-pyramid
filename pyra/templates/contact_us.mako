<%inherit file="default.html"/>\
<%namespace name="Base" file="base.mako"/>
<%def name="includes()">
    <link href="${h.web_asset_url('/css/sass/stylesheets/screen.css')}" rel="stylesheet">
</%def>


<div class="content">
    <div class="content_left_column">
        ${Base.content_menu(None)}
    </div>

    <div class="content_right_column">
        <div class="content_box">
            <div class="header_1">
${c.site_name} prides itself on being responsive
            </div>
            <div class="text">
<p>
Please do not hesitate to contact us with your enquiries in relation to expession data requests, protocol and biostats information or any other requests. We will endeavour to respond in a timely fashion. Thanks for your interest in ${c.site_name}!
</p>
            </div>
        </div>
        <div class="content_box">
            <a id="contact_us"></a>
            <div class="header_2">
                Contact Us
            </div>
            <div class="text">
                <table class="margin_top_small invisible_table" >
                <tr>
                    <td>Email:</td>
                    <td>${c.feedback_email}</td>
                </tr>
                <tr>
                    <td>Address:</td>
                    <td>30 Royal Parade, Kenneth Myer Building (144)<br/> University of Melbourne, Parkville, Victoria</td>
                </tr>
                </table>
            
            </div>
        </div>
        <div class="content_box">
            <a id="suggest"></a>
            <div class="header_2">
                Suggest a Dataset 
            </div>
            <div class="text">
                
                <p>You can suggest a dataset that goes straight into our dataset queue, Agile_org.
                <ul><li>
                    <a target="_blank" href="/main/suggest_dataset">Click here to go to Agile_org to add a new dataset</a>
                </ul></li>
                </p>
            </div>
        </div>
 
    </div>
</div>


