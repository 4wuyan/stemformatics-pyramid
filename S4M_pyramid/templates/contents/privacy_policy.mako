<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link href="${h.url('/css/sass/stylesheets/screen.css')}" type="text/css" rel="stylesheet">
</%def>


<div class="content">
    <div class="content_left_column">
        ${Base.content_menu(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column">
        <div class="content_box">
            <div class="header_1">
                ${c.site_name}  is subject to the laws governing privacy in
                Australia; the Commonwealth Privacy Act 1988.
            </div>
            <div class="text">
                <p>
                Registered users of ${c.site_name} must provide a valid E-mail address and a password, with
                other information suggested to be provided as well.
                </p>
                <p>
                Any personal information received from visitors to this website will
                be treated as confidential. Your personal contact details will be held
                and used strictly in accordance with the aforementioned privacy
                legislation.
                </p>
                <p>
                While ${c.site_name} will use this information to track usage, we will
                not make membership details available to third parties or pass on any
                personal information to third parties without your permission.
                </p>
                <p>
                Of the information we learn about you from your visit to this website,
                we store only the following: the domain name from which you access the
                internet, the date and time you access our site, the internet address
                of the website from which you direct-linked to our site, information
                regarding the pages within our network which you visit and what you
                click on. This information is used to measure the number of visitors
                to the various sections of our site and to help us make our site more
                useful to visitors. This information is collected by Google Analytics and stored anonymously. Unless it is specifically stated otherwise, no
                additional information will be collected about you. This information
                will not be passed on to any other third party without your permission.
                </p>
                <p>
                When inquiries are emailed to us, we store the question and the email
                address information so that we can respond electronically.
                </p>
                <p>
                Email addresses and other contact information that are provided to
                ${c.site_name} by persons requesting more information or registering
                for training events will be held on a secure internal list. The
                contact list will not be provided to another third party without the
                knowledge and prior consent of the user.
                </p>

            </div>
        </div>
    </div>
</div>


