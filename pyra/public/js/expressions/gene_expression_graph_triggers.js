var small_width = 1275; // comment here
var large_width = 4300;
var small_height = 900;
var large_height = 2500;

var largeWidth = 4000;
var AUTOCOMPLETE_TIMEOUT = 5000;
var standardHeight = 964;
var standardIE7Height = 984;
var ie7ChangeInnerDiv = 758;

// make these variables global
var ds_id = 0;
var db_id = '';
var this_graph_data = {};
function afterGraphDrawn(){
    db_id = this_graph_data.view_data.db_id;
    contextHelpClick();
    check_remove_loading();
    hide_tables();
    add_buttons_for_viewing_graph_tables();
    set_draggables();
    plot_hover();

    // add buttons must be set first
    set_clicks();

}
function set_draggables(){
    $('div.movable_legend').draggable();
}

function set_autocomplete(){
    set_gene_search_and_autocomplete();
    set_probe_search_and_autocomplete();
    set_feature_search_and_autocomplete();
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

        $('#geneSearchForm').unbind();

        $('#geneSearchForm').submit(function(){
            $("#geneSearch").autocomplete('close');
            var gene = $('#geneSearch').val();
            change_gene(gene);
            return false;
        });

   }





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
function set_feature_search_and_autocomplete(){
    var graphRadioValue='default';

    var details = new Object();
    details.id = "#featureSearch";
    details.data_url = BASE_PATH + 'genes/get_feature_search_autocomplete?feature_type=all&db_id='+db_id;
    details.target_url = BASE_PATH + 'expressions/feature_result?graphType='+graphRadioValue+'&datasetID='+ds_id+'&feature_type=miRNA&db_id='+db_id+'&feature_id=';
    details.append_to = ".searchBox";
    setup_feature_search_autocomplete(details);





    $('#featureSearchSubmit').click(function(){
        chosen_feature_action();
        return false;
	});


    $('#featureSearchForm').submit(function(e){
        e.preventDefault();
        chosen_feature_action();
        return false;
    });


}



function check_remove_loading(){
    // check if graph is found
    if ($('div.legend').length != 0){
        $('div.loading').removeClass('loading');
    }
}

function hide_tables(){
    $("#showTableData"+ds_id+" table").hide();
    $("#showRawTableData"+ds_id+" table").hide();
    $('#zoomGraphTableButton').hide();
}

function add_buttons_for_viewing_graph_tables(){
    $('#showGraphTableButton').click(function(){

        $('#showTableData'+ds_id+' table').toggle();
        $('#zoomGraphTableButton').toggle();


    });

    $('#zoomGraphTableButton').click(function(){
		// add font-size to be normal 12px;

        if ($('#showTableData'+ds_id+' td').css('font-size') == '8px'){
            $('#showTableData'+ds_id+' td').css('font-size','12px');
            $(this).html('- COLLAPSE TABLE');
        } else {
            $('#showTableData'+ds_id+' td').css('font-size','8px');
            $(this).html('+ EXPAND TABLE');
        }
    });

 }

function plot_hover(){
    var previousPoint = null;

    $(this_graph_data.view_data.graph_id).bind("plothover", function (event, pos, item) {


        if (item) {
            if (previousPoint != item.datapoint) {
                previousPoint = item.datapoint;

                $("#tooltip").remove();
                // don't show standard deviation

                graph_type = this_graph_data.view_data.graph_type ;
                var x1 = pos.pageX.toFixed(2),
                y1 = pos.pageY.toFixed(2);

                intX = parseInt(x1)
                intY = parseInt(y1)

                offset = this_graph_data.view_data.plot.offset();
                switch (graph_type){

                    case "scatter":
                        probe = item.series.label;
                        sample_number = item.datapoint[0];
                        expression_value = item.series.data[sample_number - 1][1];
                        sample_id = item.series.data[sample_number - 1][2];
                        description = sample_id + ' - ' + probe;
                        break;
                    case "bar":
                    case "box":
                        description = item.series.hoverLabel;
                        break;
                    case "line":
                        description = item.series.hoverLabel+ ' [' + item.series.show_xaxis_labels_full[item.dataIndex] + ']';

                    break;

                }

                showTooltip(intX  - offset.left + 210, intY - offset.top + 170,description);
            }
        }
        else {
            $("#tooltip").remove();
            previousPoint = null;
        }

    });

}

function showTooltip(x, y, contents) {

    $('<div id="tooltip">' + contents + '</div>').css( {
        position: 'absolute',
        display: 'none',
        top: y,
        left: x,
        border: '1px solid #fdd',
        padding: '2px',
        'z-index': 101,
        'background-color': '#fee',
        opacity: 0.80
    }).appendTo(this_graph_data.view_data.graph_id).fadeIn(200);
}


function click_linkButtons(){
    $('a.linkButtons').click(function(event){
        //handle ie7
        if ($(this).attr('id') !='help'){

            if(event.preventDefault) { event.preventDefault();} else {  event.returnValue = false; }
        }
    });
}

function set_clicks(){

    click_choose_graph_type();
    click_toggle_sd();
    click_choose_sort_type();
    click_zoom_horizontal();
    click_no_set_min_y_axis();
    click_choose_datasets();
    click_gene_info();
    click_view_genes();
    click_export_functions();
    click_share_link();
    click_linkButtons();
    click_select_probes();
    // not in use:
    // click_zoom_vertical();
    // click_normal_link();
}

function click_select_probes(){

    $('#toggle_select_probes').unbind();
    $('#toggle_select_probes').on('click',function(){
        if (this_graph_data.view_data.click_to_select_probes == false){
            this_graph_data.view_data.click_to_select_probes = true;
            selectGraphToDraw();

            probe_name_element = $('#probe_name');
            if (probe_name_element.length){
                probe_name = probe_name_element.html();
            } else {
                probe_name = 'Probe';
            }


            new_html =  '<div id="store_and_submit_select_probes" class="select_probes">' +
                        '<div class="title">Select '+probe_name+'s</div>'+
                        '<div class="help">Click on the '+probe_name+'s under the graph to select and then submit to view them</div>'+ '<textarea></textarea>'+
                        '<input type="submit"></submit>' +
                        '</div>'
            $('body').append(new_html);
            $('div.select_probes').draggable();
            $('div.select_probes input').click(function(){
                var url = new URL(document.URL);
                var probes=$('div.select_probes textarea').val();
                probes = probes.replace(/\s{1,}/g,DELIMITER);
                url.get_data['select_probes'] = encodeURIComponent(probes);
                new_url = url.get_url();

                window.location = new_url;

            });

        } else {
            if (this_graph_data.view_data.click_to_select_probes == true){
                this_graph_data.view_data.click_to_select_probes = false;
                selectGraphToDraw();
                $('div.select_probes input').unbind();
                $('div.select_probes').draggable('disable');
                $('#store_and_submit_select_probes').remove();


            }
        }
    });

}

function toggle_standard_deviation(){
    var sd_option = this_graph_data.view_data.show_standard_deviation;

    if (sd_option == "on"){
        this_graph_data.view_data.show_standard_deviation = 'off';
    } else {
        this_graph_data.view_data.show_standard_deviation = 'on';
    }
    selectGraphToDraw();
}


function check_choose_dataset_immediately(){
    this_graph_data.choose_dataset_immediately = $('#choose_dataset_immediately').html();
    if (this_graph_data.choose_dataset_immediately == 'True'){
        $('#chooseDatasets').click();

    }

}



function chosen_probe_action(probe){
    var graphRadioValue='default';
    window.location = BASE_PATH + 'expressions/probe_result?graphType='+graphRadioValue+'&datasetID='+ds_id+'&probe='+encodeURIComponent(probe)+'&db_id='+db_id;

}


function chosen_feature_action(){
    var graphRadioValue='default';
    var feature = $('#featureSearch').val().replace('+','%2B');
    window.location = BASE_PATH + 'expressions/feature_result?graphType='+graphRadioValue+'&datasetID='+ds_id+'&feature_type=miRNA&feature_id='+encodeURIComponent(feature)+'&db_id='+db_id;

}

function change_gene(gene){
        if (gene != '' && gene != undefined){
            graph_type = this_graph_data.view_data.graph_type;
            sort_by = this_graph_data.view_data.sort_by;
            if (!window.location.origin)
               window.location.origin = window.location.protocol+"//"+window.location.host;
            new_url = window.location.origin + window.location.pathname + '?graphType='+graph_type+'&datasetID='+ds_id+'&gene='+gene+'&db_id='+db_id+'&sortBy='+sort_by;
            window.location = new_url;
        }
}





function set_large(){
    // sometimes it doesn't render using the css height so we have to force it here.
    if (CURRENT_URL.queryKey.size == "large") {
        $(this_graph_data.view_data.graph_id).height(large_height).width(large_width);
    } else {
        $(this_graph_data.view_data.graph_id).height(small_height).width(small_width);
    }
}

function click_choose_graph_type(){
    $('a.chooseGraphType').unbind();
    $('a.chooseGraphType').on("click",function(){
        var choice = $(this).attr('clickChoose');

        /* Box plot and bar graph show the same values, scatterplot is different */
        var old_url = window.location.href;

        switch (choice){

            case "scatter":
                var new_url = old_url.replace(/graphType=[A-za-z]*/g,"graphType=scatter");
                break;
            case "bar":
                var new_url = old_url.replace(/graphType=[A-za-z]*/g,"graphType=bar");
                break;
            case "line": // T#569
                var new_url = old_url.replace(/graphType=[A-za-z]*/g,"graphType=line");
                break;

            case "box":
                var new_url = old_url.replace(/graphType=[A-za-z]*/g,"graphType=box");
                break;
        }

        // needed for the graph size to reset
        var new_url = new_url.replace("&size=large","");

        window.location = new_url;


    });

}


function click_toggle_sd(){
    $("#toggleSD,a.toggle_sd").unbind();
    $("#toggleSD,a.toggle_sd").click(function(){
        toggle_standard_deviation();
    });
}


function click_choose_sort_type(){
    $("a.chooseSortType").unbind();
    $("a.chooseSortType").click(function(){
        var choice = $(this).attr('clickChoose');
        $(this).addClass('bold');
        /* Box plot and bar graph show the same values, scatterplot is different */
        var old_url = window.location.href;

        var new_url = old_url.replace('#','').replace('%20').replace(/\&sortBy=[A-za-z 0-9\-]*/g,"");

        new_url = new_url +  "&sortBy="+choice;

        window.location = new_url;


    });
}


function click_zoom_vertical(){
    $("#zoomVerticalGraphButton").unbind();
    $('#zoomVerticalGraphButton').click(function(){
        var height = $(this_graph_data.view_data.graph_id).css('height');
        if (height == '503px'){
            $(this_graph_data.view_data.graph_id).css('height','200px');
            selectGraphToDraw();
        } else {
            $(this_graph_data.view_data.graph_id).css('height','503px');
            selectGraphToDraw();
        }

    });
}

function click_zoom_horizontal(){
    graph_id = this_graph_data.view_data.graph_id;


    large_width = this_graph_data.view_data.probe_list.length *350;
    if (large_width > 10000) {
        large_width = 10000;
    }

    if (large_width < small_width){
        large_width = small_width;
    }


    $('#zoomHorizontalGraphButton').unbind();
    $('#zoomHorizontalGraphButton').click(function(){
        var width = $(graph_id).css('width');
        if (width == small_width+'px'){
            $(graph_id).css('width',large_width+'px');
            $('div.backgroundGraph').css('width',(large_width + 110) +'px');
            $('#xaxis_labels'+ds_id).css('width',(large_width - 110) +'px');
            this_graph_data.view_data.expand_horizontally = true;
            this_graph_data.view_data.expand_horizontally_width = large_width;

            selectGraphToDraw();
        } else {
            $(graph_id).css('width',small_width);
            $('div.backgroundGraph').css('width',(small_width + 110) +'px');
            $('#xaxis_labels'+ds_id).css('width',(small_width - 110) +'px');
            this_graph_data.view_data.expand_horizontally = false;
            selectGraphToDraw();
        }
    });
}

function click_no_set_min_y_axis(){
    $('#no_set_min_y_axis_link').unbind();
    $('#no_set_min_y_axis_link').click(function(){
        no_set_min_y_axis = this_graph_data.view_data.min_y_axis;
        if (no_set_min_y_axis == null) {
            this_graph_data.view_data.min_y_axis = this_graph_data.view_data.original_min_y_axis;
        } else {
            this_graph_data.view_data.min_y_axis = null;
        }
        selectGraphToDraw();
    });
}


function click_normal_link(){
    $('a.normal_link').unbind();
    $('a.normal_link').click(function(){
            window.location = $(this).attr('href');
    });


}
function click_choose_datasets(){
    $('#chooseDatasets').unbind();
    $('#chooseDatasets').click(function(e){
        if(e.preventDefault) { e.preventDefault();} else {  e.returnValue = false; }

        show_all_datasets();
        choose_dataset_filter();

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

function click_view_genes(){
    $('#viewGenes').unbind();
    $('#viewGenes').click(function(){
        $('#geneSearchForm').submit();
    });
}

function click_export_functions(){
     $('.export_graph_data').unbind();
     $('.export_graph_data').click(function(){
        ds_id = $(this).attr('data-id');

        identifier = '#show_graph_data'+ds_id + ' table';
        $(identifier).table2CSV();
    });


    export_image_button_click();
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

                    var post_url = BASE_PATH + 'auth/share_gene_expression';
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
