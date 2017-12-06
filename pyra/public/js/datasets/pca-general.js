//setup margins
  setup_margins = function(graph){
    options = graph.options;
    page_options.marginForGraph = options.marginForGraph;
    page_options.marginForBar = options.marginForBar;

    page_options.width = options.width - page_options.marginForGraph.left - page_options.marginForGraph.right;
    page_options.height = options.height - page_options.marginForGraph.top - page_options.marginForGraph.bottom;

    page_options.barChartWidth = options.barChartWidth - page_options.marginForBar.left - page_options.marginForBar.right;
    page_options.barChartHeight = options.barChartHeight - page_options.marginForBar.top - page_options.marginForBar.bottom;

    page_options.fullWidth = options.fullWidth;
    page_options.fullHeight = options.fullHeight;

    graph.page_options = page_options;
    return graph;
  };

  setup_x_axis = function(graph){
    var page_options = graph.page_options;
    var svg = graph.svgForGraph;
    var options = graph.options;
    //setup the scale for x axis, this is a linear scale
    scaleX = d3.scale.linear()
        .range([0,page_options.width]);
    //setup domain
    scaleX.domain(d3.extent(options.data,
      function(d){
        var xDomain;
        xDomain = d[options.xDomain];
        return xDomain;
      })).nice();
    //setup xaxis
    var xAxis = d3.svg.axis()
        .scale(scaleX)
        .orient("bottom");

    //append as a group
    svg.append("g")
        .attr("class", "xAxis axis")
        .attr("transform", "translate(0," + page_options.height +")")
        .call(xAxis)
      .append("text")
        .attr("class", "label")
        .attr("x", page_options.width)
        .attr("y", -6)
        .style("text-anchor", "end")
        .text(options.x_axis_title);
    graph.svgForGraph = svg;
    graph.scaleX = scaleX;
    return graph;
  };

  setup_y_axis = function(graph){
    var page_options = graph.page_options;
    var svg = graph.svgForGraph;
    var options = graph.options;
    //setup the scale for y axis, this is a linear scale
    scaleY = d3.scale.linear()
        .range([page_options.height, 0]);
    //setup domain
    scaleY.domain(d3.extent(options.data,
      function(d){
        var yDomain;
        yDomain = d[options.yDomain];
        return yDomain;
      })).nice();
    //setup y axis
    var yAxis = d3.svg.axis()
        .scale(scaleY)
        .orient("left");

    //append as a group
    svg.append("g")
        .attr("class", "yAxis axis")
        .call(yAxis)
      .append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text(options.y_axis_title);
    graph.svgForGraph = svg;
    graph.scaleY = scaleY;
    graph.yAxis = yAxis;
    return graph;
  };

  setup_legend = function(graph){
      var svg = graph.svgForLegend;
      var page_options = graph.page_options;
      var color = page_options.color;
      var width = page_options.width;
      var max_legend_items = 15;
      var extra_legend_items = 0;
      var largest_legend_item_length = 0;
      var size = 5;
      var max_legend_name_length = 25;
      var rows =1;
      var legend_num=1;
      var legendRectSize = options.legend_rect_size;
      var border_counter = 1;
      var increment_counter= false;

      var legend = svg.selectAll(".legend")
          .data(color.domain())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) {
              if (increment_counter) {
                border_counter ++;
                increment_counter = false;
              }
              legend_num ++;
              var horizontal = ((200*(border_counter-1)))
              var vertical = (legend_num * options.indent_bottom_padding) - options.indent_top_padding;
              if(d.length > (2 * max_legend_name_length)) {
                  rows = Math.ceil((d.length/max_legend_name_length)/2); //calculates how many rows are required by legend_name and as one row can handle two text rows, thus divided by 2
                  legend_num++;
              }
              else {
                rows = 1;
              }
              if (vertical > 400) {
                  legend_num = 1;
                  increment_counter = true;
                }
             return "translate("+horizontal+","+vertical+")";
           });

      legend.append("rect")
          .attr("x", 1)
          .attr("width", legendRectSize)
          .attr("height", legendRectSize)
          .style("fill", color);
      var delimiter = "_";
      var max_length_for_legend_name = 17;
      legend.append("text")
          .attr("x", 20)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "start")
          .text(function(d,i) { if(i>extra_legend_items) {extra_legend_items += 1;}
                                if(d.length > largest_legend_item_length) {largest_legend_item_length = d.length}
                                return d.replace(regex_function(max_length_for_legend_name,delimiter), "$&\n"); }).call(wrap,size);
      var full_height_var = options.height + "px";
      var full_width_var = largest_legend_item_length + (options.indent_legend_item_padding * border_counter) + "px";
      document.getElementsByClassName('svgForLegendClass')[0].setAttribute("height",full_height_var);
      document.getElementsByClassName('svgForLegendClass')[0].setAttribute("width",full_width_var);
      document.getElementsByClassName('divForLegend')[0].style.height = full_height_var;
      document.getElementsByClassName('divForLegend')[0].style.width = full_width_var;
      graph.svgForLegend = svg;
      return graph;
  };

  // http://stackoverflow.com/questions/2232603/regular-expressions-to-insert-r-every-n-characters-in-a-line-and-before-a-com
  regex_function = function(size,delimiter) {
    var regex_expression =  new RegExp("(.{" + size + "})"+ delimiter, "g");
    return regex_expression;
  }

  setup_svg = function(graph){
    var options = graph.options;
    var page_options = graph.page_options;

    var marginForGraph = page_options.marginForGraph;

    var scatterHeight = options.height;
    var legend_width = options.legend_width;
    var legend_height = options.legend_height;
    var full_width = page_options.fullWidth;
    var full_height = page_options.fullHeight;
    // clear out html
    $(options.target).html('')
            .css("width", full_width + "px" )
            .css("height", full_height + "px")
            .css("margin-top", options.top_margin + "px");

    // setup the SVG. We do this inside the d3.tsv as we want to keep everything in the same place
    // and inside the d3.tsv we get the data ready to go (called options.data here)

    var divForPCA = d3.select(options.target).append("div")
        .attr("class", "divForPCA");
    $(".divForPCA")
        .css("width", options.width + "px")
        .css("height",options.height + "px")
        .css("position", "absolute")
        .css("left",options.graph_left_padding + "px");

    var svgForGraph = divForPCA.append("svg")
        .attr("width", options.width)
        .attr("height",options.height);

      svgForGraph = svgForGraph.append("g")
        // this is just to move the picture down to the right margin length
        .attr("transform", "translate(" + (marginForGraph.left) + "," + (marginForGraph.top) + ")");

    var divForLegend = d3.select(options.target).append("div")
        .attr("class", "divForLegend");
    $(".divForLegend").css("width", options.legend_width + "px")
        .css("height",options.height + "px")
        .css("position", "absolute")
        .css("left", options.legend_left_padding + "px");
    $(".divForLegend").css("left", (options.legend_left_padding ) + "px")
        .css("font-family", options.font_css).css("font-size", options.title_text_size);
    divForLegend.append("text").text(function(){return "Legend"}).attr("id","legend-title");
    svgForLegend = divForLegend.append("div").attr("class","legendSVG").append("svg")
        .attr("width", options.legend_width)
        .attr("height",options.legend_height)
        .attr("class","svgForLegendClass")
        .append("g")
        // this is just to move the picture down to the right margin length
        .attr("transform", "translate(" + (0) + "," + (20) + ")");

    /*
    The zoom function works in the whole svg area.
    If we put 2 plots in one svg element, we will find that the circles in the scatter plot can reach the bar chart area when zooming in.
    So, we use one svg for scatter plot, one svg for bar chart to make sure that the zoom function only works in the scatter plot.
    */

    graph.svgForGraph = svgForGraph;
    graph.svgForLegend = svgForLegend;
    return graph;
  };

  setup_svg_bar = function(graph){
    var options = graph.options;
    var page_options = graph.page_options;
    var full_width = page_options.fullWidth;
    var marginForBar = page_options.marginForBar;
    var legend_width = options.legend_width;

    var divForBar = d3.select(options.target).append("div")
        .attr("class", "divForBar");
    $(".divForBar")
        .css("width", (options.bar_graph_width ) + "px")
        .css("height", options.barChartHeight + "px")
        .css("position", "absolute")
        .css("left", (options.bar_graph_left_padding ) + "px");

    var svgForBar = divForBar.append("svg")
        .attr("width", options.barChartWidth)
        .attr("height", options.barChartHeight)
      .append("g")
        // this is just to move the picture down to the right margin length
        .attr("transform", "translate(" + (marginForBar.left) + "," + (marginForBar.top) + ")");

    graph.svgForBar = svgForBar;
    return graph;
  };

  // http://bl.ocks.org/mbostock/7555321
  // break text element to text spans and split word after certain length
  function wrap(text, width) {
    var lineHeight = 1.1;
    text.each(function() {
      var text = d3.select(this),
          words = text.text().split("\n").reverse(),
          word,
          line = [],
          lineNumber = 0, // this needs to be in loop so that it incremneted within each legend and for next legend it goes to zero again
          y = text.attr("y"),
          x = text.attr("x"),
          dy = parseFloat(text.attr("dy")),
          tspan = text.text(null).append("tspan").attr("x", x).attr("y", y-16).attr("dy", 0 + "em");
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(" "));
        if ( tspan.node().getComputedTextLength() > width)  {
          line.pop();
          var word_length = tspan.node().getComputedTextLength()/2;
          tspan.text(line.join(" "));
          line = [word];
          tspan = text.append("tspan").attr("x", x).attr("y", y - 16).attr("dy", lineHeight+ lineNumber +  "em").text(word);
          lineNumber++;
        }
      }
    }
  )};

$(document).ready(function() {
  var value = $(document.getElementById('pca_type')).html().replace(/ /g,"").replace(/_/g,' ');
  $("#change_pca").val(value);

});
