<%inherit file="/default.html"/>\
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
        % else:
            <!-- call to graph_data files should always be precedded by call to biojs files for graphs to work  -->
            <script type="text/javascript" src="${h.web_asset_url('/js/expressions/graph_data.min.js')}"  ></script>
            <script type="text/javascript" src="${h.web_asset_url('/js/expressions/helper.min.js')}"  ></script>
            <script type="text/javascript" src="${h.web_asset_url('/js/expressions/biojs.min.js')}"  ></script>
        % endif

        <script src="//cdn.jsdelivr.net/alertifyjs/1.8.0/alertify.min.js"></script>
        <link rel="stylesheet" href="//cdn.jsdelivr.net/alertifyjs/1.8.0/css/alertify.min.css"/>

        <script type="text/javascript" src="${h.web_asset_url('/js/expressions/graph_new.js')}"  ></script>

        <script type="text/javascript" src="${h.web_asset_url('/js/md5-min.js')}"  ></script>
        <link type="text/css" href="${h.web_asset_url('/css/genes/search.css')}" rel="stylesheet" />
        <link type="text/css" href="${h.web_asset_url('/css/expressions/result.css')}" rel="stylesheet" />
        <link type="text/css" href="${h.web_asset_url('/css/genes/gene_info.css')}" rel="stylesheet" />
</%def>
<%
    probe_name = c.probe_name
%>

<div class="hidden" id="probe_name">${probe_name}</div>
<div class="content">
        <div id="db_id" class="hidden">${c.db_id}</div>
	      <div id="ref_id" class="hidden">${c.ref_id}</div>
        <div id="choose_dataset_immediately" class="hidden">${c.choose_dataset_immediately}</div>
        <div id="ds_id" class="hidden">${c.ds_id}</div>
        <div id="chip_type" class="hidden">${c.chip_type}</div>
        <div id="ref_type" class="hidden">${c.ref_type}</div>
        <div id="sortBy" class="hidden">${c.sortBy}</div>
        <div id="symbol" class="hidden">${c.symbol}</div>
        <div id="graphType" class="hidden">${c.graphType}</div>
        <div id="select_probe" class="hidden">${c.select_probes}</div>
        <div id="url" class="hidden">${c.url}</div>
</div>

% if c.ref_type == 'gene_set_id':
<div id="gene_set_name" class="hidden">${c.gene_set_name}</div>
%endif

% if c.ref_type == 'ensemblID':
       <div class="breadcrumbs" id="breadcrumb"><a class="basic_link" href="${h.url('/genes/search')}">Gene Search</a> >> <a class="basic_link" id="searchGene" href="${h.url('/genes/search?gene=')}${c.symbol}">${c.symbol}</a> >> <a class="basic_link" href="${h.url('/genes/summary?gene=')}${c.ref_id}&db_id=${c.db_id}">${c.symbol} Summary</a> >> <a class="basic_link" href="${h.url('/datasets/search')}">Dataset Browser </a>>> <a class="basic_link" href="${h.url('/datasets/summary?datasetID=')}${c.ds_id}"> Summary</a> >> <span class="current">Expression Results</span></div>
%else:
       ${Base.wb_breadcrumbs()}
%endif


    <div class="backgroundGraph" style="background-color:#FFFFFF;border:none">
        <div class="innerDiv">
            <div class="innerBackgroundGraph">
                <div class="innerDiv" id="white_background_control">
                      <div class='graphControls'>
                            <a id="chooseDatasets" class="chooseDatasetsButton" href="${request.url.replace('result?','choose_dataset?')}" ><span>CHANGE DATASETS</span><img src="${h.url('/images/show_genes.png')}"/></a>
                             % if c.ref_type == 'gene_set_id':
                                   <a id="chooseGeneList" class="chooseDatasetsButton" href="${h.url('/workbench/histogram_wizard?datasetID='+str(c.ds_id))}" ><span>CHANGE GENE LIST</span><img src="${h.url('/images/show_genes.png')}"/></a>

                             %endif

                             <div id=datasetSelectDiv> </div>
                             ${Base.pre_enclosed_search_box()}
                             %if c.ref_type == 'ensemblID':
                                 <%
                                      text.search_action ='#'
                                      text.input_id = 'geneSearch'
                                      text.search_value = c.symbol
                                      text.input_class = 'geg'
                                 %>
                               ${Base.search_box(text)}
                             %endif
                             %if c.ref_type == 'probeID':
                                 <%
                                      text.search_action ='#'
                                      text.input_id = 'probeSearch'
                                      text.search_value = c.ref_id
                                      text.input_class = 'geg'
                                 %>
                               ${Base.search_box(text)}
                             %endif
                             %if c.ref_type == 'miRNA':
                                 <%
                                      text.search_action ='#'
                                      text.input_id = 'featureSearch'
                                      text.search_value = c.ref_id
                                      text.input_class = 'geg'
                                 %>
                               ${Base.search_box(text)}
                            %endif

                            <div class="clear"></div>
                               <ul class="buttonMenus">
                                   <li id="exportMenu">
                                       <a class="button dropdown"><span><span class="icon go"></span>Export &amp; Share</span><span class="arrow down"></span></a>
                                       <ul class="submenu">
                                           <li><a href="#" data-id="${c.ds_id}" class="export_graph_data">Export Graph Data</a></li>
                                           <li><a data-type="svg" href="#" data-id="#graph" class="exportImageButton">Export Graph As SVG</a></li>
                                           <li><a data-type="pdf" href="#" data-id="#graph" class="exportImageButton">Export Graph As PDF</a></li>
                                           <li><a data-type="png" href="#" data-id="#graph" class="exportImageButton">Export Graph As PNG</a></li>
                                           <li><a href="#" id="share_link">Share</a></li>
                                       </ul>
                                   </li>
                                   <li id="graphOptionsMenu">
                                        <a class="button dropdown"><span><span class="icon eye"></span>Graph Options</span><span class="arrow down"></span></a>
                                        <ul class="submenu">
                                          % if 'box' in c.list_of_valid_graphs:
                                          <li><a href="#" class=chooseGraphType clickChoose=box >Choose Boxplot Graph</a></li>
                                          % endif
                                          % if 'bar' in c.list_of_valid_graphs:
                                          <li><a href="#" class=chooseGraphType clickChoose=bar >Choose Bar Graph</a></li>
                                          % endif
                                          % if 'scatter' in c.list_of_valid_graphs:
                                          <li><a href="#" class=chooseGraphType clickChoose=scatter >Choose Scatter Graph</a></li>
                                          % endif
                                          % if 'violin' in c.list_of_valid_graphs:
                                          <li><a href="#" class=chooseGraphType clickChoose=violin >Choose Violin Graph</a></li>
                                          % endif
                                          % if 'line' in c.list_of_valid_graphs:
                                              <li><a href="#" class=chooseGraphType clickChoose=line >Choose Line Graph</a></li>
                                          % endif
                                          <li><a href="#" id="zoomHorizontalGraphButton">Toggle Expand Graph Horizontally</a></li>
                                          <li><a href="#" id="no_set_min_y_axis_link" >Toggle Automatic Minimum Y axis</a></li>
                                          <li class="chooseSD" id="chooseSD"><a href="#" id="toggleSD" >Toggle Standard Deviation</a></li>
                                          <li class="toggle_select_probes" ><a href="#" id="toggle_select_probes" >Toggle Select ${probe_name}</a></li>
                                          <li id="showScatterDiv"><a href="#" id="showScatter" >Toggle scatter</a></li>
                                        </ul>
                                    </li>
                                    <li id="analysisMenu">
                                          <a class="button dropdown"><span><span class="icon glass"></span>Analysis</span><span class="arrow down"></span></a>
                                          <ul class="submenu">
                                              <li><a href="${h.url('/datasets/search?ds_id='+str(c.ds_id))}" >Dataset Summary Information</a></li>
                                          % if c.ref_type != 'gene_set_id':
                                              % if c.ref_type == 'ensemblID':
                                              <li><a id="YugeneButton" href="${h.url('/genes/summary?gene='+ str(c.ref_id)+'&db_id='+str(c.db_id))}" >Yugene Interactive Graph: all datasets</a></li>
                                              <li><a target="_blank" href="${c.innate_db_object.get_single_gene_url(c.ref_id)}" >Innate DB Gene Information</a></li>
                                              <li><a target="_blank" href="${c.string_db_object.get_single_gene_url(c.ref_id)}" >String DB Gene Information</a></li>
                                              %endif
                                          %else:
                                              <li><a href="${h.url('/workbench/gene_set_view/'+str(c.ref_id))}" >Gene List Information</a></li>
                                              <li><a id="hc" href="${h.url('/workbench/hierarchical_cluster_wizard?gene_set_id='+str(c.ref_id)+'&datasetID='+str(c.ds_id))}" >Hierarchical Cluster using the Gene List</a></li>
                                              %if c.select_probes is not None:
                                              <li><a id="hc" href="${h.url('/workbench/hierarchical_cluster_wizard?select_probes='+str(c.select_probes)+'&datasetID='+str(c.ds_id))}" >Hierarchical Cluster using selected probes</a></li>
                                              %endif
                                              <li><a id="gla" href="${h.url('/workbench/gene_set_annotation_wizard?gene_set_id='+str(c.ref_id))}" >Gene List Annotation</a></li>

                                          %endif
                                          % if c.uid and c.ref_type == 'ensemblID':
                                              <li><a id="multiviewButton" href="${h.url('/expressions/multi_dataset_result?graphType=scatter&gene='+ str(c.ref_id)+'&db_id='+str(c.db_id))}" >Multiview Expression Graph: view 4 datasets</a></li>

                                          % endif
                                          % if c.uid and c.ref_type == 'ensemblID' and c.dataset_status == "Available":
                                                  % if c.allow_genePattern_analysis:
                                                      <li><a id="geneNeighbourhoodButton" href="${h.url('/workbench/gene_neighbour_wizard?datasetID='+ str(c.ds_id) + '&gene='+ str(c.ref_id)+'&db_id='+str(c.db_id))}" >Gene Neighbourhood: find similar expression profiles</a></li>
                                                % endif
                                                  <li><a id="foldChangeViewerButton"  href="${h.url('/workbench/fold_change_viewer_wizard?datasetID='+ str(c.ds_id) + '&gene='+ str(c.ref_id)+'&db_id='+str(c.db_id))}" >Fold Change Viewer</a></li>

                                          % endif
                                          </ul>
                                    </li>
                                    % if c.ref_type == 'ensemblID':
                                        ${Base.genomeMenu()}
                                    %endif
                                    % if c.ref_type == 'ensemblID':
                                        <li id="infoMenu">
                                            <a class="geneInfoButton button"><span><span class="icon info"></span>Information</span><span class="arrow right"></span></a>
                                        </li>
                                    % endif
                                        <li id="helpMenu">
                                            <a href="#" class="button helpPopup"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a>
                                        </li>
                                  </ul>

                      </div>
                  </div>
             </div>
        </div>
     </div>



<div id="notification" class="notification">
  <div class="notification-title">
  </div>
 </div>
<div class="displayGraphs">
<div id="graphDiv">

</div>
</div>
</div>

<div class="multi_select">
    <div class="title">Select dataset</div>
    <div class="basic_help">Select a dataset to view</div>
     <%

        url_link = "&datasetID=" if c.url.find('?') != -1 else "?datasetID="

        # strip out any datasetID values in the url
        import re
        expression='\&datasetID=[0-9]+'
        clean_url = re.sub(expression,'',c.url)

        expression='\?datasetID=[0-9]+\&'
        clean_url = re.sub(expression,'?',clean_url)
        url = clean_url+url_link
    %>

    ${Base.choose_datasets_table(c.datasets,url)}
</div>

<form id="svgform" method="post" action="${h.url('/main/export_d3')}">
 <input type="hidden" id="output_format" name="output_format" value="">
 <input type="hidden" id="file_name" name="file_name" value="">
 <input type="hidden" id="data" name="data" value="">
</form>

<div id="export-wrapper"><div id="export-graph"></div></div>
    % if c.ref_type == 'ensemblID':
        ${Base.displayGeneDetail()}
    %endif
