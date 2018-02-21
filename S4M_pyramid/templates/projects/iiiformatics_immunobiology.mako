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
    Immunobiology - 3IIIformatics - Glasgow University
                </div>
                <div class="text">
                <p>
Immunology research within the Institute of Infection, Immunity and Inflammation incorporates interests ranging from the very basic scientific analysis of immune and inflammatory processes, through translational efforts, to more focused clinical studies. We believe that this combination of interests provides a seamless ‘pipeline’ allowing our research to progress efficiently from ‘bench to bedside’ and this is an important aspect of our research philosophy.
                </p>
                <p>
                </p>
                <p>
                <ul>
                    <li>
                        <a target = "_blank" href="${h.url('/datasets/search?filter=iii_immunobiology')}">View Datasets associated with Immunology</a>
                    </li>
                </ul>
                </p>
                </div>        
            </div>        
        </div>
    </div>
</div>

