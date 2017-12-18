$(document).ready(function() {
  datasets =  $("#multi_view_datasets").html().replace(/\[|]/g, '').replace(/ /g, '').split(",");
  ref_id =  $("#ensemblID").html();
  ref_type = "ensemblID"
  graphType = $('#graphType').html();
  db_id = $('#db_id').html();
  normal_graph_box_width = 900;
  sortBy = "Sample_Type";
  ds_id = 0;
  symbol = $('#symbol').html();
  show_min_y_axis = false;
  legend_required = "yes";
  show_axis = "no"; // this toggles x axis when sample type and probe together are greater than 30
  ref_name = {};
  ref_name[symbol] = symbol
  graph_box_width = 900;
  previous_action = "";
  scatter_needed= "yes";
  scaling_required  = "yes";
  whiskers_needed = true;
  full_width = 1460;
  full_height = 1000;
if(ref_type == "ensemblID") {ref_type_for_title = "Gene"}

if (graphType== "" || graphType == undefined || graphType == "default") {graphType = "box"}


var window_url = window.location.href;
http_variable = window_url.split("stemformatics")[0]
dataset_data_object = {};
data_object = {};
multiview_graph = "yes";
sample_type_hover = {};
tooltip_box = {};
// first get first row only
for(var i=0;i< 3; i++) {
if(datasets[i] != undefined)
{
  ajax1(datasets[i]);
}
else {
  break;
}
}
// now get the rest of graphs
for(var i=3; i< datasets.length;i++){
  if(datasets[i] != undefined) {
    ajax1(datasets[i]);
  }
  else{
    return;
  }
}

$('a.chooseGraphType').on("click",function(){
    graphType = $(this).attr('clickChoose');
    var ds_id = $(this).attr('data-id');
    var shrink;
    for(var i=0;i< datasets.length; i++) {
      // if data is null than exit for loop
      if(data_object[datasets[i]] == null) {continue;}
      if(datasets[i] == ds_id) {shrink = "no";}
      else {shrink = "yes";}
      draw_graph(datasets[i],graph_data_error,dataset_error,shrink);
    }

});

  export_graph_data();
  export_graph_image();
  click_share_link();
  click_gene_info();
  toggleYaxis();
  multiview_toggle_SD();
  click_view_genes();
  multiview_set_autocomplete();
  contextHelpClick();

});


function contextHelpClick(){
    $helpButton = $('a.helpPopup,a.helpbtnPopup,#helpMenu');
    $helpButton.unbind("click");
    $helpButton.click(function(event){
        if (helpsystem.pageHelp.isOn) {
            helpsystem.pageHelp.turnOff();
            $helpButton.removeClass('active');
        } else {
            helpsystem.pageHelp.turnOn();
            $helpButton.addClass('active');
        }
        return false;
    });
}

function multiview_toggle_SD(){
  $("#toggleSD").on('click',function(){
    var dataset_id = $(this).attr('data-ds_id');
    var shrink_graph = "no";
    if(options.whiskers_needed != undefined) {
      options.whiskers_needed = !options.whiskers_needed;
      whiskers_needed= !whiskers_needed;
    }
  draw_graph(dataset_id,graph_data_error,dataset_error,shrink_graph);
  });

}

function multiview_set_autocomplete(){
multiview_set_gene_search_and_autocomplete();
}

function change_gene(gene){
    if (gene != '' && gene != undefined){
        graph_type = graphType;
        sort_by = sortBy;
        if (!window.location.origin)
           window.location.origin = window.location.protocol+"//"+window.location.host;
        new_url = window.location.origin + window.location.pathname + '?graphType='+graph_type+'&gene='+gene+'&db_id='+db_id;
        window.location = new_url;
    }
}


function multiview_set_gene_search_and_autocomplete(){
  var AUTOCOMPLETE_TIMEOUT = 5000;
if ($("#geneSearchForm").is(":visible")){
    $("#geneSearch").autocomplete({
        source: BASE_PATH + 'genes/get_autocomplete?db_id='+db_id,
        minLength: 4, // because the names are very small eg. STAT1
        timeout: AUTOCOMPLETE_TIMEOUT,
        appendTo: ".searchBox",
        select: function(event, ui) {
            var gene = ui.item.ensembl_id;
            change_gene(gene);
        }
    }).data("ui-autocomplete")._renderItem = function( ul,item ){
        return $("<li></li>").append("<a> <div class='symbol'>" + item.symbol + "</div><div class='species'>"+item.species+"</div><div class='aliases'>"+item.aliases+"</div><div class='description'>"+item.description+"</div><div class='clear'></div></a>").appendTo(ul);
    };


    $("#geneSearch").keypress(function(e){

            if(e.which == 13){
                e.preventDefault();
                var gene = $('#geneSearch').val();
                change_gene(gene);
                return false;
            }
        });

    $('#geneSearchForm').unbind();

    $('#geneSearchForm').submit(function(){
        $("#geneSearch").autocomplete('close');
        var gene = $('#geneSearch').val();
        change_gene(gene);
        return false;
    });

}

}

function click_view_genes(){
$('#viewGenes').unbind();
$('#viewGenes').click(function(){
    $('#geneSearchForm').submit();
});
}

function expand_svg(){
  var full_scale = 1;
  var graphdiv = document.getElementById(lastClickedGraph);
  var last_clicked_ds_id = ds_id;

  var div = document.getElementById('modalDiv');
  var translate_x = 150;
  var translate_y = 200;
  var menu_div = document.getElementById("menu_"+ds_id);
  var expanded_svg_width = full_width;
  var expanded_svg_height = full_height- 100;
  // move svg to modal and show all hidden fields
  $("#modalDiv").append(menu_div);
  div.appendChild(graphdiv);
  $('#modalDiv #menu_'+ds_id).css('display','block');

  $('#modalDiv .legendClass').show();
  $('#modalDiv .legend-title').show();
  $('#modalDiv .legend_border').show();
  $('#modalDiv .x_axis_label').show();
  $('#modalDiv .y_axis_label').show();
  $('#modalDiv #main_title').show();
  $('#modalDiv #s4m-logo').show();
  $('#modalDiv #subtitle').show();
  // expand svg
  var svgdiv = d3.select("#modalDiv #" + lastClickedGraph + "-svg")
          .attr("width", expanded_svg_width )
          .attr("height", expanded_svg_height); // these are being calculated in general.js
  var groupdiv = d3.select("#modalDiv #" + lastClickedGraph + "-group")
      .attr("transform", "translate(" + translate_x + "," + translate_y + ")" + " scale(" + full_scale + "," + full_scale + ")")
      .on({
          "mouseover": function(d) {
            d3.select(this).style("cursor", "default")
          },
          "mouseout": function(d) {
            d3.select(this).style("cursor", "default")
          }
        });
  $("#datasetTitle"+ds_id).css("display","none");
  contextHelpClick();
}

function shrink_svg(ds_id){
  var shrink_scale = 0.4;
  var menu_div = document.getElementById("menu_"+ds_id);
  var childdiv = document.getElementById("graphDiv_"+ds_id);
  var contentdiv = document.getElementById("content"+ds_id);
  var shrink_width = full_width * 0.45/1.05;
  var shrink_height = full_height * 0.35;

  // copy back to thumbnail from modal
  contentdiv.appendChild(menu_div);
  $("#content"+ds_id).append(childdiv);
  $('#content'+ ds_id + ' #menu_'+ds_id).css('display','none')

  // shrink back svg to thumbnail

  var svgdiv = d3.select("#content" + ds_id + " #graphDiv_" + ds_id + "-svg")
                  .attr("width", shrink_width)
                  .attr("height", full_height * 0.35);
  var groupdiv = d3.select("#content" + ds_id + " #graphDiv_" + ds_id + "-group")
       .attr("transform", "translate(40,80)" + " scale(" + shrink_scale + "," + shrink_scale + ")")
       .on({
           "mouseover": function(d) {
             d3.select(this).style("cursor", "pointer")
           },
           "mouseout": function(d) {
             d3.select(this).style("cursor", "default")
           }
         });
  scaling_required = "yes"; // opne_modal() is executed on if this is yes, so evrytime modal is closed, this should be set as yes for modal to open next time
  $('#content'+ds_id+ ' .legend-title').hide();
  $('#content'+ds_id+' .legendClass').hide();
  $('#content'+ds_id+' .x_axis_label').hide();
  $('#content'+ds_id+' .y_axis_label').hide();
  $('#content'+ds_id+' #main_title').hide();
  $('#content'+ds_id+' #s4m-logo').hide();
  $('#content'+ds_id+' #subtitle').hide();
  $('#content'+ds_id+' .legend_border').hide();
  $('#modalDiv .x_axis_label').show();
}

function show_rows(clicked_element) {
  var num = clicked_element.id.split("_")[1];
  document.getElementById(clicked_element.id).style.display = 'none';
  var row_id = "row_"+num;
  document.getElementById(row_id).style.display = 'block';
}

function ajax1(dataset_id) {
  return $.ajax({
    url : http_variable + "stemformatics.org/expressions/dataset_metadata?ds_id=" + dataset_id,
    success: function(response) {
      dataset_metadata = JSON.parse(response);
      dataset_data_object[dataset_id] = JSON.parse(dataset_metadata.data);
      dataset_error = dataset_metadata.error;
      if(dataset_error == "") {
        dataset_data_object[dataset_id]["sampleTypeDisplayGroups"] = JSON.parse(dataset_data_object[dataset_id]["sampleTypeDisplayGroups"])
        dataset_data_object[dataset_id]["ds_id"] = dataset_id; // added ds_id so that it can be used on tooltip
      }
      if((dataset_data_object[dataset_id]["lineGraphOrdering"]) && (dataset_data_object[dataset_id]["lineGraphOrdering"] != "NULL") && (dataset_data_object[dataset_id]["lineGraphOrdering"] != "")) {
        dataset_data_object[dataset_id]["lineGraphOrdering"] = JSON.parse(dataset_data_object[dataset_id]["lineGraphOrdering"]);
      }

      if ((dataset_data_object[dataset_id]['detectionThreshold']) == "" || isNaN(dataset_data_object[dataset_id]['detectionThreshold']) ) {
        dataset_data_object[dataset_id]['detectionThreshold'] = "NULL";
      }
      if ((dataset_data_object[dataset_id]['medianDatasetExpression']) == "" || isNaN(dataset_data_object[dataset_id]['medianDatasetExpression']) ){
        dataset_data_object[dataset_id]['medianDatasetExpression'] = "NULL";
      }
      graph_data_url = http_variable + 'stemformatics.org/expressions/graph_data?db_id='+db_id+'&ds_id='+dataset_id+'&ref_id='+ref_id+'&ref_type='+ref_type+'&graph_type='+graphType;
      var id = document.getElementById("datasetID"+dataset_id);
      $("#dataset"+dataset_id).append("<div id='datasetTitle" +dataset_id + "' style='display:none;font-size:13px;text-align:center'>"+dataset_data_object[dataset_id]["Title"]+"</div>");
      ajax2(dataset_id);
      }
  });
}

function sort_array(s1, s2) {
  var s1lower = s1.toLowerCase();
  var s2lower = s2.toLowerCase();
  return s1lower > s2lower? 1 : (s1lower < s2lower? -1 : 0);
}

// this function sorts an data such as probes, or second sort by options such as time, gender
// same function can be used to sort alphabetic data (disease state data, gender data ) or numeric data (in case of time the data is 0,3,6,9) or alplhanumeric (in case of probes ILMN_16547). The data is sorted and passed in options to ensure that when the probe/gender/time etc are plotted on x axis, they are in alphabetical order
var reA = /[^a-zA-Z]/g;
var reN = /[^0-9]/g;
function sortAlphaNum_array(a,b) {
    var AInt = parseInt(a, 10);
    var BInt = parseInt(b, 10);

    if(isNaN(AInt) && isNaN(BInt)){
        var aA = a.replace(reA, "");
        var bA = b.replace(reA, "");
        if(aA === bA) {
            var aN = parseInt(a.replace(reN, ""), 10);
            var bN = parseInt(b.replace(reN, ""), 10);
            return aN === bN ? 0 : aN > bN ? 1 : -1;
        } else {
            return aA > bA ? 1 : -1;
        }
    }else if(isNaN(AInt)){//A is not an Int
        return 1;//to make alphanumeric sort first return -1 here
    }else if(isNaN(BInt)){//B is not an Int
        return -1;//to make alphanumeric sort first return 1 here
    }else{
        return AInt > BInt ? 1 : -1;
    }
}


function ajax2(dataset_id) {
  return $.ajax({
    url: graph_data_url,
    success: function(response) {
      graph_data = JSON.parse(response);
      data_object[dataset_id] = JSON.parse(graph_data.data);
      graph_data_error = graph_data.error;

      if (graph_data_error == "") {
        unique_probes = []; //list of unique probes
        for(i = 0; i< data_object[dataset_id].length; i++) {
          if((unique_probes.indexOf(data_object[dataset_id][i].Probe) == -1)) { unique_probes.push(data_object[dataset_id][i].Probe); }
        }
        unique_probes_sorted = unique_probes.sort(sort_array);

        // for each limit sort by option lets calculate x axis label
        limitSortByArray = dataset_data_object[dataset_id]["limitSortBy"].split(",");
        x_axis_label_object = {}
        for(i=0;i < limitSortByArray.length; i++) {
          groupByOption = limitSortByArray[i];
          groupByOption_with_underscore = groupByOption.replace(" ","_");
          x_axis_label_object[groupByOption_with_underscore] = []
              for(j = 0; j< data_object[dataset_id].length; j++) { // iterate over data_object[dataset_id]
                if((x_axis_label_object[groupByOption_with_underscore].indexOf(data_object[dataset_id][j][groupByOption_with_underscore]) == -1 )) {
                    x_axis_label_object[groupByOption_with_underscore].push(data_object[dataset_id][j][groupByOption_with_underscore]);
                  }
              }
        }
      }
      var shrink_graph = "yes";
      main_title = "Gene Expression Graph for Gene " + symbol +" grouped by Sample Type";
      draw_graph(dataset_id,graph_data_error,dataset_error,shrink_graph);
    }// end success
  });
}

function changeUrl(choice) {
    var queries = {} ;
    $.each(document.location.search.substr(1).split('&'), function(index,value){
          var params = value.split('=');
          queries[params[0].toString()] = params[1].toString();
      });

      queries['graphType'] = choice;
      window.history.pushState({}, '', "?"+$.param(queries));
    }

function draw_graph(datasetID,graph_data_error,dataset_error,shrink_graph) {
    probe_name = $("#probe_name_"+datasetID).html()
    data = data_object[datasetID];
    scaling_required= shrink_graph;
    // toggle min y axis should always be false for bar graph
    if (graphType == "bar"){show_min_y_axis = false;}
    var sortbyOption = "Sample_Type";
    var graphDiv = document.getElementById("graphDiv_"+datasetID);
    if(graphType == "scatter") {
     var colours = dataset_data_object[datasetID]['probeColours'];
   }
   else {
     var colours = create_array_of_colours_for_legend(dataset_data_object[datasetID]["sampleTypeDisplayGroups"],dataset_data_object[datasetID]["sampleTypeDisplayGroupColours"]);
   }

    if (graph_data_error == "" && dataset_error == ""){
      if (graphType == "scatter") {
        $("li.chooseSD").show();
        changeUrl('scatter');
        run_scatter_gene_expression_graph(colours,graphDiv,sortbyOption,show_min_y_axis,legend_required,ref_name,main_title,whiskers_needed,scaling_required,dataset_data_object[datasetID],probe_name);
      }
      else if (graphType == "box") {
        var bar_graph = "no";
        $("li.chooseSD").hide();
        changeUrl('box');
        run_box_bar_gene_expression_graph(colours,graphDiv,bar_graph,sortbyOption,show_min_y_axis,legend_required,ref_name,main_title,whiskers_needed,scaling_required,dataset_data_object[datasetID],probe_name);
      }
      else if (graphType == "bar") {
        var bar_graph = "yes";
        $("li.chooseSD").show();
        changeUrl('bar');
        run_box_bar_gene_expression_graph(colours,graphDiv,bar_graph,sortbyOption,show_min_y_axis,legend_required,ref_name,main_title,whiskers_needed,scaling_required,dataset_data_object[datasetID],probe_name);
      }
      else if (graphType == "violin") {
        $("li.chooseSD").hide();
        changeUrl('violin');
        run_violin_gene_expression_graph(colours,graphDiv,sortbyOption,show_min_y_axis,ref_name,main_title,scaling_required,dataset_data_object[datasetID],probe_name);
      }
    }
    else {
          $("#graphDiv_"+datasetID).append("<div class='errorTextColumn' style = 'margin-top:12vh;margin-left:2vw;'><div id='errorText' class='title errorBox'><div id='message'>Graph Not Found.</div><div id='prompt'> <span id = 'prompt-message'>The Graph is not available for chosen parameters.</span> </div></div></div>");
    }
    if(shrink_graph == "yes") {
      shrink_svg(datasetID);
      // add mouseover function for displaying dataset information
      $("#content"+datasetID).mouseover(function() {
        $("#datasetTitle"+datasetID).css("display","block");
      });
      $("#content"+datasetID).mouseout(function() {
        $("#datasetTitle"+datasetID).css("display","none");
      });
    }
    else {
      expand_svg(datasetID);
    }

}

function create_array_of_colours_for_legend(legend_names, colour_object) {
    var colour_counter = {};
    var colours = {}
  // legend_names is an object containing sample_type and corresponding sample_type_group
  // colour object is an object having list of colour for each sample type group
  for(var sample_type in legend_names) {
      var group = legend_names[sample_type];

      // create a counter for every group
      if(!(group in colour_counter)) {
         colour_counter[group] = 0;
      }
      else {
        colour_counter[group] = colour_counter[group] + 1;
      }

      // now get the colour for that sample type
      colours[sample_type] = colour_object[group][colour_counter[group]];
  }
  return colours;
}

// http://stackoverflow.com/questions/8847766/how-to-convert-json-to-csv-format-and-store-in-a-variable
function ConvertToTSV(objArray,ds_id) {
      var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
      var str = '';

      var header = Object.keys(data_object[ds_id][0]).join(",");
      header = header.replace(/,/g, "\t");

      for (var i = 0; i < array.length; i++) {
          var line = '';
          for (var index in array[i]) {
              if (line != '') line += '\t'
              line += array[i][index];
          }
          str += line + '\r\n';
      }

      return header + "\n" + str;
  }

function export_graph_data(){
    $(".export_graph_data").on("click",function(){
        var ds_id = $(this).attr('data-id');
        var tsv_data = ConvertToTSV(data_object[ds_id],ds_id);
        $("body").append('<form id="exportform" action="' + BASE_PATH + 'main/export?format=tsv" method="post" target="_blank"><input type="hidden" id="exportdata" name="exportdata" /></form>');
        $("#exportdata").val(tsv_data);
        $("#exportform").submit().remove();

    });
}

function click_gene_info(){
    $('a.geneInfoButton').unbind();
    $('a.geneInfoButton').click(function(){
        $('#displayGeneDetail').modal({
            onShow: function (dialog){
                $('#simplemodal-container').width('auto');
            }
        });
    });
}

function toggleYaxis() {
  $(".no_set_min_y_axis_link").on('click',function(){
    var ds_id = $(this).attr('data-ds_id');
    var  shrink_graph = "no";
    show_min_y_axis = !show_min_y_axis;
    draw_graph(ds_id,graph_data_error,dataset_error,shrink_graph)
  });
}

function export_graph_image() {
    $("a.exportImageButton").on("click",function(){
      d3.selectAll('.probe_text').style("opacity",0);
      d3.selectAll('.hidden-probe_text').style("opacity",1);

      d3.selectAll('.exposed_legend').style("opacity",0);
      d3.selectAll('.hidden_legend').style("opacity",1);

      var svg = document.querySelector( "svg" );
      var svg_xml = new XMLSerializer().serializeToString( svg );

      output_format = $(this).attr('data-type');

      var form = document.getElementById("svgform");
       form['output_format'].value = output_format;
       form['file_name'].value = "Stemformatics_image";
       form['data'].value = svg_xml ;
       form.submit();

       // toggle probe names for bar box
      d3.selectAll('.probe_text').style("opacity",1);
      d3.selectAll('.hidden-probe_text').style("opacity",0);
      //toggle legend for scatter
      d3.selectAll('.exposed_legend').style("opacity",1);
      d3.selectAll('.hidden_legend').style("opacity",0);
    });

}

function click_share_link(){
    var elements = $('#share_link,a.share_link');
    elements.unbind().click(function(){
        var ds_id = $(this).attr('data-id');
        value = check_user_logged_in_for_sharing(); // this is in main.js
        if (value == false){ return false; }

        var gene_set_id_element = $('#gene_set_id');
        if (gene_set_id_element.length ==0){
            gene_set_id = 0;
        } else {
            gene_set_id = gene_set_id_element.html();
        }

        $('#wb_modal_title').html('Share this graph');
        var form_html  = "<form id='share_link_form'>" +
                "<div id=help_share_link_form>Please note that you can add more than one email address separating each with commas and no spaces. Please be aware that this does not share private objects, such as datasets or gene lists. If the email address you use doesn't have access, they will not be able to view this graph.</div>" +
                "<dl>" +
                    // "<dt>From Name:</dt><dd><input class='share_input' type='text' name='from_name' value='"+$('#full_name').html()+"'/></dd>" +
                    "<dt id='to_email_label'>To Email:</dt><dd><input id='to_email_input' class='share_input' type='text' name='to_email' value=''/></dd>" +
                    "<dt>Subject:</dt><dd><input class='share_input' type='text' name='subject' value='"+SITE_NAME+" - Expression " + $('div.title').html() +"'/></dd>" +
                    "<dt>Body:</dt><dd><textarea class='share_input' name='body' >Here is a link I thought you might want to see:\r\n"+ window.location.href +"\r\n\r\n"+"From \""+$('#full_name').html()+"\" " + $('#user').html() +" via "+SITE_NAME+"</textarea></dd>" +
                    "<dt><button id='share_link_form_submit' type='button'>Submit</button></dt><dd></dd>" +
                "</dl>" +
                "<div class='clear'/>"+
                "<input type='hidden' name='ds_id' value="+ds_id+">"+

                "<input type='hidden' name='gene_set_id' value="+gene_set_id+">"+
            "</form>" +

            "<div class='clear'/>";

        $('#wb_modal_content').html(form_html);

        $('#modal_div').modal({
            minHeight: 480,
            /* minWidth: 400, */
            onShow: function (dialog) {
                var modal = this;
                $('#share_link_form_submit').unbind('click');
                $('#share_link_form_submit').click(function(e){
                    // stop things from happening first
                    e.preventDefault();

                    $(this).html('Sharing...').addClass('wait');
                    $('#simplemodal-container').addClass('wait');

                    var post_url = http_variable + 'stemformatics.org/auth/share_gene_expression';
                    $.post(post_url, $("#share_link_form").serialize(),
                        function(data) {
                            $('#wb_modal_title').html('Share this graph');
                            $('#wb_modal_content').html(data);
                            $('#simplemodal-container').height('auto').removeClass('wait');
                        }
                    );

                });
            }
        });
    });

}

function toggle(div_id) {
        var scale = 1;
	var el = document.getElementById(div_id);

	if ( el.style.display == 'none' ) {
            el.style.display = 'block';
            if(div_id == 'blanket') {
              return;
            }
            ds_id = lastClickedGraph.split("_")[1];
            expand_svg(ds_id);
        }
	else {
          el.style.display = 'none';
          if(div_id == 'blanket') {
            return;
          }
          // shrink svg
          shrink_svg(ds_id);

          // removes everything from modal
          $('#modalDiv #graphDiv_'+ds_id).remove();
          $('#modalDiv #menu_'+ds_id).remove();
        }
}

function blanket_size(modalDivVar) {
	if (typeof window.innerWidth != 'undefined') {
		viewportheight = window.innerHeight/2;
	} else {
		viewportheight = document.documentElement.clientHeight/2;
	}
	if ((viewportheight > document.body.parentNode.scrollHeight) && (viewportheight > document.body.parentNode.clientHeight)) {
		blanket_height = viewportheight;
	} else {
		if (document.body.parentNode.clientHeight > document.body.parentNode.scrollHeight) {
			blanket_height = document.body.parentNode.clientHeight;
		} else {
			blanket_height = document.body.parentNode.scrollHeight;
		}
	}
	var blanket = document.getElementById('blanket');
	blanket.style.height = blanket_height + 'px';
	var modalDiv = document.getElementById(modalDivVar);
	modalDiv_height=blanket_height/2-400;//200 is half popup's height
	modalDiv.style.top = modalDiv_height/3 + 'px';
}
function window_pos(modalDivVar) {
	if (typeof window.innerWidth != 'undefined') {
		viewportwidth = window.innerHeight;
	} else {
		viewportwidth = document.documentElement.clientHeight;
	}
	if ((viewportwidth > document.body.parentNode.scrollWidth) && (viewportwidth > document.body.parentNode.clientWidth)) {
		window_width = viewportwidth;
	} else {
		if (document.body.parentNode.clientWidth > document.body.parentNode.scrollWidth) {
			window_width = document.body.parentNode.clientWidth;
		} else {
			window_width = document.body.parentNode.scrollWidth;
		}
	}
	var modalDiv = document.getElementById(modalDivVar);
	window_width=window_width/2-400;//200 is half popup's width
	modalDiv.style.left = window_width + 'px';
}

function open_modal(windowname,action) {
  if(previous_action == action) {
    return;
  }
  previous_action = action;
	blanket_size(windowname);
	window_pos(windowname);
	toggle('blanket');
	toggle(windowname);
}
