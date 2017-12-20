// if you don't specify a html file, the sniper will generate a div with id "rootDiv"
var module = {} // setup module as an object so that the biojs will work
//var d3 = require("d3");
//------------------------------------------------- EDITED FOR TESTING ----------------------------------
function round_to_two_decimal_places(num){
   new_num = Math.round(num * 100) / 100;
   return new_num;
}

// tip which is displayed when hovering over a collumn. Displays the sample type
//of the collumn
var tip = d3.tip()
   .attr('class', 'd3-tip');

// this tooltip function is passed into the graph via the tooltip
var tooltip = d3.tip()
   .attr('class', 'd3-tip')
   .offset([0, +110])
   .html(function(d) {
      temp =
           "Probe: " + d.Probe + "<br/>" +
           "Line Group: " + d.LineGraphGroup +"<br/>"+
           "Day: " + d.Day + "<br/>" +
     "Sample ID: " + d.Replicate_ID + "<br/>"
       return temp;
   });


/* Extracting the data from the csv files for use in the graph
* Also sets relevent options based on the data passed in (for example
* calculating the min and max values of the graph */

function run_line_gene_expression_graph(colours,graphDiv,sortByOption,show_min_y_axis,ref_name,main_title,scaling_required,dataset_data,probe_name_for_tooltip,ref_type) {
  // changes done by Isha
      var multi_group = sortByOption.split(",").length;
    var sort_option_array = new Array();
    sortByOption = remove_spaces(sortByOption);
    var split_options = sortByOption.split(",");
    if (split_options[0] == "Sample_Type" || split_options[1] == "Sample_Type") {
        first_option = "Sample_Type";
    } else {
        first_option = split_options[0];
    }
    day_state_order = Object.keys(dataset_data['lineGraphOrdering']).sort(function(a,b){return dataset_data['lineGraphOrdering'][a]-dataset_data['lineGraphOrdering'][b]}); // this order the day states
    if (day_state_order != "none") {
         data.sort(function(a, b) {
                return day_state_order.indexOf(a.Day) - day_state_order.indexOf(b.Day);
            })
    } else {
    //SORTING FOR LINEGRAPH
        data.sort(function(a, b) { return a.Day.localeCompare(b.Day);});
    }
    if((unique_probes.length * day_state_order.length) > 20){
        show_days = "no";
    }
    else {
      show_days = "yes";
    }
    max = 0;
    min = 0;
    number_of_increments = 0;
    count = 0;
    //make an array to store the number of probes for the legend
    probes_types = new Array();
    probes = new Array();
    probe_count = 0;
    // changes done by Isha
    sample_count = 0;
    //Saving the sample types and corrosponding id to use when
    //itterating over for the hovering over the ample types and altering the scatter
    //points for that sample type
    line_groups = new Array();
    line_group_array = new Array();
    line_group_colour_array = {};
    count = 0;
    line_group_count = 0;
    j = 0;
    //need to put in the number of colours that are being used (so that it
    //can reiitterate over them again if necesary
    number_of_colours = 39;
    colour_count = 0;
    days = [];
    sample_id_list = [];
    sample_type_hover = {};
    day_names = "";
    day_count = 0;
    first_option = "LineGraphGroup";
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
        if($.inArray(d.Replicate_ID, sample_id_list) == -1){
            sample_id_list.push(d.Replicate_ID);
            sample_count++;
        }
        if ($.inArray(d.Day, days) == -1) {
              day_count ++;
              days.push(d.Day);
              sample_type_hover[d.Day] = d.Day;
        }
        if($.inArray(d[first_option], sort_option_array) == -1){
            sort_option_array.push(d[first_option]);
        }
        if($.inArray(d.LineGraphGroup, line_group_array) == -1) {
            //Gives each sample type a unique id so that they can be grouped
            //And highlighted together
            line_group_array.push(d.LineGraphGroup);
            line_groups[d.LineGraphGroup] = line_group_count;
            sample_type_hover[d.LineGraphGroup] = d.LineGraphGroup;
            j++;
            line_group_count ++;
        }
        count++;

    });

     /* Set up colour arrays */
    var sort_colour = {};
    sort_colour = colours
//if (first_option != "Sample_Type" ) {
            setup_colours_for_group(sort_option_array.sort(), sort_colour,
         number_of_colours,colours);
//    }
    for (day in days) {
        day_names = days[day] + " " + day_names;
    }
    // The number of increments is how large the increment size is for the
    // y axis (i.e. 1 per whole numner etc) e.g. or an increment per number = max - min
    number_of_increments = max - min;
    if (number_of_increments < dataset_data["medianDatasetExpression"])  {
      number_of_increments = Math.ceil(dataset_data["medianDatasetExpression"]);
    }
    else if (number_of_increments < dataset_data["detectionThreshold"])  {
      number_of_increments = Math.ceil(dataset_data["detectionThreshold"]);
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
    line_groups = line_groups;
    probe_count = probe_count;
    title = "Line Graph";
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
    // this tooltip function is passed into the graph via the tooltip

    //The main options for the graph
    var options = {
      multi_group: multi_group,
      colour_array: sort_colour,
      probe_name_for_tooltip:probe_name_for_tooltip,
      tip_decoy: tip,
      legend_text: "yes",
      legend_shorten_text: "no",
      substring_legend_length: 15,
      days: days,
      day_count: day_count,
      ref_type: ref_type,
      jitter: "no",
      test: "no", //Only used to test the data -> outputs the values to
      //a file on the computer
      test_path: "/home/ariane/Documents/stemformatics/bio-js-box-plot/test/box_plot_test.csv", //Path to save the test file to including name
      bar_graph: "yes",
      draw_scatter_on_box: scatter_needed,
      radius: 3,
      sort_by_sample_id: "no",
      /******** Options for Sizing *****************************************/
      legend_padding: 190,
      legend_rect_size: 20,
      height: 400,
      ref_name: ref_name,
      //Need to change this depending on whether it is the probe or
      //sample_type which is appearing on the legend -> can be changed to
      //accomadate more options if necessary (Ariane)
      legend_list: {name: "sample_id", list: line_group_array},//Select the list you want on the legend (i.e. sample_id_list)
      line_group_colour_array: sort_colour,//line_group_colour_array,
      x_axis_list: unique_probes_sorted,
      legend_probe_tip: "none",
      /** Added when merging **/
      legend_list: {name: "line_groups", list: line_group_array},//Select the list you want on the           // line_group_colour_array: line_group_colour_array,
      x_axis_list: unique_probes_sorted,
      legend_probe_tip: "none",
      width: graph_box_width,
      margin:{top: 250, left: 130, bottom: 300, right: 250},
      initial_padding: 10,
      x_axis_label_padding: 10,//padding for the x axis labels (how far below the graph)
      text_size: "12px",
      increment: number_of_increments * increment_value, // To double the number of increments ( mutliply by 2, same for
      // reducing. Number of increments is how many numbers are displayed on the y axis. For none to
      // be displayed multiply by 0
      display: {hoverbars: "yes", error_bars: "yes", legend: "yes", horizontal_lines: "yes", vertical_lines: "yes", x_axis_labels: "yes", y_axis_title: "yes", horizontal_grid_lines: "yes"},
      probe_list: probes_types,
      circle_radius: 4,  // for the scatter points
      hover_circle_radius: 8,
      /*********** End of sizing options **********************************/
      /******** Options for Data order *****************************************/
      // If no orders are given than the order is taken from the dataset
      box_width: 50,
      box_width_wiskers: 5,
      sortByOption: "Day",//sortByOption,
      show_min_y_axis: show_min_y_axis,
      day_state_order: day_state_order, //Order of the day state on the x axis
      line_group_order: dataset_data["sampleTypeDisplayOrder"], //Order of the sample types on the x axis
      probe_order: unique_probes_sorted,	//Order of the probes on the x axis
      //Including the day state on the x axis causes the order to change as the data becomes
      //sorted by probes and day state
      include_day_x_axis: show_days, //Includes the day state on the x axis
      size_of_day_labels: 200, //The size allotted to the day state labels
      x_axis_padding: 50,
      /******** End Options for Data order *****************************************/
      background_colour: "white",
      background_stroke_colour:  "black",
      background_stroke_width:  "1px",
      colour: colours,
      font_style: "Arial",
      grid_colour: "black",
      grid_opacity: 1,
      y_label_text_size: "14px",
      y_label_x_val: 60,
      data: data,
      // eq. yes for x_axis labels indicates the user wants labels on the x axis (sample types)
      // indicate yes or no to each of the display options below to choose which are displayed on the graph
      domain_colours : ["#FFFFFF","#7f3f98"],
      error_bar_width:5,
      error_stroke_width: "1px",
      error_dividor:100,//100 means error bars will not show when error < 1% value
      //horizontal lines takes a name, colour and the yvalue. If no colour is given one is chosen at random
      horizontal_lines: [["Detection Threshold "+dataset_data['detectionThreshold'], "green", dataset_data['detectionThreshold']], ["Median "+dataset_data['medianDatasetExpression'], , dataset_data['medianDatasetExpression']]],
      horizontal_line_value_column: 'value',
      //to have horizontal grid lines = width (to span accross the grid), otherwise = 0
      horizontal_grid_lines: width,
      legend_class: "legend",
      legend_range: [0,100],
      line_stroke_width: "2px",
      show_legend_tooltip: "yes",
      legend_toggle_opacity: "no",
      legend_text: "yes",
      sample_id_order: dataset_data["sampleTypeDisplayOrder"],
      sample_id_list: sample_id_list,

     //default number of colours iis 39 (before it reitterates over it again
      number_of_colours: 39,
      //2 is the chosen padding. On either side there will be padding = to the interval between the points
      //1 gives 1/2 the interval on either side etc.
      padding: 2,
      probe_count: probe_count,
      axis: "top",
      sample_id_count: sample_count,
      probes: probes,
      line_groups: line_groups,
      num_sample_types: line_group_count,
      // Can fit 4 subtitles currently
      subtitles: [subtitle1],
      stroke_width:"3px",
      stroke_width_for_line : "2px",
      stroke_width_num: 3,
      target: target,
      title: main_title,
      title_class: "title",
      tip: tip,//second tip to just display the sample type
      tooltip: tooltip, // using d3-tips
      //tooltip1: tooltip1, // using d3-tips unique_id: "chip_id",
      watermark:"http://www.stemformatics.org/img/logo.gif",
      x_axis_text_angle:-45,
      x_axis_title: "Line Groups",
      x_column: 'Line_Group_ID',
      x_middle_title: 500,
      y_axis_title: dataset_data["yAxisLabel"],
      y_column: 'Expression_Value'
  }

   var instance = biojsvislinegraph(options);

   // Get the d3js SVG element
   var tmp = graphDiv;
   var svg = tmp.getElementsByTagName("svg")[0];
   // Extract the data as SVG text string
   var svg_xml = (new XMLSerializer).serializeToString(svg);

}
