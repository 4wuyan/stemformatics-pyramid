<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
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
    3IIIformatics - Glasgow University
                </div>
                <div class="text">
                <p>
Infectious, autoimmune and inflammatory diseases place an enormous global burden on human and animal health. The Institute of Infection, Immunity and Inflammation comprises scientists and clinicians working together to promote and develop research, drug discovery and ultimately improvements in patient care in this area of critical international importance.
                </p>
                <p>
The 3IIIformatics resource provides a collaborative hub for researchers interested in comparing systems-scale datasets from experimental series addressing host responses to acute infection, inflammation, tolerance, chronic infection and chronic inflammatory disease. Data collections for programmes on Rheumatoid Arthritis; Molecular Parasitology and Immunobiology can be accessed from the main dataset page (<a href="${h.url('/datasets/search')}">link</a>) or from the side-bar menu on this page.
                </p>
                <p>
                <ul>
                    <li>
                        <a target = "_blank" href="${h.url('/datasets/search?filter=iii_main')}">View Datasets associated with 3IIIformatics</a>
                    </li>
                </ul>
                </p>
                </div>        
            </div>        
        </div>
    </div>
</div>

