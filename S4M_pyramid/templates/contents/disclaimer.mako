<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link href="${h.url('/css/contents/privacy_policy.css')}" type="text/css" rel="stylesheet">
</%def>


    <!-- links on the leftColumn -->
   <div class="content">
    <div class="content_left_column">
        ${Base.content_menu('disclaimer')}
    </div>
    <div class="content_right_column">
        <div class="content_box">
            <div class="header_1">
                ${c.site_name} provides links to other Internet sites only for the
                convenience of internet users.
            </div>
            <div class="text">
                <p>
                ${c.site_name} is not responsible for the availability or content of
                these external sites, nor do we endorse, warrant or guarantee the
                products, services or information described or offered at these other
                Internet sites.
                </p>
                <p>
                It is not the intention of ${c.site_name} to provide specific medical
                advice, but rather to provide users with information. No specific
                medical advice is provided on the website, and ${c.site_name} urges
                users to seek the services of qualified medical practitioners for any
                personal health concerns. Information obtained here is not intended to
                take the place of proper medical advice from a fully qualified health
                professional.
                </p>
                <p>
                The views and opinions of authors expressed on ${c.site_name} websites
                do not necessarily state or reflect those of the contributing
                organisations, and they may not be used for advertising or product
                endorsement purposes without the author's explicit written permission
                </p>
            </div>
        </div>

    </div>
</div>



