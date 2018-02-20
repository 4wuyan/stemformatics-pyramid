<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link href="${h.url('/css/contents/privacy_policy.css')}" type="text/css" rel="stylesheet"> 
    <link href="${h.url('/css/contents/glossary.css')}" type="text/css" rel="stylesheet"> 
</%def>


    <!-- links on the leftColumn -->
    ${Base.links()}  
    
    
    <div class="rightColumn">
        <div id="rotating-item-wrapper"  class="imageRotation">
            <div class="rotating-item">
                <img class="large" src="${h.url('/images/contents/ST_Header_Glossary.jpg')}">
                
            </div>
            
            
        </div>
        <div class="mainTextColumn">
            <div class="introductionText">
                
                <!-- <h1>Coming soon</h1> -->
                Sorry, the glossary is not yet populated. Perhaps in the meantime, you'd like to know <a href="http://www.stemcellcentre.edu.au/For_the_Public/FactSheets.aspx" target="_blank">more about stem cells?</a>
            </div>
           
            
        </div>
       
    </div>
