var min_border_margin = 50;
large = false;
if (CURRENT_URL.queryKey.size == "large") {
    large = true;
    var min_border_margin = 200;
}


function plot_yugene_graph(graph_values,graph_id,label_dimensions,title,limit_xaxis) {
    
    var graph_details = [];
    
    count = 0;
    for (var type in graph_values) {
        
        for (var item in graph_values[type]){
            
            if (item != 'line'){
            
                var label = graph_values[type][item]['graphing_options']['label'];
                
                
                var data = graph_values[type][item]['data'];
                var color = graph_values[type][item]['graphing_options']['color'];
                
                if (graph_values[type][item]['graphing_options']['color'] == 'auto') {
                    // top lines for probes                    
                    graph_details[count] = {label: label, data: data, hoverable: true , clickable: true, bars: {show:true, fill: true}}
                } else {
                    // this is for the datasets below 0
                    graph_details[count] = {label: '', hoverable: true, data: data, bars: {show:true}, color: color}    
                }
            
                count++;
            }
        }
    }
    
    
    
    var options = {
        xaxis: {min:-0.5,show:false},
        yaxis: {min:-0.1, max:1, show:false},
        grid: {minBorderMargin: min_border_margin, backgroundColor: "#FFF",hoverable: true, clickable: true},
        selection: {mode: "x" }
	};
  
    if (limit_xaxis != undefined){
        options.xaxis.min = limit_xaxis.min;
        options.xaxis.max = limit_xaxis.max;
    }  

    var plot = $.plot($(graph_id), graph_details, options);
    var angle_horizontal = 0;
    var angle_diagonal = -Math.PI / 6;
    var angle_vertical = -Math.PI / 2;

    view_data = new Object();

    view_data.plot = plot;
    view_data.y_axis_label = 'Yugene Value';
    view_data.label_dimensions = label_dimensions;

    view_data.xaxis_title = 'Samples';

    view_data.title = '';
    view_data.title_id = '';
    view_data.title_dataset = title;
    view_data.title_grouped = '';
    draw_xaxis_title(view_data);
    draw_title(view_data);
    draw_yaxis_labels(view_data);

    return view_data;
   
}

function draw_xaxis_title(view_data){
    var label_dimensions = view_data.label_dimensions;
    var axes_data = view_data.plot.getAxes();
    var min_y = axes_data.yaxis.min;
    var max_y = axes_data.yaxis.max;

    txt =new Object();
    txt.text = view_data.xaxis_title;
    txt.angle = angle_horizontal; 
    txt.plot = view_data.plot;
    txt.y = min_y - 0.11;

    if (label_dimensions.hasOwnProperty('xaxis_label_y')){
        txt.y= min_y - label_dimensions.xaxis_label_y; 
    }
    else {        
        txt.y=min_y - 0.1; 
    }

    if (label_dimensions.hasOwnProperty('xaxis_center_label_x')){
        txt.abs_x = label_dimensions.xaxis_center_label_x ;
    }
    else {        
        txt.abs_x = 433;
    }



    txt.width = 1200;
    txt.text_align = "center";
    txt.fill_style = "#000";
    txt.large = large;
    draw_text_on_canvas(txt);

}



