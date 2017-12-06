
$(document).ready(function() {


    $('#chooseDatasetTable').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 1, "asc" ]],
        "oLanguage": {
          "sSearch": "Filter: "
        },
        "bAutoWidth": false } );


});
