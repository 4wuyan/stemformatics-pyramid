// if you don't specify a html file, the sniper will generate a div with id "rootDiv"
// var app = require("biojs-vis-scatter-plot");

var module = {};// setup module as an object so that the biojs will work

function round_to_two_decimal_places(num){
    new_num = Math.round(num * 100) / 100;
    return new_num;
}

increment_value = 1;

// tip which is displayed when hovering over a collumn. Displays the sample type
//of the collumn
var tip = d3.tip()
    .attr('class', 'd3-tip')
    .html(function(d) {
        sample_type = d.sample_type;
        temp =
            "Sample Type: " +  sample_type + "<br/>"
        return temp;
    });


function run_scatter_gene_expression_graph(colours, graphDiv,sortByOption, show_min_y_axis, legend_required, ref_name,main_title, whiskers_needed, scaling_required, dataset_data, probe_name_for_tooltip,ref_type ) {
    whiskers_needed = false // hardcoding whiskers to be false for scatter graph [As only 2000 dataset had technical replicates and now all those replicates now been set to different samples]
    var multi_group = sortByOption.split(",").length;
    /* Extracting the data from the csv files for use in the graph
     * Also sets relevent options based on the data passed in (for example
     * calculating the min and max values of the graph */
     div_name = "content"+dataset_data["ds_id"];
     var tooltip_multiview =  d3.tip()
         .attr('class', 'd3-tip')
         .attr('id', 'tooltip_multiview_'+dataset_data["ds_id"])
         .offset([100,400])
         .html(function () {
             temp = "Title - " + dataset_data["Title"];
             return temp;
         });
     // this tooltip function is passed into the graph via the tooltip
     var tooltip_scatter = d3.tip()
         .attr('class', 'd3-tip')
         .offset([0, +110])
         .html(function(d) {
             probe = d.Probe;
             // 2 decimal places on the display only
             Expression_Value = round_to_two_decimal_places(d[y_column]);
             lwr = round_to_two_decimal_places(d.Expression_Value - d.Standard_Deviation);
             upr = round_to_two_decimal_places(d.Expression_Value + d.Standard_Deviation);
             temp =
                 probe_name_for_tooltip +": " + d.Probe + "<br/>" +
                 "Replicate ID: " + d.Replicate_ID +"<br/>"+
                 "Log2 Expression: " + Expression_Value + " [" + lwr + ";" + upr +"]<br/>"
                // "MSC predicted "+msc_call+"/"+total+" iterations<br/>"
             return temp;
         });


        max = 0;
        min = 0;
        number_of_increments = 0;
        count = 0;
        //make an array to store the number of probes for the legend
        probes_types = new Array();
        probes = new Array();
        probe_count = 0;
        //Saving the sample types and corrosponding id to use when
        //itterating over for the hovering over the ample types and altering the scatter
        //points for that sample type
        sample_types = new Array();
        sample_type_array = new Array();
        sample_type_count = 0;
        if(multiview_graph != "yes") { // if graph is not multiview, only than sample_type hover object will created, otherwise if multiview it uses the sample_type_hover object defined in graph_multi_view.js so that sample types for all the datasets can be merged
            sample_type_hover = {};
        }

        //need to put in the number of colours that are being used (so that it
        //can reiitterate over them again if necesary
        number_of_colours = 39;
        colour_count = 0;
        data.forEach(function(d){
            // ths + on the front converts it into a number just in case
            d.Expression_Value = +d.Expression_Value;
            d.Standard_Deviation = +d.Standard_Deviation;
            d.Probe = d.Probe;
            //calculates the max value of the graph otherwise sets it to 0
            //calculates the min value and uses this if max < 0 otherwise sets to 0
            //increment valye = max - min.
            if(d.Expression_Value + d.Standard_Deviation > max){
                max = d.Expression_Value + d.Standard_Deviation;
            }
            if(d.Expression_Value - d.Standard_Deviation < min){
                min = d.Expression_Value - d.Standard_Deviation;
            }
            if($.inArray(d.Probe, probes_types) == -1){
                probes_types.push(d.Probe);
                probe_count++;
            }
            if($.inArray(d.Sample_Type, sample_type_array) == -1) {
                //Gives each sample type a unique id so that they can be grouped
                //And highlighted together
                sample_type_array.push(d.Sample_Type);
                sample_types[d.Sample_Type] = sample_type_count;
                sample_type_hover[d.Sample_Type] = d.Sample_Type_Long;
                sample_type_count ++;
            }
            count++;

        });
        probes_types = probes_types.sort(sortAlphaNum_array)
        /* Set up colour arrays */

        var probe_colour = {};//new Array();
        probe_colour = setup_colours_for_group(probes_types, probe_colour,
            number_of_colours, colours);
        var sample_colour =  {};//new Array();
        sample_colour = setup_colours_for_group(sample_type_array.sort(), sample_colour,
            number_of_colours, colours);

        // The number of increments is how large the increment size is for the
        // y axis (i.e. 1 per whole numner etc) e.g. or an increment per number = max - min
        // changes done by isha

        number_of_increments = max - min;
        // this is when max-min is 0
        if (number_of_increments < dataset_data["medianDatasetExpression"])  {
           if (number_of_increments < dataset_data["detectionThreshold"])  {
            number_of_increments = Math.ceil(dataset_data["detectionThreshold"]);
          }
          else {
            number_of_increments = Math.ceil(dataset_data["medianDatasetExpression"]);
          }
        }
        // Turn number of increments into a whole number
        number_of_increments = Math.ceil(number_of_increments);

        if((number_of_increments * increment_value) < 6) {
          number_of_increments = 6;
        }
        if((number_of_increments * increment_value) > 10) {
          number_of_increments = 10;
        }
        probes = probes;
        sample_types = sample_types;
        probe_count = probe_count;
        title = main_title;
        subtitle1 = dataset_data["Title"]
        subtitle2 = dataset_data["cellsSamplesAssayed"]
        target = graphDiv;

        // can always use just a straight value, but it's nicer when you calculate
        // based off the number of samples that you have
        width = data.length*1;
        horizontal_grid_lines = width;
        if (width < 1000){
            width = 1000;
        }
        var split_sort_by_option = sortByOption.split(',');
        if (split_sort_by_option[0] == "Sample Type") {
            split_sort_by_option[0] = "Sample_Type";
        } else if (split_sort_by_option[1] == "Sample Type") {
            split_sort_by_option[1] = "Sample_Type";
        }
        //The main options for the graph
        var options = {
            split_sort_by_option: split_sort_by_option,
            multi_group: multi_group, // Indicates there is only 1 group on the x axis (probes)
            legend_list: {name: "probes", list: probes_types},
            probe_name_for_tooltip:probe_name_for_tooltip,
	        colour_array: probe_colour, //probe_colours=
            /******** Options for Sizing *****************************************/
            legend_padding: 190,
            legend_rect_size: 20,
            ref_type: ref_type,
    	    height: 400,
            width: graph_box_width,
            margin:{top: 250, left: 130, bottom: 300, right: 250},
            initial_padding: 10,
            x_axis_label_padding: 10,//padding for the x axis labels (how far below the graph)
            text_size: "12px",
            title_text_size: "16px",
            tooltip_multiview: tooltip_multiview,
            increment: number_of_increments * increment_value, // To double the number of increments ( mutliply by 2, same for
            // reducing. Number of increments is how many numbers are displayed on the y axis. For none to
            // be displayed multiply by 0
            // changes masde by isha to show horizontal and vertical lines
            display: {hoverbars: "no", error_bars: "yes", legend: legend_required, horizontal_lines: "yes", legend_hover: "no", vertical_lines: "yes", x_axis_labels: "yes", y_axis_title: "yes", horizontal_grid_lines: "yes"},

            circle_radius: 2,  // for the scatter points
            hover_circle_radius: 10,
            /*********** End of sizing options **********************************/

            background_colour: "white",
            background_stroke_colour:  "black",
            background_stroke_width:  "1px",
            colour: colours,
          	font_style: "Arial",
          	grid_colour: "black",
            ref_name: ref_name,
          	grid_opacity: 1,
          	y_label_text_size: "14px",
          	y_label_x_val: 60,
            data: data,
            whiskers_needed: whiskers_needed,
            sortByOption: sortByOption,
            show_min_y_axis: show_min_y_axis,
            // eq. yes for x_axis labels indicates the user wants labels on the x axis (sample types)
            // indicate yes or no to each of the display options below to choose which are displayed on the graph
            domain_colours : ["#FFFFFF","#7f3f98"],
            error_bar_width:5,
    	    error_stroke_width: "1px",
            error_dividor:100,//100 means error bars will not show when error < 1% value
            //horizontal lines takes a name, colour and the yvalue. If no colour is given one is chosen at random
            horizontal_lines: [["Detection Threshold "+dataset_data["detectionThreshold"] , "green",dataset_data["detectionThreshold"]], ["Median "+dataset_data["medianDatasetExpression"], , dataset_data["medianDatasetExpression"]]],
            horizontal_line_value_column: 'value',
            //to have horizontal grid lines = width (to span accross the grid), otherwise = 0
            horizontal_grid_lines: width,
            legend_class: "legend",
            legend_range: [0,100],
            line_stroke_width: "2px",
           //default number of colours iis 39 (before it reitterates over it again)
            number_of_colours: 39,
            //2 is the chosen padding. On either side there will be padding = to the interval between the points
            //1 gives 1/2 the interval on either side etc.
            padding: 2,
            probe_count: probe_count,
            probes: probes_types,
            //sample type order indicates whether or not the samplese need to be represented in a specific order
            //if no order is given then the order from the data set is taken
            second_sort_by_order: "none", //Order of the second_sort_by state on the x axis
            sample_type_order:dataset_data["sampleTypeDisplayOrder"],// "DermalFibroblast, hONS", // "BM MSC,BM erythropoietic cells CD235A+,BM granulopoietic cells CD11B+,BM hematopoietic cells CD45+,Developing cortex neural progenitor cells,Ventral midbrain neural progenitor cells,Olfactory lamina propria derived stem cells",
            sample_types: sample_types,
            // Can fit 4 subtitles currently
            subtitles: [subtitle1],
            stroke_width:"3px",
            target: target,
            title: title,
            title_class: "title",
            tip: tip,//second tip to just display the sample type
            tooltip: tooltip_scatter, // using d3-tips
            //tooltip1: tooltip1, // using d3-tips unique_id: "chip_id",
            watermark:"http://www.stemformatics.org/img/logo.gif",
            x_axis_text_angle:-45,
            x_axis_title: "Samples",
            x_column: 'Sample_ID',
            x_middle_title: 500,
            y_axis_title: dataset_data["yAxisLabel"],
            y_column: 'Expression_Value'
        }

        var instance = biojsvisscatterplot(options);

          // Get the d3js SVG element
          var tmp = graphDiv;
          var svg = tmp.getElementsByTagName("svg")[0];
          // Extract the data as SVG text string
          var svg_xml = (new XMLSerializer).serializeToString(svg);

}
