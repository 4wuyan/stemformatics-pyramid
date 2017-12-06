function share_gene_list_link() {
    $('a.share_gene_list_link').click(function(e){
        var this_object = $(this);
        click_on_share_gene_list_link(this_object); 
    });
}

function edit_gene_list_link(){
    $('a.edit_gene_list_link').click(function(){
        var this_object = $(this); 
        click_on_edit_gene_list_link(this_object); 
    });
}

function publish_gene_list_link(){
    $('a.publish_gene_list_link').click(function(){
        var this_object = $(this); 
        click_on_publish_gene_list_link(this_object);   
        
    });
} 

function delete_gene_list_link(){
    $('a.delete_gene_list_link').click(function(e){
        e.preventDefault();
        var this_object = $(this); 
        click_on_delete_gene_list_link(this_object);   
        
    });
} 

function click_on_delete_gene_list_link(this_object){
    /* nicer confirm dialog for deleting a gene list */
    // stop things from happening first
    var gene_set_id = this_object.data('id');
    var gene_set_name = this_object.data('name') ;
    var delete_url = this_object.attr('href');
         
    $('#wb_modal_title').html('Confirm Gene List Deletion');
    $('#wb_modal_content').html('<div class="confirm">Are you sure you want to delete the gene list "'+gene_set_name+'"? </div><div class="answer"><button class="button" id="yes">Yes</button> <button class="button" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div><div class="clear"></div></div>');
    $('#modal_div').modal({
        minHeight: 180,  
        onShow: function (dialog) {
            var modal = this;
            
            // if the user clicks "yes"
            $('button').click(function () {
                var answer = $(this).html();
                // close the dialog
                modal.close(); // or $.modal.close();
                
                if (answer == 'Yes'){
                    window.location = delete_url;
                } 
                
            });
            
        }
    
    });
        
        
    
 
}


function click_on_publish_gene_list_link(this_object){
    $('#wb_modal_title').html('Publish as a Public Gene List');
    var gene_set_id = this_object.data('id');
    var gene_set_name = this_object.data('name') ;
    var gene_set_description = this_object.data('description') ;
    var publish_gene_set_email_address = this_object.data('email');
    var username = $('#user').html();
    var full_name = $('#full_name').html();
    
    
    var form_html  = "<form id='modal_form'>" +
            "<div id=help_modal_form>Please enter in any extra information about your gene list and why you would like it published.</div>" +
            "<dl>" + 
                "<dd><input id='to_email_input' class='share_input' type='hidden' name='to_email' value='"+publish_gene_set_email_address+"'/></dd>" +
                "<input type='hidden' name='publish' value='true'/>"+
                "<dd><input class='share_input' type='hidden' name='subject' value='"+SITE_NAME+" - Publishing Gene List " + gene_set_name +" " + gene_set_id + "'/></dd>" +
                "<dt>Gene List Description:</dt><dd><textarea class='share_input' name='gene_set_description' >"+gene_set_description+"</textarea></dd>" +
                "<dt>Message:</dt><dd><textarea class='share_input' name='body' >I would like to submit this gene list as a public gene list for the "+SITE_NAME+" community. \r\n \r\nFrom \""+full_name+"\"" + username +" via "+SITE_NAME+"</textarea></dd>" +
                "<dt class='no_margin_bottom'><button type='button'>Submit</button></dt><dd class='no_margin_bottom'></dd>" +
            "</dl>" +
            "<div class='clear'/>"+
        "</form>" +
        
        "<div class='clear'/>";
    
    
    
    $('#wb_modal_content').html(form_html);
    $('#modal_div').modal({
        minHeight: 570,  
        /* minWidth: 400, */
        onShow: function (dialog) {
            var modal = this;
            
            
            $('dt button').click(function(e){
                // stop things from happening first
                e.preventDefault();
                $(this).html('Submitting...').addClass('wait');
                $('#simplemodal-container').addClass('wait');
                
                var post_url = BASE_PATH + 'auth/share_gene_set/'+gene_set_id;
                $.post(post_url, $("#modal_form").serialize(), 
                    function(data) {
                        $('#wb_modal_title').html('Publish this Gene List');
                        $('#wb_modal_content').html(data.replace('sharing','publishing'));
                        $('#simplemodal-container').height('auto').removeClass('wait');
                    }
                
                );
                
                
            
            });
            
            
        }
    
    });
}
 
function click_on_share_gene_list_link(this_object){
        
        $('#wb_modal_title').html('Share Gene List');
        
        var gene_set_id = this_object.data('id');
        var gene_set_name = this_object.data('name') 
        var gene_set_description = this_object.data('description') 
        var username = $('#user').html();
        var full_name = $('#full_name').html();
        var form_html  = "<form id='modal_form'>" +
                "<div id=help_modal_form>Please note that you can add more than one email address separating each with commas and no spaces. This gene list will be copied over to the gene list list of the users whose email addresses you specify.</div>" +
                "<dl>" + 
                    "<dt id='to_email_label'>To Email:</dt><dd><input id='to_email_input' class='share_input' type='text' name='to_email' value=''/></dd>" +
                    "<dt>Subject:</dt><dd><input class='share_input' type='text' name='subject' value='"+SITE_NAME+" - Sharing Gene List " + gene_set_name +"'/></dd>" +
                    "<dt>Body:</dt><dd><textarea class='share_input' name='body' >I have shared a gene list that I thought you might want to view - \"" + gene_set_name +"\" \r\n" + gene_set_description +"\r\nClick here to access this shared gene list:\r\n"+window.location.protocol + "//" + window.location.host +BASE_PATH +"workbench/gene_set_index\r\n\r\nYou can also login (or register if you don't have a free "+SITE_NAME+" account) and go to Manage My Gene Lists > Manage current gene lists to see this gene list I just shared with you. \r\n \r\nFrom \""+full_name+"\"" + username +" via "+SITE_NAME+"</textarea></dd>" +
                    "<dt class='no_margin_bottom'><button  type='button'>Submit</button></dt><dd class='no_margin_bottom'></dd>" +
                    "<div class='clear'></div>"+
                "</dl>" +
                "<div class='clear'></div>"+
            "</form>" +
            
            "<div class='clear'></div>";
        
        
        
        $('#wb_modal_content').html(form_html);
        
        $('#modal_div').modal({
            minHeight: 465,  
            /* minWidth: 400, */
            onShow: function (dialog) {
                var modal = this;
                
                $('dt button').click(function(e){
                    // stop things from happening first
                    e.preventDefault();
                    $(this).html('Sharing...').addClass('wait');
                    $('#simplemodal-container').addClass('wait');
                    
                    // var gene_set_id = $('#gene_set_id').html();
                    
                    var post_url = BASE_PATH + 'auth/share_gene_set/'+gene_set_id;
                    
                    $.post(post_url, $("#modal_form").serialize(), 
                        function(data) {
                            $('#wb_modal_title').html('Share Gene List');
                            $('#wb_modal_content').html(data);
                            $('#simplemodal-container').height('auto').removeClass('wait');
                        }
                    
                    ); 
                    
                
                });
                
                
            }
        
        });
            
} 

function click_on_edit_gene_list_link(this_object){
        $('#wb_modal_title').html('Update Gene List');
        var gene_set_id = this_object.data('id');
        var gene_set_name = this_object.data('name') ;
        var gene_set_description = this_object.data('description') ;
        var publish_gene_set_email_address = this_object.data('email');
        var username = $('#user').html();
        var full_name = $('#full_name').html();
        var raw_href = this_object.attr('href');
        
        var oldName = gene_set_name;

        var form_html  = "<form id='modal_form' action='"+BASE_PATH + 'workbench/update_gene_set_name?gene_set_id='+gene_set_id+"'>" +
                "<input class='share_input' type='hidden' name='gene_set_id' value='" + gene_set_id +"'/>" +
                "<dl>" + 
                    "<dt>Gene List Name:</dt><dd><input class='share_input' type='text' id='gene_set_name' name='gene_set_name' value='" + gene_set_name +"'/></dd>" +
                    "<dt>Gene List Description:</dt><dd><textarea class='share_input' name='gene_set_description' >"+gene_set_description+"</textarea></dd>" +
                    "<dt class='no_margin_bottom'><button type='button'>Submit</button></dt><dd class='no_margin_bottom'></dd>" +
                "</dl>" +
                "<div class='clear'/>"+
            "</form>" +
            
            "<div class='clear'/>";
         
        $('#wb_modal_content').html(form_html);
        $('#modal_div').modal({
            onShow: function (dialog) {
                var modal = this;
                $('dt button').click(function(e){
                    // stop things from happening first
                    e.preventDefault();
                    $('#modal_form').submit(); 
                });
            }
        });  
}
