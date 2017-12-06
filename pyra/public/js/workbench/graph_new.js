var reA = /[^a-zA-Z]/g;
var reN = /[^0-9]/g;
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


$(document).ready(function() {
  show_min_y_axis = "false";
  ref_name = "";
  ds_id = $('#ds_id').html();
  db_id = $('#db_id').html();
  symbol = $('#symbol').html();
  sortBy = "Sample_Type";
  multiview_graph = "no";
  choose_dataset_immediately = $('#choose_dataset_immediately').html();
  probe_list = $("#probe_list").html().replace(/\[|]/g, '').replace(/ /g, '').replace(/','/g,';').replace(/'/g,'').split(';');
  ref_type = 'probeID';
  var window_url = window.location.href;
  graph_status  = "loading";
  http_variable = window_url.split("stemformatics")[0];
  dataset_data_url = http_variable + "stemformatics.org/expressions/dataset_metadata?ds_id=" + ds_id;
  // for(var i=0; i< probe_list.length; i ++) {
  //   main_title[i] = "Expression Graph for " + probe_list[i] + " for Dataset " + ds_id + " for Gene " + symbol +" grouped by Sample Type";
  // }

  legend_required = "no";
  function ajax1() {
    return $.ajax({
      url : dataset_data_url,
      success: function(response) {
        dataset_metadata = JSON.parse(response);
        dataset_data = JSON.parse(dataset_metadata.data);
        if((dataset_data["lineGraphOrdering"]) && (dataset_data["lineGraphOrdering"] != "NULL")) {
          dataset_data["lineGraphOrdering"] = JSON.parse(dataset_data["lineGraphOrdering"]);
        }

        dataset_error = dataset_metadata.error;
        if ((dataset_data['detectionThreshold']) == "" || isNaN(dataset_data['detectionThreshold']) ) {
          dataset_data['detectionThreshold'] = "NULL";
        }
        if ((dataset_data['medianDatasetExpression']) == "" || isNaN(dataset_data['medianDatasetExpression']) ){
          dataset_data['medianDatasetExpression'] = "NULL";
        }
        // call the data for each probe
        probe_list.every(ajax2)
        }
    });
  }

  function sortSampleId(a,b) {
    return a.Sample_ID > b.Sample_ID ? 1 : -1;
  }

  graph_box_width = 900;

  function ajax2(probe) {
    var graph_data_url = http_variable + 'stemformatics.org/expressions/graph_data?db_id='+db_id+'&ds_id='+ds_id+'&ref_id='+unescape(probe)+'&ref_type=' + ref_type  + '&graph_type=scatter';
    var graphDiv = document.getElementById("graphDiv_"+probe);
    return $.ajax({
      url: graph_data_url,
      success: function(response) {
        graph_data = JSON.parse(response);
        json_data = JSON.parse(graph_data.data);
        if(json_data != null) {
          data = (json_data.sort(sortSampleId));
        }
        else {
          data = "";
        }
        graph_data_error = graph_data.error;

        if (graph_data_error == "") {
          unique_probes = []; //list of unique probes
          for(i = 0; i< data.length; i++) {
            if((unique_probes.indexOf(data[i].Probe) == -1)) { unique_probes.push(data[i].Probe); }
          }
          unique_probes_sorted = unique_probes.sort(sortAlphaNum_array);

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
        main_title = "Expression Graph for " + probe + " for Dataset " + ds_id + " for Gene " + symbol +" grouped by Sample Type";
        whiskers_needed= true;
        scaling_required = "no";
        var colours = dataset_data['probeColours'];
        run_scatter_gene_expression_graph(colours,graphDiv,"Sample_Type",show_min_y_axis,legend_required,ref_name,main_title,whiskers_needed,scaling_required,dataset_data);
      }// end success
    });
  }

ajax1();

});
