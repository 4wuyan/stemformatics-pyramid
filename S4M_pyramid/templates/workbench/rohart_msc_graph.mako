<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link type="text/css" href="${h.url('/css/genes/search.css')}" rel="stylesheet" />
    <link type="text/css" href="${h.url('/css/expressions/result.css')}" rel="stylesheet" />
    <link type="text/css" href="${h.url('/css/genes/gene_info.css')}" rel="stylesheet" />


    % if c.production != 'true' or c.debug is not None:
        <script type="text/javascript" src="${h.url('/js/msc_signature/rohart_msc_test.js')}"  ></script>
        <script type="text/javascript" src="${h.url('/js/msc_signature/rohart_msc_graph.js')}"  ></script>
    %else:
        <script type="text/javascript" src="${h.url('/js/msc_signature/rohart_msc_test_min.js')}"></script>
    %endif


    <script type="text/javascript" src="${h.url('/js/landing_pages.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/expressions/geg.min.js')}"  ></script>
    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js','/js/external_asset_dependencies/d3-3.5.5.min.js')}"></script>
    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3-tip/0.6.3/d3-tip.min.js','/js/external_asset_dependencies/d3-tip-0.6.3.min.js')}"></script>
    <script>
        $(document).ready(function() {
            base_url = BASE_PATH+"workbench/rohart_msc_graph";
            filter_dict = {'rohart_msc_test':true};
            set_view_datasets(base_url,filter_dict);

            contextHelpClick(); // from main.js

            // set the position of div.graphControls
            background_graph_left = $('div.backgroundGraph').offset().top;
            $('div.graphControls').attr('left',background_graph_left - 140);
        });
    </script>

</%def>



<div class="content landing_page_analysis">
    <div class="baseMarginLeft" >
        <div id="ds_id" class="hidden">${c.ds_id}</div>
        <div id="dataset_details" class="hidden">${c.dataset_json}</div>

        <div class="clear"></div>
        <%def name="show_all_option()"> </%def>
        ${Base.pre_enclosed_search_box()}
        <% text.title = "Choose a dataset to score with the Rohart MSC test" %>
        ${Base.setup_dataset_search_box_variables()}
        ${Base.enclosed_search_box(text,self.show_all_option)}

        <div class='graphControls' style="position:absolute;top:330px;left:0px;">
                <ul class="buttonMenus no_margin_top" >

                    <li id="exportMenu">
                        <a class="button dropdown"><span><span class="icon go"></span>Export &amp; Share</span><span class="arrow down"></span></a>
                        <ul class="submenu">
                            <!-- <li><a href="#" target="${c.ds_id}" class="export_graph_data">Export Graph Data</a></li> -->
                            <!-- EPS using imagemagick was 137MB!!!! <li><a data-type="eps" href="#" class="export_d3_button">Export Graph As EPS</a></li> -->
                            <li><a data-type="svg" href="#" class="export_d3_button">Export Graph As SVG</a></li>
                            <li><a data-type="pdf" href="#" class="export_d3_button">Export Graph As PDF</a></li>
                            <li><a data-type="png" href="#" class="export_d3_button">Export Graph As PNG</a></li>
                            <!-- <li><a href="#" id="share_link">Share</a></li>  -->
                        </ul>
                    </li>
                    <li id="infoMenu">
                        <a href="${h.url('/datasets/summary?ds_id=')}${c.ds_id}" class="dataset_info_button button" target="_blank"><span><span class="icon info"></span>Dataset Summary</span><span class="arrow right"></span></a>
                        <a href="#" id="show_data_table" class="show_data_table button"><span><span class="icon info"></span>Graph Data</span><span class="arrow right"></span></a>
                    </li>
                   <li id="helpMenu">
                        <a href="#" class="button helpPopup"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a>
                    </li>
                </ul>

         </div>


        <!-- This is where the graph starts -->
        <div class="clear">




            <div class='backgroundGraph'>
                <div class="innerDiv">

                    <div class="innerBackgroundGraph">
                        <div class="" id="white_background_control">



                            <div class="clear"></div>
                          </div>
                        <div class="clear"></div>
                    </div>
                </div>
                <div class="clear"></div>
                <div class='displayGraphs loading'>
                    <div class="innerDiv">
                        <div id="graph" class="graph">
                        </div>
                    </div>
                    <div class=clear></div>
                </div>
                <div class=clear></div>
            </div>
        </div>

    </div>

</div>

<form id="svgform" method="post" action="${h.url('/main/export_d3')}">
 <input type="hidden" id="output_format" name="output_format" value="">
 <input type="hidden" id="file_name" name="file_name" value="">
 <input type="hidden" id="data" name="data" value="">
</form>
