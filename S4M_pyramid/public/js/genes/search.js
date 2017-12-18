var AUTOCOMPLETE_TIMEOUT = 5000,
    GRAPH_TIMEOUT = 10000;
    module = {};// setup module as an object so that the biojs will work

var $graph = $('div.preview div.graph'),
    $loading = $('div.preview div.loading'),
    $noData = $('div.preview div.noData'),
    $graphContainer = $('div.preview div.graphContainer');



/* Extracting the data from the csv files for use in the graph
 *  * Also sets relevent options based on the data passed in (for example
 *   * calculating the min and max values of the graph */
function run_biojs_yugene_graph(graph_id,ensembl_id,db_id,filters){

    // this is to get the filtered datasets as well as the rest
    filters_json = JSON.stringify(filters);
    data_url= '/expressions/return_yugene_filtered_graph_data?gene='+ensembl_id+'&db_id='+db_id+'&format_type=tsv&filters='+filters_json;


    d3.tsv(data_url,function (error,data){

        max = 1;  // YuGene is between 1 and 0
        min = 0;
        number_of_increments = 2;
        count = 0;

        data.forEach(function(d){

            d.chip_type = +d.chip_type;
            d.ds_id = +d.ds_id;
            d.x_position = +d.x_position;
            d.yugene_value = +d.yugene_value;

        });

        title = "";
        target = graph_id;

        width = 300;
        height = 200;
        if (filters != null){
            ds_id_array = filters['ds_ids'];
        } else {
            ds_id_array = Array();
        } 
        var options = {
            initial_padding: 10,
            background_colour: "white",
            background_stroke_colour:  "black",
            background_stroke_width:  "2px",
            ds_id_array: ds_id_array,
            data: data,
            fill_area_colour:"#C8C8C8",
            height: height,
            horizontal_grid_lines: width,
            legend_class: "legend",
            increment: number_of_increments,
            legend_range: [0,100],
            line_stroke_width: "2px",
            margin_legend: width - 190,
            margin:{top: 20, left:60, bottom: 40, right: 0},
            padding: 40,
            setup_brush: false,
            target: target,
            title: title,
            title_class: "title",
            tip: tip,//second tip to just display the sample type
            tooltip: tooltip, // using d3-tips
            watermark:false, // or put in the URL
            width: width,
            x_axis_text_angle:-45,
            x_axis_title: "Samples",
            x_column: 'x_position',
            y_axis_title: "YuGene Value",
            y_column: 'yugene_value'
        }

        var new_instance = biojsvisyugenegraph(options);

        // Get the d3js SVG element
        var tmp = document.getElementById(graph_id);
        //var svg = tmp.getElementsByTagName("svg")[0];
        // Extract the data as SVG text string
        //var svg_xml = (new XMLSerializer).serializeToString(svg);


        
    });
}




$(document).ready(function() {

    ensembl_id = $('#ensembl_id').html();
    db_id = $('#db_id').html()
    graph_id = '#yugene_graph';
    filters = null;


    base_url = BASE_PATH+"genes/search";
    filter_dict = {};
    search_button_id = "#viewGenes";
    input_text_field_id = "#geneSearch";
    data_type = "genes"; 
    set_search_and_choose(base_url,filter_dict,search_button_id,input_text_field_id,data_type);





    var search = $('#geneSearch').val();   
    var ensembl_id = $('#ensembl_id').html();   
    if (search != '' && ensembl_id == '') {
            data_type = 'genes';
            base_url = BASE_PATH+data_type+"/search"; 
            ajax_url =BASE_PATH + data_type + "/search_and_choose_"+data_type+"_ajax" 

            var options = {
                base_url: base_url,
                data_type: data_type,
                ajax_url: ajax_url
            }

            var this_ajax_search = ajax_search(options);
            filter = search;
            filter_dict = {};
            filter_dict['filter'] = filter;
            this_ajax_search.get_data_from_ajax(filter_dict);

    } 
    if (ensembl_id != ''){
        run_biojs_yugene_graph(graph_id,ensembl_id,db_id,filters);
    }



    var $graph = $('div.preview div.graph'),
        $loading = $('div.preview div.loading'),
        $noData = $('div.preview div.noData'),
        $graphContainer = $('div.preview div.graphContainer');
    
    $('#geneSearch').focus();
    set_clicks();    
    gene_and_feature_search_actions();

   
    $noData.hide();
    
    $('#geneResults').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 1, "asc" ]],
        "aoColumns": [{"bSortable": false}, null, null],
        "bAutoWidth": false
    });
    
    var show_selections = $('#show_selections').html();
    if (show_selections == 'True') {
        show_all_genes();
    }
    
    $('div.show_all_button a').click(function(){ show_all_genes();});

    // make all the buttons open up in another window
    $('div.more_info div.large_icon a').attr("target","_blank");

    $('div.export_more_info a').click(function(){ show_more_info();});




     
});

// T#2372 will need to call ajax instead of showing multi_select (which will be removed)
// T#2372 will have to call set_view_genes(base_url,filter_dict,button_id,input_id);
function show_all_genes(){
    $('.multi_select').modal({minWidth:700,maxHeight:800});
}

function show_more_info(){
    $('.more_info').modal({minWidth:684,minHeight:788});
}

function drawPreviewGraph(graph_values) {
    label_dimensions = set_label_dimensions();            
    plot_yugene_graph(graph_values,'div.graph',label_dimensions,'');
   
    $('div.legend table').hide();
    
    $('div.preview div.graph').append('');
}


function gene_and_feature_search_actions(){

    // removed feature search in T#1822 v5.2

    
    $("#geneSearch").autocomplete({
        source: BASE_PATH + 'genes/get_autocomplete',
        minLength: 4, // because the names are very small eg. STAT1
        timeout: AUTOCOMPLETE_TIMEOUT,
        appendTo: ".search_box",
        select: function(event, ui) {  
            var ensembl_id = ui.item.ensembl_id;
            window.location = BASE_PATH + 'genes/search?ensembl_id='+ensembl_id+'&gene='+ensembl_id;
        }
    }).data("ui-autocomplete")._renderItem = function( ul,item ){
        return $("<li></li>").append("<a> <div class='symbol'>" + item.symbol + "</div><div class='species'>"+item.species+"</div><div class='aliases'>"+item.aliases+"</div><div class='description'>"+item.description+"</div><div class='clear'></div></a>").appendTo(ul);
    };
   
 
}

function set_clicks(){

    contextHelpClick();

   
    $('#geneResults td').click(function(event) {
        
        // prevent event if the click happened on a link
        if ($(event.target).is($(this).parent().find('a'))) {
            return true;
        }
        
        var $checkbox = $(this).parent().find('input:checkbox');
        
        if ($checkbox.length == 1) {
            $('#geneResults input:checkbox').attr('checked', false);
            $checkbox.attr('checked', true);
            
            var symbol    = $checkbox.attr('data-symbol'),
                ensemblID = $checkbox.attr('data-ensemblid'),
                entrezID  = $checkbox.attr('data-entrezid'),
                aliases   = $checkbox.attr('data-aliases'),
                species   = $checkbox.attr('data-species'),
                db_id     = $checkbox.attr('data-dbid');
            
            $graphContainer = $('div.preview div.graphContainer');
            $loading = $('div.preview div.loading');
            $loading.show();
            
            // now get the flot expression details for this gene
            $.ajax({
                url: BASE_PATH + 'expressions/return_gene_search_graph',
                type: 'post',
                dataType: 'json',
                timeout: GRAPH_TIMEOUT,
                data: {geneSearch: ensemblID, db_id: db_id},
                success: function(data) {
                    
                    if (!$.isEmptyObject(data)) {
                        $noData.hide();
                        $graphContainer.show();
                        graph_values = jQuery.parseJSON(data.graph_values); 
                        drawPreviewGraph(graph_values);
                        
                        $graphContainer.click(function(){
                            window.location = BASE_PATH + 'genes/summary?gene='+ensemblID+'&db_id='+db_id;
                        });
                        
                    } else {
                        $graphContainer.hide();
                        $noData.show();
                    }
                    
                    updateGeneDetails(symbol, ensemblID, entrezID, aliases, db_id, species);
                    $loading.hide();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $loading.hide();
                    $graphContainer.hide();
                    $noData.show();
                    
                    if (jqXHR.status === 0){
                    } else if (jqXHR.status === 404){
                    } else if (jqXHR.status === 500){
                    } else if (textStatus === 'parsererror'){
                        console.log("JSON Parse Error");
                    } else if (textStatus === 'timeout'){
                    } else {
                    }
                }
            }); // end of ajax
        }
    }); // end of click event


}

// Still need tip and tooltip for yugene graph
var tip = d3.tip()
    .attr('class', 'd3-tip')
    .html(function(d) {
        temp = '';
        return temp;
    });
var tooltip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([0, +110])
    .html(function(d) {
        temp = '';
       return temp;
    });
        


