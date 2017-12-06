$(document).ready(function(){

    $('table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 0, "desc" ]],
        "bAutoWidth": false } );
        
           
    $('#open_all_links').click(function(){
        
        $('tr a').each(function(){
            window.open($(this).attr('href'));
        });
    });
});
