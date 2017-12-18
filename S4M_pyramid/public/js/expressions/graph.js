var bandwidth_line_width = 15;
var roundTo = 5;
var y_axis_adjustment = 7;
// ['#','#','#','#','#','#','#','#','#','#']
var splitAttribute = '|';
var max_y_axis = null;
var minXaxis = -0.5;

var floorValue = -999999999;
var minStartingValue = 100000000000;
var maxStartingValue = -100000000000;

var angle_horizontal = 0;
var angle_diagonal = -Math.PI / 6;
var angle_vertical = -Math.PI / 2;
var angle_logo = Math.PI / 2;

function draw_logo(view_data){
      var canvas = view_data.plot.getCanvas()
      var ctx = canvas.getContext("2d");
      var imageObj = new Image();
      var set_y_axis_for_logo = 355;

      // for PG header
      if (view_data.header == 'grandiose'){
          var imageObj2 = new Image();
          imageObj2.onload = function() {
            ctx.save();
            var angle_logo = Math.PI / 2;
            ctx.rotate(angle_logo);
            ctx.fillStyle="#000000";
            ctx.fillRect(430,-canvas.width + min_border_margin -60,272,54);
            ctx.drawImage(imageObj2, 430, -canvas.width + min_border_margin -60);
            ctx.restore();
          };
          imageObj2.src = '/images/grandiose/Project_Grandiose.gif';
          set_y_axis_for_logo = 200;
      }

      // option 1 - with full STEMFORMATICS down the right
      imageObj.onload = function() {
        ctx.save();
        var angle_logo = Math.PI / 2;
        ctx.rotate(angle_logo);
        this_width = $('canvas.flot-overlay').css('width').replace('px','');
        set_x_axis_for_logo =  -this_width + min_border_margin -40;
        ctx.drawImage(imageObj, set_y_axis_for_logo,set_x_axis_for_logo);
        ctx.restore();
      };
      imageObj.src = '/img/logo.gif';


}


function draw_legend_on_canvas(view_data){

    kinetic_width = 1800;
    kinetic_height = 800;
    var container_id = 'kinetic_legend';
    var layer = new Kinetic.Layer();
    var simpleText = new Kinetic.Text({
        x: 20,
        y: 20,
        text: 'Legend',
        fontSize: 36,
        align: "center",
        fontFamily: 'sans-serif',
        fill: "black"
    });
    layer.add(simpleText);


    var legends = new Object();
    legends.offset_y = 35;
    legends.start_y = 70;
    legends.this_y = legends.start_y;
    legends.this_x = 25;
    legends.height_of_square = 11;
    legends.width_of_square = 15;
    legends.txt_y_offset = 1;

    var sample_type_display_order = view_data.sample_type_display_order;
    var plot = view_data.plot;
    //var ctx = plot.getCanvas().getContext("2d");

    var plot_data = view_data.plot_data;
    number_of_legends = 0;
    if (view_data.graph_type == 'scatter'){
        for (var probe in view_data.plot_data){
            colour = view_data.probe_color_dict[probe]['color'];
            raw_probe = probe;
            display_probe_id = view_data.probe_color_dict[probe]['display_probe_id'] + ' ' + raw_probe;
            url = "";
            txt_colour = "black";
            var number_mapped_genes = view_data.probe_information[probe];
            if (number_mapped_genes > 1){
                txt_colour = "red";
                display_probe_id= display_probe_id +'*';
                chip_type = view_data.chip_type;
                db_id = view_data.db_id;
                url = '/probes/multi_map_summary?probe_id='+encodeURIComponent(raw_probe)+'&chip_type='+chip_type+'&db_id='+db_id;
            }
            mouse_over = probe;
            draw_individual_legends(layer,legends,display_probe_id,colour,txt_colour,url,view_data,mouse_over);
            number_of_legends ++;
        }
    } else {

        if (view_data.graph_type == 'line'){
            sample_type_display_order = [];
        }


        var sample_type_colours = {};
        for (var sample_type in plot_data){

            // check for second_sort_by state
            if (sample_type.indexOf("|") != -1){
                original_sample_type = sample_type;
                temp_sample_type = sample_type.split("|");
                sample_type = temp_sample_type[1];
                colour = plot_data[original_sample_type].color;
            } else {
                colour = plot_data[sample_type].color;
            }

            if (view_data.graph_type == 'line'){
                pos = jQuery.inArray(sample_type, sample_type_display_order);
                if (pos == -1){
                    sample_type_display_order.push(sample_type);
                    sample_type_display_order.sort();
                }
            }

            sample_type_colours[sample_type] = colour;
        }

        for (var pos in sample_type_display_order){
            sample_type = sample_type_display_order[pos];
            colour = sample_type_colours[sample_type];
            url = "";
            txt_colour = "black";
            mouse_over = ""
            layer = draw_individual_legends(layer,legends,sample_type,colour,txt_colour,url,view_data,mouse_over);
            number_of_legends ++;
        }
    }
    number_of_legend_columns = Math.ceil(number_of_legends/20);
    width = 300;
    if (number_of_legend_columns > 1){
        width = 30 + (number_of_legend_columns) * 200;
        height = 800;
    } else {
        height = (number_of_legends * 35) + 100;
    }

    $('#kinetic_legend').css('width',width+'px').css('height',height+'px');


    var stage = new Kinetic.Stage({
        container: container_id,
        width: width,
        height:height
    });

    stage.add(layer);


}

function draw_individual_legends(layer,legends,name,colour,txt_colour,url,view_data,mouse_over){

    if (legends.this_y > 740){
        legends.this_y = legends.start_y;
        legends.this_x = legends.this_x + 200;
    }
    var rect = new Kinetic.Rect({
        x: legends.this_x-2,
        y: legends.this_y-2,
        width: legends.width_of_square+4,
        height: legends.width_of_square+4,
        fill: 'white',
        stroke: 'black',
        strokeWidth: 1
      });

      // add the shape to the layer
    layer.add(rect);

    var rect = new Kinetic.Rect({
        x: legends.this_x,
        y: legends.this_y,
        width: legends.width_of_square,
        height: legends.width_of_square,
        fill: colour,
        stroke: 'black',
        strokeWidth: 1
      });

      // add the shape to the layer
    layer.add(rect);

    var simpleText = new Kinetic.Text({
        x: legends.this_x + 20,
        y: legends.this_y + legends.txt_y_offset,
        text: name,
        fontSize: 12,
        align: "left",
        width: 180,
        fontFamily: 'sans-serif',
        fill: txt_colour
    });


    if (view_data.graph_type == 'scatter' && view_data.ref_type != 'miRNA'){
        simpleText.setName(mouse_over);
        simpleText.on('mouseover', function(e) {
            display_name_full = e.targetNode.attrs.text;
            $('#generic_tooltip').hide().html(display_name_full).css('top',e.pageY).css('left',e.pageX + 30).show();

        });
        simpleText.on('mouseout', function(e) {
            $('#generic_tooltip').hide();
        });
    }



    if (url != ""){
        simpleText.url = url;
        simpleText.on('click', function() {
            window.location = this.url;
        });
    }
    layer.add(simpleText);

    legends.this_y = legends.this_y + legends.offset_y;
    return layer;

}


// suggest you use stemformatics_tools/color_creator/color_creator.pl
// eg. perl color_creator.pl CC0066
// ['#CC0066','#BB005E','#AA0056','#99004E','#880046','#77003E','#660036','#55002E','#440026','#33001E']
function draw_xaxis_labels(view_data){
    xaxis_labels = view_data.xaxis_labels;
    var offset = view_data.plot.getPlotOffset();
    var axes = view_data.plot.getAxes();
    if (view_data.click_to_select_probes == undefined){
        view_data.click_to_select_probes = false;
    }

    kinetic_width = 1170;
    if (view_data.expand_horizontally){
        kinetic_width = view_data.expand_horizontally_width;
    }
    var container_id = 'xaxis_labels'+view_data.ds_id;
    var stage = new Kinetic.Stage({
        container: container_id,
        width: kinetic_width,
        height: 220
    });

    var layer = new Kinetic.Layer();
    for (var i in xaxis_labels){
        var level = xaxis_labels[i]['level'];
        var xaxis_position = xaxis_labels[i]['xaxis_position'];
        var id = xaxis_labels[i]['id'];
        var name = xaxis_labels[i]['name'];
        var number_mapped_genes = view_data.probe_information[id];
        var type = xaxis_labels[i]['type'];
        txt =new Object();
        multi_map = false;
        txt.fill_style = "black";
        raw_probe = id;
        if (number_mapped_genes > 1 && view_data.click_to_select_probes == false){
            txt.fill_style = "red";
            name = name + '*';
            multi_map = true;
        }


        txt.angle = angle_diagonal;
        txt.plot = view_data.plot;
        if (large){
            if (level == 1) { txt.abs_y = 2155;}
            if (level == 2) { txt.abs_y = 2500;}

        } else {
            if (level == 1) { txt.abs_y = 735;kinetic_y=101;}
            if (level == 2) { txt.abs_y = 790;kinetic_y=195;}

        }


        txt.x = xaxis_position + 0.2;



        txt.text_align = "right";
        txt.font= "12px sans-serif";
        var axes = txt.plot.getAxes();

        if (type == 'Probe' && view_data.ref_type != 'miRNA'){
            txt.text = name + ' ' + id;
        }else {
            txt.text = name;
        }

        length_of_name = txt.text.length;
        if (length_of_name >= 20){
            half_length_of_name = length_of_name / 2;
            name1 = txt.text.slice(0, half_length_of_name);
            name2 = txt.text.slice(half_length_of_name);
            txt.text = name1;
            draw_text_on_canvas(txt);

            txt.text = name2;
            txt.abs_y = txt.abs_y + 15;
            draw_text_on_canvas(txt);


        } else {
           draw_text_on_canvas(txt);
        }

        kinetic_x = axes.xaxis.p2c(txt.x) + offset.left - 178;


        var simpleText = new Kinetic.Text({
            x: kinetic_x,
            y: kinetic_y,
            text: name,
            fontSize: 13,
            align: "right",
            rotationDeg: 330,
            fontFamily: 'sans-serif',
            width: 200,
            fullText: txt.text,
            fill: txt.fill_style
        });

        if (type == 'Probe' && view_data.ref_type != 'miRNA'){
            simpleText.setName(id);
            simpleText.on('mouseover', function(e) {
                display_name_full = e.targetNode.attrs.text + ' ' + e.targetNode.attrs.name;
                $('#generic_tooltip').hide().html(display_name_full).css('top',e.pageY).css('left',e.pageX + 30).show();

            });
            simpleText.on('mouseout', function(e) {
                $('#generic_tooltip').hide();
            });
        }



        if (multi_map){
            simpleText.raw_probe = raw_probe;
            simpleText.chip_type = view_data.chip_type;
            simpleText.db_id = view_data.db_id;
            simpleText.on('click', function() {
                window.location = '/probes/multi_map_summary?probe_id='+encodeURIComponent(this.raw_probe)+'&chip_type='+this.chip_type+'&db_id='+this.db_id;
            });
        }
        if (view_data.click_to_select_probes){

            simpleText.raw_probe = raw_probe;
            simpleText.on('click', function() {
                /*
                var url = new URL(document.URL);
                url.get_data['select_probes'] = encodeURIComponent(this.raw_probe);
                console.log(this.raw_probe);
                new_url = url.get_url();

                window.location = new_url;
                */
                var values_textarea = $('div.select_probes textarea');
                var values = values_textarea.val();

                if (values == ''){
                    values_textarea.val(this.raw_probe);
                } else {
                    values_textarea.val(values + ' ' +this.raw_probe);

                }

            });
        }
        layer.add(simpleText);

    }
    stage.add(layer);
}


function set_markings_to_array(view_data){
    markings = [];
    for (var vertical_line in view_data.markings){
        markings[vertical_line] = view_data.markings[vertical_line];
    }
    return markings;
}

function is_array(input){
    return typeof(input)=='object'&&(input instanceof Array);
}

function roundNumber(num, dec) {
	var result = Math.round(num*Math.pow(10,dec))/Math.pow(10,dec);
	return result;
}


function drawGraph(view_data){
    // v0.8 flot using function to draw labels on canvas    function drawAxisLabels() {
    graph_id = view_data.graph_id ;
    view_data.plot = $.plot($(graph_id),view_data.flot_data, view_data.options);

    draw_xaxis_labels(view_data);
    draw_yaxis_labels(view_data);
    draw_title(view_data);
    draw_detection_threshold_and_median(view_data);
    draw_legend_on_canvas(view_data);
    draw_logo(view_data);
    return view_data;
}
function draw_detection_threshold_and_median(view_data){


    var ctx = txt.plot.getCanvas().getContext("2d");
    var offset = txt.plot.getPlotOffset();
    var axes = txt.plot.getAxes();
    var y_axis_adjustment_lines = 20;

    detection_threshold = view_data.detection_threshold;
    if (detection_threshold != undefined && detection_threshold != 0 && detection_threshold != 'NULL' ){
        // The title
        txt =new Object();
        txt.text = "DT ("+detection_threshold+")";
        txt.angle = angle_horizontal;
        txt.plot = view_data.plot;
        //txt.y = detection_threshold;

        txt.abs_y = axes.yaxis.p2c(detection_threshold) + offset.top + y_axis_adjustment_lines;


        txt.x = view_data.min_x_axis;
        txt.width = 200;
        txt.text_align = "left";
        txt.fill_style = "#000";
        draw_text_on_canvas(txt);
    }

    median_dataset_expression = view_data.median_dataset_expression;
    if (median_dataset_expression != undefined && median_dataset_expression != 0 && median_dataset_expression != 'NULL'){
        txt =new Object();
        txt.text = "Med ("+median_dataset_expression+")";
        txt.angle = angle_horizontal;
        txt.plot = view_data.plot;
        txt.abs_y = axes.yaxis.p2c(median_dataset_expression) + offset.top + y_axis_adjustment_lines;
        txt.x = view_data.min_x_axis;
        txt.width = 200;
        txt.text_align = "left";
        txt.fill_style = "#000";
        draw_text_on_canvas(txt);

    }




}

// Found this function here http://www.html5canvastutorials.com/tutorials/html5-canvas-wrap-text-tutorial/
function wrapText(txt, maxWidth, lineHeight) {

    if (txt.text == undefined){
        return false;
    }

    maxWidth = txt.maxWidth;
    lineHeight = txt.lineHeight;

    var context = txt.plot.getCanvas().getContext("2d");
    var text = txt.text;

    var offset = txt.plot.getPlotOffset();
    var axes = txt.plot.getAxes();
    if (txt.hasOwnProperty('x')){
        x = axes.xaxis.p2c(txt.x) + offset.left;
    }
    if (txt.hasOwnProperty('y')){
        y = axes.yaxis.p2c(txt.y) + offset.top + y_axis_adjustment;
    }
    if (txt.hasOwnProperty('abs_x')){
        x = txt.abs_x;
    }
    if (txt.hasOwnProperty('abs_y')){
        y = txt.abs_y;
    }


    var words = text.split(' ');
    var line = '';

    for(var n = 0; n < words.length; n++) {
        var testLine = line + words[n] + ' ';
        var metrics = context.measureText(testLine);
        var testWidth = metrics.width;
        if (testWidth > maxWidth && n > 0) {
            context.fillText(line, x, y);
            line = words[n] + ' ';
            y += lineHeight;
        }
        else {
            line = testLine;
        }
    }
    context.fillText(line, x, y);
}

function draw_title(view_data){
    // The title
    var axes_data = view_data.plot.getAxes();
    var min_y = axes_data.yaxis.min;
    var max_y = axes_data.yaxis.max;
    var min_x = axes_data.xaxis.min;
    var max_x = axes_data.xaxis.max;



    txt =new Object();
    txt.text = view_data.cells_samples_assayed;
    txt.angle = angle_horizontal;
    txt.plot = view_data.plot;

    range = max_y - min_y;
    txt.y = max_y + (range /10);
    if (label_dimensions.hasOwnProperty('xaxis_center_label_x')){
        txt.abs_x = label_dimensions.xaxis_center_label_x;
    }
    else {
        txt.x =(max_x-min_x )/2;
    }
    txt.font= "16px sans-serif";
    txt.text_align = "center";
    // txt.fill_style = "#F15D22";
    txt.fill_style = "#000";

    txt.maxWidth = 900;
    txt.lineHeight = 16;
    wrapText(txt);




    txt.text = view_data.title_dataset;
    txt.y = txt.y + (range /15);
    wrapText(txt);

    txt.text = view_data.title + view_data.title_id + ' ' +view_data.title_grouped;
    txt.y = txt.y + (range /15);
    draw_text_on_canvas(txt);





}
function calc_decimal_places(number){
    temp = 1/number;

    if (temp > 0 && temp <= 10){
        return 1;
    }
    if (temp > 10 && temp <= 100){
        return 2;
    }
    if (temp > 100 && temp <= 1000){
        return 3;
    }

}
function draw_yaxis_labels(view_data){

    label_dimensions = view_data.label_dimensions;

    var axes_data = view_data.plot.getAxes();
    var max_y = axes_data.yaxis.max;
    //var min_y = label_dimensions.small_yaxis_tick_start;
    original_min_y = parseInt(view_data.original_min_y_axis);
    if ( original_min_y < 0 ){
        var min_y = original_min_y;
    } else {
        var min_y = 0;
    }
    decimal_places = calc_decimal_places(max_y);

    if (max_y > 0 && max_y < 1){
        multiplier = Math.pow(10,decimal_places);
        min_y = min_y * multiplier;
        max_y = max_y * multiplier;
    } else {
        multiplier = 1;
    }

    for (var i=min_y;i<=max_y;i++){
        var value = i / multiplier;
        //var value = (i / multiplier).toFixed(label_dimensions.yaxis_decimal_places);
        txt =new Object();
        txt.angle = angle_horizontal;
        txt.plot = view_data.plot;
        txt.font= " 12px sans-serif";
        txt.abs_x = label_dimensions.yaxis_ticks_abs_x;
        txt.y = value;
        txt.text = value;
        txt.width = 200;
        txt.text_align = "right";
        draw_text_on_canvas(txt);
    }

    // y axis label
    txt =new Object();
    txt.text = view_data.y_axis_label;
    txt.angle = angle_vertical;
    txt.plot = view_data.plot;
    txt.abs_y = label_dimensions.yaxis_label_abs_y;
    txt.abs_x = label_dimensions.yaxis_label_abs_x;

    txt.width = 200;
    txt.text_align = "center";
    draw_text_on_canvas(txt);


}




function set_detection_threshold_and_median(view_data,flot_data,count){

    detection_threshold = view_data.detection_threshold;
    min_x_axis = view_data.min_x_axis;
    max_x_axis = view_data.max_x_axis;

    if (detection_threshold != undefined && detection_threshold != 0 ){
        flot_data[count] = {data: [[min_x_axis,detection_threshold],[max_x_axis,detection_threshold]],color:'blue', label: false, lines: { show: true}};
        count++;
    }

    var median_dataset_expression = view_data.median_dataset_expression;
    if (median_dataset_expression != undefined && median_dataset_expression != 0 ){
        flot_data[count] = {data: [[min_x_axis,median_dataset_expression],[max_x_axis,median_dataset_expression]],color:'green', label: false, lines: { show: true}};
    }
    return flot_data;
}


Object.prototype.hasOwnProperty = function(property) {
    return this[property] !== undefined;
};





//function draw_text_on_canvas(rotate_angle_in_radians,plot,x, y, text, maxWidth,is_large) {
function draw_text_on_canvas(txt) {

    var ctx = txt.plot.getCanvas().getContext("2d");
    var offset = txt.plot.getPlotOffset();
    var axes = txt.plot.getAxes();
    if (txt.hasOwnProperty('x')){
        x = axes.xaxis.p2c(txt.x) + offset.left;
    }
    if (txt.hasOwnProperty('y')){
        y = axes.yaxis.p2c(txt.y) + offset.top + y_axis_adjustment;
    }
    if (txt.hasOwnProperty('abs_x')){
        x = txt.abs_x;
    }
    if (txt.hasOwnProperty('abs_y')){
        y = txt.abs_y;
    }

    ctx.textBaseline = "bottom";
    ctx.fillStyle= (txt.fill_style !== undefined)?txt.fill_style:"#000";

    ctx.lineStyle= (txt.line_style !== undefined)?txt.line_style:"#FFF";
    ctx.font= (txt.font !== undefined)?txt.font:"16px sans-serif";

    txt.large = typeof large !== 'undefined' ? txt.large: false;
    if (txt.large){ ctx.font="50px sans-serif"; }


    ctx.textAlign= (txt.text_align !== undefined)?txt.text_align:"left";
    //metric will receive the measures of the text
    var metric = ctx.measureText(txt.text);
    ctx.save(); // this will "save" the normal canvas to return to
    // We want to find the center of the text (or whatever point you want) and rotate about it
    var tx = x;
    var ty = y;

    // Translate to near the center to rotate about the center
    ctx.translate(tx,ty);
    // Then rotate...
    // default to -Math.PI / 6
    ctx.rotate(txt.angle);
    // Then translate back to draw in the right place!
    ctx.translate(-tx,-ty);
    ctx.fillText(txt.text, x, y);
    ctx.restore(); // This will un-translate and un-rotate the canvas


}
