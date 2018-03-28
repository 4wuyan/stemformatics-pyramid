<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
<script type="text/javascript" src="${h.url('/js/projects/iiiformatics.js')}"></script>
</%def>





<div class="content iiiformatics">
    <div class="content_left_column">
        ${Base.content_menu_iii(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column ">
        <div class="box display">
            <div id="introduction" class="content_box">
                <a id="introduction"></a>
                <div class="header_1">
    Arthritis Research UK Rheumatoid Arthritis Pathogenesis Centre of Excellence - 3IIIformatics - Glasgow University
                </div>
                <div class="text">
                <p>
The Centre aims to find out more about the causes of rheumatoid arthritis. Rheumatoid arthritis develops when environmental factors interact in people with a geneticially predisposed immune system to somehow cause arthritis. Why this happens and especially why the joint is attacked is very uncertain. 
                </p>
                <p>
                </p>
                <p>
                <ul>
                    <li>
                        <a target = "_blank" href="${h.url('/datasets/search?filter=iii_arthritis')}">View Datasets associated with Rheumatoid Arthritis Pathogenesis Centre of Excellence</a>
                    </li>
                </ul>
                </p>
  </div>        
            </div>        
        </div>
    </div>
</div>

