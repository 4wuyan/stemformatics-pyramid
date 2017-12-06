$(document).ready(function() {

   $('input[type=checkbox]').click(function() {
        var chip_id = $(this).val() ;
        var checkbox = $('#remove_chip_ids_'+chip_id);

        checkbox.attr("checked", !checkbox.attr("checked"));
   });    
   $('form').submit(function(){
        if ($('input.choose_samples:checked').length == 0){
            $('#wb_modal_title').html('Issue with number of Samples Selected');
            var content_html = '<p>Please select at least one sample.</p>';
            $('#wb_modal_content').html(content_html);
            $('#modal_div').modal( { minHeight: 35, minWidth: 400 });
            return false;
        }
   });
});
