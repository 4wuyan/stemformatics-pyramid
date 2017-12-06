$(document).ready(function() {

    $('#exportTableCSVButton').click(function(){
                $('#showGNOutput').table2CSV();	
            });          
    $('#submitSaveAsGeneSetButton').click(function(){
        $('#saveAsGeneSet').submit();
    });            
});
