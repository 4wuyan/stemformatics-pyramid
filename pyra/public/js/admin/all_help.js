
$(document).ready(function() {
   
    $('.dumpMenu .upload').on('click', function () {
        $('#upload_help_modal').modal();
    });
    
    $('.dumpMenu .upload').on('submit', function (event) {
        if (!$("#jsonfile").val()) {  // no file
            $('#upload_help_modal .save-error').html("Must select a file");
            event.preventDefault();
        }
    });
    
});