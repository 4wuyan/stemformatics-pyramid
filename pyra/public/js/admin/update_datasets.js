$(document).ready(function() {

    $('#updateMenu ul.submenu a').click(function(e){
        // stop things from happening first
        e.preventDefault();
        this_object = $(this);
        
        ds_id = this_object.attr('ds_id')
        handle = $('#'+ds_id+'handle').html();

        type = this_object.attr('class');

        switch (type){
            case 'makePublic':
                $('#wb_modal_title').html('Confirm Public for Dataset '+ ds_id);
                $('#wb_modal_content').html('Are you sure you want to change to the public status for this dataset '  +ds_id+'? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
                break;                
            case 'makePrivate':
                $('#wb_modal_title').html('Confirm Private for Dataset '+ ds_id);
                $('#wb_modal_content').html('Are you sure you want to change to the private status for this dataset '  +ds_id+'? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
                break;                
            case 'togglePublished':
                $('#wb_modal_title').html('Confirm Published Status Toggle for Dataset '+ ds_id);
                $('#wb_modal_content').html('Are you sure you want to toggle the publishing status for this dataset '  +ds_id+'? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
                break;                
            case 'toggleYugene':
                $('#wb_modal_title').html('Confirm Yugene Status Toggle for Dataset '+ ds_id);
                $('#wb_modal_content').html('Are you sure you want to toggle the yugene status for this dataset '  +ds_id+'? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
                break;               
            case 'toggleMSC':
                $('#wb_modal_title').html('Confirm MSC Status Toggle for Dataset '+ ds_id);
                $('#wb_modal_content').html('Are you sure you want to toggle the MSC test access for this dataset '  +ds_id+'? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
                break;                
            case 'toggleLimited':
                $('#wb_modal_title').html('Confirm Limited Status Toggle for Dataset '+ ds_id);
                $('#wb_modal_content').html('Are you sure you want to toggle the limited status for this dataset '  +ds_id+'? <button class="submit" id="yes">Yes</button> <button class="submit" id="no">No</button><div id="deleteURL" class="hidden">'+$(this).attr('href')+'</div>');
                break;                
                
        } 

        $('#modal_div').modal({
            onShow: function (dialog) {
                var modal = this;
                
                // if the user clicks "yes"
                $('button').click(function (e) {
                    e.preventDefault();
                    var answer = $(this).html();
                    // close the dialog
                    modal.close(); // or $.modal.close();
                    
                    if (answer == 'Yes'){
                        switch (type){
                            case 'makePrivate':
                                updated_field = 'private';
                                new_value = "True";
                                break;
                            case 'togglePublished':
                                updated_field = 'published';
                                published = $('#'+ds_id+'published').html();
                                if (published == 'Published') { new_value = "False"; } else { new_value = "True"}
                                break;
                            case 'toggleYugene':
                                updated_field = 'show_yugene';
                                yugene = $('#'+ds_id+'yugene').html();
                                if (yugene == 'Show Yugene') { new_value = "False"; } else { new_value = "True"}
                                break;
                            case 'toggleMSC':
                                updated_field = $('#msc_values_access').html();
                                yugene = $('#'+ds_id+'msc_access').html();
                                if (yugene == 'True') { new_value = "False"; } else { new_value = "True"}
                                break;
                            case 'toggleLimited':
                                updated_field = 'show_limited';
                                limited = $('#'+ds_id+'limited').html();
                                if (limited == 'Show Limited') { new_value = "False"; } else { new_value = "True"}
                                break;

                            case 'makePublic':
                                window.location = BASE_PATH + 'admin/make_dataset_public/'+ds_id;
                                return;// want to leave before it runs the window.location command below. 
                                break;


                        }
                        window.location = BASE_PATH + 'admin/update_dataset_single_field/'+ds_id+'?new_value='+new_value+'&updated_field='+updated_field;
                        
                    } 
                    
                });
                
            }
        
        }); 
    });
    $('.annotate').off('click');
    $('.updateHandle').off('click').click(function(e){
        e.preventDefault();
        var this_object = $(this);
        var ds_id = this_object.attr('ds_id');
        handle = $('#'+ds_id+'handle').html();
        $('#handle').val(handle).css('width','700').css('line-height','22px');
        $('#update_handle').modal({
            minHeight:160,
            minWidth:800,
            onShow: function (dialog) {
                var modal = this;
                
                // if the user clicks "yes"
                $('button').click(function (e) {
                    e.preventDefault();
                    // close the dialog
                    handle = $('#handle').val();
                    updated_field = 'handle';
                    modal.close(); // or $.modal.close();
                    url = BASE_PATH + 'admin/update_dataset_single_field/'+ds_id+'?new_value='+handle+'&updated_field='+updated_field;
                    window.location = url;
                });
                
            }
        
        });
    }); 
    
 });
