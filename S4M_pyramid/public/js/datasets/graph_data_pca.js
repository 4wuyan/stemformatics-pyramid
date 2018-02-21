require=(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({"biojs-vis-pca":[function(require,module,exports){
/*
 * biojs-vis-pca
 * https://github.com/tingxuanz/biojs-vis-pca
 *
 * Copyright (c) 2016 tingxuan zhang
 * Licensed under the Apache-2.0 license.
 */

/**
@class biojsvispca
 */

//a tutorial for drawing scatter plot with d3.js
//http://bl.ocks.org/mbostock/3887118
var  biojsvispca;
module.exports = biojsvispca = function(init_options){

  //define options as defaults
  default_options = function(){
    var options = {
        marginForGraph:{top: 20, right: 20, bottom: 30, left: 40},
        width: 960 - 40 - 20,
        height: 500 - 20 - 30
    }
    return options;
  };
  $("#change_pca").change(function(){
    var val = $(this).val();
    val = val.replace(/ /g,"_");
    current_url = window.location.href;
    new_url_array = current_url.split("&pca_type");
    new_url= new_url_array[0] + "&pca_type="+ val; // this will change the folder name and will display pca.html for that folder name

    window.location.href = new_url;

  })
  $("#show_sample").click(function() {

    show_sample();
     if((typeof show_sample_id != "undefined") ) {
        if(show_sample_id != '') {
            sample_info = data_by_sample[show_sample_id]
                    svgForcircles.append("circle")
                    .data([sample_info])
            .attr("class", "dot")
        .attr("r", options.circle_radius)
        .attr("cx", function(){
          var x;
          x = sample_info[options.xDomain];
          return scaleX(x);})
        .attr("cy", function(){
          var y;
          y = sample_info[options.yDomain];
          return scaleY(y);})
        .style("fill", function() {
          var groupByoption;
          groupByoption = sample_info[options.groupByoption];
          return color(groupByoption);})
        .style("stroke-width",3)
        .on('mouseover', tooltip.show)
        .on('mouseout', tooltip.hide);

        }
    }

    //default_graph();

  })
  function show_sample() {
    show_sample_id = $("#sample").val();

  }
  /**
   * Sets up the actual scatter points on the graph, assigns colours based on
   * types also has a tooltip (see simple.js for tooltip setup)
   * with relevent info aobut each point
   * @param {type} graph
   * @returns {unresolved}
   */

  setup_scatter = function(graph){
    svg = graph.svgForGraph;
    options = graph.options;
    page_options = graph.page_options;

    tooltip = options.tooltip;
    svg.call(tooltip);

    if(options.colorDomain != undefined){
      page_options.colorDomain = options.colorDomain;
      page_options.color = d3.scale.ordinal().domain(page_options.colorDomain).range(options.domain_colors);
    } else {
      page_options.color = d3.scale.category20();
    }

    color = page_options.color;
    svgForcircles = svg.append("svg").attr("id","svgForcircles").attr("width", page_options.width)
    .attr("height", page_options.height).append("g")

    svgForcircles.selectAll(".dot")
        .data(options.data)
      .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("r", options.circle_radius)
        .attr("cx", function(d){
          var xDomain;
          xDomain = d[options.xDomain];
          return graph.scaleX(xDomain);})
        .attr("cy", function(d){
          var yDomain;
          yDomain = d[options.yDomain];
          return graph.scaleY(yDomain);})
        .style("fill", function(d) {
          var groupByoption;
          groupByoption = d[options.groupByoption];
          return color(groupByoption);})
        .on('mouseover', tooltip.show)
        .on('mouseout', tooltip.hide);

    graph.svgForGraph = svg;
    return graph;

  };

//re-color all points based on the groupByoption
change_scatter_color = function(graph){
  var svg = graph.svgForGraph;
  var options = graph.options;

 var  color = d3.scale.category20();
  svg.selectAll(".dot")
    .style("fill", function(d) {
      var groupByoption;
      groupByoption = d[options.groupByoption];
      return color(groupByoption);
    })
  graph.page_options.color = color;
  graph.svgForGraph = svg;
  return graph;
};

setup_zoom = function(graph){
  var svg = graph.svgForGraph;
  var options = graph.options;
  var page_options = graph.page_options;

  var zoom = d3.behavior.zoom()
      .x(graph.scaleX)
      .y(graph.scaleY)
      .on("zoom", function(){
        var x = d3.svg.axis()
             .scale(graph.scaleX)
             .orient("bottom");
        var y = d3.svg.axis()
             .scale(graph.scaleY)
             .orient("left");
        svg.select(".xAxis").call(x);
        svg.select(".yAxis").call(y);
        svg.selectAll(".dot")
          .attr("cx", function(d){
            var xDomain;
            xDomain = d[options.xDomain];
            return graph.scaleX(xDomain);})
          .attr("cy", function(d){
            var yDomain;
            yDomain = d[options.yDomain];
            return graph.scaleY(yDomain);});
      });


  svg.append("rect")
    .attr("id","brush_rect")
    .attr("width", page_options.width)
    .attr("height", page_options.height)
    .attr("class", "zoom")
    .style("fill", "none")
    .style("pointer-events", "fill")
    .style("visibility", "hidden")
    .call(zoom);


  graph.svgForGraph = svg;
  return graph;
};

/*
  Delete existing zoom behavior at brushstart and setup a new one at brushend.
  This can keep the scale and points' position in consistency.
*/
setup_brush = function(graph){
  var svg = graph.svgForGraph;
  var options = graph.options;
  var page_options = graph.page_options;
  var color = page_options.color;
  var durationTime = 500; //duration time of the transition

  tooltip = options.tooltip;
  svg.call(tooltip);

  var brush = d3.svg.brush()
       .x(graph.scaleX)
       .y(graph.scaleY)
       .on("brushstart", function() { //delete the existing zoom behavior at brushstart
         d3.selectAll(".zoom").remove();
       })
       .on("brushend", function() {
         var x = graph.scaleX;
         var y = graph.scaleY;

         /*
            brush.extent() returns the current brush extent.
            The extent is a two-demensional array [[x0, y0], [x1,y1]],
            where x0 and y0 are the lower bounds of the extent, and x1 and y1 are the upper bounds of the extent.

            Check https://github.com/d3/d3-3.x-api-reference/blob/master/SVG-Controls.md#brush_extent
            or details about brush.extent().
         */
         var extent = brush.extent();

         /* the set of x.domain and y.domain aims to acheieve the zoom after brush*/

         // set the domain of x axis scale to current lower and upper bounds of brush extent along x axis.
         x.domain([extent[0][0], extent[1][0]]);
         // set the domain of y axis scale to current lower and upper bounds of brush extent along y axis.
         y.domain([extent[0][1], extent[1][1]]);

         var xAxis = d3.svg.axis()
                      .scale(x)
                      .orient("bottom");
         var yAxis = d3.svg.axis()
                      .scale(y)
                      .orient("left");

         // Setup a new zoom behavior so that we can zoom and pan the plot after brush finish.
         setup_zoom(graph);

         /*
         if you append your zoom/brush after your data points, the zoom/brush overlay will catch all of the pointer events,
         and your tooltips will disappear on hover.
         You want to append the zoom/brush before your data points, so that pointer events on the data generate a tooltip,
         and those on the overlay generate a zoom/brush.
         */
         /* Remove and append all dots again, so that all dots are appended after the zoom.
            Thus the tooltip can work correctly.
         */
         svg.selectAll(".dot").remove();
         $('#svgForcircles').remove()
         svgForcircles = svg.append("svg").attr("id","svgForcircles").attr("width", page_options.width)
         .attr("height", page_options.height).append("g")
         svgForcircles.selectAll(".dot")
             .data(options.data)
           .enter()
             .append("circle")
             .attr("class", "dot")
             .attr("r", options.circle_radius)
             .attr("cx", function(d){
               var xDomain;
               xDomain = d[options.xDomain];
               return graph.scaleX(xDomain);})
             .attr("cy", function(d){
               var yDomain;
               yDomain = d[options.yDomain];
               return graph.scaleY(yDomain);})
             .style("fill", function(d) {
               var groupByoption;
               groupByoption = d[options.groupByoption];
               return color(groupByoption);})
             .on('mouseover', tooltip.show)
             .on('mouseout', tooltip.hide);

            svg.select(".xAxis")
              .call(xAxis);

            svg.select(".yAxis")
              .call(yAxis);

            d3.event.target.clear();
            d3.select(this).call(d3.event.target);

            // Delete the brush so that we can switch to zoom automatically.
            d3.selectAll(".brush").remove();
       });

  svg.append("g")
    .attr("class", "brush")
    .call(brush);

  graph.svgForGraph = svg;
  return graph;
};


  setup_x_axis_for_bar_chart = function(graph){
    var page_options = graph.page_options;
    var svg = graph.svgForBar;
    var options = graph.options;
    var data = [];
    //only store the top components, number of components is decided by options.numberOfComponents
    for (var i = 0; i < options.numberOfComponents; i++) {
      data[i] = options.barChartData[i];
    }
    //setup the scale for x axis, this is a linear scale
    var barChartScaleX = d3.scale.ordinal()
        .rangeRoundBands([0,page_options.barChartWidth], .1);
    //setup domain
    barChartScaleX.domain(data.map(function(d) {return d.prcomp}));
    //setup xaxis
    var xAxis = d3.svg.axis()
        .scale(barChartScaleX)
        .orient("bottom");

    //append as a group
    svg.append("g")
        .attr("class", "barChartXAxis axis")
        .attr("transform", "translate(0," + page_options.barChartHeight +")")
        .call(xAxis)
      .append("text")
        .attr("class", "label")
        .attr("x", page_options.barChartWidth)
        .attr("y", -6)
        .style("text-anchor", "end")
        //.text(options.x_axis_title);
    graph.svgForBar = svg;
    graph.barChartScaleX = barChartScaleX;
    return graph;
  };

  setup_y_axis_for_bar_chart = function(graph){
    var page_options = graph.page_options;
    var svg = graph.svgForBar;
    var options = graph.options;
    var data = [];

    //only store the top components, number of components is decided by options.numberOfComponents
    for (var i = 0; i < options.numberOfComponents; i++) {
      data[i] = options.barChartData[i];
    }
    //setup the scale for y axis, this is a linear scale
    var barChartScaleY = d3.scale.linear()
        .range([page_options.barChartHeight,0]);
    //setup domain
    barChartScaleY.domain([0, d3.max(data, function(d) { return d.eigenvalue;})]);
    //setup y axis
    var yAxis = d3.svg.axis()
        .scale(barChartScaleY)
        .orient("left");

    //append as a group
    svg.append("g")
        .attr("class", "barChartYAxis axis")
        .call(yAxis)
      .append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end");
        // .text(options.y_axis_title);
    graph.svgForBar = svg;
    graph.barChartScaleY = barChartScaleY;
    graph.barChartYAxis = yAxis;
    return graph;
  };

  setup_bar = function(graph){
    var page_options = graph.page_options;
    var svg = graph.svgForBar;
    var options = graph.options;
    var data = [];
    //only store the top components, number of components is decided by options.numberOfComponents
    for (var i = 0; i < options.numberOfComponents; i++) {
      data[i] = options.barChartData[i];
    }

    var bar = svg.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("clicked", "false")
      .attr("id", function(d) {return d.prcomp;})
      .attr("x", function(d) {return graph.barChartScaleX(d.prcomp); })
      .attr("y", function(d) {return graph.barChartScaleY(d.eigenvalue); })
      .attr("height", function(d) {return page_options.barChartHeight - graph.barChartScaleY(d.eigenvalue); })
      .attr("width", graph.barChartScaleX.rangeBand())
      .attr("fill", function(d) {
        var color;
        // if a bar is clicked, fill it with red
        if ((d.prcomp === options.clickedBars[0]) || (d.prcomp === options.clickedBars[1])) {
          color = "red";
        } else {
          color = "steelblue";
        }
        return color;
      });
    svg.selectAll(".bartext")
      .data(data)
      .enter()
      .append("text")
      .attr("class", "bartext")
      .attr("text-anchor", "start")
      .attr("x", function(d) {return graph.barChartScaleX(d.prcomp); })
      .attr("y", function(d) {return graph.barChartScaleY(d.eigenvalue); })
      .text(function(d){
        return parseInt((d.eigenvalue/screetable_total)*100) + "%"
      })
    graph.svgForBar = svg;
    return graph;
  };

// update PCA according to the bars that user clicks.
  update_PCA = function(graph){
    var svg = graph.svgForGraph;
    var page_options = graph.page_options;
    var options = graph.options;

    options.xDomain = options.clickedBars[0];
    options.yDomain = options.clickedBars[1];
    options.x_axis_title = options.clickedBars[0];
    options.y_axis_title = options.clickedBars[1];

    //convert the corresponding data to number format
    options.data.forEach(function(d) {
      d[options.xDomain] = +d[options.xDomain];
      d[options.yDomain] = +d[options.yDomain];
    });

    //remove these elements first, or the new elements will overlap with old ones
    d3.select(".xAxis").remove();
    d3.select(".yAxis").remove();
    d3.selectAll(".zoom").remove();
    d3.selectAll(".dot").remove();

    graph = setup_x_axis(graph);
    graph = setup_y_axis(graph);
    graph = setup_zoom(graph);
    graph = setup_scatter(graph);

    graph.svgForGraph = svg;
    return graph;

  };

  setup_graph = function(graph){
    //setup all the graph elements
    graph = setup_margins(graph);
    graph = setup_svg(graph);
    graph = setup_svg_bar(graph);
    graph = setup_x_axis(graph);
    graph = setup_y_axis(graph);

    var svg = graph.svgForGraph;
    var page_options = graph.page_options;
    var positonY = 0;
    var positonXForBrush = page_options.width - 80;
    var options = graph.options;

      pca_length = options.data.length;
      data_by_sample = {}
      for (i=0;i<pca_length;i++) {
        data_by_sample[options.data[i]['SampleID']] = options.data[i];
      }

    /*
      if you append your zoom/brush after your data points, the zoom/brush overlay will catch all of the pointer events,
      and your tooltips will disappear on hover.
      You want to append the zoom/brush before your data points, so that pointer events on the data generate a tooltip,
      and those on the overlay generate a zoom/brush.
    */
    graph = setup_zoom(graph);
    graph = setup_scatter(graph);

    graph = setup_legend(graph);
    graph = setup_x_axis_for_bar_chart(graph);
    graph = setup_y_axis_for_bar_chart(graph);
    graph = setup_bar(graph);

    d3.select(".brushButton")
      .on("click", function(){
        graph = setup_brush(graph);
      });
    graph.svgForGraph = svg;
    return graph;
  };


  init = function(init_options){
      var options = default_options();
      options = init_options;
      page_options = {}; // was new Object() but jshint wanted me to change this
      var graph = {}; // this is a new object
      graph.options = options;
      graph = setup_graph(graph);
      var target = $(options.target);
      target.addClass('scatter_plot');
      svgForGraph = graph.svgForGraph;
      svgForBar = graph.svgForBar;
      return graph;
  } ;
  // constructor to run right at the start
  init(init_options);

};

/**
 * Private Methods
 */

/*
 * Public Methods
 */

},{}]},{},[]);
