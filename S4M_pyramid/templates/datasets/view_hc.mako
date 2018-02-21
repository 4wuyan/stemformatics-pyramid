<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    <link href="${h.url('/css/datasets/view_hc.css')}" type="text/css" rel="stylesheet"> 
</%def>


    <!-- links on the leftColumn -->
    ${Base.links()}  

    <div class="content">
        <h1>Hierarchical Cluster for Dataset ${c.handle}</h1>
        <img class="header" src="${h.url('/images/datasets/')}${c.datasetID}_hc_header.png"><br />
        <img class="body"   src="${h.url('/images/datasets/')}${c.datasetID}_hc_body.png">
    </div>
