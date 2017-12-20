// setup url
$(document).ready(function() {
    $('input.submit').click(function(){
        var users = '';
        $('tr input:checked').each(function(){
            var object = $(this);
            user_id = object.attr('id');
            users = users+','+user_id;
        });
        user_ids = users.substring(1);
        group_ids = $('#group_ids').html();
        if (group_ids == null){
            group_ids = '';
        }
        user_emails = $('#user_emails').val();
        base_url = $('#base_url').html();
        url = base_url +'&user_ids='+user_ids+'&user_emails='+user_emails;
        window.location = url;
    });

    $('table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 0, "desc" ]],
        "bAutoWidth": false } );
 
});
