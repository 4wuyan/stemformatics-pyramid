$(document).ready(function(){


    $('a.popup').click(function(){
            
            window.open($(this).attr('href'), "SelectUniqueGene", "status = 1, height = 860, width = 1024, resizable = 0" );
            return false;
    });


});
