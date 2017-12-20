

$(document).ready(function() {

    $('#select').unbind( 'click'); 
    
    $('#select').click(function(){
        
        // toggle clicks all or none
        
        var total = $('#gene_set_items input[type="checkbox"]');
        
        var checked = $('#gene_set_items input[type="checkbox"]:checked');
        
        // if all checked then toggle to all unchecked
        
        if (total.length == checked.length) {
            $('#gene_set_items input[type="checkbox"]').each(function(){ $(this).attr('checked', false)});
        } else {
            // toggle all to checked
            $('#gene_set_items input[type="checkbox"]').each(function(){ $(this).attr('checked', true)});
        }
    });
    
    
    $('a.popup').click(function(){
            
            window.open($(this).attr('href'), "SelectUniqueGene", "status = 1, height = 860, width = 1024, resizable = 0, scrollbars=1" );
            return false;
    });
    
    $('#saveGeneSet').unbind().click(function(){
        if ($('input[type=checkbox]').length == 0) { // no valid genes
            $('#wb_modal_title').html('Save Gene List Error');
            $('#wb_modal_content').html('This gene list must have at least one valid gene.');
            return false;
        } else if ($('#gene_set_name').val().length == 0) { // no name set yet
            $('#details_modal').modal();
            return false;
        }
    });
    
    $('#finalGeneSetSave').click(function() {
        if ($('#modal_gene_set_name').val().length == 0) {
            $('#details_modal .save-error').html("Gene list must have a name!");
        } else {
            $('#gene_set_name').val($('#modal_gene_set_name').val());
            $('#description').val($('#modal_description').val());
            $.modal.close();
            $('#saveGeneSet').click();
        }
    });
    
    
    $('#summary').show();
    
    $('h2').click(function(){
        
        // want to show the table underneath and also change the + to a -
        
        var object = $(this);
        
        var header_id = object.attr('id');
        
        var table_id = header_id.replace('header','table');
                
        var table_object = $('#'+table_id);
        
        var showing = table_object.css('display');
        
        if (showing == 'none') {
            table_object.show();
            object.find('img').attr('src',BASE_PATH+'images/workbench/minus.png');
        } else {
            table_object.hide();
            object.find('img').attr('src',BASE_PATH+'images/workbench/plus.png');
        }
        
        
    });
    
    $('#select_all_ambiguous_checkbox').click(function(){
    
        var this_object = $(this);
        
        
        if (this_object.attr('checked') == 'checked') {
            $('#select_all_ambiguous').val('1');
        } else {
            $('#select_all_ambiguous').val('0');
        }
        
        
    });
    
    $('#export_ambiguous').click(function(){
        $('#ambiguous_table').table2CSV();	
    });
    
    $('#export_not_found').click(function(){
        $('#not_found_table').table2CSV();	
    });
    
    $('#export_ok').click(function(){
        $('#ok_table').table2CSV();	
    });
    
});

/* this is to ensure it calls revalidate when dealing with ambigous genes */
function CallAlert()
{
   $('#revalidate').click();
}


