var graphWidth = 512;
var graphHeight = 376;
var maxYAxis = 20;
var AUTOCOMPLETE_TIMEOUT = 5000;
var graph_values = {};
var view_data = '';
var module = {};// setup module as an object so that the biojs will work


var tip = d3.tip()
    .attr('class', 'd3-tip')
    .html(function(d) {
        sample_type = d.sample_type;
        temp =
            "Sample Type: " +  sample_type + "<br/>"
        return temp;
    });
var tooltip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([0, +110])
    .html(function(d) {
        probe = d.Probe;
        // 2 decimal places on the display only
        Expression_Value = round_to_two_decimal_places(d[y_column]);
        lwr = round_to_two_decimal_places(d.Expression_Value - d.Standard_Deviation);
        upr = round_to_two_decimal_places(d.Expression_Value + d.Standard_Deviation);
        temp =
        "Sample: " + d.sample_id +"<br/>"+
        "Dataset: " + d.ds_id +"<br/>"+
        "YuGene Value: " + Expression_Value +"<br/>"
        // "MSC predicted "+msc_call+"/"+total+" iterations<br/>"
        return temp;
    });




$('body').append('<div id="values" class="hidden"></div>');


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

        title = "Samples ranked by expression";
        target = graph_id;

        width = 900;
        height = 400;
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
            margin:{top: 30, left:100, bottom: 50, right: 0},
            padding: 40,
            setup_brush: true,
            target: target,
            title: title,
            title_class: "title",
            tip: tip,//second tip to just display the sample type
            tooltip: tooltip, // using d3-tips
            watermark:"http://www.stemformatics.org/img/logo.gif",
            width: width,
            x_axis_text_angle:-45,
            x_axis_title: "Samples",
            x_column: 'x_position',
            x_middle_title: 500,
            y_axis_title: "YuGene rank",
            y_column: 'yugene_value'
        }

        var new_instance = biojsvisyugenegraph(options);

        // Get the d3js SVG element
        var tmp = document.getElementById(graph_id);
        //var svg = tmp.getElementsByTagName("svg")[0];
        // Extract the data as SVG text string
        //var svg_xml = (new XMLSerializer).serializeToString(svg);


        get_breakdown_of_filtered_data();

    });
}

// callback to get the filtered data back using ajax
get_breakdown_of_filtered_data = function(){
    // note that start is the lower number

    yugene_value_start = $('#yugene_value_start').html();
    yugene_value_end = $('#yugene_value_end').html();
    ensembl_id = $('#ensemblID').html();
    db_id = $('#db_id').html();
    filters = {filter_value_start:yugene_value_start ,filter_value_end: yugene_value_end};
    filters = JSON.stringify(filters);
    limit_summary = 25;
    height = 1000;
    width = 800;

    // can include 'Cell Type,Tissue,Sample Type,Organism Part,Disease State'
    metadata_list = 'Tissue';
    metadata_list = 'Cell Type';
    metadata_list = 'Generic sample type';
    data_url = '/expressions/return_breakdown_of_yugene_filtered_data?db_id='+db_id+'&gene='+ensembl_id+'&filters='+filters+'&metadata_list='+metadata_list;


    /* Extracting the data from the csv files for use in the graph
     * Also sets relevent options based on the data passed in (for example
     * calculating the min and max values of the graph */
    d3.tsv(data_url,function (error,data_bar_graph){

        data_bar_graph.forEach(function(d){
            // ths + on the front converts it into a number just in case
            d.number = +d.number;
            d.full_count = +d.full_count;
            d.coverage = +d.coverage;
        })
        order_by = $('#sample_breakdown').val();
sort_by_coverage_and_count = function(a,b) {
          return ( ( b["coverage"] )-(a["coverage"] ) || b["number"] - a["number"])
        }

sort_by_count = function(a,b) {
          return ( b["number"] - a["number"])
        }

        // http://stackoverflow.com/a/19326174
        // use slice() to copy the array and not just make a reference
        // this is so that we can sort easily
        sort_by_number = data_bar_graph.slice(0);
        sort_by_number.sort(function(a,b) {
                  if(order_by == "count" || typeof(order_by) =="undefined") {
                    return sort_by_count(a,b);
                  }
                  else {
                    return sort_by_coverage_and_count(a,b);
                  }
        });




        data_bar_graph = Array();
        // now limit the summary

        // if not many breakdowns get returned reduce the size of the limit
        array_length = sort_by_number.length;
        if (array_length < limit_summary){
            limit_summary = array_length;
        }

        for(var i=0; i<limit_summary; i++) {

          data_bar_graph.push(sort_by_number[i]);

        }

        title = "Sample types highlighted in graph (Top "+limit_summary+" terms)";
        target = '#sample_summary';

        horizontal_space_for_labels = 300;
        margin = {top: 80, left:100, bottom: 40, right: 0};
        inner_margin= 10; // margin between the bars and the outer box
        height_margin_for_title = 25;
        line_height = 20;
        line_y_adjustment = 7;

        //The main options for the graph
        var options = {
            initial_padding: 10,
            background_colour: "white",
            background_stroke_colour:  "black",
            background_stroke_width:  "2px",
            data: data_bar_graph,
            gap_between_groups: 5,
            height: height,
            order_by : order_by,
            max_length_of_generic_sample_type: 63,
            height_margin_for_title : height_margin_for_title,
            horizontal_space_for_labels: horizontal_space_for_labels, // this is for giving space on the left side of the bar graphs and for the numbers on the right
            inner_margin: inner_margin, // margin between the bars and the outer box
            line_height: line_height,
            line_y_adjustment : line_y_adjustment,
            margin: margin,
            target: target,
            title: title,
            title_class: "title",
            watermark:"/img/logo.gif",
            width:  width // suggest 50 per sample
        }

        var instance = new biojsvissummaryhorizontalbargraph(options);
        document.getElementById('sample_breakdown_div').style.display = 'block';

    });


}




$(document).ready(function() {

    //return_breakdown_of_yugene_filtered_data

    set_gene_search_form();
    graph_id = '#yugene_graph';
    ensembl_id = $('#ensemblID').html();
    db_id = $('#db_id').html();

    if ($(graph_id).html() != null){
        //filters = {'ds_ids':[4000,6068,6344,6114,6037]}
        // the filters are for showing datasets along the line
        filters = null;
        run_biojs_yugene_graph(graph_id,ensembl_id,db_id,filters);

    }

    $('#sample_breakdown').change(function() {
        var val = $(this).val();
        if (val == 'count') {
          sort_by_number.sort(function(a,b) {
              return sort_by_count(a,b);
          });
        }
        else if (val == 'coverage') {
          sort_by_number.sort(function(a,b) {
            return sort_by_coverage_and_count(a,b);
          });
        }
        data_bar_graph =[];
        for(var i=0; i<limit_summary; i++) {
          data_bar_graph.push(sort_by_number[i]);
        }
        options.order_by = val;
        options.data = data_bar_graph;
        var instance = new biojsvissummaryhorizontalbargraph(options);
    });

    set_clicks();

});



function set_clicks(){

    contextHelpClick();


    $("a.export_d3_button").click(function(){
        this_div = $(this).attr('data-id');
        ensembl_id = $('#ensemblID').html();

        var tmp = document.getElementById(this_div);
        var svg = tmp.getElementsByTagName("svg")[0];
        // Extract the data as SVG text string
        var svg_xml = (new XMLSerializer).serializeToString(svg);

        output_format = $(this).attr('data-type');
        var form = document.getElementById("svgform");
        form['output_format'].value = output_format;
        form['file_name'].value = this_div+'_'+ensembl_id;
        form['data'].value = svg_xml ;
        form.submit();

    });





    $('#new_ds_id').click(function(e){
        graph_id = '#yugene_graph';
        ensembl_id = $('#ensemblID').html();
        db_id = $('#db_id').html();

        //proof of concept of changing datasets
        filters = {'ds_ids':[5008]}
        run_biojs_yugene_graph(graph_id,ensembl_id,db_id,filters);

    });


    $('#infoMenu').click(function(e){
        $('#displayGeneDetail').modal({
            onShow: function (dialog){
                $('#simplemodal-container').width('auto');
            }
        });

    });

    $('#viewGenes').click(function(e){
        $('#geneSearchForm').submit();
    });


    $('#exportTableCSVButton').click(function(){
                $('#downloadGeneSearch').table2CSV();
            });



    $('#share_link').unbind().click(function(){
        value = check_user_logged_in_for_sharing(); // this is in main.js
        if (value == false){ return false; }

        var ds_id = $('#datasetID').html();
        $('#wb_modal_title').html('Share this graph');
        var form_html  = "<form id='share_link_form'>" +
                "<div id=help_share_link_form>Please note that you can add more than one email address separating each with commas and no spaces." +
                "<dl>" +
                    // "<dt>From Name:</dt><dd><input class='share_input' type='text' name='from_name' value='"+$('#full_name').html()+"'/></dd>" +
                    "<dt id='to_email_label'>To Email:</dt><dd><input id='to_email_input' class='share_input' type='text' name='to_email' value=''/></dd>" +
                    "<dt>Subject:</dt><dd><input class='share_input' type='text' name='subject' value='"+SITE_NAME+" -  " + $('div.title').html() +"'/></dd>" +
                    "<dt>Body:</dt><dd><textarea class='share_input' name='body' >Here is a link I thought you might want to see:\r\n"+ window.location.href +"\r\n\r\n"+"From \""+$('#full_name').html()+"\" " + $('#user').html() +" via "+SITE_NAME+"</textarea></dd>" +
                    "<dt class='no_margin_bottom'><button id='share_link_form_submit' type='button'>Submit</button></dt><dd class='no_margin_bottom'></dd>" +
                "</dl>" +
                "<div class='clear'/>"+
            "</form>" +

            "<div class='clear'/>";



        $('#wb_modal_content').html(form_html);
        $('#modal_div').modal({
            minHeight: 445,
            /* minWidth: 400, */
            onShow: function (dialog) {
                var modal = this;


                $('#share_link_form_submit').click(function(e){
                    // stop things from happening first
                    e.preventDefault();

                    var post_url = BASE_PATH + 'main/send_email';
                    $.post(post_url, $("#share_link_form").serialize(),
                        function(data) {
                            $('#wb_modal_title').html('Share this graph');
                            $('#wb_modal_content').html(data);
                            $('#simplemodal-container').height('auto');
                        }

                    );

                });


            }

        });


    });


}

function set_gene_search_form(){


    var db_id = $('#db_id').html();
    $("#geneSearch").autocomplete({
        source: BASE_PATH + 'genes/get_autocomplete',
        minLength: 4, // because the names are very small eg. STAT1
        timeout: AUTOCOMPLETE_TIMEOUT,
        appendTo: ".searchBox",
        select: function(event, ui) {
            var gene = ui.item.ensembl_id;
            var db_id = ui.item.db_id;
            new_url = BASE_PATH + 'genes/summary?&gene='+gene+'&db_id='+db_id;
            window.location = new_url;
        }
    }).data("ui-autocomplete")._renderItem = function( ul,item ){
        return $("<li></li>").append("<a> <div class='symbol'>" + item.symbol + "</div><div class='species'>"+item.species+"</div><div class='aliases'>"+item.aliases+"</div><div class='description'>"+item.description+"</div><div class='clear'></div></a>").appendTo(ul);
    };


    $('#geneSearchForm').submit(function(){

        $("#geneSearch").autocomplete('close');
        var db_id = $('#db_id').html();
        var gene = $('#geneSearch').val();
        new_url = BASE_PATH + 'genes/summary?&gene='+gene+'&db_id='+db_id;
        window.location = new_url;
        return false;
    });


}
