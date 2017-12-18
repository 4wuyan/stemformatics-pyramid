$(document).ready(function() {
    $('tr.sample').removeClass('hidden').hide();
    $('a.toggle_samples').click(function(){
        ds_id = $(this).attr('data-id');
        $('tr.samples_of_'+ds_id).toggle();  
    });

    $('th.toggle_select_all').unbind('click');
    $('th.toggle_select_all').click(function(){
        number_selected = $('div.dataset_results input:checked').length;

        if (number_selected == 0){
            // if none selected, then select all
            $('div.dataset_results input').prop('checked',true);


        } else {
            // if one or more selected, then select none
            $('div.dataset_results input').prop('checked',false);

        }

        
    });
    $('a.searchButton').click(function(){
        $('#searchForm').submit();
    });
    $('a.export').click(function(){
        var ds_ids = Array();
        $('div.dataset_results input:checked').each(function(){
            ds_id = $(this).attr('name');
            ds_ids.push(ds_id); 
        });
        url = $(this).attr('href');
        url_ds_ids_text = ds_ids.join(',');
        window.location = url + '&ds_ids=' + url_ds_ids_text;
        return false;
    });

});

