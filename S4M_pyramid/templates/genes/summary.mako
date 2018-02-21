<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js','/js/external_asset_dependencies/d3-3.5.5.min.js')}"></script>
    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3-tip/0.6.3/d3-tip.min.js','/js/external_asset_dependencies/d3-tip-0.6.3.min.js')}"></script>

    <script type="text/javascript" src="${h.url('/js/genes/summary.js')}"  ></script>
    <script type="text/javascript" src="${h.url('/js/expressions/biojs-vis-yugene-graph.js')}"  ></script>


    <link type="text/css" href="${h.web_asset_url('/css/expressions/biojs-vis-yugene-graph.css')}" rel="stylesheet" />

    <script type="text/javascript" src="${h.url('/js/expressions/biojs-vis-summary-horizontal-bar-graph.js')}"  ></script>

    <link type="text/css" href="${h.web_asset_url('/css/genes/gene_info.css')}" rel="stylesheet" />

    <link type="text/css" href="${h.web_asset_url('/css/genes/summary.css')}" rel="stylesheet" />
</%def>
<%def name="show_all_option()">
</%def>


    <div class="content">


        <div id="ensemblID" class="hidden">${c.ensemblID}</div>
        <div id="symbol" class="hidden">${c.symbol}</div>
        <div id="db_id" style="display:none">${c.db_id}</div>
        <% species = c.species_dict[c.db_id]['name'] %>

        ${Base.pre_enclosed_search_box()}
        <%
        text.title = "Gene Search for YuGene"
        text.help = "Enter Symbol or Ensembl IDs for more precise results. It will provide suggestions via an autocomplete after four characters."
        text.input_id = "geneSearch"
        text.search_button_id = "viewGenes"
        text.search_action ='#'
        text.search_value = c.symbol
        text.input_class = ""
        %>
        ${Base.enclosed_search_box(text,self.show_all_option)}
        <div class="clear">

        <div id=overallGraphDiv>
            <div id="graphingOptions">

                <div class="clear"></div>
                <div class="yugeneTitle">
                    <div class="innerDiv"><div id="title" class="hidden">Yugene Interactive Graph for ${species} ${c.symbol}</div>
                                    </div>
                </div>

                <ul class="buttonMenus">
                    <!--
                     <li id="zoomMenu">
                        <a id="reset" class="button plain"><span class="icon glass"></span>Zoom Original</a>
                    </li>
                    -->
                     <li id="exportMenu">
                        <a class="button dropdown"><span><span class="icon go"></span>Export & Share</span><span class="arrow down"></span></a>
                        <ul class="submenu">
                            <!-- <li><a href="${h.url('/genes/download_yugene?gene='+str(c.ensemblID)+'&db_id='+str(c.db_id))}" >Export Yugene Graph Data</a></li> -->
                            <li><a href="#" id="exportTableCSVButton">Export Gene Summary</a></li>
                            <li><a data-type="svg" href="#" data-id="yugene_graph" class="export_d3_button">Export Graph As SVG</a></li>
                            <li><a data-type="pdf" href="#" data-id="yugene_graph" class="export_d3_button">Export Graph As PDF</a></li>
                            <li><a data-type="png" href="#" data-id="yugene_graph" class="export_d3_button">Export Graph As PNG</a></li>
                            <li><a data-type="svg" href="#" data-id="sample_summary" class="export_d3_button">Export Summary As SVG</a></li>
                            <li><a data-type="pdf" href="#" data-id="sample_summary" class="export_d3_button">Export Summary As PDF</a></li>
                            <li><a data-type="png" href="#" data-id="sample_summary" class="export_d3_button">Export Summary As PNG</a></li>
                            <li><a href="#" id="share_link">Share Yugene Interactive Graph</a></li>
                        </ul>
                    </li>
                    <li id="viewMenu">
                        <a class="button dropdown"><span><span class="icon bargraph"></span>View</span><span class="arrow down"></span></a>
                        <ul class="submenu">
                            <li><a href="${h.url(str('/expressions/result?graphType=box&gene='+c.ensemblID+'&db_id='+str(c.db_id)))}" >Gene Expression Graph: choose one dataset</a></li>
                        %if c.user:
                            <li><a href="${h.url(str('/expressions/multi_dataset_result?graphType=box&gene='+c.ensemblID+'&db_id='+str(c.db_id)))}" >Multiview Expression Graph: compare 9 datasets</a></li>
                        % endif
                        </ul>
                    </li>
                    ${Base.genomeMenu()}
                    <!--
                    <li id="new_ds_id">
                        <a  class="button"><span><span class="icon info"></span>New DS_ID</span><span class="arrow right"></span></a>
                    </li>
                    -->
                    <li id="infoMenu">
                        <a  class="button"><span><span class="icon info"></span>Info</span><span class="arrow right"></span></a>
                    </li>
                    <li id="helpMenu">
                        <a href="#" class="button help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a>
                        <!-- <a href="${h.url('/contents/site_features_gene_summary')}" class="button help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> -->
                    </li>
                </ul>
                <div id="yugene_value_start" class="hidden"></div>
                <div id="yugene_value_end" class="hidden"></div>
            </div>

            <div id="yugene_graph"></div>
                <div id="sample_breakdown_div">
                <select id="sample_breakdown" name="">
                    <option value="count">Order by Count</option>
                    <option value="coverage">Order by Coverage</option>
                </select>
              </div>

            <div id="sample_summary">  </div>
            <div class="height16px"></div>
       </div>

        <div class="clear"></div>
        ${Base.displayGeneDetail()}

        <% aliases = c.data[c.ensemblID]['Synonyms'] %>

        <div id="downloadData" class="hidden">
            <table id="downloadGeneSearch" class="hidden">
                <tr class="headers">
                    <th class="symbolColumn">Symbol</th>
                    <th class="descriptionColumn">Description</th>
                    <th class="descriptionColumn">Entrez Gene ID</th>
                    <th class="descriptionColumn">Ensembl ID</th>
                    <th class="descriptionColumn">Aliases</th>
                </tr>
                <tr>
                    <td class="symbolColumn">${c.symbol}</td>
                    <td class="descriptionColumn">${c.data[c.ensemblID]['description'].replace('<br />','')}</td>
                    <td class="descriptionColumn">${c.data[c.ensemblID]['EntrezID']}</td>
                    <td class="descriptionColumn">${c.ensemblID}</td>
                    <td class="descriptionColumn">${aliases}</td>
                </tr>
            </table>
        </div>

        <div class="clear"></div>



    </div>

    <div id="displayHelpDetail" class="showDetail showHelp searchDiv hidden modalInnerDiv" >
        <div class="innerDiv ">
            <div class='title'>Help Introduction</div>
            <div class="modalInnerDiv smallPadding smallWindow orangeBorder">
                The Yugene Interactive graph allows you to compare the stem cell gene expressions across all the ${c.site_name} datasets for a particular gene.
            </div>
            <div class='smallTitle largeMarginTop smallMarginBottom'>Samples</div>
            <div class="smallWindow ">
                The lines at the top are the samples arranged by order using a cumulative proportion. The lines at the bottom denote the different datasets that these samples belong to.
                You can hover your mouse over the graph to find out information about that sample.
            </div>
            <div class='smallTitle largeMarginTop smallMarginBottom'>Interactive Graph</div>
            <div class="smallWindow ">
                You can zoom in and  you can also click to view the Gene Expression Graph of any interesting sample that you see.
                To zoom in, simply click and drag a selection in the white space horizontally. To get back to the original size, simply click the Esc key or click on the Zoom Original button.
            </div>
        </div>
        <div class="clear"></div>
    </div>
</div>

<form id="svgform" method="post" action="${h.url('/main/export_d3')}">
 <input type="hidden" id="output_format" name="output_format" value="">
 <input type="hidden" id="file_name" name="file_name" value="">
 <input type="hidden" id="data" name="data" value="">
</form>
