$(document).ready(function() {

    $('#exportTableCSVButton').click(function(){
                $('#showCMSOutput').table2CSV();	
            });          
   
   $('#save_image').click(function(e){
        
        if(e.preventDefault) { e.preventDefault();} else {  e.returnValue = false; }
        
        var file_url = $('img.heatmap').attr('src');
        
        window.location = file_url+'&download=true';
        
    });
    $('#submitSaveAsGeneSetButton').click(function(){
        $('#saveAsGeneSet').submit();
    });     
});
