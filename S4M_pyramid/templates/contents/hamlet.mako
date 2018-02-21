<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link href="${h.url('/css/contents/privacy_policy.css')}" type="text/css" rel="stylesheet"> 
    <link href="${h.url('/css/contents/publications.css')}" type="text/css" rel="stylesheet"> 
</%def>


    <!-- links on the leftColumn -->
    ${Base.links()}  
    
    
    <div class="rightColumn">
        
        
        <div class="mainTextColumn">
            <div class="introductionText">
                
                <h1>
                    Hamlet - Heat map viewer
                </h1>
                <!-- -->
                <div class="publicationBody">
                    <br/>
                    <a class="nofloat" target="_blank" href="http://hamlet.wehi.edu.au">Hamlet</a> is an online application designed to help analyse datasets, manily by using heatmaps. 
                    It can be used to visualize trends in the data, or cluster the data, for example (see below for a list of main features). 
                    It is primarily targeted at users who are familiar with the data they wish to analyse but may not have experience in programming, hence being unable to take advantage of more advanced tools such as R. 
                    It has been developed by Nick Seidenman and Jarny Choi from the <a class="nofloat" href="http://www.wehi.edu.au/">Walter and Eliza Hall Institute</a> in Melbourne as a way of analysing microarray expression data. 
                    Its development is also supported by the ${c.site_name} project, and the application is currently hosted at QFAB. 
                    The code, which is primarily written in python, is open source. 
                </div>
                <img id="hamlet_image" src= "http://ncascr.griffith.edu.au/heatmap-dev/images/screenshot1.jpg"/>
                <a target="_blank" href="http://hamlet.wehi.edu.au">Link to Hamlet</a>
                
            </div>
        </div>
    </div>
