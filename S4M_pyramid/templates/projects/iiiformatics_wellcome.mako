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
    Wellcome Trust Centre for Molecular Parasitology - 3IIIformatics - Glasgow University
                </div>
                <div class="text">
                <p>
The Wellcome Trust Centre for Molecular Parasitology (WTCMP) is a research Centre aiming to make a large impact on parasitic diseases by gaining understanding of basic processes in parasites and exploiting them to develop new approaches to disease control.
                </p>
                <p>
                </p>
                </div>                       
                <p>
                <ul>
                    <li>
                        <a target = "_blank" href="${h.url('/datasets/search?filter=iii_wellcome')}">View Datasets associated with WTCMP</a>
                    </li>
                </ul>
                </p>
 
            </div>        
        </div>
    </div>
</div>

