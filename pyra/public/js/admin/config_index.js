edit_config_url=BASE_PATH+'admin/edit_config';



function setup_edit_html(ref_type,ref_id){

    html =
        '<div class="div_edit_config">'+
            '<form id="form_edit_config" >'+
                '<input name="ref_type" type="hidden" value="'+ref_type+'">'+
                '<input id="edit_ref_id" name="ref_id" type="text" value="'+ref_id+'">'+
                '<br/>'+
                '<input id="form_edit_config_submit" class="margin_top_small" type="submit">'+
            '</form>'+
        '</div>';

    return html;

}



$(document).ready(function(){

    $('#chooseDatasetTable').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 0, "desc" ]],
        "oLanguage": {
          "sSearch": "Filter: "
        },
        "bAutoWidth": false } );


    /* nicer confirm dialog for deleting a job */
    $('a.edit_config').click(function(e){
        // stop things from happening first
        e.preventDefault();

        var this_link = $(this);

        var this_url = this_link.attr('href');

        var ref_type= this_link.attr('data-ref-type');
        var ref_id = $('#'+ref_type+'_value').html();

        $('#wb_modal_title').html('Edit ref_type "'+ref_type+'"');
        edit_html = setup_edit_html(ref_type,ref_id);
        $('#wb_modal_content').html(edit_html);
        $('#modal_div').modal({
            persist: true,
            onShow: function (dialog) {
                var modal = this;

                // if the user clicks "yes"
                $('#form_edit_config_submit').click(function (e) {
                    e.preventDefault();
                    var answer = $(this).html();
                    // close the dialog
                    modal.close(); // or $.modal.close();

                    url = edit_config_url;
                    data = $('#form_edit_config').serialize(); // serialize form via jquery
                    edit_ref_id = $('#edit_ref_id').val();
                    var request = $.ajax({
                        type: "POST",
                        data: data,
                        url: url
                    });


                    request.done(function(data) {
                        alert( "Request OK." );
                        $('#'+ref_type+'_value').html(edit_ref_id);

                    });

                    request.fail(function( jqXHR, textStatus ) {
                      alert( "Request failed: " + textStatus );
                    });





                });

            }

        });



    });



});
