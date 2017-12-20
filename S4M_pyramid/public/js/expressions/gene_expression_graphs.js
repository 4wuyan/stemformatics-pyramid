large = false;
var min_border_margin = 200;
if (CURRENT_URL.queryKey.size == "large") {
    large = true;
    var min_border_margin = 400;
}

function set_label_dimensions(){
    
    // for Gene Expression Graphs
    var label_dimensions = new Object();
    label_dimensions.yaxis_ticks_abs_x = 195;
    label_dimensions.yaxis_label_abs_x = 170;
    label_dimensions.yaxis_label_abs_y = 430;

    label_dimensions.yaxis_tick_offset = 0.2;
    label_dimensions.yaxis_tick_start = 0;
    label_dimensions.yaxis_tick_steps = 1;
    label_dimensions.yaxis_decimal_places = 0;

    return label_dimensions;

}

function graph_data(ds_id,graph_id,db_id){

    json_view_data = $("#json_view_data"+ds_id).html();
    this.view_data = jQuery.parseJSON(json_view_data);
    this.view_data.graph_id = graph_id;
    this.view_data.show_standard_deviation = "on"; 
    this.view_data.original_min_y_axis = this.view_data.min_y_axis;
 
    this.view_data.label_dimensions = set_label_dimensions();
    // Use Jquery to get select list element
    json_datasets = $('#dataSets').html();
    /* set the sort by values */
    this.dataSets = jQuery.parseJSON(json_datasets);
    this.ds_id = ds_id; 
    this.db_id = db_id;


}    


function selectGraphToDraw(){
	$('div.displayGraphs').addClass('loading');
    graph_type = this_graph_data.view_data.graph_type;
    line_graph_available = this_graph_data.view_data.line_graph_available;

    if (this_graph_data.view_data.plot_data == '{}'){
        $('div.loading').removeClass('loading');
        $(this_graph_data.graph_id).html('<div class="noGraphData">No data found for these parameters.</div>');
    } else {
        $('div.majorLabel').removeClass('majorLabel').addClass('majorLabelVertical');

        switch (graph_type){
        
            case "scatter":
                drawScatterPlot(this_graph_data.view_data);
            break;
            
            case "bar":
                drawBarPlot(this_graph_data.view_data);
            break;
            
                
            case "box":
                this_graph_data.view_data.show_standard_deviation="on";
                drawBoxPlot(this_graph_data.view_data);
                $('li.chooseSD').hide();
                break;

            case "line": // T#569
                this_graph_data.view_data.show_standard_deviation="on";
                drawLinePlot(this_graph_data.view_data);
                $('li.chooseSD').hide();
               
            break;
        }
        
    } 

    // gene_expression_graph_triggers.js
	afterGraphDrawn();
}

function drawScatterPlot(view_data){
	
    var probes = view_data.probe_list;
    var plot_data = view_data.plot_data;
    // finalise plot data 
    var flot_data = [];
    var count = 0;
    var colourCount = 0;
    // do this first so the real points overlay this
    var list_color_dict = {};
    var number_of_samples = view_data.number_of_samples;
    min_x_axis = view_data.min_x_axis; 
    max_x_axis = view_data.max_x_axis;
    var show_standard_deviation = view_data.show_standard_deviation;
    if (show_standard_deviation == 'on'){
        sd_data = view_data.plot_data_sd;
        for (var position in probes){
            probe_id = probes[position]; 
            if (sd_data.hasOwnProperty(probe_id) ){
            
                var color = view_data.probe_color_dict[probe_id]['color'];
                for (var list in sd_data[probe_id]){
                    if (sd_data[probe_id].hasOwnProperty(list) ){
                        flot_data[count] = {data: sd_data[probe_id][list], label: null, color: color,lines: {show: true}, bandwidth: {show: true, lineWidth: bandwidth_line_width, lineThickness: 2}};
                        count++;
                    }
                }
            }
            
            
        }    
        
    }
    if (view_data.hasOwnProperty('draw_scatter_with_lines')){
        draw_scatter_with_lines = view_data.draw_scatter_with_lines;
    } else{
        draw_scatter_with_lines = false;
    }
    for (var position in probes){
        probe_id = probes[position]; 
        if (plot_data.hasOwnProperty(probe_id) ){
            var color = view_data.probe_color_dict[probe_id]['color'];
            flot_data[count] = {data: plot_data[probe_id], color: color, label: probe_id,lines: {show: draw_scatter_with_lines},points: { show: true}};
            count++;
            colourCount++;
        }
    }

    
    flot_data = set_detection_threshold_and_median(view_data,flot_data,count);
    view_data.flot_data = flot_data;
    markings =  set_markings_to_array(view_data);
    var min_y_axis = view_data.min_y_axis;
    var max_y_axis = view_data.max_y_axis;
    var options = {
            //xaxis: {min:min_x_axis, max:max_x_axis, mode:null},
            xaxis: {min:min_x_axis, max:max_x_axis,ticks:[], mode:null},
            yaxis: {min:min_y_axis, max:max_y_axis, font: {
                 size: 0,
                 family: "sans-serif",
                 variant: "small-caps"
               }
            }, 
            grid: { minBorderMargin: min_border_margin, backgroundColor: "#FFF",markings: markings, hoverable: true}
            
		};
    

    view_data.options = options;
    var plot = drawGraph(view_data);
    
                     
    
    
}


function drawBarPlot(view_data){
	
    var plot_data = view_data.plot_data;
    // finalise plot data 
    var flot_data = [];
    // final plot data 
    var count = 0;
    var nextColourIndex = Array();
    markings =  set_markings_to_array(view_data);
    xaxis_labels = view_data.xaxis_labels;
    min_x_axis = view_data.min_x_axis;
    max_x_axis = view_data.max_x_axis;
    var show_standard_deviation= view_data.show_standard_deviation;
    for (var list in plot_data){
        

        if (plot_data.hasOwnProperty(list) ){
            
            var color = plot_data[list]['color'];
            
            
           var label = list;
            for (var instance in plot_data[list]['values']){
                if (plot_data[list]['values'].hasOwnProperty(instance) ){

                    var standard_deviation = plot_data[list]['values'][instance]['sd'];
                    var average = plot_data[list]['values'][instance]['average'];
                    var xaxis = plot_data[list]['values'][instance]['xaxis'];
                    var extra_info = plot_data[list]['values'][instance]['extra_info'];
                    var probe = plot_data[list]['values'][instance]['level_above'];
                    
                    flot_data[count] = {data: [[xaxis,average]],color:color,hoverLabel: list + extra_info + ' - ' + probe, label: label, bars: { show: true, barWidth: 1, align: "center"}};
                    label = null;// only want to have one label to stop duplicates
                    count++;
                    if (show_standard_deviation == 'on' && standard_deviation > 0){
                        // tried setting it up in json but it kept picking this up as an Object and not an array when decoding json
                        flot_graph_data = new Array(); // had to make it an array otherwise it wouldn't get picked up 
                        flot_graph_data[0] = new Array(); 
                        flot_graph_data[1] = new Array(); 
                        flot_graph_data[0][0]  = xaxis;
                        flot_graph_data[0][1]  = average + standard_deviation;
                        flot_graph_data[1][0]  = xaxis;
                        flot_graph_data[1][1]  = average - standard_deviation;
                        flot_data[count] = {data: flot_graph_data, label: null, color: color,lines: {show: true}, bandwidth: {show: true, lineWidth: bandwidth_line_width, lineThickness: 3}, hoverable: false};
                        count++;
                    }
                }
            }
        }
    }

    var min_y_axis = view_data.min_y_axis;
    var max_y_axis = view_data.max_y_axis;
    flot_data = set_detection_threshold_and_median(view_data,flot_data,count);
    view_data.flot_data = flot_data;
    view_data.options = set_options_bar_and_box(view_data);
    
    drawGraph(view_data);
    
    
}

function drawBoxPlot(view_data){
    var plot_data = view_data.plot_data;

    // finalise plot data 
    var flot_data = [];
    var count = 0;
    var nextColourIndex = Array();
    var markings = set_markings_to_array(view_data);
    xaxis_labels = view_data.xaxis_labels;
    min_x_axis = view_data.min_x_axis;
    max_x_axis = view_data.max_x_axis;
    
    // have to set this for the color
    
    var countList = 0;
    for (var list in plot_data){
        
        if (plot_data.hasOwnProperty(list) ){
           var color = plot_data[list]['color'];
            for (var instance in plot_data[list]['values']){
                if (plot_data[list]['values'].hasOwnProperty(instance) ){
                
                    var average = plot_data[list]['values'][instance]['average'];
                    var maxValue = plot_data[list]['values'][instance]['max'];
                    var median = plot_data[list]['values'][instance]['median'];
                    var minValue = plot_data[list]['values'][instance]['min'];
                    var sd = plot_data[list]['values'][instance]['sd'];
                    var xaxis = plot_data[list]['values'][instance]['xaxis'];
                    var Q1 = plot_data[list]['values'][instance]['Q1'];
                    var Q3 = plot_data[list]['values'][instance]['Q3'];
                    var probe = plot_data[list]['values'][instance]['level_above'];
                    var extra_info = plot_data[list]['values'][instance]['extra_info'];
                    // min and max with the lines
                    var hoverLabel = list + extra_info + ' - ' + probe; 
                    // have to calculate line width
                    flot_data[count] = {data: [[xaxis,maxValue],[xaxis,minValue]],hoverLabel: hoverLabel, label: null, color: color,lines: {show: true}, bandwidth: {show: true, lineWidth: 15, lineThickness: 3}, hoverable: true};
                    count++;
                    
                    // box part
                    var labelSet = null;
                    // this is to allow only one cell type sample type shown in legend
                    if (instance == 0){
                        labelSet = list;
                    }
                    
                    flot_data[count] = {data: [[xaxis,Q3,Q1]],color: color,hoverLabel: hoverLabel, label: labelSet , bars: { show: true, barWidth: 0.8, align: "center", fill: true, fillColor: color}};
                    count++; 
                    
                    // median
                    flot_data[count] = {data: [[xaxis,median,median]],color: '#FFF', label: null, bars: { show: true, barWidth: 0.8, align: "center"}, hoverable: false};
                    count++; 
                }
            }
        }
    }
    flot_data = set_detection_threshold_and_median(view_data,flot_data,count);
    view_data.flot_data = flot_data;
    min_y_axis = view_data.min_y_axis;
    max_y_axis = view_data.max_y_axis;
    

    view_data.options = set_options_bar_and_box(view_data);
    var plot = drawGraph(view_data);
       
}

function set_options_bar_and_box(view_data){
    
    var options = {
            series: { bandwidth: 
                        {   
                            active: true , 
                            drawBandwidth: 
                                function(ctx, bandwidth, x, y1, y2, color) { 
                                    ctx.beginPath();
                                    ctx.strokeStyle = color;
                                    ctx.lineWidth = 1;
                                    ctx.moveTo(x, y1);
                                    ctx.stroke();
                                    ctx.beginPath();
                                    ctx.strokeStyle = color;
                                    ctx.lineWidth = bandwidth.lineWidth;
                                    ctx.lineThickness = 1;
                                    ctx.lineThickness = bandwidth.lineThickness;
                                    ctx.moveTo(x,y1);
                                    ctx.lineTo(x,y1 + ctx.lineThickness);
                                    ctx.stroke();
                                }
                        }
                     
                    },
            xaxis: {min:view_data.min_x_axis, max:view_data.max_x_axis,ticks:view_data.x_axis_ticks, mode:null,font: { size:0 } },
            yaxis: {min:view_data.min_y_axis, max:view_data.max_y_axis, font: {
                 size: 0,
                 family: "sans-serif",
                 variant: "small-caps"
               }
            }, 

            grid: { minBorderMargin: min_border_margin, backgroundColor: "#FFF",markings: markings, hoverable: true }
		};
    return options;
}

// This is for the line graph in Gene Expression Graph
function drawLinePlot(view_data){
	
    // finalise plot data 
    var plot_data = view_data.plot_data;
    
    var flot_data = [];
    var count = 0;
    var markings = set_markings_to_array(view_data);
    min_x_axis = view_data.min_x_axis;
    max_x_axis = view_data.max_x_axis;
  
    // have to set this for the color
    
    var show_standard_deviation="on";
    
    var countList = 0;
    var checkLabels = {};
    list_color_dict = {};

    // This is to show the day value when the labels are not shown (in summary xaxis label mode)
    var show_xaxis_labels_full = {};

    if (typeof view_data.xaxis_labels_original === "undefined") {
        view_data.xaxis_labels_original = view_data.xaxis_labels;
    }

    for (var list in view_data.xaxis_labels_original.full){
        label_name = view_data.xaxis_labels_original.full[list].name; 
        xaxis_position = view_data.xaxis_labels_original.full[list].xaxis_position; 
        show_xaxis_labels_full[xaxis_position] = label_name;
    }

    for (var list in plot_data){
        if (plot_data.hasOwnProperty(list) ){
            values_array = new Array();
            var base_count = 0;
            for (var item in plot_data[list]['values']){
                var standard_deviation = plot_data[list]['values'][item]['sd'];
                var average = plot_data[list]['values'][item]['average'];
                var xaxis = plot_data[list]['values'][item]['xaxis'];
                var extra_info = plot_data[list]['values'][item]['extra_info'];
                var color = plot_data[list]['color'];
                label = null;
                values_array[xaxis] = [xaxis,average];
                if (show_standard_deviation == 'on' && standard_deviation > 0){
                
                    // tried setting it up in json but it kept picking this up as an Object and not an array when decoding json
                    graph_data = new Array(); // had to make it an array otherwise it wouldn't get picked up 
                    graph_data[0] = new Array(); 
                    graph_data[1] = new Array(); 
                    graph_data[0][0]  = xaxis;
                    graph_data[0][1]  = average + standard_deviation;
                    graph_data[1][0]  = xaxis;
                    graph_data[1][1]  = average - standard_deviation;
                    flot_data[count] = {data: graph_data, label: null, color: color,lines: {show: true}, bandwidth: {show: true, lineWidth: 30, lineThickness: 3}, hoverable: false};
                    count++;
                }
            }
            
            temp_label = list.split('|');
            new_label = temp_label[1] + ' - ' + temp_label[0];
            flot_data[count] = {data: values_array,color:color,hoverLabel: new_label + extra_info, label: label, points: { show: true }, lines: {show: true}, show_xaxis_labels_full: show_xaxis_labels_full};
            count++; 
        }
    }
    view_data.options = set_options_bar_and_box(view_data);


    // this is checking total values of the original full xaxis labels. It's not perfect.
    if (view_data.expand_horizontally || Object.keys(view_data.xaxis_labels_original.full).length < 35 ){
        view_data.xaxis_labels = view_data.xaxis_labels_original['full'];
    }    
    else {
        view_data.xaxis_labels = view_data.xaxis_labels_original['summary'];
    } 
    view_data.flot_data = set_detection_threshold_and_median(view_data,flot_data,count);


    drawGraph(view_data);
    
    
}



