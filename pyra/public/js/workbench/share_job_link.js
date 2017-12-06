$(document).ready(function(){

    
        
        
    $('#share_link').unbind().click(function(e){
        e.preventDefault();
        value = check_user_logged_in_for_sharing(); // this is in main.js
        if (value == false){ return false; }
        
        $('#wb_modal_title').html('Share this Job');
        
        var this_object = $(this);
        
        
        var count = 0;
        var text = '';
        var job_id = '';
        $('#job_titles td').each(function () { 
            
            // if odd, then add a : instead of a ' '
            if (count%2 == 0) {
                html = $(this).html(); 
                var new_text = $("<div/>").html(html).text();
                text = text + "\r\n" + new_text;
            } else {
                html = $(this).html(); 
                var new_text = $("<div/>").html(html).text();
                text = text + ' : ' + new_text;
            }
            
            if (count == 1){
                job_id = $(this).html();
            }
            
            count++;
        });
        
        // var job_name = job_id + ' with dataset ' + $('#job_handle_'+job_id).html() + ' with parameters ' + $('#job_parameters_'+job_id).html();
        var job_name = text;
        
        var form_html  = "<form id='share_link_form'>" +
                "<div id=help_share_link_form>Please note that you can add more than one email address separating each with commas and no spaces. This gene set will be copied over to the gene set list of the users whose email addresses you specify.</div>" +
                "<dl>" + 
                    "<dt id='to_email_label'>To Email:</dt><dd><input id='to_email_input' class='share_input' type='text' name='to_email' value=''/></dd>" +
                    "<dt>Subject:</dt><dd><input class='share_input' type='text' name='subject' value='"+SITE_NAME+" - Sharing Job: " + job_id +"'/></dd>" +
                    "<dt>Body:</dt><dd><textarea class='share_input' name='body' >I have shared a job that I thought you might want to view - \"" + job_name +"\" \r\n\r\nClick here to access this shared job:\r\n"+window.location.protocol + "//" + window.location.host +BASE_PATH +"workbench/job_view_result/"+job_id+"\r\n\r\nYou can also login (or register if you don't have a free "+SITE_NAME+" account) and go to Manage My Analysis Jobs > Current and pending analysis jobs to see this gene set I just shared with you. \r\n \r\nFrom \""+$('#full_name').html()+"\" " + $('#user').html() +" via "+SITE_NAME+"</textarea></dd>" +
                    "<dt><button id='share_link_form_submit' type='button'>Submit</button></dt><dd></dd>" +
                "</dl>" +
                "<div class='clear'/>"+
            "</form>" +
            
            "<div class='clear'/>";
        
        
        
        $('#wb_modal_content').html(form_html);
        
        $('#modal_div').modal({
            minHeight: 475,  
            /* minWidth: 400, */
            onShow: function (dialog) {
                var modal = this;
                
                
                $('#share_link_form_submit').click(function(e){
                    // stop things from happening first
                    e.preventDefault();
                    $(this).html('Sharing...').addClass('wait');
                    $('#simplemodal-container').addClass('wait');
                    // var gene_set_id = $('#gene_set_id').html();
                    
                    var post_url = BASE_PATH + 'auth/share_job/'+job_id;
                    
                    $.post(post_url, $("#share_link_form").serialize(), 
                        function(data) {
                            $('#wb_modal_title').html('Share this Job');
                            $('#wb_modal_content').html(data);
                            $('#simplemodal-container').height('auto').removeClass('wait');
                        }
                    
                    ); 
                    
                    
                    
                
                });
                
                
            }
        
        });
            
        
    });
    
            

});
