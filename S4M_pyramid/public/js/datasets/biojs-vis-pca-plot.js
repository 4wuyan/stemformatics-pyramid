
var rootDiv = document.getElementById("graphDiv");

var app = require("biojs-vis-pca");


//Create array which will contain all groupby options such as SampleType
var groupByOptions = [];

// This is the groupby option that will be used to render the scatter plot
var groupByoption;

//set default values for xDomain, yDomain
var xDomain = "PC1"; //xDomain is used to setup the domain for x axis and circle\'s cx attribute in scatter_plot
var yDomain = "PC2"; //yDomain is used to setup the domain for y axis and circle\'s cy attribute in scatter_plot

//store the data for bar chart
var barChartData;

//store the metadata about how all points are grouped
var metadata;

// number of principle components that will be displayed in bar chart
var numberOfComponents = 5;

//number of bars that are clicked
var numOfClickedBars = 0;

//store the clicked bars\' ids
var clickedBarId = [];

var body = document.getElementsByTagName("body")[0];
var ds_id = $(document.getElementById('ds_id')).html().replace(/\s/g, '');
var pca_type = $(document.getElementById('pca_type')).html().replace(/\s/g, '');
//Create a form for groupby options
var groupBySelectList = document.createElement("form");
groupBySelectList.id = "colorSelect";
body.appendChild(groupBySelectList);

// ==========================
// EACH PCA GRAPH IS BUILD USING 3 DATA FILES, WHICH MEANS WE HAVE TO MAKE 3 CALLS TO GET THESES FILES.
// METADATA.TSV AND SCREETABLE.TSV WILL BE DOWNLOADED FIRST AND DATA WILL BE STORED IN variables
// ONCE THE ABOVE FILES HAS BEEN FETCHED , ONLY AFTER THAN PCA.TSV DATA SHOULD BE FETCHED
// ==========================
// I tried replacing d3.tsv calls with ajax calls, but than it was slower as I have to manipulate tsv data to dict which took more time

//load the metadata for groupby options
d3.tsv("/datasets/return_pca_data?ds_id="+ds_id+"&pca_type="+pca_type+"&file_name=metadata", function(error, data) {
    metadata = data;

    /*
    For the tsv file, we expect rows as sample ids
    and columns as group by options
    (except for 1st one which is sample id and
    columns with name ReadFile1 & ReadFile2 which are irrelevant to group by options)
    */
    /*
    After load the file, all data are stored in metadata.
    metadata is an array of objects. All bojects use same column names (eg. SampleType) as keys.
    We want to get these keys as groupByOptions.
    */
    groupByOptions = Object.keys(metadata[0]);

    //We would like to remove SampleID, ReadFile1 and ReadFile2 from groupByOptions, because they won\'t be used as groupby options.
    var itemsToBeRemoved = ["SampleID", "ReadFile1", "ReadFile2"];
    for (var i = 0; i < itemsToBeRemoved.length; i++) {
      var index = groupByOptions.indexOf(itemsToBeRemoved[i]); //find index of target item in groupByOptions
      if (index !== -1) {
        groupByOptions.splice(index, 1);
      }

    }

    /*In order to allow users to choose different groupByOptions,
    we need to create radio button elements in the form for each groupByoption.
    */

    for (var i = 0; i < groupByOptions.length; i++) {
        var option = document.createElement("input");
        option.type = "radio";
        option.name = "color";
        option.id = groupByOptions[i];
        option.value = groupByOptions[i];

        //A radio button doesn\'t come with text attribute, we need a label element for the radio button to show some text.
        var label = document.createElement("label");
        label.htmlFor = option.id;
        label.innerHTML = groupByOptions[i];

        if (i === 0) {
          option.checked = true; // set the first option element as default option
        }
        groupBySelectList.appendChild(option);
        groupBySelectList.appendChild(label);

        var br = document.createElement("br");
        groupBySelectList.appendChild(br); // append the radio button element and label element to the select list
    }

    //set the default groupByoption
    groupByoption = groupByOptions[0];
});

//create and append the reset button
var resetButton = document.createElement("button");
resetButton.id = "resetButton";
resetButton.className = "button"
resetButton.innerHTML = "Reset";

/*
when click the reset button, first reset the variables, then re-draw the graph.
*/
resetButton.onclick = function(){
  numOfClickedBars = 0;
  clickedBarId = [];
  xDomain = "PC1";
  yDomain = "PC2";
  groupByoption = groupByOptions[0];
  default_graph();
  groupBySelectList.childNodes[0].checked = true; //reset the select list
};
$("#button_div").append(resetButton);

var brushButton = document.createElement("button");
brushButton.id = "brushButton";
brushButton.innerHTML = "Select Zoom";
brushButton.className = "brushButton button";
$("#button_div").append(brushButton);


// create the tooltip for points in scatter plot
var tooltip = d3.tip()
    .attr("class", "d3-tip")
    .offset([0, +110])
    .html(function(d){
        sampleID = d.SampleID;
        Xaxis = d[xDomain];
        Yaxis = d[yDomain];
        temp = "SampleID: " + sampleID + "<br/>"

        for(i=0;i<groupByOptions.length;i++) {
          temp += groupByOptions[i]+ ": " + d[groupByOptions[i]] + "</br>"
        }

        temp += Xaxis + ", " + Yaxis
        return temp;
    });


    // render the default graph, use SampleType as color domain

    default_graph = function (){
    d3.tsv("/datasets/return_pca_data?ds_id="+ds_id+"&pca_type="+pca_type+"&file_name=pca", function(error, data) {
          data.forEach(function(d) {
            d[xDomain] = +d[xDomain];
            d[yDomain] = +d[yDomain];
          });

          target = rootDiv;
          var options = {
            metadata: metadata,
            clickedBars: clickedBarId,
            numOfClickedBars: numOfClickedBars,
            numberOfComponents: numberOfComponents,  //used to determine how many components will be showed in the bar chart
            barChartData: barChartData,
            barChartHeight:400,
            barChartWidth: numberOfComponents * 50,
            groupByoption: groupByoption,
            xDomain: "PC1",
            yDomain: "PC2",
            circle_radius: 8,
            data: data,
            height: 500, // height for scatter plot
            width: 800,  //width for scatter plot
            bar_graph_width: 300,
            legend_width: 300,
            legend_height: 500,
            legend_rect_size:18,
            indent_bottom_padding: 30,
            indent_top_padding: 60,
            indent_legend_item_padding: 200,
            bar_graph_left_padding: 0,
            graph_left_padding: 300,
            legend_left_padding: 1200,
            legend_top_padding: 100,
            font_style: "Arial",
            main_title: "PCA Graph",
            title_text_size: "16px",
            graph_top_padding: 100,
            fullWidth: 1360, //width for the whole graph
            fullHeight: 700, //height for the whole graph
            top_margin: 100,
            marginForGraph: {
              top: 10,
              right: 20,
              bottom: 30,
              left: 40
            },
            marginForBar: {
              top: 10,
              right: 20,
              bottom: 30,
              left: 100
            },
            target: target,
            tooltip: tooltip,
            x_axis_title: "PC1",
            y_axis_title: "PC2",
          };


          //merge each SampleID\'s metadata to its raw data
    var metadata_object = {};
          for (var i = 0; i < options.metadata.length; i++) {
             //jQuery.extend(options.data[i],options.metadata[i]);
        row = options.metadata[i];
        sample_id = row.SampleID;
        metadata_object[sample_id] = row;

          }

          for (var i = 0; i < options.metadata.length; i++) {
            sample_id = options.data[i].SampleID;
            row =  metadata_object[sample_id];
             jQuery.extend(options.data[i],metadata_object[sample_id]);

          }

          var instance = new app(options);


          // Get the d3js SVG element
          var tmp = document.getElementsByTagName("body")[0];
          var svgForGraph = tmp.getElementsByTagName("svg")[0];
          var svgForLegend = tmp.getElementsByTagName("svg")[1];
          var svgForBar = tmp.getElementsByTagName("svg")[2];

          // Extract the data as SVG text string
          var svgForScatter_xml = (new XMLSerializer).serializeToString(svgForGraph);
          var svgForLegend_xml = (new XMLSerializer).serializeToString(svgForLegend);
          var svgForBar_xml = (new XMLSerializer).serializeToString(svgForBar);

          //get the settings of graph
          var graph = init(options);

          change_color(graph);
          click_bar_to_choose_PCA(graph);


    });
    }


//load the bar chart data
d3.tsv("/datasets/return_pca_data?ds_id="+ds_id+"&pca_type="+pca_type+"&file_name=screetable", function(error, data) {
screetable_total = 0;
data.forEach(function(d,i) {
  d.eigenvalue = +d.eigenvalue;
  if ((i+1) == data.length) {
    screetable_total += parseInt(d.eigenvalue);
  }
  else {
    screetable_total += parseFloat(d.eigenvalue);
  }
});
barChartData = data;
default_graph(); // make sure this function is called at last when variable barChartData has been set up, this also downloads data for pca.tsva
});

function change_color(graph){
  d3.select("#colorSelect")
    .on("change", function(){
      // update the groupByoption
      var groupBySelectList = document.getElementById("colorSelect");
      for (var i = 0; i < groupBySelectList.childNodes.length; i++) {
        if (groupBySelectList.childNodes[i].checked === true) {
          options.groupByoption = groupBySelectList.childNodes[i].id;
        }
      }


      //change the color of scatter points
      change_scatter_color(graph);

      // the legend needs to be updated
      d3.selectAll(".legend").remove();
      setup_legend(graph);
    });
}

function click_bar_to_choose_PCA(graph){
  d3.selectAll(".bar")
    .on("click",function(){
        var clicked = this.getAttribute("clicked");
        var id = this.getAttribute("id");

        if (options.numOfClickedBars < 2) {
          if (clicked === "false") {
            d3.select(this)
            .attr("clicked", "true")
            .attr("fill", "red");
            options.numOfClickedBars = options.numOfClickedBars + 1;
            options.clickedBars.push(id);
          }

          if(options.numOfClickedBars === 2){
            update_PCA(graph);
          }
        }
  });
}
