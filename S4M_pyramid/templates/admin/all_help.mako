<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<% import urllib %>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/admin/all_help.css')}" >
    <script type="text/javascript" src="${h.url('/js/admin/all_help.js')}"></script>
</%def>
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            <div class="hidden" id="show_help_flag">NO</div>
            
            <div class="innerDiv"><div class="title">Help List</div></div>
            
            <div>
                <ul class="buttonMenus main">
                    <li class="newMenu">
                        <a class="button dropdown"><span>New</span><span class="arrow down"></span></a>
                        <ul class="submenu">
                            <li><a href="${h.url('/admin/edit_tutorial')}">Tutorial</a></li>
                            <li><a href="${h.url('/admin/edit_pageguide')}">Page Guide</a></li>
                       </ul>
                    </li>
                    <li class="dumpMenu">
                        <a class="button dropdown"><span>Help Dump</span><span class="arrow down"></span></a>
                        <ul class="submenu">
                            <li><a class="download" href="${h.url('/admin/download_help_dump')}">Download</a></li>
                            <li><a class="upload" href="#">Upload</a></li>
                            <li><a href="#">--------------</a></li>
                            <li><a class="delete_all" href="${h.url('/admin/delete_all_help')}">Delete All Help</a></li>
                       </ul>
                    </li>
                </ul>
            </div>
            
            <div class="clear"></div>
            
            <table>
                <thead>
                    <tr>
                        <th class="long">Tutorials</th>
                        <th class="long">Action</th>
                    </tr>
                </thead>
                <tbody>
                        %for tutorial_name in c.help_list["tutorials"]: 
                            <tr>
                                <td>${tutorial_name}</td>
                                <td class="action">
                                    <ul class="buttonMenus">
                                        <li class="actionMenu">
                                            <a class="button dropdown"><span>Actions .....</span><span class="arrow down"></span></a>
                                            <ul class="submenu">
                                                <li><a href="${h.url('/admin/edit_tutorial?name='+ tutorial_name)}">Edit</a></li>
                                                <li><a href="${h.url('/admin/delete_tutorial?name='+ tutorial_name)}">Delete</a></li>
                                           </ul>
                                        </li>
                                    </ul>
                                </td>
                            </tr>
                        %endfor
                        %if not c.help_list["tutorials"]:
                            <tr>
                                <td colspan="2"><em>none</em></td>
                            </tr>
                        %endif
                </tbody>
            </table>
            
            <table>
                <thead>
                    <tr>
                        <th class="long">Page Guides</th>
                        <th class="long">Action</th>
                    </tr>
                </thead>
                <tbody>
                        %for page_name in c.help_list["page_guides"]: 
                            <tr>
                                <td>${page_name}</td>
                                <td class="action">
                                    <ul class="buttonMenus">
                                        <li class="actionMenu">
                                            <a class="button dropdown"><span>Actions .....</span><span class="arrow down"></span></a>
                                            <ul class="submenu">
                                                <li><a href="${h.url('/admin/edit_pageguide?page='+ page_name )}">Edit</a></li>
                                                <li><a href="${h.url('/admin/delete_pageguide?page='+ page_name )}">Delete</a></li>
                                           </ul>
                                        </li>
                                    </ul>
                                </td>
                            </tr>
                        %endfor
                        %if not c.help_list["page_guides"]:
                            <tr>
                                <td colspan="2"><em>none</em></td>
                            </tr>
                        %endif
                </tbody>
            </table>
        
        </div>
    </div>
    
    <div id="upload_help_modal" class="modal simplemodal-data">
        <div id="wb_modal_title" class="wb_modal_title">
            Upload Help Data
        </div>
        <div id="wb_modal_content" class="wb_modal_content">
            <div class="save-error"></div>
            <form id="upload_help_form" action="${h.url('/admin/upload_help_dump')}" method="post" enctype="multipart/form-data">
                <input id="helpdump" type="file" name="helpdump"/>
                <input class="button" type="submit" value="Upload!"/>
            </form>
        </div>
    </div>
    
