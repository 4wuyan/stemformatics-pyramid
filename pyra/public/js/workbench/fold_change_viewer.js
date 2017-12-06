
function reset_table() {
    
    var sample_type_1 = $('#sample_type_1').val();
    var sample_type_2 = $('#sample_type_2').val();
    
    var json_view_data = $('#json_view_data').html();
    
    var view_data = jQuery.parseJSON(json_view_data);
    
    var probe_list = view_data.raw_probe_list;
    var is_log_2 = view_data.log_2;    

    for ( var i = 0; i < probe_list.length; i++){
        var probe = probe_list[i];
        
        value1 = view_data.plot_data[sample_type_1]['values'][i]['average'];
        value2 = view_data.plot_data[sample_type_2]['values'][i]['average'];
        
        if (is_log_2){
            fold_change = Math.pow(2,value2 - value1);
        } else {
            fold_change = value2 / value1;
        }
        row_count = i + 2;
        
        $('#fold_change_output_table tr:eq('+row_count+') td:eq(1)').html(value1);
        $('#fold_change_output_table tr:eq('+row_count+') td:eq(2)').html(fold_change);
        $('#fold_change_output_table tr:eq('+row_count+') td:eq(3)').html(value2);
        
        
    } 

    
}


$(document).ready(function() {


    
    $('select').change(function(){
        
        
        reset_table();
        
        
        
    });

    $('#exportTableCSVButton').click(function(){
		$('#fold_change_output_table').table2CSV();	
	});
    
    
    reset_table();
    
});
