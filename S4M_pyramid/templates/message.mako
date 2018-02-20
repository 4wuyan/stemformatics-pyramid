<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link href="${h.url('/css/contents/error.css')}" type="text/css" rel="stylesheet"> 
</%def>
    ${Base.links()}  
    <div class="rightColumn">

        <div class="mainTextColumn">
            <div id="errorText">
                
                <div id=message><h1>Message</h1></div>
                <div id=prompt>
                    ${c.message}
                </div>
            </div>
           
            
        </div>
       
    </div>
