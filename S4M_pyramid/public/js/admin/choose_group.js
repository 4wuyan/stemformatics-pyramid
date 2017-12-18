// setup url
$(document).ready(function() {
    $('input.submit').click(function(){
        var groups = '';
        $('tr input:checked').each(function(){
            var object = $(this);
            group_id = object.attr('id');
            groups = groups+','+group_id;
        });
        groups = groups.substring(1);
        base_url = $('#base_url').html();
        window.location = base_url + 'group_ids='+groups;
    });
    
    $('#choose_group_table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 0, "desc" ]],
        "bAutoWidth": false } );
 

});
