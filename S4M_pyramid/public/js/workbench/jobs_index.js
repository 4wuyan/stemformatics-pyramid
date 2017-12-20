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
    $('a.delete').click(function(e){
        // stop things from happening first
        e.preventDefault();

        var this_link = $(this);

        var this_delete_url = this_link.attr('href');

        var job_id = this_link.attr('id').replace('del_','');

        $('#wb_modal_title').html('Confirm Job Deletion');
        $('#wb_modal_content').html('Are you sure you want to delete job #' + job_id + '? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
        $('#modal_div').modal({
            onShow: function (dialog) {
                var modal = this;

                // if the user clicks "yes"
                $('button').click(function () {
                    var answer = $(this).html();
                    // close the dialog
                    modal.close(); // or $.modal.close();

                    if (answer == 'Yes'){
                        window.location = this_delete_url;
                    }

                });

            }

        });



    });

    $('a.remove').click(function(e){
        e.preventDefault();

        var remove_url = $(this).attr('href');

        var job_id = $(this).attr('id').replace('rem_','');

        $('#wb_modal_title').html('Confirm Shared Job Removal');
        $('#wb_modal_content').html('Are you sure you want to remove shared job #'+job_id+'? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button>');

        $('#modal_div').modal({
            onShow: function (dialog) {
                $('button.submit').click(function () {
                    $.modal.close();
                    if ($(this).html() == 'Yes'){
                        window.location = remove_url;
                    }
                });
            }
        });
    });


});
