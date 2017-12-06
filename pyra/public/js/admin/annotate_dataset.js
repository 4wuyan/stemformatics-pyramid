var AUTOCOMPLETE_TIMEOUT = 5000,
    SAVE_VALIDATE_TIMEOUT = 300000; // changes done for big dataset 6646
    GRAPH_TIMEOUT = 10000;
var isSorted = [false,false,false,false,false,false,false,false]; //for storing if a column has been sorted
var isSorted = [false];
var mandatory_fields = ['First Authors','Publication Citation','Publication Date','showAsPublication','Title','Publication Title','GEO Accession','Authors','Affiliation','Contact Email','Contact Name', 'PubMed ID', 'AE Accession','Description', 'cellsSamplesAssayed'];
//var ms_handle = Array();
//var bs_md_handle = Array();




function get_ds_id(){

    var ds_id = $('#ds_id').html();
    return ds_id;

}

/*
    This is a function to create a json code that can be then displayed to the user.
    The idea is that the user can then copy this to another stemformatics/3i instance
    and use the load_json to update the annotations of the identical dataset.
*/
function create_json(bs_md_handle,ms_handle){

    data_final = new Object();
    headers = get_headers(); // already in json
    biosamples_metadata = bs_md_handle.handsontable("getData");
    metastore = ms_handle.handsontable("getData");


    json_bs_md = JSON.stringify(biosamples_metadata)
    json_ms = JSON.stringify(metastore)

    data_final['biosamples_metadata'] = json_bs_md;
    data_final['metastore'] = json_ms;
    data_final['headers'] = headers;

    json_data_final = JSON.stringify(data_final);

    return json_data_final;

}
function get_list_of_chip_ids_from_biosamples_metadata(headers,biosamples_metadata){

    chip_id_position = headers.indexOf('chip_id');
    chip_ids = new Array();
    for (var position in biosamples_metadata) {

        chip_id = biosamples_metadata[position][chip_id_position];
        if (chip_id != undefined){
            chip_ids.push(chip_id);
        }
    }

    return chip_ids;
}

function get_chip_type(){
    chip_type = $('#chip_type').html();
    return chip_type;
}


function replace_ds_id_and_chip_type_in_biosamples_metadata(headers,biosamples_metadata,ds_id,chip_type){

    chip_type_position = headers.indexOf('chip_type');
    ds_id_position = headers.indexOf('ds_id');
    for (var position in biosamples_metadata) {

        biosamples_metadata[position][chip_type_position] = chip_type;
        biosamples_metadata[position][ds_id_position] = ds_id;
    }

    return biosamples_metadata;
}


/*
    This is a function to save the json data. It does a check of the chip_ids to ensure
    that we have the right dataset (as the ds_id may not be the same....

    ohhh - that might be an issue. There is a ds_id in the json data....
*/
function save_json(json_data_file){

    data_final = new Object();
    data_file = jQuery.parseJSON(json_data_file);
    json_bs_md = data_file['biosamples_metadata'];
    json_ms = data_file['metastore'];
    json_headers = JSON.stringify(data_file['headers']); // this can stay as json

    biosamples_metadata = jQuery.parseJSON(json_bs_md);
    metastore = jQuery.parseJSON(json_ms);

    // need to replace the chip_type and ds_id with the original chip_type and ds_id
    ds_id = get_ds_id();
    chip_type = get_chip_type();
    //biosamples_metadata = replace_ds_id_and_chip_type_in_biosamples_metadata(headers,biosamples_metadata,ds_id,chip_type);

    bs_md_handle = load_bs_md_into_table(biosamples_metadata);

    if (bs_md_handle == false){
        alert('This is not the correct dataset metadata as the chip ids are different. Save failed.');
    }

    ms_handle = load_ms_into_table(metastore);
    set_headers(json_headers);

    data_final['biosamples_metadata'] = biosamples_metadata;
    data_final['metastore'] = metastore;
    data_final['headers'] = json_headers;



    return data_final;

}


// This is to setup the metastore table in handsontable
function load_ms_into_table(metastore){

    for (var mkey in metastore) {
      if (metastore.hasOwnProperty(mkey)) {
        metastore[mkey][0] = HTMLDecode(metastore[mkey][0]);
        metastore[mkey][1] = HTMLDecode(metastore[mkey][1]);
      }
    }

    //metastore = metastore.replace('&quot;',"'");
    var ms_handle = $("#metastore_grid").handsontable({
            cols: metastore[0].length,
            rows: metastore.length,
            colHeaders: ['Type','Value']
            });


    // allowHtml = true allows the sampleTypeDisplayGroups to be set
    ms_handle.handsontable("loadData", metastore,allowHtml=true);
    hide_non_mandatory_dataset_fields();

    return ms_handle;
}

// from here:
// http://stackoverflow.com/questions/7837456/comparing-two-arrays-in-javascript
/*
[1, 2, [3, 4]].equals([1, 2, [3, 2]]) === false;
[1, "2,3"].equals([1, 2, 3]) === false;
[1, 2, [3, 4]].equals([1, 2, [3, 4]]) === true;
[1, 2, 1, 2].equals([1, 2, 1, 2]) === true;
*/


function test_equal(original_array,array) {
    // if the other array is a falsy value, return
    if (!array)
        return false;

    // compare lengths - can save a lot of time
    if (original_array.length != array.length)
        return false;

    for (var i = 0, l=original_array.length; i < l; i++) {
        // Check if we have nested arrays
        if (original_array[i] instanceof Array && array[i] instanceof Array) {
            // recurse into the nested arrays
            if (!original_array[i].equals(array[i]))
                return false;
        }
        else if (original_array[i] != array[i]) {
            // Warning - two different object instances will never be equal: {x:20} != {x:20}
            return false;
        }
    }
    return true;
}


// This is to setup the metastore table in biosamples metadata
function load_bs_md_into_table(biosamples_metadata){
    headers = get_headers();

    // first have to check that the chip_ids are the same
    old_chip_ids = get_original_chip_ids();
    new_chip_ids = get_list_of_chip_ids_from_biosamples_metadata(headers,biosamples_metadata);

    old_chip_ids = old_chip_ids.sort();
    new_chip_ids = new_chip_ids.sort();


    if (test_equal(old_chip_ids,new_chip_ids)!== true){
        return false;
    }




    var bs_md_handle = $("#biosamples_metadata_grid").handsontable({
            cols: biosamples_metadata[0].length,
            rows: biosamples_metadata.length,
            colHeaders: headers
            });


    bs_md_handle.handsontable("loadData", biosamples_metadata);
    initialise_hiding_columns();
    trigger_checklist_for_headers();

    return bs_md_handle;
}

function get_headers(){
    headers = jQuery.parseJSON($("#json_headers").html());
    return headers;
}

function set_headers(json_headers){
    $('#json_headers').html(json_headers);
    return true;
}



function setup_hotkeys(){

    key('ctrl+s,alt+s', function(){ save_validate('Save',bs_md_handle,ms_handle,headers); return false });
    key('alt+v', function(){ save_validate('Validate',bs_md_handle,ms_handle,headers); return false });
    key('alt+b', function(){ window.location = '#home'; return false });
    key('alt+e', function(){ window.location = '#validate'; return false });

}

function get_original_chip_ids(){
    json_chip_ids = $('#chip_ids').html();
    chip_ids = jQuery.parseJSON(json_chip_ids);
    return chip_ids;
}

$(document).ready(function(){
        $('#controls').draggable();
        $('body').addClass('wide_for_annotations');
        var headers = get_headers();
        var biosamples_metadata = jQuery.parseJSON($("#json_biosamples_metadata").html());
        var metastore = jQuery.parseJSON($("#json_metastore").html());

        var bs_md_handle = load_bs_md_into_table(biosamples_metadata);
        var ms_handle = load_ms_into_table(metastore);


        // hide weird extra table header
        $('div [style*=absolute] tr.htColHeader').parent().hide();
        $('#metastore_div').hide();
        $('#biosamples_metadata_grid').hide();

        setup_hotkeys();

        set_clicks(bs_md_handle,ms_handle);
        update_handle();


        // check that gid is not selected and do one quick check to run this
        $('div.select_group input[type="checkbox"]:checked').each(function(){
            this_object = $(this);
            group_clicked(this_object);
        });

        // Sometimes there is a problem when the element isn’t created by the time the help runs
        // In this case, simply call helpsystem.run(); once all elements are finished.
        helpsystem.run();

        // toggle controls
        $(".toggle_controls_expand").live('click',function(){
          $(document.getElementById("steps")).addClass("hidden");
          $(document.getElementById("other")).addClass("hidden");
          $(document.getElementById("other_buttons")).addClass("hidden");
          $(this).addClass("toggle_controls_shrink").removeClass("toggle_controls_expand");
          $(document.getElementById('toogle_controls_expand_image')).attr("src",'/images/workbench/plus.png');
        })


        $(".toggle_controls_shrink").live('click',function(){
          $(document.getElementById("steps")).removeClass("hidden");
          $(document.getElementById("other")).removeClass("hidden");
          $(document.getElementById("other_buttons")).removeClass("hidden");
          $(this).addClass("toggle_controls_expand").removeClass("toggle_controls_shrink");
          $(document.getElementById('toogle_controls_expand_image')).attr("src",'/images/workbench/minus.png');
        })

});


function initialise_hiding_columns(){
    var headers = jQuery.parseJSON($("#json_headers").html());
    $('#biosamples_metadata_grid table th').show();
    $('#biosamples_metadata_grid table td').show();

    var columns = Array();
    $('div.select_column input:checked').each(function() {
        name = $(this).attr('name');
        columns.push(name);
    });

    // skip the first column as a check
    for (var i=1; i< headers.length; i++){
        count = i +1;

        header = headers[i];
        if ($.inArray(header, columns) == -1 ){
            $('#biosamples_metadata_grid table th:nth-child('+count+')').hide();
            $('#biosamples_metadata_grid table td:nth-child('+count+')').hide();
        }
    }
}

function trigger_checklist_for_headers(){

    $('#choose_columns input').click(function() {
        initialise_hiding_columns();
    });
    $('#choose_groups input').click(function() {
        this_object = $(this);
        group_clicked(this_object);
    });}


function group_clicked(this_object){
    list_of_columns = this_object.attr('data-value');
    checked = this_object.attr('checked');
    temp = list_of_columns.split(',');
    for ( temp_count in temp){
        column_name = temp[temp_count];
        if (checked != undefined){
            $('div.select_column input[name="' +column_name+'"]').attr('checked',true);
        } else {
            $('div.select_column input[name="' +column_name+'"]').attr('checked',false);
        }
    }
    initialise_hiding_columns();


}

function update_handle(){

    $('#update_handle').click(function (e) {
        var ds_id = get_ds_id();
        e.preventDefault();
        // close the dialog
        handle = $('#handle').val();
        updated_field = 'handle';
        url = BASE_PATH + 'admin/update_dataset_single_field/'+ds_id+'?new_value='+handle+'&updated_field='+updated_field;


        $.ajax({
          url: url
        }).done(function() {
          alert('Done. Refresh the page to see the updated handle.');
        });

    });


}



function hide_non_mandatory_dataset_fields(){
    $('#metastore_grid tbody tr').addClass('hidden');

    for (count in mandatory_fields) {
        field  = mandatory_fields[count];
        $("#metastore_grid tr:contains('"+field+"')").removeClass('hidden');

    }

}

function show_all_dataset_fields(){
    $('#metastore_grid tbody tr').removeClass('hidden');

}

function toggle_show_all_dataset_fields(){
    this_button = $('#show_all')
    value = this_button.val();
    if (value == 'Show All'){
        show_all_dataset_fields();
        this_button.val('Show Mandatory');
    } else {
        hide_non_mandatory_dataset_fields();
        this_button.val('Show All');
    }

}

function refresh_show_all_dataset_fields(){
    value = $('#show_all').val();
    if (value == 'Show All'){
        hide_non_mandatory_dataset_fields();
    } else {
        show_all_dataset_fields();
    }
}


function create_html_for_create_json(json_data_file){

    var html =
       '<div class="import_export_annotations">' +
           '<div class="help margin_bottom_small">' +
               'Simply copy into your clipboard. Then paste it into the Data to Import of the other dataset. Close by selecting the x at the top right of the modal window.' +
           '</div>'+
           '<textarea id="create_json_data">'+
           json_data_file +
           '</textarea>'+
        '</div>';

    return html;
}

function create_html_for_save_json(){

    var html =
       '<div class="import_export_annotations">' +
           '<div class="help margin_bottom_small">' +
               'Simply paste the previous data into your clipboard. Then paste it into the Data to Import of the other dataset. You should check that the metadata looks OK before you select Save and then Set Front End to make it available to the end users.'+
           '</div>'+
           '<textarea id="save_json_data">'+
           '</textarea>'+
           '<button id="update_annotations">'+
                'Update Annotations'+
           '</button>'+
        '</div>';

    return html;
}


function set_clicks(bs_md_handle,ms_handle){

    $("#save_json").click(function(){
        html = create_html_for_save_json();
        ds_id = get_ds_id();

        $('#wb_modal_title').html('JSON Data Import for Dataset '+ds_id);
        $('#wb_modal_content').html(html);

        $('#modal_div').modal({
            minHeight: 450,
            minWidth: 800,
            onShow:function (dialog){


                $('#update_annotations').click(function(){
                    json_data_file = $('#save_json_data').val();
                    data_file = save_json(json_data_file);
                    $.modal.close();
                });

            }
        });


    });

    $("#create_json").click(function(){

        json_data_file = create_json(bs_md_handle,ms_handle);
        html = create_html_for_create_json(json_data_file);

        ds_id = get_ds_id();

        $('#wb_modal_title').html('JSON Data Created for Dataset '+ds_id);
        $('#wb_modal_content').html(html);
        $('#modal_div').modal({
            minHeight: 400,
            minWidth: 800,
            onShow:function (dialog){

                $("#create_json_data").focus(function()
                {
                    this.select();
                });
            }
        });

    });


    $("#biosamples_metadata_grid th.htColHeader").click(function(){
            var column = $(this).parent().children().index($(this));
            biosamples_metadata = bs_md_handle.handsontable("getData");
            sortOnColumn(biosamples_metadata, column, isSorted[column]);
            isSorted[column] = !isSorted[column];
            bs_md_handle.handsontable("loadData", biosamples_metadata);
    });

    $("#show_all").click(function(){
        toggle_show_all_dataset_fields();
    });
    $('.sample_type_ui').click(function(){
        $('.toggleable').hide();
        var headers = jQuery.parseJSON($("#json_headers").html());
        sample_type_ui($(this).html(),bs_md_handle,ms_handle,headers);
    });

    $('button.send').click(function(){
        var headers = jQuery.parseJSON($("#json_headers").html());
        save_validate($(this).html(),bs_md_handle,ms_handle,headers);
    });

    $("#metastore_grid th.htColHeader").click(function(){
            var column = $(this).parent().children().index($(this));
            metastore_metadata = ms_handle.handsontable("getData");
            sortOnColumn(metastore_metadata, column, isSorted[column]);
            isSorted[column] = !isSorted[column];
            ms_handle.handsontable("loadData", metastore_metadata);
            refresh_show_all_dataset_fields();
    });

   $('#export_biosamples').on('click', function() {
       $('#biosamples_metadata_grid').table2CSV();
   });

    $('#samples_header').click(function(){

        $('.toggleable').hide();
        $('.sample_metadata').show();

    });

    $('#button_select_columns_individually').click(function(){
        $('#div_select_columns_individually').modal(
            {
                persist:true,
                minWidth: 400,
                minHeight: 600
            }
        );

    });

    $('#button_select_columns_by_group').click(function(){
        $('#div_select_columns_by_group').modal(
            {
                persist:true,
                minWidth: 400,
                minHeight: 500
            }


        );

    });


    $('#dataset_header').click(function(){
        $('.toggleable').hide();

        div_object = $('#metastore_div');
        div_object.show();

        //ms_handle.handsontable("loadData",metastore);


        object = $(this);
        var showing = div_object.css('display');
        if (showing == 'block') {
            object.find('img').attr('src',BASE_PATH+'images/workbench/minus.png');
        } else {
            object.find('img').attr('src',BASE_PATH+'images/workbench/plus.png');
        }

    });


    $('#test_header').click(function(){
        $('.toggleable').hide();

        div_object = $('#test_info');
        div_object.show();

    });


    $('#clear').click(function(){
        $('#sortable').remove();
        $('#page').html('');
    });

    $('#genes_header').click(function(){
        $('.toggleable').hide();
        div_object = $('#genes_info');
        div_object.show();
        set_top_genes(ms_handle,bs_md_handle);
    });

}


function sortOnColumn(data, column, descending) {
    descending = descending || false;
    data.sort((function(column) {
        return function(a, b) {
            var str1 = a[column];
            var str2 = b[column];
            if (typeof a[column] === "String") {
                var str1 = a[column].toLowerCase();
                var str2 = b[column].toLowerCase();
            }
            if (str1 < str2) {
                return (descending) ? 1 : -1;
            }
            if (str1 > str2) {
                return (descending) ? -1 : 1;
            }
            return 0;
        }
    })(column));
}

// Also clears now
function save_validate(button_type,bs_md_handle,ms_handle,headers){
    var ds_id = get_ds_id();
    biosamples_metadata = bs_md_handle.handsontable("getData");
    metastore = ms_handle.handsontable("getData");



    if (button_type =="Clear"){
       $('#ajax_message').hide();
    } else {
       $('#ajax_message').show();
       $('#ajax_message').html('Processing...');
        document.body.style.cursor='wait';
        $.ajax({
            url: "/admin/save_and_validate_dataset_annotations",
            type: "POST",
            timeout: SAVE_VALIDATE_TIMEOUT,
            error: function(x, t, m) {
                if(t==="timeout") {
                    alert("This request timed out.");
                } else {
                    alert(t);
                }
                document.body.style.cursor='auto';
            },
            data: { 'ds_id':ds_id,'action':button_type,'json_bs_md':JSON.stringify(biosamples_metadata), 'json_ds_md':JSON.stringify(metastore),'json_headers':JSON.stringify(headers) }
        }).done(function(msg  ) {
            document.body.style.cursor='auto';

            $('#ajax_message').html(msg);
            $('#ajax_message base').remove();
        });
    }
}

function select_for_groups(list_of_sample_types,set_group) {

    return_text = "<select>";
    i = 0;
    for (var sample_type in list_of_sample_types){
        if (set_group == i){ is_selected = "selected" ; } else { is_selected = ""; }
        return_text += "  <option "+is_selected+" value=\""+i+"\">Group "+i+"</option>"
        i++;
    }
    return_text += "</select>"
    return return_text;
}

function sample_type_ui (button_type,bs_md_handle,ms_handle,headers){
    var ds_id = get_ds_id();

    biosamples_metadata = bs_md_handle.handsontable("getData");
    var pos = headers.indexOf("Sample Type");
    list_of_current_sample_types = [];

    for (var sample in biosamples_metadata) {
        sample_type = biosamples_metadata[sample][pos];
        if (list_of_current_sample_types.indexOf(sample_type) == -1){
            list_of_current_sample_types.push(sample_type);
        }
    }

    html_for_sorting = load_sample_types(ms_handle,list_of_current_sample_types);
    $('body').append(html_for_sorting);
    $('#sortable ul').sortable();
    sampleTypeDisplayOrder = '';
    sampleTypeDisplayGroups = '{';
    $('#sortable').draggable();
    $('#save_sample_type_ordering').click(function () {
        $('#sortable ul li ').each(function() {
            var this_object = $(this);
            this_group = this_object.find('div.select_group').find('option:selected').html();
            this_sample_type = this_object.find('div.sample_type').html();
            sampleTypeDisplayOrder += this_sample_type + ',';
            sampleTypeDisplayGroups += '"'+this_sample_type + '":'+this_group.replace('Group ','')+',';
        });
        sampleTypeDisplayOrder = sampleTypeDisplayOrder.slice(0,-1);
        sampleTypeDisplayGroups = sampleTypeDisplayGroups.slice(0,-1)+ '}';
        save_sample_types(ms_handle,sampleTypeDisplayOrder,sampleTypeDisplayGroups);
        $('#sortable').remove();
    });
}

function load_sample_types (ms_handle,list_of_current_sample_types){
    metastore = ms_handle.handsontable("getData");
    for (var row in metastore){
        type = metastore[row][0];
        if (type == "sampleTypeDisplayOrder"){
            sampleTypeDisplayOrderArray = metastore[row][1].split(',');
        }
        if (type == "sampleTypeDisplayGroups"){
            sampleTypeDisplayGroupsArray = jQuery.parseJSON(metastore[row][1]);
        }
    }

    var help='    <div class="content"> <table id="ordering_help" ><tr><td></td></tr><tr><td><ol>    <li>This allows you to "group" sample types together to have similar colours and also change the order of the graphs by dragging and moving the sample types (in their white rows).</li><li>The sample types with the same group will have similar colours. The top sample type will be the first sample type seen on the left of the graph and the bottom sample type will be the sample type shown on the far right of the graph in boxplot, bar graph and scatterplot graphs.</li> <li>This grey bar is moveable, you can click and drag this anywhere on the page</li> <li>Click Save Sample Type Ordering at the bottom of this grey bar. Then you can click on Validate, then Save on the Control Bar. To check that it has worked click Set Front End on the Control Bar then select Test Dataset link and then click on the Gapdh Graph link.</li><li>If you want to remove the changes, simply click on Clear in the Control Bar. </ol></td></tr></table> </div>';



    html_for_sorting = "<div id='sortable'><h1>Sample Type Ordering</h1>"+help+"<ul id='sortableul'>";

    used_sample_types = [];

    for (var order in sampleTypeDisplayOrderArray){
        old_ordered_sample_type = sampleTypeDisplayOrderArray[order];
        value = list_of_current_sample_types.indexOf(old_ordered_sample_type) != -1
        if (value) { is_current = true; } else { is_current = false; }

        if (is_current){
            set_group = sampleTypeDisplayGroupsArray[old_ordered_sample_type];
            select_html = select_for_groups(list_of_current_sample_types,set_group);
            html_for_sorting += "<li class='ui-state-default'><span class='ui-icon ui-icon-arrowthick-2-n-s'></span><div class='select_group'>"+select_html+"</div><div class='sample_type'>"+old_ordered_sample_type+"</div></li>";
            used_sample_types.push(old_ordered_sample_type);
        }

    }

    for (var count in list_of_current_sample_types){
        sample_type = list_of_current_sample_types[count];
        if (used_sample_types.indexOf(sample_type) == -1){
            set_group = 0;
            select_html = select_for_groups(list_of_current_sample_types,set_group);
            html_for_sorting += "<li class='ui-state-default'><span class='ui-icon ui-icon-arrowthick-2-n-s'></span><div class='select_group'>"+select_html+"</div><div class='sample_type'>"+sample_type+"</div></li>";
            used_sample_types.push(sample_type);

        }
    }

    html_for_sorting +="</ul><button id='save_sample_type_ordering' class='sample_type_ui'>Save Sample Type Ordering</button></div>";

    return html_for_sorting;
}


function save_sample_types (ms_handle,sampleTypeDisplayOrder,sampleTypeDisplayGroups){
    metastore = ms_handle.handsontable("getData");
    for (var row in metastore){
        type = metastore[row][0];
        if (type == "sampleTypeDisplayOrder"){
            metastore[row][1] = sampleTypeDisplayOrder;
        }
        if (type == "sampleTypeDisplayGroups"){
            metastore[row][1] = sampleTypeDisplayGroups;
        }
    }
    ms_handle.handsontable("loadData",metastore);

}


function HTMLDecode(s){
    return jQuery('<div></div>').html(s).text();
}

function set_top_genes(ms_handle,bs_md_handle){

    actual_row = 0;
    // get values from topDifferentiallyExpressedGenes
    metastore = ms_handle.handsontable("getData");
    for (row in metastore){
        name = metastore[row][0];

        if (name == 'topDifferentiallyExpressedGenes'){
            actual_row = row;
            value = metastore[row][1];
            // add these values into textarea
            $('#genes_info textarea').val(value);
            break;
        }
    }


    $('#genes_info input').click(function(){
        // when submit is clicked, use genes/get_autocomplete with the textarea val and the db_id(?)
        var value = $('#genes_info textarea').val();
        var db_id = $('#db_id').html();

        value = value.replace(/ +/g,',');
        value = value.trim();
        url = BASE_PATH + 'genes/get_autocomplete?db_id='+db_id+'&term='+value;

        $.ajax({
          url: url
        }).done(function(return_data) {

            var data = jQuery.parseJSON(return_data);
            html = setup_genes_of_interest_table(data);
            $('#view_genes_found').html(html);

            $('#view_genes_found input[type=submit]').click(function(){
                var genes = Array();
                $('#view_genes_found input[type="checkbox"]:checked').each(function(){
                    var ensembl_id = $(this).attr('name');
                    genes.push(ensembl_id);
                });


                var genes_string = genes.join(",");
                var headers = jQuery.parseJSON($("#json_headers").html());
                metastore = ms_handle.handsontable("getData");
                metastore[actual_row][1] = genes_string;
                ms_handle.handsontable("loadData", metastore);
                save_validate('Save',bs_md_handle,ms_handle,headers);
                set_top_genes(ms_handle,bs_md_handle);
            });
        });
    });


    // when returned, setup a table with selections and then save those selections into the database proper

}

function setup_genes_of_interest_table(data){
    var html =  "<table>"+
                "<thead>"+
                "<tr>"+
                    "<th>Select</th>"+
                    "<th>EnsemblID</th>"+
                    "<th>Symbol</th>"+
                    "<th>Aliases</th>"+
                    "<th>Description</th>"+
                "</tr>"+
                "</thead>"+
                "<tbody>";

    for (row in data){
        ensembl_id = data[row]['ensembl_id'];
        aliases = data[row]['aliases'];
        description = data[row]['description'];
        symbol = data[row]['symbol'];

        new_html_row = "<tr>"+
            "<td><input type='checkbox' name='"+ensembl_id+"'></input></td>" +
            "<td>"+ensembl_id+"</td>" +
            "<td>"+symbol+"</td>" +
            "<td>"+aliases+"</td>" +
            "<td>"+description+"</td>" +
            "</tr>";
        html = html + new_html_row;
    }
    html = html + "</tbody></table><input type='submit'></submit>";
    return html;
}
