// http://stackoverflow.com/questions/486896/adding-a-parameter-to-the-url-with-javascript
function changeUrl(value,key) {
  key = encodeURI(key); value = encodeURI(value);
  var kvp = document.location.search.substr(1).split('&');
  var i=kvp.length; var x; while(i--)  {
      x = kvp[i].split('=');
      if (x[0]==key)  {
          x[1] = value;
          kvp[i] = x.join('=');
          break;
      }
  }
  if(i<0) {kvp[kvp.length] = [key,value].join('=');}

  window.history.pushState({}, '',"?"+kvp.join('&'))
}

var reA = /[^a-zA-Z]/g;
var reN = /[^0-9]/g;
function sort_object(a,b){
    return a.Mapped_gene === b.Mapped_gene ? 0 : a.Mapped_gene > b.Mapped_gene ? 1 : -1;

  }

function sortAlphaNum_array(a,b) {
  // var a = a.toLowerCase();
  // var b = b.toLowerCase();
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

function sort_array(s1, s2) {
  var s1lower = s1.toLowerCase();
  var s2lower = s2.toLowerCase();
  return s1lower > s2lower? 1 : (s1lower < s2lower? -1 : 0);
}

function sortSampleId(a,b) {
  return a.Replicate_ID > b.Replicate_ID ? 1 : -1;
}

function sort_array_of_objects(a,b) {
  var alower = a.key.toLowerCase();
  var blower = b.key.toLowerCase();
  return ((alower < blower) ? -1 : ((alower > blower) ? 1 : 0));
}

function create_array_of_colours_for_legend(legend_names, colour_object,sorted_sample_types) {
    var colour_counter = {};
    var colours = {}
  // legend_names is an object containing sample_type and corresponding sample_type_group
  // colour object is an object having list of colour for each sample type group
  for(var i=0; i<sorted_sample_types.length; i++ ) {
    var group = legend_names[sorted_sample_types[i]];

    // create a counter for every group
    if(!(group in colour_counter)) {
       colour_counter[group] = 0;
    }
    else {
      colour_counter[group] = colour_counter[group] + 1;
    }
    // now get the colour for that sample type
    colours[sorted_sample_types[i]] = colour_object[group][colour_counter[group]];
  }
  return colours;
}

function add_limit_sort_by_options_to_dropdown() {
  if (dataset_data["limitSortBy"] != 'SampleType') {
    tempList = dataset_data["limitSortBy"].split(",");
    for(i=0;i<tempList.length;i++) {
      $('#graphOptionsMenu ul').append(" <li><a href='#'' class=chooseSortType clickChoose='"+tempList[i]+"'>Group By "+tempList[i]+"</a></li>");
      if(tempList[i] != "Sample Type") {
        $('#graphOptionsMenu ul').append(" <li><a href='#'' class=chooseSortType clickChoose='"+tempList[i]+",Sample Type"+"'>Group By Sample type and "+tempList[i]+ "</a></li>");
      }
    }
  }
}

function multi_map_probe_click() {
    var options = options;
    for (var i=0;i< options.probe_order; i++) {
      $("#xLabel-"+options.probe_order[i]).on("click",function(){})
    }
}
function draw_graph_with_axis() {
  $("#x_axis_button").css("display", "none");
  show_axis = "yes";
  graph_box_width = expanded_graph_box_width; // will change this to be calculated based on probes afterwards
  toggle_counter = 1; // change the toggle counter as it is toggled
  draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
}

function draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis) {
  // title is created for new graph
  main_title = return_title(ref_type_for_title,symbol,sortBy);

  // toggle min y axis should always be false for bar graph
  if (graphType == "bar"){show_min_y_axis = false;}

  // when line graph only sort by Sample type
  if(graphType == "line") {sortBy = "Sample_Type";}

  // before making graph, create a colours first for legend that can be passed on to the graph
  if (graphType == "box" || graphType == "bar" || graphType == "violin") {
    var sorted_sample_types = Object.keys(dataset_data['sampleTypeDisplayGroups']).sort(function(a,b){return dataset_data['sampleTypeDisplayGroups'][a]-dataset_data['sampleTypeDisplayGroups'][b]})
    var colours = create_array_of_colours_for_legend(dataset_data["sampleTypeDisplayGroups"],dataset_data["sampleTypeDisplayGroupColours"],sorted_sample_types)
  }
  else {
    var colours = dataset_data['probeColours'];
  }
  $("a.chooseSortType").show();

  if (graph_data_error == "" && dataset_error == ""){
    if (graphType == "scatter") {
      $("li.toggle_select_probes").hide();
      $("li.chooseSD").show(); // this is to show toggle Standard_Deviation option in dropdown
      document.getElementById("showScatterDiv").style.display = "none";
      changeUrl('scatter','graphType');
      run_scatter_gene_expression_graph(colours,graphDiv,sortBy,show_min_y_axis,legend_required,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,probe_name,ref_type);
    }
    else if (graphType == "box") {
      $("li.toggle_select_probes").show();
      $("li.chooseSD").hide();

      document.getElementById("showScatterDiv").style.display = "block";



      changeUrl('box','graphType');
      run_box_bar_gene_expression_graph(colours,graphDiv,"no",sortBy,show_min_y_axis,legend_required,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,probe_name,ref_type);
    }
    else if (graphType == "bar") {
      $("li.toggle_select_probes").show();
      $("li.chooseSD").show();
      document.getElementById("showScatterDiv").style.display = "block";
      changeUrl('bar','graphType');
      run_box_bar_gene_expression_graph(colours,graphDiv,"yes",sortBy,show_min_y_axis,legend_required,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,probe_name,ref_type);
    }
    else if (graphType == "line") {
      $("a.chooseSortType").hide();
      $("li.toggle_select_probes").show();
      $("li.chooseSD").hide();
      document.getElementById("showScatterDiv").style.display = "none";
      changeUrl('line','graphType');
      run_line_gene_expression_graph(colours,graphDiv,sortBy,show_min_y_axis,ref_name,main_title,scaling_required,dataset_data,probe_name,ref_type);
    }
    else if (graphType == "violin") {
      $("li.toggle_select_probes").show();
      $("li.chooseSD").hide();
      document.getElementById("showScatterDiv").style.display = "none";
      changeUrl('violin','graphType');
      run_violin_gene_expression_graph(colours,graphDiv,sortBy,show_min_y_axis,ref_name,main_title,scaling_required,dataset_data,probe_name,ref_type);
    }
  }

  else {
    // used for probe and miRNa search mainly, when the search does not match any valid ref_id
    $("#graphDiv").append("<div class='errorTextColumn'><div id='errorText' class='title errorBox'><div id='message'>Graph Not Found.</div><div id='prompt'> <span id = 'prompt-message'>The Graph is not available for chosen parameters.</span> <br><br> Please Try Following: <br><br> Change Dataset using 'Change Datasets' button provided above <br><br> Change "+ ref_type_for_title+" name using the search box provided above <br><br>If you typed the page address in the Address bar, check the spelling and use of upper-case and lower-case letters. </div></div></div>");

    disable_buttons();
  }
}

function disable_buttons() {
  $('.buttonMenus > li> a').on('click', function(event) {
    event.preventDefault();
    return false;
   })
  $('.geneInfoButton').addClass("disabled");
}

function toggle_SD(){
      $("#toggleSD").unbind();
      $("#toggleSD").on('click',function(){
        if(options.whiskers_needed != undefined) {
          options.whiskers_needed = !options.whiskers_needed;
          whiskers_needed= !whiskers_needed;
        }
        draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,options.whiskers_needed,scaling_required,dataset_data,show_axis);
      });

}

// http://stackoverflow.com/questions/8847766/how-to-convert-json-to-csv-format-and-store-in-a-variable
function ConvertToTSV(objArray) {
      var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
      var str = '';

      var header = Object.keys(data[0]).join(",");
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

function toggleYaxis() {
  $("#no_set_min_y_axis_link").on('click',function(){
    show_min_y_axis = !show_min_y_axis;
    draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis)
  });
}
toggle_counter = 0;
function toggleHorizontal(){
  $("#zoomHorizontalGraphButton").on("click",function(){
    if((unique_probes_sorted.length * dataset_data['sampleTypeDisplayOrder'].split(",").length * 40) > graph_box_width || (ref_type == "gene_set_id")){ // expand when num of probes * sample types * 40 pixels < 900 pixels
      if(toggle_counter == 0) {
        graph_box_width = expanded_graph_box_width;
        toggle_counter++;
        show_axis = "yes";
        draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
      }
      else{
        toggle_counter--;
        graph_box_width = normal_graph_box_width;
        show_axis = "no";
        draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
      }

    }
    else if(graph_box_width > normal_graph_box_width) {
      if(toggle_counter == 1) { toggle_counter --;}
      graph_box_width = normal_graph_box_width;
      draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
    }
  });
}

function click_share_link(){
    var elements = $('#share_link,a.share_link');
    elements.unbind().click(function(){

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

function export_graph_image() {


    $("a.exportImageButton").on("click",function(){
      d3.selectAll('.probe_text').style("opacity",0);
      d3.selectAll('.hidden-probe_text').style("opacity",1);
      d3.selectAll('.exposed_legend').style("opacity",0);
      d3.selectAll('.hidden_legend').style("opacity",1);

      var svg = document.querySelector( "svg" );
      var svg_xml = new XMLSerializer().serializeToString( svg);
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

function export_graph_data(){
    // force download is made by ading headers Content-Disposition in the data returned from server, unable to download the file from client side on IE and Safari
    $(".export_graph_data").on("click",function(){
        var tsv_data = ConvertToTSV(data);
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


function choose_dataset_filter(){
    choose_dataset = $('#choose_dataset').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 0, "asc" ]],
        "aoColumns": [null],
        "bAutoWidth": false,
        "oLanguage": {"sSearch": "Filter: "},
    });
}

function show_all_datasets(){
    $('.multi_select').modal({minWidth:800,maxHeight:500});
}

function set_gene_search_and_autocomplete(){
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

        $('#viewGenes,#geneSearchSubmit').click(function(){
            var gene = $('#geneSearch').val();
            change_gene(gene);
            return false;
      	});
        $('#geneSearchForm').submit(function(e){
            e.preventDefault();
            var gene = $('#geneSearch').val();
            change_gene(gene);
            return false;
        });

   }

}

function set_feature_search_and_autocomplete(){
    var graphRadioValue='default';

    var details = new Object();
    details.id = "#featureSearch";
    details.data_url = BASE_PATH + 'genes/get_feature_search_autocomplete?feature_type=all&db_id='+db_id;
    details.target_url = BASE_PATH + 'expressions/feature_result?graphType='+graphType+'&datasetID='+ds_id+'&feature_type=miRNA&db_id='+db_id+'&feature_id=';
    details.append_to = ".searchBox";
    setup_feature_search_autocomplete(details);

    $('#viewGenes,#featureSearchSubmit').click(function(){
        chosen_feature_action();
        return false;
	});
    $('#featureSearchForm').submit(function(e){
        e.preventDefault();
        chosen_feature_action();
        return false;
    });

}


function chosen_feature_action(){
    var graphRadioValue='default';
    var feature = $('#featureSearch').val().replace('+','%2B');
    window.location = BASE_PATH + 'expressions/feature_result?graphType='+graphRadioValue+'&datasetID='+ds_id+'&feature_type=miRNA&feature_id='+encodeURIComponent(feature)+'&db_id='+db_id;

}

function set_probe_search_and_autocomplete(){
    $("#probeSearch").autocomplete({
        source: BASE_PATH + 'datasets/autocomplete_probes_for_dataset?ds_id='+ds_id,
        minLength: 2, // because the names are very small eg. STAT1
        timeout: AUTOCOMPLETE_TIMEOUT,
        appendTo: ".searchBox",
        select: function(event, ui) {
            var probe = ui.item.value;
            chosen_probe_action(probe);
        }
    });
    $('#viewProbes,#probeSearchSubmit').click(function(){
        var probe = $('#probeSearch').val();
        chosen_probe_action(probe);
        return false;
	});
    $('#probeSearchForm').submit(function(e){
        e.preventDefault();
        var probe = $('#probeSearch').val();
        chosen_probe_action(probe);
        return false;
    });
}

function chosen_probe_action(probe){
    window.location = BASE_PATH + 'expressions/probe_result?graphType='+graphType+'&datasetID='+ds_id+'&probe='+encodeURIComponent(probe)+'&db_id='+db_id;

}

function change_gene(gene){
        if (gene != '' && gene != undefined){
            if (!window.location.origin)
               window.location.origin = window.location.protocol+"//"+window.location.host;
            new_url = window.location.origin + window.location.pathname + '?graphType='+graphType+'&datasetID='+ds_id+'&gene='+gene+'&db_id='+db_id;
            window.location = new_url;
        }
}

function click_choose_datasets(){
    $('#chooseDatasets').unbind();
    $('#chooseDatasets').click(function(e){
        if(e.preventDefault) { e.preventDefault();} else {  e.returnValue = false; }

        show_all_datasets();
        choose_dataset_filter();

    });
}
function click_select_probes(){

    $('#toggle_select_probes').unbind();
    $('#toggle_select_probes').on('click',function(){
        if (click_to_select_probes == false){
            click_to_select_probes = true;

            probe_name_element = $('#probe_name');
            if (probe_name_element.length){
                probe_n = probe_name_element.html();
            } else {
                probe_n = 'Probe';
            }


            new_html =  '<div id="store_and_submit_select_probes" class="select_probes">' +
                        '<div class="title">Select '+probe_n+'s</div>'+
                        '<div class="help">Click on the '+probe_n+'s under the graph to select and then submit to view them</div>'+ '<textarea id="textarea-probe"></textarea>'+
                        '<input type="submit"></submit>' +
                        '</div>'
            $('body').append(new_html);
            $('div.select_probes').draggable();
            $('div.select_probes input').click(function(){
                var url = new URL(document.URL);
                var probes=$('div.select_probes textarea').val();

                // probes = probes.replace(/\s{1,}/g,DELIMITER);console.log(probes)
                url.get_data['select_probes'] = encodeURIComponent(probes);
                new_url = url.get_url();

                window.location = new_url;

            });

        } else {
            if (click_to_select_probes == true){
                click_to_select_probes = false;
                $('div.select_probes input').unbind();
                $('div.select_probes').draggable('disable');
                $('#store_and_submit_select_probes').remove();

            }
        }
    });

}

function return_title(ref_type_for_title,ref_id_name,sortByoption) {
  var sortByoption = sortByoption.split("_").join(" ");
  var title_prefix = "Gene";
  if(ref_type == "probeID") {
   if (ref_id_name.match(/\s/g)) {
      ref_id_name = "Selected";
    }
    else {
      ref_id_name = symbol;
    }
    title_prefix = "";
  }
  else if (ref_type == "gene_set_id") {
    ref_id_name = "";
    title_prefix = "";
  }
 if (graphType == "line"){
    var main_title =  title_prefix +" Expression Graph for " + ref_type_for_title + " " + ref_id_name + " grouped by line groups";
    }
    else {
    var main_title =  title_prefix +" Expression Graph for " + ref_type_for_title + " " + ref_id_name + " grouped by "+ sortByoption;
}

  return main_title;
}

// asks for notification premission
//Notification.requestPermission().then(function(result) {
//});

function spawnNotification() {
  var permission = Notification.permission;
  if (permission !== "denied") {
    show_notifications = true;
  }
}

$(document).ready(function() {
    AUTOCOMPLETE_TIMEOUT = 5000;
    // y_axis_label = $('#y_axis').html();
    ds_id = $('#ds_id').html();
    db_id = $('#db_id').html();
    ref_id = $('#ref_id').html();
    symbol = $('#symbol').html();
    unique_probes_sorted = [];
    gene_set_name= $('#gene_set_name').html();
    probe_name = $("#probe_name").html();
    chip_type = $("#chip_type").html();
    show_notifications = false;
    show_axis = "no"; // this toggles x axis when sample type and probe together are greater than 30
    if(chip_type == 'None' || chip_type == "") {
      $("#graphDiv").append("<div class='errorTextColumn'><div id='errorText' class='title errorBox'><div id='message'>Graph Not Found.</div><div id='prompt'> <span id = 'prompt-message'>The Graph is not available for chosen parameters.</span> <br><br> Please Try Following: <br><br> Change Dataset using 'Change Datasets' button provided above <br><br> Change Gene name using the search box provided above <br><br>If you typed the page address in the Address bar, check the spelling and use of upper-case and lower-case letters. </div></div></div>");
      disable_buttons();
      // notification
      // alertify.set('notifier','position', 'top-right');
      // alertify.notify('Error notification message.','custom',15);
    }
    graphType = $('#graphType').html();
    click_to_select_probes = false;
    if (graphType== "" || graphType == undefined || graphType == "default") {graphType = "box"}
    ref_type = $('#ref_type').html();
    legend_required = "yes";
    whiskers_needed = true;
    multiview_graph = "no";
    ref_name = {}; // this hold the name of mapped gene which is prefixed to probe name on x axis

    scaling_required = "no" // this is used when multi view to make graph small
    // this is required to build up title
    if(ref_type == "ensemblID") {ref_type_for_title = "Gene"}
    else if(ref_type == "probeID" ) {ref_type_for_title = "Probe"}
    else if (ref_type == "miRNA") {ref_type_for_title = "miRNA"}
    else if(ref_type == "gene_set_id") {ref_type_for_title = gene_set_name; symbol=ref_id;}

    sortBy = $('#sortBy').html();
    if (sortBy == "" || sortBy == undefined || sortBy== "Sample Type") {
      sortBy = "Sample_Type";
    }
    var graphDiv = document.getElementById("graphDiv");
    var window_url = window.location.href;
    select_probes = $('#select_probe').html();
    http_variable = window_url.split("stemformatics")[0]
    show_min_y_axis = false;
    normal_graph_box_width = 900;
    graph_box_width = normal_graph_box_width;
    main_title = return_title(ref_type_for_title,symbol,sortBy);

    if (select_probes != "") { // select_probes is the one causes the parameter bug
      graph_data_url = '/expressions/graph_data?db_id='+db_id+'&ds_id='+ds_id+'&ref_id='+encodeURIComponent(select_probes)+'&ref_type=' + 'ensemblID'  + '&graph_type=' + graphType;
    }
    else {
          
          graph_data_url = '/expressions/graph_data?db_id='+db_id+'&ds_id='+ds_id+'&ref_id='+encodeURIComponent(ref_id)+'&ref_type=' + ref_type  + '&graph_type=' + graphType;
    }

    dataset_data_url = "/expressions/dataset_metadata?ds_id=" + ds_id;


    function ajax1() {
      return $.ajax({
        url : dataset_data_url,
        success: function(response) {
          dataset_metadata = JSON.parse(response);
          dataset_data = JSON.parse(dataset_metadata.data);
          dataset_error = dataset_metadata.error;
          if(dataset_error == "") {
            dataset_data["sampleTypeDisplayGroups"] = JSON.parse(dataset_data["sampleTypeDisplayGroups"])

          if((dataset_data["lineGraphOrdering"]) && (dataset_data["lineGraphOrdering"] != "NULL") && (dataset_data["lineGraphOrdering"] != "")) {
            dataset_data["lineGraphOrdering"] = JSON.parse(dataset_data["lineGraphOrdering"]);
          }

          if ((dataset_data['detectionThreshold']) == "" || isNaN(dataset_data['detectionThreshold']) ) {
            dataset_data['detectionThreshold'] = "NULL";
          }
          if ((dataset_data['medianDatasetExpression']) == "" || isNaN(dataset_data['medianDatasetExpression']) ){
            dataset_data['medianDatasetExpression'] = "NULL";
          }
          }
          }
      });
    }

    function ajax2() {
      return $.ajax({
        url: graph_data_url,
        success: function(response) {
          graph_data = JSON.parse(response);
          json_data = JSON.parse(graph_data.data);
          if(json_data != null) {
            data = json_data //(json_data.sort(sortSampleId));
          }
          else {
            data = "";
          }
          graph_data_error = graph_data.error;

          if (graph_data_error == "") {
            unique_probes = []; //list of unique probes

            if(ref_type == "gene_set_id") {
              sorted_data = data.sort(sort_object)
              for(i = 0; i< sorted_data.length; i++) {
                // .indexOf is supported by all browsers therefore it should be used
                if((unique_probes.indexOf(data[i].Probe) == -1)) { unique_probes.push(data[i].Probe); }
              }
              unique_probes_sorted = unique_probes
            }
            else {
              for(i = 0; i< data.length; i++) {
                // .indexOf is supported by all browsers therefore it should be used
                if((unique_probes.indexOf(data[i].Probe) == -1)) { unique_probes.push(data[i].Probe); }
              }
              unique_probes_sorted = unique_probes.sort(sortAlphaNum_array);
            }

            // for each limit sort by option lets calculate x axis label
            limitSortByArray = dataset_data["limitSortBy"].split(",");
            x_axis_label_object = {}
            for(i=0;i < limitSortByArray.length; i++) {
              groupByOption = limitSortByArray[i];
              groupByOption_with_underscore = groupByOption.replace(" ","_");
              x_axis_label_object[groupByOption_with_underscore] = []
                  for(j = 0; j< data.length; j++) { // iterate over data
                    if((x_axis_label_object[groupByOption_with_underscore].indexOf(data[j][groupByOption_with_underscore]) == -1)) {
                        x_axis_label_object[groupByOption_with_underscore].push(data[j][groupByOption_with_underscore]);
                      }
                  }

            }
          }
        }// end success
      });
    }

    $.when(ajax1(),ajax2()).done(
      function(){
          scatter_needed = "yes";
          expanded_graph_box_width  = unique_probes_sorted.length * dataset_data['sampleTypeDisplayOrder'].split(",").length * 40;
          if(expanded_graph_box_width < graph_box_width) {expanded_graph_box_width= graph_box_width;}
          add_limit_sort_by_options_to_dropdown();
          if(ref_type == 'ensemblID') {
            ref_name[symbol] = symbol;
          }
          else if (ref_type == "probeID"){
            var ref_id_array = ref_id.split(" ")
            for(var i =0; i < ref_id_array.length; i++) {
              for(var j =0; j < data.length; j++) {
                if(data[j]["Probe"] == ref_id_array[i]) {
                  ref_name[data[j]["Probe"]] =data[j]["Mapped_gene"] ;
                  break;
                }
              }
            }
          }
          else if(ref_type == "miRNA") {
            ref_name[symbol] = symbol;
          }
          else if(ref_type = "gene_set_id") {
            for(var i=0;i<unique_probes_sorted.length;i++) {
              for(var j =0; j < data.length; j++) {
                if(data[j]["Probe"] == unique_probes_sorted[i]) {
                  ref_name[data[j]["Probe"]] =data[j]["Mapped_gene"] ;
                  break;
                }
              }
            }
          }
          $("#showScatter").click(function () {
                            // scatter onoff
                            if(scatter_needed == "yes") {scatter_needed = "no";}
                            else {scatter_needed = "yes";}
                            draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
              });
          draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);

          // gene search
          if ($("#geneSearchForm").is(":visible")){
            $('#viewGenes').click(function(){
                var ref_id = $('#geneSearch').val();
                graph_data_url = http_variable + 'stemformatics.org/expressions/graph_data?db_id='+db_id+'&ds_id='+ds_id+'&ref_id='+ref_id+'&ref_type='+ref_type + '&graph_type=' + graphType ;
                $.when(ajax2()).done(
                  function(){
                    // clear and draw graph again
                    $("#graphDiv").empty();
                    $('#graphOptionsMenu .chooseSortType').remove();
                    add_limit_sort_by_options_to_dropdown();
                    draw_graph(graph_data_error,dataset_error,"box",sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
                  });
               });
            }
          // gene search end

          // other js stuff
            $("a.chooseSortType").click(function(){
              sortBy  = $(this).attr('clickChoose');
              sortBy = sortBy.replace(" ","_");
              changeUrl(sortBy,'sortBy');
              draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
            });

              $('a.chooseGraphType').on("click",function(){
                graphType = $(this).attr('clickChoose');
                draw_graph(graph_data_error,dataset_error,graphType,sortBy,show_min_y_axis,ref_name,main_title,whiskers_needed,scaling_required,dataset_data,show_axis);
              });

              toggle_SD();
              toggleYaxis();
              toggleHorizontal();
              click_share_link();
              export_graph_image();
              export_graph_data();
              click_gene_info();
              contextHelpClick();
              click_select_probes();
              click_choose_datasets();
              if($('#choose_dataset_immediately').html() == 'True'){
                  $('#chooseDatasets').click();
              }
              set_gene_search_and_autocomplete();
              set_probe_search_and_autocomplete();
              set_feature_search_and_autocomplete();

       });



     });
