
function chosenDatasetTableClick() {
    $('#chosenDatasetTable input[type=checkbox]').click(function(){

            var this_object = $(this);

            var ds_id = this_object.attr('id').split('delete')[1];

            $('#'+ds_id).attr('checked',false);

            this_object.parents('tr').remove();
        });

}

function setup_chosenDatasetTable(ds_id){
    var table_row = $('#'+ds_id).parents('tr').html();
    if (table_row != undefined){
        table_row = "<tr>" + table_row.replace(ds_id,"delete"+ds_id) + "</tr>";
    }
    $("#table_chosen_none_row").hide();
    $('#chosenDatasetTable tr:last').after(table_row);
    $('#'+ds_id).attr('checked',true);

}

$(document).ready(function() {

    var temp = $('#loaded_datasets').html();
    var loaded_datasets = jQuery.parseJSON(temp);

    for (var count in loaded_datasets){
        var ds_id = loaded_datasets[count];


        setup_chosenDatasetTable(ds_id);
    }

    chosenDatasetTableClick();

    $('#chooseDatasetTable').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 1, "asc" ]],

        "bAutoWidth": false } );


   $('#chooseDatasetTable input[type=checkbox]').click(function(){

        var this_object = $(this);

        var ds_id = this_object.attr('id');

        var checked = this_object.is(':checked');

        if (checked) {

            setup_chosenDatasetTable(ds_id);
            chosenDatasetTableClick();

        } else {
            $('#delete'+ds_id).parents('tr').remove();
        }

    });


   $('input.save').click(function(){

        base_url = $("#base_url").attr('href');

        datasets = '';
        count = 0;
        $('#chosenDatasetTable input').each(function(index,value){
          if(!!document.documentMode) {//checks if IE
            ds_id = $(this).attr('id').split('delete')[0]; // attr('id') = '6394' on IE
          }
          else {
            ds_id = $(this).attr('id').split('delete')[1]; // attr('id') = 'delete6394' in rest of browsers
          }
            datasets = datasets + ',' + ds_id;
            count ++;
        });

       if (count >= 2 && count <= 9) {
           datasets = datasets.slice(1);

           var newURL = base_url + '&datasets='+datasets;

           window.location = newURL;
        } else {
            error_title = 'Error when choosing multiple datasets';
            $('#wb_modal_title').html(error_title);
            error_html = 'Must choose between 2 and 9 datasets';
            $('#wb_modal_content').html(error_html);
            $('#modal_div').modal();
        }

    });


});
