

/*  This is for the alternate index mako */
$(document).ready(function() {

    $('#exportTableCSVButton').click(function(){
                $('#downloadPageHistoryTable').table2CSV();	
            });          
            
    /* nicer confirm dialog for clearing history */
    $('a.clear_history').click(function(e){
        // stop things from happening first
        e.preventDefault();
        
        var this_link = $(this);
        
        var this_delete_url = this_link.attr('href');
        
        $('#wb_modal_title').html('Confirm Clear History');
        $('#wb_modal_content').html('Are you sure you want to clear your history? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
        $('#modal_div').modal({
            onShow: function (dialog) {
                var modal = this;
                
                // if the user clicks "yes"
                $('button').click(function () {
                    var answer = $(this).html();
                    // close the dialog
                    modal.close(); // or $.modal.close();
                    
                    if (answer == 'Yes'){
                        window.location = this_delete_url;
                    } 
                    
                });
                
            }
        
        });
            
        
    
    });
            


});

    
