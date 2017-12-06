$(document).ready(function() {

    $('#exportTableCSVButton').click(function(){
                $('#RankedGenes').table2CSV();
            });

    $('#exportTableCSVButton_for_na_rows').click(function(){
                $('#NaRows').table2CSV();
            });

    $('#exportTableCSVButton_for_na_columns').click(function(){
                $('#NaColumns').table2CSV();
            });

    $('#save_image').click(function(e){

        if(e.preventDefault) { e.preventDefault();} else {  e.returnValue = false; }

        var file_url = $('img.hc_heatmap').attr('src');

        window.location = file_url+'&download=true';

    });

});
