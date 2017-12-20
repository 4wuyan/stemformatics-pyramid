/*
 Copyright 2015 Ariane Mora

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.


 This is a standalone unit to call when you want to create a box plot graph.

 */
/* global d3 */

var biojsvislinegraph;

module.exports = biojsvislinegraph = function (init_options)
{



/**
 * Sorts the sorted probe types by day state if necesary so that they can
 *  be grouped by both day state and probe on the x axis
 *  http://bl.ocks.org/phoebebright/raw/3176159/ for sorting
 * @param {type} graph
 * @returns {unresolved}
 */
    sort_x_by_probe_and_day_state = function (graph) {
        options = graph.options;
        //Check if there is an order given for the day states, if none given order by dataset
        if (options.probe_order !== 'none') {
            var day_state_order = options.day_state_order;
            var probe_order = options.probe_order;
            var nested_values = d3.nest()
                    .key(function (d) {
                        return d.Probe;
                    })
                    .sortKeys(function (a, b) {
                        return probe_order.indexOf(a) - probe_order.indexOf(b);
                    })
                    .key(function (d) {
                        return d.Day;//LineGraphGroup;
                    })
                    .sortKeys(function(a,b){return day_state_order.indexOf(a) - day_state_order.indexOf(b);})
                    .key(function (d) {
                        return d.LineGraphGroup; //Does this need to be sorted?
                    })
                    .entries(options.data);
        } else {
            var nested_values = d3.nest()
                    .key(function (d) {
                        return d.Probe;
                    })
                    .key(function (d) {
                        return d.Day;
                    })
                    .key(function (d) {
                        return d.LineGraphGroup;
                    })
                    .entries(options.data);
        }
        graph.nested_values = nested_values;
        return graph;
    };


/**
 *  Sorts the sorted probe types by linegraph group so that the line can be
 *  drawn correctly.
 *  http://bl.ocks.org/phoebebright/raw/3176159/ for sorting
 *  @param {type} graph
 *  @returns {unresolved}
 */
    sort_x_by_probe_and_linegroup = function (graph) {
        options = graph.options;
        sample_type_count = 0;
        //Check if there is an order given for the day states, if none given order by dataset
        if (options.probe_order !== 'none') {
            var line_order = options.line_group_order;
            var probe_order = options.probe_order;
            var nested_values = d3.nest()
                    .key(function (d) {
                        return d.Probe;
                    })
                    .sortKeys(function (a, b) {
                        return probe_order.indexOf(a) - probe_order.indexOf(b);
                    })
                    .key(function (d) {
                        return d.LineGraphGroup;
                    })
                    .sortKeys(function(a,b){return line_order.indexOf(a) - line_order.indexOf(b);})
                    .entries(options.data);
        } else {
            var nested_values = d3.nest()
                    .key(function (d) {
                        return d.Probe;
                    })
                    .key(function (d) {
                        return d.LineGraphGroup;
                    })
                    .entries(options.data);
        }
	    graph.nested_line_group = nested_values;
        return graph;
    };


    add_line = function (graph) {
        var options = graph.options;
        var nested_values = graph.nested_line_group;
        var stroke_width = graph.stroke_width_for_line;
        var scaleY = graph.scaleY;
        var colour_array = options.colour_array;
        var mapping = graph.multiple_sample_mapping;
        var prevday = 0;
        var svg = graph.svg;
        var day_order = options.day_state_order;
        var expression_values = [];
        for (var probe in nested_values) {
            var probe_name =  nested_values[probe].key;
            var values = nested_values[probe].values;
            for (var lg in values) {
                var linegroup = values[lg].key;
                var lg_values = [];
                var temp_lg_values = values[lg].values;
                // only non NaN values will be passed
                for(i=0; i < temp_lg_values.length; i++ ) {
                  if(temp_lg_values[i].Expression_Value == temp_lg_values[i].Expression_Value) {
                    lg_values.push(temp_lg_values[i])
                  }

                }
                // For each itteration we want the first day to be drawn when
                // it is connected to the next day
                prevday = 0;
                for (var s in lg_values) {
                    var sample = lg_values[s];
                    var day = sample.Day;

                    if (! isNaN(sample.Expression_Value)) {
                        if (day != prevday && prevday != 0) {
                            var prev_sample = lg_values[s - 1];
                            if (day_state_order.indexOf(sample.Day) -
                                     day_state_order.indexOf(prev_sample.Day) == 1) {
                                var x1 = get_x_value(graph, prev_sample);
                                var x2 = get_x_value(graph, sample);
                                var y1 = mapping[probe_name + prevday + linegroup + prev_sample.Replicate_ID];
                                var y2 = mapping[probe_name + day + linegroup + sample.Replicate_ID];
                                if (y1 == undefined || isNaN(y1)) {
                                    y1 = prev_sample.Expression_Value;
                                }
                                if (y2 == undefined || isNaN(y2)) {
                                    y2 = sample.Expression_Value;
                                }
                                /* If either produce an NaN result don't draw
                                 * the line*/
                                if (isNaN(y1) || isNaN(y2)) {
                                    y1 = 0;
                                    y2 = 0;
                                }
                                svg = add_scatter_line(svg, colour_array[linegroup], x1, x2, scaleY(y1),
                                    scaleY(y2), stroke_width);
                            }
                        }
                      prevday = day;
                  }
                }
            }
        }
        graph.svg = svg;
        return graph;
    }

    /**
     * Main function for setting up the line graph
     * itterates through the sorted values and for each probe; then for each
     * line group within each probe group (i.e. if this is the chosen option)
     * creates the line and scatter points
     * @param {type} graph
     * @returns {biojsvislinegraph.setup_line_graph.graph}
     */
    setup_line_graph = function (graph) {
        var options = graph.options;
        var nested_values = graph.nested_values;
        var stroke_width = options.stroke_width;
        var box_width = options.box_width;
        var box_width_wiskers = box_width / 2;
        var scaleY = graph.scaleY;
        var colour_array = options.colour_array;
        var sample_id_names = [];
        var expresion_vals = [];
        var multiple_sample_mapping = {};
        if (options.sort_by_sample_id === "no") {
            for (var probe in nested_values) {
                var row = nested_values[probe];
                var values = row.values;
                var probe_name = row.key;
                var probe_num = parseInt(probe);
                for (var d in values) {
                    // These are the expression values for a specific sample grouped by the probe
                    // then the day type so now we need to append all the expression values for this
                    // group then calculate the box plot and draw the values
                    var dayrow = values[d];
                    var days = dayrow.values;
                    day = dayrow.key;
                    for (var lg in days) {
                        var linevals = days[lg].values;
                        var linegroup = days[lg].key;
                        var x_buff = get_x_value(graph, linevals[0]);
                        var colour = colour_array[linegroup];
                        //for (var val in linevals) {
                        if (linevals.length != 1) {
                            //Need to add each of the sample values to the list
                            //so that the name can be added to the scatter
                            //tooltip
                            sample_id_names = [];
                            expression_vals = [];
                            for (var val in linevals) {
                                if (! isNaN(linevals[val].Expression_Value) ) {
                                    sample_id_names.push(linevals[val].Replicate_ID);
                                    expression_vals.push(linevals[val].Expression_Value);
                                }
                            }
                            if (expression_vals.length != 0) {

                                var scatter_tooltip = make_scatter_tooltip(probe_name,
                                    linegroup, day, sample_id_names, sample_id_names, "Day: ");
                                var bar_vals = calculate_error_bars(expression_vals);
                                var tooltip_box = "none";
                                svg = add_line_to_box(stroke_width, x_buff - box_width_wiskers /2, box_width / 2,
                                    bar_vals[0], svg, scaleY, colour, box_width_wiskers / 2, undefined, graph,tooltip_box);
                                //Add max line
                                svg = add_line_to_box(stroke_width, x_buff - box_width_wiskers/2, box_width / 2,
                                        bar_vals[2], svg, scaleY, colour, box_width_wiskers / 2, undefined, graph,tooltip_box);
                                //Add median lines

                                svg = add_vertical_line_to_box(stroke_width, x_buff, bar_vals[0],
                                        bar_vals[2], svg, scaleY, colour,graph,tooltip_box);
                                svg = add_single_scatter(bar_vals[1], x_buff, graph, scatter_tooltip,
                                    linegroup);
                                // We need to add each of the sample id's to the
                                // mapping so that when we draw the line to them
                                // the line goes to the condensed point
                                for (var st in sample_id_names) {
                                    multiple_sample_mapping[probe_name + day + linegroup + sample_id_names[st]] = bar_vals[1];
                                }
                            }
                        } else if (! isNaN(linevals[0].Expression_Value)) {
                            var scatter_tooltip = make_scatter_tooltip(probe_name,
                                linegroup, day, linevals[0].Sample_Type,
                                    linevals[0].Replicate_ID, "Day: ");
                            svg = add_single_scatter(linevals[0].Expression_Value, x_buff,
                                    graph, scatter_tooltip, linegroup);
                        }
                    }
                }
            }
        } else {
            data = options.data;
            if (options.sample_id_order !== "none") {
                sample_order = options.sample_id_order;
                data.sort(function (a, b) {
                    return sample_order.indexOf(a.Replicate_ID) - sample_order.indexOf(b.Replicate_ID);
                });
            } else {
                data.sort(function (a, b) {
                    return a.Replicate_ID.localeCompare(b.Replicate_ID);
                });
            }
            id_size = options.width / data.length;
            scale_x = d3.scale.ordinal()
                    .rangePoints([id_size / 2, options.width - id_size / 2]); //No padding for now
            scale_x.domain(options.sample_id_list);
            graph.scale_x = scale_x;
            graph.id_size = id_size;
            graph = add_scatter_for_sample_ids(data, graph, options.colour, scale_x);
            if(options.include_day_x_axis === "yes"){
              graph = setup_extra_labels(graph, scale_x, 0);
            }
        }
        graph.multiple_sample_mapping = multiple_sample_mapping;
        //graph.line_group_list = line_group_list;
        return graph;
    };
    /**
     * Adds a single scatter point
     * @param {non-scaled Expression value from the data} y_value
     * @param {scaled int based on which day it is} x_value
     * @param {object} graph
     * @param {string colour} colour
     * @param {tooltip} scatter_tooltip
     * @param {which group it belongs to, from the data} LineGraphGroup
     * @returns {nm$_index.svg|type.nm$_index.svg}
     */
    add_single_scatter = function (y_value, x_value, graph, scatter_tooltip, LineGraphGroup) {
        options = graph.options;
        radius = options.radius;
        scaleY = graph.scaleY;
        if (scatter_tooltip !== null) {
            svg.call(scatter_tooltip);
        }
        svg.append("circle")
                .attr("class", function (d) {
                    //adds the sample type as the class so that when the sample type is overered over
                    //on the x label, the dots become highlighted
                    return "sample-type-" + LineGraphGroup;
                })
                .attr("r", radius) //radius 3.5
                .attr("cx", x_value)
                .attr("cy", scaleY(y_value))
                .style("stroke", options.background_stroke_colour)
                .style("stroke-width", "1px")
                .style("fill", function (d) {
                        return options.colour_array[LineGraphGroup];
                    } )
                .attr("opacity", 0.8)
                .on('mouseover', scatter_tooltip.show)
                .on('mouseout', scatter_tooltip.hide);
        return svg;

    };

    make_day_label_tooltip = function () {
        var tooltip_label = d3.tip()
                .attr('class', 'd3-tip')
                .offset([150,-50])
                .html(function (d) {
                    temp =
                             d.substring(d.lastIndexOf('-') + 1) + "<br/>";
                    return temp;
                });
        return tooltip_label;
    };

    /**
     * Function to setup day labels
     */
  /**
     * Prepares the data for the x axis and adds the labels to the x axis
     * This is to make the sample types replace the sample ids
     * Height offset is used if we are havig a second set of labels
     * Label_num tells us whether it is the first or second label for placement
     * and knowing which label we are using
     */
    setup_day_labels = function (graph, height_offset, class_name, collective_name, label_num) {
        svg = graph.svg;
        var map = graph.name_mapping_with_space;
        page_options = graph.page_options;
        options = graph.options;
        var vertical_lines = graph.multi_xaxis_list;
        var tip = make_day_label_tooltip();
        svg.call(tip);
        // handle gaps between samples oin the x axis
        // in the same function you want to store the padding
        // and you want to calculate that last padding too
        var num_lines = vertical_lines.length;
        //vertical_lines = graph.multi_xaxis_list;//graph.vertical_lines;
        var multi_scaleX = graph.multi_scaleX;
        var info;
        svg.selectAll(class_name)  // text for the xaxes - remember they are on a slant
                .data(vertical_lines).enter()
                .append("text") // when rotating the text and the size
                .text(
                  function(d,i){
                        // this gets the day name from the string 'probename-day'  and can handle any number of hyphen in probename
                        var day =  d.substring(d.lastIndexOf('-') + 1);
                        return day;
                })
                .attr("class", "x_axis_diagonal_labels")
                .style("text-anchor", "end")
                .attr("id", function(d) {
                    //return "xLabel-" + d.label1;
                    /* This is used during testing to check the correct sample
                    * is displayed */
                })
                // Even though we are rotating the text and using the cx and the cy, we need to
                // specify the original y and x
                .attr("y", page_options.height + height_offset)
                .attr("x",
                        function (d, i) {
                            var x_value = multi_scaleX(map[d]);
                            return x_value;
                        }
                ) // when rotating the text and the size
                .style("font-family", options.font_style)
                .style("font-size", options.text_size)
                .attr("transform",
                        function (d, i)  {
                            var x_value = multi_scaleX(map[d]);
                            var y_value = page_options.height + height_offset;
                            return "rotate(" + options.x_axis_text_angle + "," + x_value + "," + y_value + ")";
                        }
                )
                /* Sets up the tooltips to display on the mouseover of the sample type label. This tooltip
                 changes the scatter points (increases the size and changes the opacity.
                 Note: due to stange sample type names (i.e. having unagreeable characters) it assigns
                 a number to each sample type and calls this rather than the sample type name.
                 This is set up in simple.js and saves in array options.sample_types where the key
                 is the sample type */
                .on('mouseover', function(d) {
                                    var day =  d.substring(d.lastIndexOf('-') + 1);
                                    var tooltip_label = d3.select('body').append("div").attr("id","x-axis-tooltip").attr("class","d3-tip").text(day).style("left", (d3.event.pageX -50) + "px").style("top", (d3.event.pageY - 50) + "px").style("display", "inline").style("opacity","1")   ;return tooltip_label})
                .on('mouseout', function(d) { $('#x-axis-tooltip').remove()});

        graph.svg = svg;
        return graph;
    }; // setup_x_axis_using_sample_types



    /**
     * Test function
     * @param {type} name
     * @param {type} box_plot_vals
     * @param {type} graph
     * @param {type} options
     * @returns {undefined}
     */
    test_values = function (name, box_plot_vals, graph, options) {
        //var fs = require('fs');
        //name in format as saved by stemformatics: name, average. standard deviation, min, max, median, Q1, Q3
        row = name + "," + 0 + "," + 0 + "," + box_plot_vals[0] + "," + box_plot_vals[4] + "," + box_plot_vals[2] + "," + box_plot_vals[1] + "," + box_plot_vals[3];
        if (options.bar_graph === "yes") {
            row = name + "," + box_plot_vals[1] + "," + 0 + "," + box_plot_vals[0] + "," + box_plot_vals[2] + "," + 0 + "," + 0 + "," + 0;
        }
    };

    get_type = function (data_point) {
        return data_point;
    }

    /**
     * MAIN FUNCTION FOR SETTING UP THE GRAPH
     * @param {type} graph
     * @returns {biojsvislinegraph.setup_graph.graph}
     */
    setup_graph = function (graph) {
	    graph.graph_type = "Line Graph";
        // setup all the graph elements
        var class_name = ".probe_text";
        var collective_name = ".probe-"; // used to show hover over name
        options = graph.options;
        var label_padding = options.x_axis_label_padding; // For if there are 2 sets of labels
        graph = setup_margins(graph);
        graph = setup_svg(graph);
        if (options.sort_by_sample_id === "no") {
            graph = sort_x_by_probe_and_day_state(graph);
        }
        graph = sort_x_by_probe_and_linegroup(graph);
        // Check if it is also being sorted by the day state on the x axis
        graph = setup_x_axis(graph, options.x_axis_list);
        graph = setup_data_for_x_axis(graph);
	    //In axis.js
	    //vertical_lines = options.x_axis_list;
        graph = setup_day_labels(graph, label_padding, class_name, collective_name, 1);
	label_padding = label_padding - 100; // this if for top axis on graph
	graph = setup_x_axis_labels(graph, null, label_padding , class_name, collective_name, 1);
        graph = setup_x_axis_labels(graph, null, label_padding , ".hidden-probe_text", collective_name, 1);
        // label_padding = label_padding + 100;

        //graph = //setup_probe_labels(graph);
        graph = setup_y_axis(graph);
        graph = setup_line_graph(graph);
        graph = add_line(graph);
        graph = setup_vertical_lines(graph);
        // Only display the vertical lines if the user chooses so
        if (options.display.vertical_lines === "yes") {
            graph = setup_vertical_lines(graph);
        }
        graph =  setup_watermark(graph);
        //graph =  setup_hover_bars(graph);
        // Display the legend if the user has specified they want the legend
        if (options.display.legend === "yes") {
            graph = setup_D3_legend(graph, options.legend_list);
        }
        if (options.display.horizontal_lines === "yes") {
            graph = setup_horizontal_lines(graph);
        }
        return graph;

    };  // end setup_graph

    // run this right at the start of the initialisation of the class
    init = function (init_options) {
        var options = default_options();
        options = init_options;
        page_options = {}; // was new Object() but jshint wanted me to change this
        var graph = {}; // this is a new object
        graph.options = options;
        graph = preprocess_lines(graph);
        graph = setup_graph(graph);
        var target = $(options.target);
        target.addClass('line_graph');
        svg = graph.svg;
        options.test_graph = graph;
    };

    // constructor to run right at the start
    init(init_options);
};
