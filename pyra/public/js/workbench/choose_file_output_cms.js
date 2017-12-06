
$(document).ready(function() {

    /* aoColumns with bSortable False stops the column from being sortable */
    $('#chooseDatasetTable').dataTable( {
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,

		"aaSorting": [[ 0, "asc" ]],
        "bAutoWidth": false } ); 

});

    
