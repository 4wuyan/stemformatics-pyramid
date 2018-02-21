<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/admin/edit_help.css')}" >
</%def>
        
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            <div class="hidden" id="show_help_flag">NO</div>
            
            <div class="innerDiv"><div class="title margin_bottom_small">New/Edit ${c.help_type.replace("_","").capitalize()}</div><a class="underline" href="https://docs.google.com/document/d/1n7UCBgaW7ljL4yZR8hT3jJVdawkqscst4r6SqqnyP3U/edit?usp=sharing">Help for the JSON data</a>           </div>  
            <form id="save-json-form" action="${h.url('/admin/save_help')}" method="post" enctype="multipart/form-data">
                
                <input id="helptype" type="hidden" name="helptype" value="${c.help_type}"/>
                <input id="close" type="hidden" name="close" value="true"/>
                
                <div>
                    % if c.help_type == "tutorial":
                        <label for="name">Tutorial Name: </label>
                    % else:
                        <label for="name">Guide Page: </label>
                    % endif
                    <div>
                        <input id="helpname" type="text" name="helpname" value="${c.help_name}"/>
                    </div>
                </div>
                
                % if c.help_type == "tutorial":
                    <div>
                        <label for="name">Start Page: </label>
                        <input id="helpname" type="text" name="startpage" value="${c.start_page}"/>
                    </div>
                % endif
                
                <div>
                    <label for="jsonfile">Upload File: </label>
                    <input id="jsonfile" type="file" name="jsonfile"/>
                </div>
                
                <div>
                    <label for="jsontext">Or Edit JSON: </label>
                    <input id="jsontext" type="hidden" name="jsontext"/>
                    <div id="json-editor">${c.help_json}</div>
                </div>
                
                <ul class="buttonMenus">
                    <li class="cancelMenu">
                        <a class="button plain" href="${h.url('/admin/help')}"><span>Cancel</span></a>
                    </li>
                    <li class="saveMenu">
                        <a class="button plain"><span>Save</span></a>
                    </li>
                    <li class="saveCloseMenu">
                        <a class="button plain"><span>Save &amp; Close</span></a>
                    </li>
                </ul>
                
            </form>
        
        </div>
    </div>
    
    
    <script type="text/javascript" src="${h.url('/js/ace/ace.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/admin/edit_help.js')}"></script>
