/*
 * biojs-vis-yugene-graph
 * https://github.com/rowlandm/biojs-vis-rohart-msc-test
 *
 * Copyright (c) 2015 rowlandm
 * Licensed under the Apache 2 license.
 */

/**
@class biojsvisyugenegraph
 */
/*
    Copyright 2015 Rowland Mosbergen

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


    This is a standalone unit to call when you want to create a scatter plot graph.

*/
var biojsvisyugenegraph;

/*
    Unfortunately due to the way callbacks are available, I had
    to put brush and dots outside the main function for scoping
    purposes.

    This is because they are used in the brushmove function that
    also had to sit outside the main function for scoping 
    purposes.
*/
var brush;
var dots;
var svg_line;
var full_data;

// Should this go outside in the stub like the tooltips?
// this is to make the dots selected change colour and to 
// show the values of the YuGene Graph that have been 
// selected on the line itself (not the dots)
brushmove = function (graph) {
    var s = brush.extent();

    // classed is a convenience function so that if the value is true
    // the element adds "selected" to the class
    // end is first as Yugene is ordered with highest values on the left
    dots.classed("selected", function(d) { 
        end = s[0];
        start = s[1];
        position = d.x_position;
        result = end <= position && position <= start; 
        return result;

    });

    end = Math.floor(s[0]);
    start = Math.floor(s[1]) + 1;

    // Please note that full_data[x] should always
    // have the x_position of x + 1
    // eg. full_data[0] has an x_position of 1
    selection_yugene_value_end = full_data[end-1].yugene_value

    // check that we don't go over the number of actual values
    // in the data store
    if (full_data.length < start){
        start = full_data.length;
    }
    selection_yugene_value_start = full_data[start-1].yugene_value

    // Relying on these divs to be there to update
    $('#yugene_value_end').html(selection_yugene_value_end);
    $('#yugene_value_start').html(selection_yugene_value_start);
}

// This is the start of the npm/nodejs/biojs standard setup of the module
module.exports = biojsvisyugenegraph = function(init_options)
{

    // This wraps the text based on a specific width
    // Derived from http://bl.ocks.org/mbostock/7555321

    /* Usage:
        svg.selectAll(".Title")
            .call(this.d3_wrap,width); 
    */
    this.d3_wrap = function (text, width) {
        text.each(function() {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            y = text.attr("y"),
            x = text.attr("x"), // set x to be x, not 0 as in the example
            dy = parseFloat(text.attr("dy")); // no dy
            // added this in as sometimes dy is not used
            if (isNaN(dy)){
                dy =0;
            } else {
                dy = dy;
            }
            tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
        
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                new_dy =++lineNumber * lineHeight + dy; // added this in as well
                tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", new_dy+ "em").text(word).attr('text-anchor','middle');
            }
        }
      });
    } // end d3_wrap

    // setup margins in a different function (sets up the page options (i.e. margins height etc)
    this.setup_margins = function(graph){
        options = graph.options;
        page_options.width = options.width - options.margin.left - options.margin.right;
        page_options.height = options.height - options.margin.top - options.margin.bottom;
        page_options.horizontal_grid_lines = 0;
        page_options.margin_top = options.margin.top;
        page_options.margin_bottom = options.margin.bottom;
        page_options.full_width = options.width + options.margin.left + options.margin.right;
        page_options.full_height = options.height;
        page_options.margin = options.margin;
        graph.page_options = page_options;
        return graph;

    } ///end setup margins
     
    //setting up the line to append for each of the values (i.e. line between scatter points)
    //http://bl.ocks.org/d3noob/e99a762017060ce81c76 helpful for nesting the probes
    this.setup_yugene_line = function(graph){
        options = graph.options;
        scaleX = graph.scaleX;
        scaleY = graph.scaleY;
        svg = graph.svg;
        height = graph.options.height - graph.options.margin.top - graph.options.margin.bottom;
        yugene_line = d3.svg.line()
            .x(function(d,i) { 
                value = d[options.x_column];
                return scaleX(value);
                })
            .y(function(d){ 
                    value = d[options.y_column];
                    return scaleY(value);
                }
            );

        var yugene_area = d3.svg.area()
            .x(function(d,i) { 
                value = d[options.x_column];
                return scaleX(value);
                })
            .y1(function(d){ 
                    value = d[options.y_column];
                    return scaleY(value);
                }
            )
            .y0(height);


        //nests through for each probe (doesn't take order into account)
        //order needs to be done separately (see above function dataNest)
        svg_line = svg.append("path")
            .attr("class", function() { return 'class-for-path'}) 
            .style("opacity", 100)
            .style("fill","none")  
            .style("stroke","black")
            .style("stroke-width","1")
            .attr("d", yugene_line(options.data));


        svg_area = svg.append("path")
            .style("opacity", 100)
            .style("fill",options.fill_area_colour)  
            .attr("d", yugene_area(options.data));



        graph.svg_area = svg_area;
        graph.svg_line = svg_line;
        graph.svg = svg;
        return graph;   
    
    }//end this.setup_yugene_line


    // Setup the y axis 
    this.setup_y_axis = function(graph){
        svg = graph.svg;
        // ########################################## Setup Y axis labels ###################################3
        /*
            For the y axis, the scale is linear, so we create a variable called y that we can use later
            to scale and do other things. in some people call it yScale
            https://github.com/mbostock/d3/wiki/Quantitative-Scales
            The range is the range of the graph from the height to 0. This is true for all y axes
        */
        var scaleY = d3.scale.linear()
            .range([page_options.height, 0]);

        // setup the yaxis. this is later called when appending as a group .append("g")
        // Note that it uses the y to work out what it should output
       //trying to have the grid lines as an option 
      var yAxis = d3.svg.axis() 
                    .scale(scaleY)
                    .orient("left")
                    //sets the number of points to increment by 1 whole number. To change see options.increment
                    .ticks(options.increment)
                    .innerTickSize(-page_options.horizontal_grid_lines)
                    .outerTickSize(0);  

        y_column = options.y_column;
        // d3.extent returns the max and min values of the array using natural order
        // we are trying to take into account not just the data but the lines as well
        // Max value of YuGene is 1, minimum value is 0
        max_value = 1;
        min_value = 0;
        scaleY.domain([min_value,max_value]).nice();
        y_axis_legend_y = (graph.full_height - options.margin.top - options.margin.bottom)/2;
        
        /*Adding the title to the Y-axis: stored in options.y_axis_title: information from
        ** http://bl.ocks.org/dougdowson/8a43c7a7e5407e47afed*/         
        svg.append("text")
          .text(options.y_axis_title)
          .attr("text-anchor", "middle")
          .style("font-family", "sans-serif")
          .style("font-size", "16px")
          .attr("transform", "rotate(-90)")
          .style("text-anchor", "middle")
          .attr("x", -y_axis_legend_y)
          .attr("y", -options.padding); //specifies how far away it is from the axis

        svg.append("g")
            .attr("class", "grid") //creates the horizontal lines accross the page
            .call(yAxis); //implementing the y axis as an axis
            

        graph.svg = svg;
        graph.scaleY = scaleY;
        graph.yAxis = yAxis;
        return graph;
    } // end this.setup_y_axis

    /* Setup the x axis, includig the scaleX which we might use to calculate our mapped values later on */
    this.setup_x_axis = function (graph){
        // ########################################## Setup X axis labels ###################################3
        page_options = graph.page_options;
        svg = graph.svg;
        options = graph.options;
        extra_y = 24;
        width = page_options.width;
        var scaleX = d3.scale.linear()  
        .range([0,width]);

        scaleX.domain(d3.extent(options.data, function(d) { return d[options.x_column]; }));

        svg.append("text") // main x axis title
            .attr("class", "label")
            .attr("x", (page_options.width + page_options.margin.left+ page_options.margin.right)/2)
            .attr("y", +page_options.height+extra_y)
            .style("text-anchor", "end")
            .style("font-family", "sans-serif")
            .text(options.x_axis_title);


        graph.svg = svg;
        graph.scaleX = scaleX;

        return graph ;
    } //end this.setup_x_axis

    // Brush is for all the options of selecting start and stop co-ordinates.
    // From example: http://bl.ocks.org/mbostock/4349545
    // This is when you start
    this.brushstart = function () {
        svg.classed("selecting", true);
    }

    // This is when you stop
    this.brushend = function () {
        svg.classed("selecting", !d3.event.target.empty());


        // now update the graph down the bottom 
        get_breakdown_of_filtered_data();
    }


    /* Similary with the code above this is used to calculate the interval between 
        the scatter points, however this is used in the hover bars (slightly 
        different as it uses the whole difference not 1/2 as with above */
    this.calculate_difference_between_samples = function(sample_id_list,scaleX){

        prev_sample_id = sample_id_list[0];
        step_sample_id = sample_id_list[1];
        value = scaleX(step_sample_id) - scaleX(prev_sample_id);
        return value;
    }

    
  
    /* Sets up the actual scatter points on the graph, assigns colours based on 
        probe types also has a tooltip (see simple.js for tooltip setup) 
        with relevent info aobut each point */
    this.setup_show_points_on_line = function(graph){
        ds_id_array = graph.options.ds_id_array;
        svg = graph.svg;
        options = graph.options;
        page_options = graph.page_options;
        scaleX = graph.scaleX;
        scaleY = graph.scaleY;
        y_column = options.y_column;
        x_column = options.x_column;
        // ######################################## Setup points on the graph ####################################3
        /*  http://bost.ocks.org/mike/circles/ 
            This pattern is so common, you’ll often see the selectAll + data + enter + append methods called 
            sequentially, one immediately after the other. Despite it being common, keep in mind that this 
            is just one special case of a data join.
        */
        tooltip = options.tooltip;
        //svg.call(tooltip);
        var x = -1;
        radius = options.circle_radius;
        probes = new Array();
        dots = svg.selectAll(".dot") // class of .dot
            .data(options.data.filter(function(d){ 
                result = $.inArray(d.ds_id,ds_id_array) !== -1;
                return result;
            })) // use the options.data and connect it to the elements that have .dot css
            .enter() // this will create any new data points for anything that is missing.
            .append("circle") // append an object circle
            .attr("class", function(d) {
                    //adds the sample type as the class so that when the sample type is overered over 
                    //on the x label, the dots become highlighted 
                    return "text-to_change_later" ;})
            .attr("r", radius) //radius 3.5
            .attr("cx", function(d) { 
                // set the x position as based off x_column
                // ensure that you put these on separate lines to make it easier to troubleshoot
                var cx = scaleX(d[options.x_column]); 
                return cx; 
            })
            .attr("cy", function(d) { 
                // set the y position as based off y_column
                // ensure that you put these on separate lines to make it easier to troubleshoot
                var cy =  scaleY(d[options.y_column]);
                return cy;
            })
            .style("stroke","black")
            .style("stroke-width","0px")
            .style("fill", function(d){
            //chooses the colour based on the probe
            //gets the colours from options
                result = $.inArray(d.ds_id, ds_id_array);
                if (result !== -1){
                    colour = options.colour[result];
                }
                
                return colour;})
            .on('mouseover', tooltip.show)
            .on('mouseout', tooltip.hide);

            graph.dots = dots;
            graph.svg = svg;
            return graph;
    }    // end of this.setup_show_points_on_line

    //Sets up the SVG element
    this.setup_svg = function (graph){
        options = graph.options;
        page_options = graph.page_options;

        full_width = page_options.full_width;
        full_height = page_options.full_height;

        graph.full_width = full_width;
        graph.full_height = full_height;
        background_stroke_width = options.background_stroke_width;
        background_stroke_colour = options.background_stroke_colour;

        // clear out html
        $(options.target)
            .html('')
            .css('width',full_width+'px')
            .css('height',full_height+'px');

        // setup the SVG. We do this inside the d3.tsv as we want to keep everything in the same place
        // and inside the d3.tsv we get the data ready to go (called options.data in here)
        var svg = d3.select(options.target).append("svg")
            .attr("width", full_width)
            .attr("height",full_height) 
        .append("g")
            // this is just to move the picture down to the right margin length
            .attr("transform", "translate(" + page_options.margin.left + "," + page_options.margin.top + ")");


        // this is to add a background color
        // from: http://stackoverflow.com/questions/20142951/how-to-set-the-background-color-of-a-d3-js-svg
        svg.append("rect")
            .attr("class", "background_rect")
            .attr("width", page_options.width)
            .attr("height", page_options.height)
            .attr("stroke-width", background_stroke_width)
            .attr("stroke", background_stroke_colour)
            .attr("fill", options.background_colour);

        height_margin_multiplier = 2;
        height_margin = 10;
        height_divisor = 1.5;
        svg.append("text")
            .attr("x", page_options.width/2)//options.x_middle_title)             
            .attr("y", 0 - (page_options.margin.top /height_divisor) + (height_margin/height_margin_multiplier)) 
            .attr("text-anchor", "middle")  
            .text(options.title).attr("class",options.title_class)
            .style("fill", "black")
            .style("font-family", "sans-serif")
            .style("font-size", "16px")
            .attr("class",options.title_class);
        

        //End subtitle setup
        max_width_of_text = 600;
        suggested_width_of_text = options.width*0.7;
        if (max_width_of_text < suggested_width_of_text){
            width_of_title = max_width_of_text;
        } else {
            width_of_title = suggested_width_of_text;
        }
        svg.selectAll("."+options.title_class)
            .call(this.d3_wrap,width_of_title); 


        graph.svg = svg;
        return graph;
    } // setup_svg

    /*  Setting up the watermark */
    // this is not in use just yet.
    this.setup_watermark = function(graph){
        svg = graph.svg;
        options = graph.options;
        extra_padding = 0;
        svg.append("image")
            .attr("xlink:href",options.watermark)
            .attr("x", page_options.height/2 - 100)
            .attr("y", -page_options.width - 2 * options.padding - extra_padding)// just out of the graphs edge
            .attr("transform", "rotate(+90)")
            .attr("width", 200)
            .attr("height", 100);

        graph.svg = svg;
        return graph;
    } // setup_watermark

    /*  Setting up the graph including y and x axes */ 
    this.setup_graph = function(graph){
        // setup all the graph elements
        graph = this.setup_margins(graph);
        graph = this.setup_svg(graph);    
        graph = this.setup_x_axis(graph);
        graph = this.setup_y_axis(graph);
        graph = this.setup_yugene_line(graph);
        graph = this.setup_show_points_on_line(graph);

        if (graph.options.watermark != false){
            graph = this.setup_watermark(graph);
        }

        return graph;

    }  // end setup_graph  

    this.setup_brush = function(graph){
        scaleX = graph.scaleX;
        // this is the way to select the items

        brush = d3.svg.brush()
            .x(scaleX)
            .extent([10, 50])
            .on("brushstart", this.brushstart)
            .on("brush",brushmove)
            .on("brushend", this.brushend);



        height = graph.page_options.height;
        radius = 5;
        var arc = d3.svg.arc()
            .outerRadius(radius)
            .startAngle(0)
            .endAngle(function(d, i) { return i ? -Math.PI : Math.PI; });

        var brushg = svg.append("g")
            .attr("class", "brush")
            .style("fill-opacity",0) // this is so that the SVG isn't seen when exported
            .call(brush);

        brushg.selectAll(".resize").append("path")
            .attr("transform", "translate(0," +  height / 2 + ")")
            .attr("d", arc);

        brushg.selectAll("rect")
            .attr("height", height);

        graph.brushg = brushg;

        return graph;
    }

    // run this right at the start of the initialisation of the class
    this.init = function(init_options){
        var options = init_options;
        page_options = {}; // was new Object() but jshint wanted me to change this
        var graph = {}; // this is a new object
        graph.options = options;

        // scope this out to handle the brush
        full_data = options.data;

        graph = this.setup_graph(graph);
        var target = $(options.target);
        target.addClass('scatter_plot');


        if (options.setup_brush == true ){
            graph = this.setup_brush(graph);
            this.brushstart();
            brushmove(graph);
        }

        svg = graph.svg;
    } 

    // constructor to run right at the start
    this.init(init_options);
}
