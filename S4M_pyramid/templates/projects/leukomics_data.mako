<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
</%def>

<%
    landing_page_name = "LEUKomics"
%>
<style>
.abstract { width: 600px; }
</style>
<div class="content iiiformatics">
    <div class="content_left_column">
        ${Base.content_menu_leukomics(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column ">
        <div class="box display">
            <div id="introduction" class="content_box">
                <a id="introduction"></a>
                <div class="header_1">
                LEUKomics
                </div>
                <div class="text">
                <img class="abstract" src="/images/leukomics/leukomics_graphical_abstract.png"></img>
                <p>
The ${landing_page_name} datasets detail gene expression in sample types relating to key areas of modern CML research. The data are fully implemented into the ${c.site_name} platform for visualization and analysis with the user-friendly bioinformatics and graphing tools. Use the links below to browse all the datasets, or to narrow down your search to your area of interest.
<ul style="list-style: none;">
<li>All LEUKomics datasets:
  <p>
    <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics')}">View Datasets associated with ${landing_page_name}</a>
  </p>
</li>
</ul>
<ol>
<li>Clinical parameters:
    <p>
      Clinically relevant patient groups such as aggressiveness of disease and response to treatment
    </p>
    <p>
      <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics:clinical parameters')}">View associated Datasets</a>
    </p>
</li>
<li>CML and normal haematopoietic cells:
  <p>
    Human stem and progenitor cells from CML patients and non-leukaemic individuals
  </p>
  <p>
     <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics:CML and normal haematopoietic cells')}">View associated Datasets</a>
  </p>
</li>
<li>Disease stage:
  <p>
    Chronic, accelerated and blast phases of CML
  </p>
  <p>
     <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics:disease stage')}">View associated Datasets</a>
  </p>
</li>
<li>Drug treatments:
  <p>
    Treatment of patients, mouse models and cells with drugs such as tyrosine kinase inhibitors
  </p>
  <p>
     <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics:drug treatments')}">View associated Datasets</a>
  </p>
</li>
<li>Mouse models:
  <p>
    Stem and progenitor cells from mouse models of CML
  </p>
  <p>
     <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics:mouse models')}">View associated Datasets</a>
  </p>
</li>
</ol>
<ul style="list-style: none;">
<li>Other:
  <p>
    Variables out with the above groups
  </p>
  <p>
     <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics:other')}">View associated Datasets</a>
  </p>
</li>
</ul>
                </p>
                <p>
The search buttons above may be used to filter the datasets by these categories. We are continuously updating to include more datasets, but if there is one in particular you would like to see here let us know. If you would like to host a dataset privately for comparison with the publicly available data you may do so through the dataset request page.
                </p>
                <p>
                <ul>
                    <li>
                        <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics')}">View Datasets associated with ${landing_page_name}</a>
                    </li>
                    <li>
                        <a target = "_blank" href="${h.url('/main/suggest_dataset')}">Suggest Datasets for ${landing_page_name}</a>
                    </li>
                </ul>
                </p>
                </div>
            </div>
        </div>
    </div>
</div>
