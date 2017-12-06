var autocompleteTimeout = 5000;

/*  This is for the alternate index mako */
$(document).ready(function() {

    // this is in main.js
    innate_db_link_clicks();

    share_gene_list_link(); 
    publish_gene_list_link(); 
    edit_gene_list_link();
    delete_gene_list_link();
   
    $('#exportTableCSVButton').click(function(){
                $('#gene_set_items_download').table2CSV();	
            });          
            
            
    $('#updateDescriptionButton').click(function(){
        $('#update_gene_set_description').modal();
    }); 

    $('#updateNameButton').click(function(){
        $('#update_gene_set_name').modal();
    }); 
    
    // can't use proper submit for modal forms so have to do it this way!
    $('button.submit').click(function(){
        
        var id = $(this).attr('id');
        
        var form_id = id.replace('submit','form');
        $('#'+form_id).submit();
        
    });
    
    $('textarea').focus();
        
    
    if ($('#gene_set_items a.delete').length > 50) {
        
        $('#histogram').unbind().click(function(){
            
            $('#wb_modal_title').html('Histogram Error');
            $('#wb_modal_content').html('This gene set is too large for showing in a histogram. The maximum number of genes allowed is 50.');
            $('#modal_div').modal();
            return false;
        });
        
    }
    
    
    if ($('#gene_set_items a.delete').length == 1) {
        
        $('#gene_set_items a.delete').unbind().click(function(){
            
            $('#wb_modal_title').html('Delete Gene Error');
            $('#wb_modal_content').html('This gene set must have at least one gene. Delete failed.');
            $('#modal_div').modal();

            return false;
        });
        
    }
    
    /* nicer confirm dialog for deleting a gene set */
    $('#deleteGeneSet').click(function(e){
        // stop things from happening first
        e.preventDefault();
        
        $('#wb_modal_title').html('Confirm Gene List Deletion');
        $('#wb_modal_content').html('Are you sure you want to delete this gene set? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
        $('#modal_div').modal({
            onShow: function (dialog) {
                var modal = this;
                
                // if the user clicks "yes"
                $('button').click(function () {
                    var answer = $(this).html();
                    // close the dialog
                    modal.close(); // or $.modal.close();
                    
                    if (answer == 'Yes'){
                        window.location = $('#deleteURL').html();
                    } 
                    
                });
                
            }
        
        });
            
        
    
    });
    
       
 
});

    
