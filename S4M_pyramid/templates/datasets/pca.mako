<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <!-- Every biojs graph has a biojs-vis-graph_name.js which download files using d3.tsv and create options object
         garph_data_graphname.js which use that downloaded data and have functions specific to graph such as create scatter or tooltip
         general_graphname.js which will have generic function such as legend and set up svg /graph div -->
    <script type="text/javascript" src="${h.web_asset_url('/js/datasets/graph_data_pca.js')}"></script>
    <script type="text/javascript" src="${h.web_asset_url('/js/datasets/pca-general.js')}"></script>
    <link href="${h.url('/css/datasets/biojs-vis-pca.css')}" type="text/css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script>
  <script type="text/javascript" src="${h.external_dependency_url('ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js','/js/external_asset_dependencies/jquery-3.2.1.min.js')}"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3-tip/0.6.3/d3-tip.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery-csv/0.8.3/jquery.csv.min.js">  </script>
</%def>
<div class="title">${c.title} PCA Graph</div>
</br>
<div class="content">
  <div class="hidden" id="ds_id">${c.ds_id} </div>
  <div class="hidden" id="pca_type">${c.pca_type} </div>
</div>
<div id="button_div">
  <input type="text" id="sample" placeholder="Sample ID">
  <select  id="change_pca" class="button">
    % for pca in c.all_pca_types:
      <option value="${pca}" id= "${pca}">${pca} PCA Plot</option>
    % endfor
  </select>
  <button type="button" id="show_sample" class="button">Show Sample</button>
</div>
<div id="graphDiv">

</div>

<script type="text/javascript" src="${h.web_asset_url('/js/datasets/biojs-vis-pca-plot.js')}"></script>
