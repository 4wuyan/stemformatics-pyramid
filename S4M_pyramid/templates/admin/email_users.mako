<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/admin/email_users.css')}" >
</%def>
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            <div class="hidden" id="show_help_flag">NO</div>
            
            <div class="innerDiv"><div class="title">${c.title}</div></div>
            
            <form id="send-email-form" action="${h.url('/admin/email_users')}" method="post">
                
                    <div class="input-row">
                        <div class="label-col"><label for="name">Send to Group:</label></div>
                        <div class="input-col">
                            <select name="group">
                                <option value="all">All users</option>
                                <option value="checked">Users with allow email checked</option>
                            </select>
                        </div>
                    </div>
                    <div class="input-row">
                        <div class="label-col"><label for="subject">Subject: </label></div>
                        <div class="input-col">
                            <input type="text" name="subject" value="${c.subject}"/>
                        </div>
                    </div>
                    <div class="input-row">
                        <div class="label-col"><label for="message">Message: </label></div>
                        <div class="input-col">
                            <p>Hi there,</p>
                            <p><textarea name="message">${c.message}</textarea></p>
                            <p>Regards,<br/>
                               ${c.site_name} Team
                            </p>
                        </div>
                    </div>
                    <div class="input-row">
                        <div class="label-col"></div>
                        <div class="input-col">
                            <ul class="buttonMenus">
                                <li class="send">
                                    <a class="button plain" onclick="$('#send-email-form').submit();"><span>Send</span></a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    
            </form>
        
        </div>
    </div>
    