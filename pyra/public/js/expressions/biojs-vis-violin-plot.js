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

var biojsvisviolingraph;

module.exports = biojsvisviolingraph = function (init_options)
{

    // Sorts the sorted probe types by sample_type state if necesary so that they can
    // be grouped by both sample_type state and probe on the x axis
    // http://bl.ocks.org/phoebebright/raw/3176159/ for sorting
    sort_x_by_probe_and_sample_type = function (graph) {
        options = graph.options;
        var sort_by_options = graph.options.sortByOption.split(',');
        //Check if there is an order given for the sample_type states, if none given order by dataset
        if (options.probe_order !== 'none') {
             if(sort_by_options.length != 1){
               sample_type_order = options.sample_type_order;
               probe_order = options.probe_order;
               nested_values = d3.nest()
                   .key(function(d) {
                       return d.Probe;
                   })
                   .sortKeys(function(a, b) {
                       return probe_order.indexOf(a) - probe_order.indexOf(b);
                   })
                   .key(function (d) {
                        var value = sort_by_options[0];
                        return d[value];
                   })
                   .key(function(d) {
                        var value = sort_by_options[1];
                        return d[value];
                   })
                    // Are we always going to be supplied a sample type
                    // ordering?
                   .sortKeys(function(a,b){return sample_type_order.indexOf(a)
                        - sample_type_order.indexOf(b);})
                   .entries(options.data);
             }
             else {
               if(sort_by_options[0] != "Sample_Type") {
                 probe_order = options.probe_order;
                  nested_values = d3.nest()
                          .key(function(d) {
                              return d.Probe;
                          })
                          .sortKeys(function(a, b) {
                            // change sdone by ISha to correct probe order
                              return probe_order.indexOf(a) - probe_order.indexOf(b);
                          })
                          .key(function (d) {
                                var value = options.sortByOption;
                                return d[value];
                          })
                          .entries(options.data);
                }
                else {
                   sample_type_order = options.sample_type_order;
                   probe_order = options.probe_order;
                   nested_values = d3.nest()
                           .key(function (d) {
                               return d.Probe;
                           })
                           .sortKeys(function (a, b) {
                               return probe_order.indexOf(a) - probe_order.indexOf(b);
                           })
                           .key(function (d) {
                               return d.Sample_Type;
                           })
                           .sortKeys(function(a,b){return sample_type_order.indexOf(a) - sample_type_order.indexOf(b);})
                           .entries(options.data);
                 }
            }
        }
        // Do we really want this as an option if the probe order isn't given?
        else {
            if (options.multi_option != 1) {
               nested_values = d3.nest()
                   .key(function(d) {
                       return d.Probe;
                   })
                   .sortKeys(function(a, b) {
                       return probe_order.indexOf(a) - probe_order.indexOf(b);
                   })
                   .key(function (d) {
                        var value = sort_by_options[0];
                        return d[value];
                   })
                   .key(function(d) {
                        var value = sort_by_options[1];
                        return d[value];
                   })

            } else {
            nested_values = d3.nest()
                    .key(function (d) {
                        return d.Probe;
                    })
                    .key(function (d) {
                        return d[sort_by_options[0]];
                    })
                    .entries(options.data);
            }
        }
        graph.nested_values = nested_values;
        return graph;
    };


    /*------------------------------Box plot Calculations--------------------------------------*/
    /* Sets up the box plot */
    setup_line_graph = function (graph) {
        sample_types_with_colour = {};
        shrink_radius = false;
        options = graph.options;
        probe_size = graph.size_of_probe_collumn;
        sample_type_size = graph.size_of_sample_type_collumn;
        nested_values = graph.nested_values;
        line_group_list = [];
        sample_type_list = [];
        violin_data_array = {}; // this will have all the values that creates scatter points
        violin_path_array_min = {}; // this will have values that will draw outer line of violin plot for left side
        violin_path_array_max = {}; // this will have values that will draw outer line of violin plot for right side

        for(var j=0; j< options.probe_list.length; j++) { // for each probe we create an object with probe_name as key, that will hold the values for all sample types for that probe
          violin_data_array[options.probe_list[j]]={};
          violin_path_array_min[options.probe_list[j]]={};
          violin_path_array_max[options.probe_list[j]]={};
          for(var i=0; i<options.sample_type_order.split(",").length; i++) {
            var sample_type = options.sample_type_order.split(",")[i];
              violin_data_array[options.probe_list[j]][sample_type] = [];
              violin_path_array_min[options.probe_list[j]][sample_type] = [];
              violin_path_array_max[options.probe_list[j]][sample_type] = [];
          }
        }

        probe = null;
        line_groups = null;
        legend_name_array = [];
        var buffer = 20;
        var multi_scale = graph.multi_scaleX;
        var scale_x;
        var sort_option_list = options.sortByOption.split(",");
        var sort_option = sort_option_list[0];
        var samples = [];
        if (options.multi_group != 1) {
            sort_option = sort_option_list[1];
        }
        var map = graph.name_mapping;

        for(j=0;j<nested_values.length;  j++) {
          for(k=0;k< nested_values[j].values.length;k++){
            if ($.inArray(nested_values[j].values[k].key, sample_type_list) == -1) {
                sample_type_list.push(nested_values[j].values[k].key);
            }
          }
        }
        for (probe in nested_values) {
            row = nested_values[probe];
            values = row.values;
            var probe_name = row.key;
            probe_num = parseInt(probe);

            violin_data_array[probe_name]={}
            violin_path_array_min[probe_name]={}
            violin_path_array_max[probe_name]={}

            if (options.multi_group != 1) {
              for (var i in values) {
                    row = values[i];
                    primary_grouping = row.values;
                    primary_group = row.key;
                    number_secondary_groups = primary_grouping.length;

                    violin_data_array[probe_name][primary_group] = {};
                    violin_path_array_min[probe_name][primary_group] = {};
                    violin_path_array_max[probe_name][primary_group] = {};

                    for (var p in primary_grouping) {
                    j = parseInt(p);
                    row_s = primary_grouping[j];
                    secondary_grouping = row_s.values;
                    secondary_group = row_s.key;
                    number_samples = secondary_grouping.length;

                    violin_data_array[probe_name][primary_group][secondary_group] = [];
                    violin_path_array_max[probe_name][primary_group][secondary_group] = [];
                    violin_path_array_min[probe_name][primary_group][secondary_group] = [];

                    var x_buffer = multi_scale(map[remove_chars(probe_name + "-" +
                         secondary_group + "-" + primary_group)]);
                    if (j != 0) {
                        var prev_grp = primary_grouping[j - 1];
                        var min = multi_scale(map[remove_chars(probe_name + "-" +
                              prev_grp.key + "-" + primary_group )]);
                    } else {
                        var min = 0;
                    }
                    if (j != number_secondary_groups - 1) {
                        var nxt_grp = primary_grouping[j + 1];
                    var max = multi_scale(map[remove_chars(probe_name + "-" +
                         nxt_grp.key + "-" + primary_group)]);
                    } else {
                        max = options.width;
                    }
                    sample_type_list = [];
                    for (var s in secondary_grouping) {
                        if((secondary_grouping[s].Expression_Value ==
                                secondary_grouping[s].Expression_Value) &&
                                    ((secondary_grouping[s].Expression_Value).toString()!=
                                        dataset_data["detectionThreshold"])) {
                            samples.push(secondary_grouping[s])
                            sample_type_list.push(secondary_grouping[s][sort_option]);
                          }
                    }
                    min = x_buffer - (x_buffer - min)/2;
                    max = x_buffer + (max - x_buffer)/2;
                  // These are the expression values for a specific sample grouped by the probe
                  // then the sample_type type so now we need to append all the expression values for this
                  // group then calculate the box plot and draw the values
  /*                  for (line_groups in second_sort_by_values) {
                      if($.inArray(second_sort_by_values[line_groups].key, legend_name_array) == -1) {
                          legend_name_array.push(second_sort_by_values[line_groups].key);
                      }
                        srow = second_sort_by_values[line_groups];
                        samples = srow.values;
                        new_samples = [];
                        for(i=0; i < samples.length; i++ ) {
                          if((samples[i].Expression_Value == samples[i].Expression_Value) && ((samples[i].Expression_Value).toString()!= dataset_data["detectionThreshold"])) {
                            new_samples.push(samples[i])
                          }
                        }
                        line_group = srow.key;

                        for(j=0; j<legend_name_array.length; j++ ) {
                          if(!sample_types_with_colour[legend_name_array[j]])
                          {sample_types_with_colour[legend_name_array[j]] = options.colour[colour_count];
                          if(colour_count < options.colour.length) {colour_count++;}
                          else {colour_count = 0;}}
                        }
*/
                        if(samples.length != 0) {
                          // Actually draw the box plot ons the graph
                          //Setup the scatter line once all the points have been placed
                          graph = setup_scatter_line(graph, probe_num, x_buffer, samples, probe_name, secondary_group, min, max, sort_option,primary_group);
                        }

                      }
                }
                // this will create scatter
                    for (var i in values) {
                      var row = values[i];
                      var primary_grouping = row.values;
                      var primary_group = row.key;
                      for (var p in primary_grouping) {
                          var j = parseInt(p);
                          var row_s = primary_grouping[j];
                          var secondary_group = row_s.key;
                          add_scatter_and_path(probe_name, secondary_group,primary_group)
                     }
                  }
            }

            else {
                for (line_groups in values) {
                  var primary_group = "";
                  if($.inArray(values[line_groups].key, legend_name_array) == -1) {
                      legend_name_array.push(values[line_groups].key);
                  }
                    // These are the expression values for a specific sample grouped by the probe
                    // then the sample_type type so now we need to append all the expression values for this
                    // group then calculate the box plot and draw the values
                    srow = values[line_groups];
                    samples = srow.values;
                    new_samples = [];
                    var x_buffer =  multi_scale(map[remove_chars(probe_name + "-" + samples[0][sort_option])]);
                    for(i=0; i < samples.length; i++ ) {
                      if((samples[i].Expression_Value == samples[i].Expression_Value) && ((samples[i].Expression_Value).toString()!= dataset_data["detectionThreshold"])) {
                        new_samples.push(samples[i])
                      }
                    }
                    line_group = srow.key;
                    for(j=0; j<legend_name_array.length; j++ ) {
                      if(!sample_types_with_colour[legend_name_array[j]])
                      {sample_types_with_colour[legend_name_array[j]] = options.colour[colour_count];
                      if(colour_count < options.colour.length) {colour_count++;}
                      else {colour_count = 0;}}
                    }
                    if (line_groups != 0) {
                    var mid =  multi_scale(map[remove_chars(probe_name + "-" + samples[0][sort_option])]);
                    var min = multi_scale(map[remove_chars(probe_name + "-" + values[parseInt(line_groups) - 1].key)]);

                    } else {
                        min = 0;
                    }
                    if (line_groups != values.length - 1) {
                        var max = multi_scale(map[remove_chars(probe_name + "-" + values[parseInt(line_groups) + 1].key)]);
                    } else {
                        max = options.width - buffer;
                    }

                    min = x_buffer - (x_buffer - min)/2;
                    max = x_buffer + (max - x_buffer)/2;

                    violin_data_array[probe_name][line_group] = [];
                    violin_path_array_min[probe_name][line_group] = [];
                    violin_path_array_max[probe_name][line_group] = [];

                if(new_samples.length != 0) {
                      // Actually draw the box plot ons the graph
                      //Setup the scatter line once all the points have been placed
                      graph = setup_scatter_line(graph, probe_num, x_buffer, new_samples,
                        probe_name, line_group, min, max, sort_option,primary_group);
                    }

                  }
                  // this will create scatter
                      for (line_groups in values) {
                        var srow = values[line_groups];
                        var samples = srow.values;
                        var line_group = srow.key;
                        add_scatter_and_path(probe_name, line_group,primary_group)
                      }

            }
            // if (options.include_sample_type_x_axis === "yes" && options.display.x_axis_labels === "yes") {
            //     graph = setup_extra_labels(graph, scale_x);
            // }
        }
        graph.line_group_list = line_group_list;
        return graph;
    };
    add_scatter_and_path = function(probe_name, line_group,primary_group) {
      if(shrink_radius == true) {radius = options.radius * estimated_shrink;}
        if(options.multi_group == 1) {
          var violin_data = violin_data_array[probe_name][line_group];
          var violin_path_min = violin_path_array_min[probe_name][line_group];
          var violin_path_max = violin_path_array_max[probe_name][line_group];
              }
        else {
          var violin_data = violin_data_array[probe_name][primary_group][line_group];
          var violin_path_min = violin_path_array_min[probe_name][primary_group][line_group];
          var violin_path_max = violin_path_array_max[probe_name][primary_group][line_group];
        }

        if((options.sortByOption.split(',')[0] == 'Sample_Type' || options.sortByOption.split(',')[1] == 'Sample_Type'))
          {colour = options.colour;} // this is when sample type is legend and colour is gradient
        else
          {colour = options.colour_array;}

        for(var j=0; j<violin_data.length; j++) {
              //add scatter
              svg = add_scatter(
                    violin_data[j]['interpolate_min_values'],
                    violin_data[j]['interpolate_max_values'],
                    violin_data[j]['current_samples'],
                    violin_data[j]['graph'],
                    violin_data[j] ['colour'],
                    violin_data[j]['centreX'],
                    0,
                    violin_data[j]['tooltip'],
                    violin_data[j]['sample_count'],
                    violin_data[j]['min'],
                    violin_data[j]['max'],
                    line_group,
                    probe_name,
                    primary_group);
          }

          // sorting points for path
          (violin_path_min).sort(function (a, b) {
              return a.y - b.y;
          });
          (violin_path_max).sort(function (a, b) {
              return a.y - b.y;
          });
          // appending path
          svg.append("path")
                  .attr("d", line(violin_path_min))
                  // .attr("d", line(interpolate_min_values))
                  .attr("stroke", colour[line_group])//"black")
                  .style("stroke-width", options.stroke_width)
                  .style("fill", "none");

          svg.append("path")
                  .attr("d", line(violin_path_max))
                  // .attr("d", line(interpolate_min_values))
                  .attr("stroke", colour[line_group])//"black")
                  .style("stroke-width", options.stroke_width)
                  .style("fill", "none");
    }
    add_scatter_for_sample_ids = function (scatter_values, graph, colour, scale_x) {
        options = graph.options;
        radius = options.radius;
        svg = graph.svg;
        scaleY = graph.scaleY;
        tooltip = options.tooltip;
        svg.call(tooltip);
        probe_count = 0;
        var line_scale = graph.multi_axis_scale;
        svg.selectAll(".dot") // class of .dot
                .data(scatter_values) // use the options.data and connect it to the elements that have .dot css
                .enter() // this will create any new data points for anything that is missing.
                .append("circle") // append an object circle
                .attr("class", function (d) {
                    //adds the sample type as the class so that when the sample type is overered over
                    //on the x label, the dots become highlighted
                    return "sample-type-" + d.LineGraphGroup;
                })
                .attr("r", radius) //radius 3.5
                .attr("cx", function (d) {

                    var cx = scale_x(d.Replicate_ID);
                    return cx;
                })
                .attr("cy", function (d) {
                    // set the y position as based off y_column
                    // ensure that you put these on separate lines to make it easier to troubleshoot
                    var cy = 0;
                    cy = scaleY(d.Expression_Value);
                    return cy;
                })
                .style("stroke", options.background_stroke_colour)
                .style("stroke-width", "1px")
                .style("fill", function (d) {
                    return options.colour_array[d.Sample_Type];
                })
                .attr("opacity", 0.8)
                .on('mouseover', tooltip.show)
                .on('mouseout', tooltip.hide);

        graph.svg = svg;
        return graph;
    };

    add_scatter = function (interpolate_min_values, interpolate_max_values, scatter_values, graph, colour, x_buffer, y_value_if_error, scatter_tooltip, sample_count, min, max,sample_name,probe_name,primary_group) {
        options = graph.options;
        svg = graph.svg;
        scaleY = graph.scaleY;
        svg.call(scatter_tooltip);
        //ariane: calculates the x value
        var centre_x = x_buffer;//get_x_value(graph, scatter_values[0]);
        toggle_count_odd = 1;
        toggle_count_even = 0;
        var cx = 0;
        var loc_max = 0;
        var loc_min = max;

        svg.selectAll(".dot") // class of .dot
                .data(scatter_values) // use the options.data and connect it to the elements that have .dot css
                .enter() // this will create any new data points for anything that is missing.
                .append("circle") // append an object circle
                .attr("id", function (d) {
                        return d.Replicate_ID;
                    })
                .attr("class", function (d) {
                    //adds the sample type as the class so that when the sample type is overered over
                    //on the x label, the dots become highlighted
                    return "sample-type-" + d.LineGraphGroup;
                })
                .attr("cx", function (d, i) {
                    if(d.Expression_Value == d.Expression_Value)
                      {
                       /* if (options.sortByOption.split(",").length == 1) {
                            centreX = line_scale(remove_chars(d.Probe + "-" + d.Disease_State + "-" + d.Sample_Type));
                        } else {
                            centreX = line_scale(remove_chars(d.Probe + "-" + d.Sample_Type));
                        }*/
                            // if (i % 2 === 0 && loc_max < max) {
                            if (i % 2 === 0 ) {
                              cx = centre_x + (radius * toggle_count_even);
                              loc_max = cx;
                              toggle_count_even++;

                              //temp = {x: cx, y: scaleY(d.Expression_Value)};
                              //graph.interpolate_values.push(temp);
                            // } else if (i % 2 === 1 && loc_min > min){
                            } else if (i % 2 === 1){
                              cx = centre_x - (radius * toggle_count_odd);
                              loc_min = cx;
                              toggle_count_odd++;
                              // temp = {x: cx, y: scaleY(d.Expression_Value)};
                              // graph.interpolate_values.push(temp);
                          }
                            return cx;
                        }
                        else {
                          return;
                        }
                })
                .attr("r", function(d){if(d.Expression_Value == d.Expression_Value ){
                              return radius;
                            }
                            else {
                              return 0;
                            }}) //radius 3.5
                .attr("cy", function (d) {
                    // set the y position as based off y_column
                    // ensure that you put these on separate lines to make it easier to troubleshoot
                    var cy = 0;
                    if (y_value_if_error === 0) {
                        if(d.Expression_Value == d.Expression_Value) {
                          cy = scaleY(d.Expression_Value);
                        }
                        else {
                          return;
                        }
                    } else {
                        cy = scaleY(y_value_if_error);
                    }
                    return cy;
                })
                .style("stroke", options.background_stroke_colour)
                .style("stroke-width", "1px")
                .style("fill", function(d) {
                        return colour;
                    })
                .attr("opacity", 0.8)
                .on('mouseover', scatter_tooltip.show)
                .on('mouseout', scatter_tooltip.hide);

        if (scatter_values.length > 1) {
            len = scatter_values.length - 1;
            temp1 = {x: centre_x - (radius * toggle_count_odd) - (radius * 2), y: scaleY(scatter_values[len].Expression_Value)};
            interpolate_min_values.push(temp1);

            temp2 = {x: centre_x + (radius * toggle_count_odd) + (radius * 2), y: scaleY(scatter_values[len].Expression_Value)};
            interpolate_max_values.push(temp2);
            if (options.multi_group != 1) {
              violin_path_array_min[probe_name][primary_group][sample_name].push(temp1);
              violin_path_array_max[probe_name][primary_group][sample_name].push(temp2);
            }
            else {
              violin_path_array_min[probe_name][sample_name].push(temp1);
              violin_path_array_max[probe_name][sample_name].push(temp2);
            }
        }
        return svg;
    };


    setup_scatter_line = function (graph, probe_num, x_buffer, sample_values, probe_name,
                sample_name, min, max, sort_option,primary_group) {
        options = graph.options;
        radius = options.radius;
        samples = sample_values;
        scaleY = graph.scaleY;
        radius = options.radius;
        max_samples = (options.width/ (options.probe_count *options.sample_type_count))/options.radius;
        tooltip = make_scatter_tooltip(probe_name, sample_name, primary_group, sort_option);
        interpolate_min_values = [];
        interpolate_max_values = [];
        colour = {};
        if((options.sortByOption.split(',')[0] == 'Sample_Type' || options.sortByOption.split(',')[1] == 'Sample_Type'))
          {colour = options.colour[sample_name];} // this is when sample type is legend and colour is gradient
        else
          {colour = options.colour_array[sample_name];} // this when tissue, gender etc is present and we do not need gradient
        //get scaled x value
        var centreX = x_buffer;//get_x_value(graph, sample_values[0]);
        //
        rad = options.level_of_overlap;
        // changes done by Isha
        if(rad > options.y_axis_largest_value) {rad = rad/200 ;}
        current_samples = [];
        sample_count = 0;

        sample_values.sort(function (a, b) {
            return a.Expression_Value - b.Expression_Value;
        });
        lwr_l = {x: centreX, y: scaleY(sample_values[0].Expression_Value) + (2 * radius)};
        interpolate_min_values.push(lwr_l);
        interpolate_max_values.push(lwr_l);

        final_diff = 0;
        diff = 0; //Difference between the sample types expression values for each ID
        if(sample_values.length != 1) {
          for (i = 0; i < sample_values.length; i++) {
              current_samples.push(sample_values[i]);
              if (i === sample_values.length - 1) {
                  diff += Math.abs(sample_values[i].Expression_Value - sample_values[i - 1].Expression_Value);
              } else {
                  diff += Math.abs(sample_values[i].Expression_Value - sample_values[i + 1].Expression_Value);
              }

              if (diff < rad) {
                sample_count++;
              } else {
                // changes done by Isha for smaple type colour
                if (diff > (2 * rad)) {
                    if (i === sample_values.length - 1) {
                        yval = sample_values[i].Expression_Value;
                        final_diff = diff;
                    } else {
                        yval = sample_values[i + 1].Expression_Value;
                    }
                    tmp = {x: centreX, y: scaleY(yval) - (diff / 2)};
                    interpolate_min_values.push(tmp);
                    interpolate_max_values.push(tmp);
                }
                // svg = add_scatter(interpolate_min_values, interpolate_max_values, current_samples, graph, colour, centreX, 0, tooltip, sample_count, min, max);
                if(current_samples.length > max_samples){ // if number of samples in row is greater than what graph can hold
                  shrink_radius = true;
                  if (estimated_shrink == 0) { // when estimated_shrink is set for first time
                    estimated_shrink = max_samples/current_samples.length;
                    prev_estimated_shrink = estimated_shrink;
                  }
                  else { // check if prev_estimated_shrink is greater than current estimated_shrink
                    if(prev_estimated_shrink > (max_samples/current_samples.length)) {
                      estimated_shrink = max_samples/current_samples.length;
                      prev_estimated_shrink = estimated_shrink;
                    }
                    else {
                      estimated_shrink = prev_estimated_shrink;
                    }
                  }
                }
                  violin_data = {};
                  violin_data['interpolate_min_values'] =interpolate_min_values;
                  violin_data['interpolate_max_values'] =interpolate_max_values;
                  violin_data['current_samples'] =current_samples;
                  violin_data['graph'] =graph;
                  violin_data['colour'] =colour;
                  violin_data['centreX'] =centreX;
                  violin_data['tooltip'] =tooltip;
                  violin_data['sample_count'] =sample_count;
                  violin_data['min'] =min;
                  violin_data['max'] =max;
                  if (options.multi_group != 1) {
                    violin_data_array[probe_name][primary_group][sample_name].push(violin_data);
                  }
                  else {
                    violin_data_array[probe_name][sample_name].push(violin_data);
                  }
                  current_samples = [];
                  sample_count = 0;

                  diff = 0;
              }
          }
        }
        else {
            violin_data = {};
            violin_data['interpolate_min_values'] =interpolate_min_values;
            violin_data['interpolate_max_values'] =interpolate_max_values;
            violin_data['current_samples'] =sample_values;
            violin_data['graph'] =graph;
            violin_data['colour'] =colour;
            violin_data['centreX'] =centreX;
            violin_data['tooltip'] =tooltip;
            violin_data['sample_count'] =sample_count;
            violin_data['min'] =min;
            violin_data['max'] =max;
            if (options.multi_group != 1) {
              violin_data_array[probe_name][primary_group][sample_name].push(violin_data);
            }
            else {
              violin_data_array[probe_name][sample_name].push(violin_data);
            }
        }


        //----------------------NEED TO FIX THIS CURRENTLY ADDING LAST SCATTER SEPARATELY -----------------------
        len = sample_values.length - 1;
        //current_samples = [];
        //current_samples.push(sample_values[len]);
        line = d3.svg.line()
                .x(function (d) {
                    return d.x;
                })
                .y(function (d) {
                    return d.y;
                })
                .interpolate("basis");
        upr_l = {x: centreX, y: scaleY(sample_values[len].Expression_Value - (final_diff)) - (2 * rad)};
        interpolate_min_values.push(upr_l);
        interpolate_max_values.push(upr_l);
        interpolate_min_values.sort(function (a, b) {
            return a.y - b.y;
        });
        interpolate_max_values.sort(function (a, b) {
            return b.y - a.y;
        });
        if (options.multi_group != 1) {
          violin_path_array_min[probe_name][primary_group][sample_name] = (interpolate_min_values);
          violin_path_array_max[probe_name][primary_group][sample_name] = (interpolate_max_values);
        }
        else {
          violin_path_array_min[probe_name][sample_name] = (interpolate_min_values);
          violin_path_array_max[probe_name][sample_name] = (interpolate_max_values);
        }

        for (i in interpolate_max_values) {
            interpolate_min_values.push(interpolate_max_values[i]);
        }

        /*   svg.append("path")
         .attr("d", line(graph.interpolate_max_values))
         .attr("stroke", "black")
         .style("stroke-width","2")
         .style("fill", "none");
         */
        // svg.append("path")
        //         .attr("d", line(interpolate_min_values))
        //         .attr("stroke", colour)//"black")
        //         .style("stroke-width", options.stroke_width)
        //         .style("fill", "none");
                /*
                 .on("mouseover", function(data, i) {
                 if (options.legend_toggle_opacity !=="no") {
                 var leg = document.getElementById(data[i].Sample_Type);
                 if (leg.style.opacity !==0) {
                 d3.select(leg).style("opacity", 0);
                 } else {
                 d3.select(leg).style("opacity", 1);
                 }
                 }
                 });*/
        graph.svg = svg;
        return graph;
    };

    make_scatter_tooltip = function (probe, sample_type, second_sort_by, sort_option) {
        var tooltip_scatter = d3.tip()
                .attr('class', 'd3-tip')
                .offset([0, +110])
                .html(function (d) {
                    var probe_name_for_tooltip = options.probe_name_for_tooltip;
                    temp = probe_name_for_tooltip +": " + probe + "<br/>" ;
                    if ((sortBy == "Sample_Type") || (sortBy == "Sample Type") ||(options.sortByOption.split(",").length != 1)) {
                        temp = temp  + "Sample Type: " + sample_type + " ["+ sample_type_hover[sample_type] + "]";
                    }
                    if(options.sortByOption.split(",").length != 1) {
                            temp = temp + "State: " + second_sort_by;
                    }
                    return temp;
                });
        return tooltip_scatter;
    };

    sort_by_sample_type = function (data, sample_type_order) {
        if (sample_type_order !== "none") {
            data.sort(function (a, b) {
                return sample_type_order.indexOf(a.Sample_Type) - sample_type_order.indexOf(b.Sample_Type);
            });
        } else {
            //SORTING FOR LINEGRAPH
            data.sort(function (a, b) {
                return a.Sample_Type.localeCompare(b.Sample_Type);
            });
        }
        return data;
    };

    add_scatter_for_multiple_reps = function (graph, sample_types_with_replicates, colour, scale_x, scatter_tooltip, min, max) {
        svg = graph.svg;
        options = graph.options;
        box_width = options.box_width;
        box_width_wiskers = box_width / 2;
        scaleY = graph.scaleY;
        // Ariane: calculates the x val
        var x_buffer = get_x_value(graph, sample_types_with_replicates[0]);

        bar_vals = calculate_error_bars_violin(sample_types_with_replicates);
        // svg = add_line_to_box(options.stroke_width, x_buffer, box_width / 2, bar_vals[0], svg, scaleY, colour, box_width_wiskers / 2,"no", graph);
        //Add max line
        // svg =  (options.stroke_width, x_buffer, box_width / 2, bar_vals[2], svg, scaleY, colour, box_width_wiskers / 2,"no", graph);
        //Add median lines
        var tooltip_box = "none";
        svg = add_vertical_line_to_box(options.stroke_width, x_buffer, bar_vals[0], bar_vals[2], svg, scaleY, colour, tooltip_box);
        svg = add_scatter(sample_types_with_replicates, graph, colour, scale_x, bar_vals[1], scatter_tooltip, min, max);
//(options.stroke_width, x_buffer, box_width, box_plot_vals[1], svg, scaleY, colour_wiskers, box_width_wiskers);
        graph.svg = svg;
        graph.temp_y_val = bar_vals[1];
        return graph;
    };

    /* Takes the array of samples for a specific sample type
     * already ordered */
    calculate_error_bars_violin = function (values_raw) {
        var values = [];
        x = 0;
        for (i in values_raw) {
            values.push(values_raw[i].Expression_Value);
        }
        var mean = get_mean_value(values);
        sum = 0;
        numbers_meaned = [];
        for (x in values) {
            numbers_meaned.push(Math.abs(values[x] - mean));
        }
        standard_deviation = get_mean_value(numbers_meaned);
        return [mean - standard_deviation, mean, mean + standard_deviation];
    };

    /*------------------------End of box plot calculations -----------------------------------*/

    get_type = function (data_point) {
        return data_point;
    }


    /*  Setting up the graph including y and x axes */
    setup_graph = function (graph) {
	graph.graph_type = "Violin Graph";
  estimated_shrink = 0;
  prev_estimated_shrink = 0;
        // setup all the graph elements
        options = graph.options;
        var label_padding = options.x_axis_label_padding; // For if there are 2 sets of labels
        graph = setup_margins(graph);
        var class_name = ".probe_text";
        var collective_name = ".probe-"; // used to show hover over name
        var class_name_for_legend = ".sample_text";
        var class_name_for_second_sort_by = ".second_sort_by";
        var collective_name_for_legend = ".sample-";
        graph = setup_svg(graph);
        if (options.sort_by_sample_id === "no") {
            graph = sort_x_by_probe_and_sample_type(graph);
        }
	    if (options.include_sample_type_x_axis === "yes" && options.display.x_axis_labels === "yes") {
		    label_padding = 80;
	    }
        // Check if it is also being sorted by the sample_type state on the x axis
        graph = setup_x_axis(graph, options.x_axis_list);
        graph = setup_data_for_x_axis(graph);
        if (options.display.x_axis_labels === "yes") {
          label_padding = label_padding - 100;
          graph = setup_x_axis_labels(graph, null, label_padding,class_name, collective_name, 1);
          graph = setup_x_axis_labels(graph, null, label_padding,".hidden-probe_text", collective_name, 1);
          label_padding = label_padding + 100;
          graph = setup_x_axis_labels(graph, null, label_padding,class_name_for_legend, collective_name, 3);


            if (options.sortByOption.split(',').length > 1) {
                label_padding += 120;
                graph = setup_x_axis_labels(graph, null, label_padding, class_name_for_second_sort_by, collective_name_for_legend, 2);
            }

        }
        graph = setup_y_axis(graph);
        graph = setup_line_graph(graph);
        // Only display the vertical lines if the user chooses so
        if (options.display.vertical_lines === "yes") {
            graph = setup_vertical_lines(graph, options.legend_list);
        }
        graph =  setup_watermark(graph);
        // Display the legend if the user has specified they want the legend
        if (options.display.legend == "yes") {
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
