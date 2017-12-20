$(document).ready(function() {
    $('tr.sample').removeClass('hidden').hide();
    $('a.toggle_samples').click(function(){
        ds_id = $(this).attr('data-id');
        $('tr.samples_of_'+ds_id).toggle();
    });

});
