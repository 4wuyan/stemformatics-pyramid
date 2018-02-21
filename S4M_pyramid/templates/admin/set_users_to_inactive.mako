<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">   
</%def>


    <div id="wb_background" class="wb_background_divs">    
        
        <div id="form" class="tables">
            <div class="innerDiv">
                <div class="title">Please Enter in a list of emails to be made inactive.</div> 
                <div class="sign_in">
                    <form action="${h.url('/admin/set_users_to_inactive')}" method="post"> 
                      <dl> 
                        <dt>List of emails:</dt> 
                        <dd><textarea name="string_of_usernames" style="width:400px;height:200px;">${c.string_of_usernames}</textarea></dd> 
                            
                      </dl> 
                      
                      <INPUT TYPE="submit" value="Submit">


                      <div class="clear"></div>
                    </form>
                </div>
                <div class="clear"></div>
            </div>
            
        </div>
    </div>
    
    ${c.result}

    
