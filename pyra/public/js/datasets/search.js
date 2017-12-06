AUTOCOMPLETE_TIMEOUT = 5000;
$(document).ready(function() {


    // This is all for using ajax to select datasets
    base_url = BASE_PATH+"datasets/search";
    filter_dict = {}; // nothing to filter
    set_view_datasets(base_url,filter_dict);
    $("#report_summary").dataTable ({
      "searching":true,
      "bPaginate": false,
      "bInfo": false,
      "oLanguage": {"sSearch": "Filter: "},
      "aaSorting": [],
    })


    // all the code below for css should opt out first div as it is for dataset search
    // css code is added here because these divs are being used accross many pages on website
    // but we only want these css changes for dataset page
    // original css for these divs is in screen.scss
    var divs = document.getElementsByClassName('enclosed_search_box')
    for (var i =1; i< divs.length; i++) {
      $(divs[i]).css('width','93%');
      $(divs[i]).css('float','right');
    }

    var basic_help_divs = document.getElementsByClassName('basic_help')
    for (var i =2; i< basic_help_divs.length; i++) {
      $(basic_help_divs[i]).css('width','100%');
    }

    var searchField_divs = document.getElementsByClassName('searchField')
    for (var i =1; i< searchField_divs.length; i++) {
      $(searchField_divs[i]).css('width','57%');
    }

    var search_box_divs = document.getElementsByClassName('search_box')
    for (var i =1; i< search_box_divs.length; i++) {
      $(search_box_divs[i]).css('width','120%');
    }

    var geneSearchForm_divs = document.getElementsByClassName('geneSearchForm')
    for (var i =2; i< geneSearchForm_divs.length; i++) {
      $(geneSearchForm_divs[i]).css('width','40%');
    }

    var filter_divs = document.getElementsByName('filter')
    for (var i =1; i< filter_divs.length; i++) {
      $(filter_divs[i]).css('width','97%');
    }

    // var geg_divs = document.getElementsByClassName('geg')
    // for (var i =1; i< geg_divs.length; i++) {
    //   $(geg_divs[i]).css('width','100%');
    // }

    // if filter specified but no ds_id selected, then run the ajax call
    db_id = $('#db_id').html();
    filter = $('#dataset_search').val();
    if (filter != "" && db_id == "") {
        filter_dict = {};
        filter_dict['filter'] = filter;

        var options = {
            base_url: base_url,
            ajax_url: BASE_PATH + "datasets/search_and_choose_datasets_ajax"
        }
        var datasets_ajax_search = ajax_search(options);
        datasets_ajax_search.get_data_from_ajax(filter_dict);
    }


    ds_id = $('#ds_id').html();
    platform_type = $('#platform_type').html();
    probe_name = $('#probe_name').html();

    if (platform_type == 'miRNA'){
        var details = new Object();
        details.id = "#miRNASearch";
        details.data_url = BASE_PATH + 'genes/get_feature_search_autocomplete?feature_type=all&db_id='+db_id;
        details.target_url = BASE_PATH + 'expressions/feature_result?graphType=default&db_id='+db_id+'&feature_type=miRNA&datasetID='+ds_id+'&feature_id=';
        details.append_to = ".searchBox";
        setup_feature_search_autocomplete(details);



        // each time the enter key pressed, get the gene details
        $('#miRNASearchForm').submit(function(){

            $("#miRNASearch").autocomplete('close');
            // getGeneDetails();
            window.location = BASE_PATH + 'expressions/feature_result?graphType=default&db_id='+db_id+'&feature_type=miRNA&feature_id=' + $("#miRNASearch").val()+ '&datasetID='+ds_id;

            return false;
        });
        $('#viewmiRNA ').click(function(){
            window.location = BASE_PATH + 'expressions/feature_result?graphType=default&db_id='+db_id+'&feature_type=miRNA&feature_id=' + $("#miRNASearch").val()+ '&datasetID='+ds_id;

        });

    }



    $('div.show_all_button a').click(function(){ show_all_datasets();});
    $('div.export_more_info a').click(function(){ show_more_info();});

    $("#probeSearchForm input").autocomplete({
        source: BASE_PATH + 'datasets/autocomplete_probes_for_dataset?ds_id='+ds_id,
        minLength: 2, // because the names are very small eg. STAT1
        timeout: AUTOCOMPLETE_TIMEOUT,
        appendTo: ".probe_search",
        select: function(event, ui) {
            var probe = ui.item.value;
            window.location = BASE_PATH + 'expressions/probe_result?graphType=default&datasetID=' +ds_id+'&probe=' +encodeURIComponent(probe)+ '&db_id=' +db_id;
        }
    });
    $("#viewProbes").click(function(){
        probe = $('#probeSearch').val();
        window.location = BASE_PATH + 'expressions/probe_result?graphType=default&datasetID=' +ds_id+'&probe=' +encodeURIComponent(probe)+ '&db_id=' +db_id;
        return false;


    });


    $("#probeSearchForm").submit(function (){
        probe = $('#probeSearch').val();
        window.location = BASE_PATH + 'expressions/probe_result?graphType=default&datasetID=' +ds_id+'&probe=' +encodeURIComponent(probe)+ '&db_id=' +db_id;
        return false;
    });

    $("#viewGenes").click(function(){
        gene = $('#geneSearch').val();
        window.location = BASE_PATH + 'expressions/result?graphType=default&datasetID=' +ds_id+'&gene=' +gene+ '&db_id=' +db_id;

    });

    $("#geneSearchForm").submit(function (){
        gene = $('#geneSearch').val();
        window.location = BASE_PATH + 'expressions/result?graphType=default&datasetID=' +ds_id+'&gene=' +gene+ '&db_id=' +db_id;
        return false;
    });

    if ($('#geneSearchForm').is(':visible')){
        $("#geneSearch").autocomplete({
            source: BASE_PATH + 'genes/get_autocomplete?db_id='+db_id,
            minLength: 4, // because the names are very small eg. STAT1
            timeout: AUTOCOMPLETE_TIMEOUT,
            appendTo: "div.gene_search",
            select: function(event, ui) {
                var gene = ui.item.ensembl_id;
                var db_id = ui.item.db_id;
                window.location = BASE_PATH + 'expressions/result?graphType=default&datasetID=' +ds_id+'&gene=' +gene+ '&db_id=' +db_id;
            }
        }).data("ui-autocomplete")._renderItem = function( ul,item ){
            return $("<li></li>").append("<a> <div class='symbol'>" + item.symbol + "</div><div class='species'>"+item.species+"</div><div class='aliases'>"+item.aliases+"</div><div class='description'>"+item.description+"</div><div class='clear'></div></a>").appendTo(ul);
        };
    };
    sample_summary_table = $('#dataset_sample_summary').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 0, "asc" ]],
        "aoColumns": [null, null],
        "bAutoWidth": false
    });
    //probe_search_triggers(selected_ds_id);

    $('#exportSampleSummaryButton').click(function(){
        $('#dataset_sample_summary').table2CSV();
    });

    choose_dataset_filter();

    // disable search bars for dataset with no data
    has_data = $(document.getElementById('has_data')).html();
    if(has_data == 'no')
    {
      $(".column2 :input").prop("disabled", true);
      $(".column2 a.searchButton").css('pointer-events','none');
      // now just enable for reports input search
      $("#report_summary_filter :input").prop("disabled", false);
    }
});

function show_more_info(){
    $('.more_info').modal({minWidth:204,minHeight:100});
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
        "bAutoWidth": false
    });
}

function show_all_datasets(){
    $('.multi_select').modal({minWidth:800,maxHeight:500});
}
