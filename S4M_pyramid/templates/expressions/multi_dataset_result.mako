<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">

    <script src="${h.external_dependency_url('cdn.jsdelivr.net/kineticjs/4.5.4/kinetic.min.js','/js/external_asset_dependencies/kinetic-4.5.4.min.js')}"  ></script>
    <script src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js','/js/external_asset_dependencies/d3-3.5.5.min.js')}"></script>
    <script src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3-tip/0.6.3/d3-tip.min.js','/js/external_asset_dependencies/d3-tip-0.6.3.min.js')}"></script>

    % if c.production != 'true' or c.debug is not None:
        <script type="text/javascript" src="${h.url('/js/expressions/gene_expression_graph_triggers.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/gene_expression_graphs.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/box_bar_line.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/axis.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/general.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/features.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/test.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph_data_scatter.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph_data_box_bar.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph_data_violin.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph_data_line.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/biojs-vis-scatter-plot.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/biojs-vis-box-bar-plot.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/biojs-vis-line-plot.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/biojs-vis-violin-plot.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph_multi_view.js')}"  ></script>
    % else:
        <script type="text/javascript" src="${h.url('/js/expressions/geg.min.js')}"  ></script>
        <!-- call to graph_data files should always be precedded by call to biojs files for graphs to work  -->
        <script type="text/javascript" src="${h.url('/js/expressions/graph_data.min.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/helper.min.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/biojs.min.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/expressions/graph_multi_view_min.js')}"  ></script>
    % endif

    <script type="text/javascript" src="${h.url('/js/md5-min.js')}"  ></script>

    <link type="text/css" href="${h.url('/css/genes/gene_info.css')}" rel="stylesheet" />
    <link type="text/css" href="${h.url('/css/expressions/multi_dataset_result.css')}" rel="stylesheet" />


</%def>
<div id="mult_dataset_graph_header">

    <a id="multiChooseDatasets" class="chooseDatasetsButton" href="${c.base_url}&amp;force_choose=yes" ><span>CHANGE DATASETS</span><img src="${h.url('/images/show_genes.png')}"/></a>

   ${Base.pre_enclosed_search_box()}
   <%
        text.search_action ='#'
        text.search_value = c.symbol
        text.input_id = 'geneSearch'
        text.input_class = 'mv'
   %>

    ${Base.search_box(text)}


    <div class='graphControls'>
        <div id=graphingOptions>
            <div class=hidden>
               <div id="multi_view_datasets" class="hidden">${c.multi_view_datasets}</div>
               <div id="ensemblID" class="hidden">${c.ensemblID}</div>
               <div id="db_id" class="hidden">${c.db_id}</div>
               <div id="symbol" class="hidden">${c.symbol}</div>
            </div>
       </div>

       <div class="height12px"></div>
           <div class=innerDiv><div class="title">Multiview Expression Graph for ${c.symbol} </div></div>
    </div>


</div>


<div id="blanket" style="display:none;"></div>
<div id="modalDiv" style="display:none;">
    <div id = "simplemodal-container">
    <a onclick="open_modal('modalDiv','close')" id="close-button" class="modalCloseImg simplemodal-close" style="visibility:visible" title="Close"></a>
    </div>
</div>

<div id="last_clicked_ds_id"></div>
<div id=overallGraphDiv style="width:90vw;">
  <div id=sortBy class="hidden">Sample Type</div>

  <div class=clear></div>

  <% count = 0 %>

 % for str_ds_id in c.multi_view_datasets:
       <% ds_id = int(str_ds_id) %>
       <% menu_id = "menu_"+str(str_ds_id) %>
       %if count % 3 == 0:
       <% row_value = "row_" + str(count) %>
       <% cursor_value = "cursor_" + str(count) %>
          %if count != 0:
                <div onclick="show_rows(${cursor_value})" id=${cursor_value} class="show_row_div"><a class="show_rows" >SHOW NEXT ROW</a></div>
          %endif
          <div id= ${row_value}>
       %endif
       <% count+= 1 %>

           <div class="content" id="content${ds_id}">
           <div id=ensemblID${ds_id} class="hidden">${c.ensemblID}</div>
           <div id=dataset${ds_id} style="height:40px;width:30vw"></div>
           <div id=${menu_id} class="menudiv" style="display:none" >
             <ul class="buttonMenus" >
                 <div id=chip_type class="hidden">${c.chip_type[ds_id]}</div>
                 <%
                     probe_name = c.view_data[ds_id]['probeName']
                 %>
                 <div id="probe_name_${ds_id}" class="hidden">${probe_name}</div>
                 <li id="exportMenu" class="exportMenu">
                     <a class="button dropdown"><span><span class="icon go"></span>Export &amp; Share</span><span class="arrow down"></span></a>
                     <ul class="submenu">
                         <li><a href="#" class="export_graph_data" data-id="${ds_id}">Export Graph Data</a></li>
                         <li><a data-type="svg" href="#" data-id="#graph${ds_id}" class="exportImageButton">Export Graph As SVG</a></li>
                         <li><a data-type="pdf"  href="#" data-id="#graph${ds_id}" class="exportImageButton">Export Graph As PDF</a></li>
                         <li><a data-type="png"  href="#" data-id="#graph${ds_id}" class="exportImageButton">Export Graph As PNG</a></li>
                         <li><a href="#" data-id="${ds_id}" id="share_link" class="share_link">Share</a></li>
                     </ul>
                 </li>
                  <li id="graphOptionsMenu" class="graphOptionsMenu">
                     <a class="button dropdown"><span><span class="icon eye"></span>Graph Options</span><span class="arrow down"></span></a>
                     <ul class="submenu">
                         <li><a href="#" class=chooseGraphType data-id="${ds_id}" clickChoose=box >Choose Boxplot Graph</a></li>
                         <li><a href="#" class=chooseGraphType data-id="${ds_id}" clickChoose=bar >Choose Bar Graph</a></li>
                         <li><a href="#" class=chooseGraphType data-id="${ds_id}" clickChoose=scatter >Choose Scatter Graph</a></li>
                         <li><a href="#" data-ds_id=${ds_id} class="no_set_min_y_axis_link" >Toggle Automatic Minimum Y axis</a></li>
                         <li class=chooseSD ><a href="#" class="toggle_sd" data-ds_id=${ds_id} id=toggleSD >Toggle Standard Deviation</a></li>
                     </ul>
                 </li>
                 <li id="analysisMenu" class="analysisMenu">
                     <a class="button dropdown"><span><span class="icon glass"></span>Analysis</span><span class="arrow down"></span></a>
                     <ul class="submenu">
                         <li><a id="YugeneButton" href="${h.url('/genes/summary?gene='+ str(c.view_data[ds_id]['ensemblID'])+'&db_id='+str(c.db_id))}" >Yugene Interactive Graph: all datasets</a></li>
                     % if c.uid and c.view_data[ds_id]['ref_type'] == 'ensemblID' and c.dataset_status == "Available":
                             % if c.allow_genePattern_analysis:
                                 <li><a id="geneNeighbourhoodButton" href="${h.url('/workbench/gene_neighbour_wizard?datasetID='+ str(c.view_data[ds_id]['ds_id']) + '&gene='+ str(c.view_data[ds_id]['ensemblID']))}" >Gene Neighbourhood: find similar expression profiles</a></li>
                           % endif
                             <li><a id="foldChangeViewerButton"  href="${h.url('/workbench/fold_change_viewer_wizard?datasetID='+ str(c.view_data[ds_id]['ds_id']) + '&gene='+ str(c.view_data[ds_id]['ensemblID']))}" >Fold Change Viewer</a></li>

                     % endif
                     </ul>
             % if c.view_data[ds_id]['ref_type'] == 'ensemblID':
                 ${Base.genomeMenu()}
             %endif
             % if c.view_data[ds_id]['ref_type'] == 'ensemblID':
                 <li id="infoMenu" class="infoMenu">
                     <a class="geneInfoButton button"><span><span class="icon info"></span>Information</span><span class="arrow right"></span></a>
                 </li>
             % endif
                 <li id="helpMenu" class="helpMenu">
                     <a href="#" class="button helpPopup"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a>
                 </li>
             </ul>
           </div>
          <div id="graphDiv_${ds_id}"></div>
          <div class=clear></div>
          <div class=clear></div>
          <div class=clear></div>
          %if count % 3 == 0:
            </div>
          %endif
       </div>

 % endfor

 ${Base.displayGeneDetail()}

</div>

<form id="svgform" method="post" action="${h.url('/main/export_d3')}">
 <input type="hidden" id="output_format" name="output_format" value="">
 <input type="hidden" id="file_name" name="file_name" value="">
 <input type="hidden" id="data" name="data" value="">
</form>
