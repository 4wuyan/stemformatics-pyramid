var ds_id = 0;
var db_id = '';
var this_graph_data = {};
var module = {};// setup module as an object so that the biojs will work


// Most of this is in expressions/graph.js
$(document).ready(function() {
    ds_id = $('#ds_id').html();    
    dataset_details = $('#dataset_details').html();    
    graph_id = '#graph';
    click_choose_datasets();

    // Note that 6329 is so low that it has 0.55 as the y axis label top.
 
    $('#graph_selection').draggable();
    $('div.graphControls').draggable();
    dataset_metadata = jQuery.parseJSON($('#dataset_details').html());


    // have to set this up here so that the tooltip can use these values
    var horizontal_lines = {'lwr':0.4337,'upr':0.5169};
    var legend_values=[200,150,100,50,0];
    // this tooltip function is passed into the graph via the tooltip
   var tooltip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, +110])
      .html(function(d) {
        msc_type = d.MSC_Type;
        // 2 decimal places on the display only
        // 95% CI [0.66,0.71] 
        // MSC 100/100
        total = d.total_subsamplings;
        msc_call = d.MSC_calls; 
        prediction = round_to_two_decimal_places(d[y_column]);
        lwr = round_to_two_decimal_places(d.lwr);
        upr = round_to_two_decimal_places(d.upr);
        percent = round_to_two_decimal_places(d.percentage);
        temp = 
            "Replicate ID: " + d.Replicate_Group_ID +"<br/>"+
            "Rohart Score [CI]: " + prediction + " [" + lwr + ";" + upr +"]<br/>"+
            "MSC predicted: "+msc_call+"/"+total+" iterations ("+percent+"%)<br/>"
        return temp; 
      });

    title = "Rohart MSC Test";
    subtitle1 = dataset_metadata[ds_id].title;
    subtitle2 = dataset_metadata[ds_id].cells_samples_assayed;
    target = "#graph";
    sample_type_hover = {}; 

    //data columns are state,type,component1,component2 tab separated
    d3.tsv('/msc_signature/get_msc_signature_values?ds_id='+ds_id,function (error,data){
        
        data.forEach(function(d){
            // ths + on the front converts it into a number just in case
            d.lwr = +d.lwr;
            d.prediction = +d.prediction;
            d.upr = +d.upr;
            d.percentage = d.MSC_calls / d.total_subsamplings * 100;
            if (!(d.Sample_Type in sample_type_hover)) {
                sample_type_hover[d.Sample_Type] = d.Sample_Type_Long;
            }
        });

        // can always use just a straight value, but it's nicer when you calculate
        // based off the number of samples that you have
        width = data.length*30 + 200;
        if (width < 1275){ // this is to keep it in line with the original css
            width = 1275;
        }
        var options = {
            background_colour: "white",
            background_stroke_colour:  "black",
            background_stroke_width:  "2px",
            circle_radius:5, 
            data: data,
            data_columns_for_colour: ["MSC_calls","total_subsamplings"],
            domain_colours : ["#FFFFFF","#f99820"], // f99820
            error_bar_width:10, 
            height: 1020,
            horizontal_line_value_column: 'value',
            horizontal_lines: horizontal_lines,  // this gets turned into an array of objects
            legend_class: "legend",
            legend_range: [0,100],
            margin:{top: 180, right: 120, bottom: 530, left: 200},
            sample_type_order: dataset_metadata[ds_id].sample_type_order,
            show_horizontal_line_labels: true,
            subtitle1: subtitle1,
            subtitle2: subtitle2,
            target: target,
            title: title,
            title_class: "title",
            tooltip: tooltip, // using d3-tips
            unique_id: "chip_id",
            watermark:"http://www.stemformatics.org/img/logo.gif",
            width:width, // suggest 50 per sample
            x_axis_text_angle:-45, 
            x_axis_title: "Samples",
            x_column:'Replicate_Group_ID',
            x_middle_title: 477,
            y_axis_title: "Rohart Score",
            y_column:'prediction' // d.prediction
        }

        var new_instance = biojsvisrohartmsctest(options);
        var column_names = ['Replicate_Group_ID','Prediction','Lower Bound','Upper Bound','MSC Calls','Total Subsamplings','Percentage %'];
        var columns_to_show_in_order = ['Replicate_Group_ID','prediction','lwr','upr','MSC_calls','total_subsamplings','percentage'];
        options = {
            title: "Graph data for Rohart MSC Test",
            column_names:column_names,
            data:data,
            min_height:400,
            min_width:1000,
            ds_id: ds_id,
            click_target_id: "#show_data_table",
            columns_to_show_in_order: columns_to_show_in_order,
            div_class: "show_data_table" 
        }
        var new_show_table = data_table(options);

    }); 
    $('div.displayGraphs').removeClass('loading');

    $("a.export_d3_button").click(function(){
        this_div = 'graph';
        var tmp = document.getElementById(this_div);
        var svg = tmp.getElementsByTagName("svg")[0];
        // Extract the data as SVG text string
        var svg_xml = (new XMLSerializer).serializeToString(svg);
        
        output_format = $(this).attr('data-type');

        var form = document.getElementById("svgform");
        form['output_format'].value = output_format;
        form['file_name'].value = 'rohart_msc_test_'+ds_id;
        form['data'].value = svg_xml ;
        form.submit();

    });
});
