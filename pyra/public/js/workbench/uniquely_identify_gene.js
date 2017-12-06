

$(document).ready(function() {


    $('a.choose').click(function(){
        
        
        oldValue = opener.document.getElementById("revalidateText").value;
        ensemblID = $(this).html();
        var original = $('#original').html();
        occurences = oldValue.split(original).length - 1;
        newValue = oldValue
        for (i=0; i < occurences;i++){
          newValue = newValue.replace(original,'');
        } 
        
        newValue = ensemblID + '\n' +newValue;
        
        opener.document.getElementById("revalidateText").value = newValue;
        
        CallParentWindowFunction();
        
        window.close();    
        
    });
    
    
    /* select all ensembl probes */
    $('#selectAll').click(function(){
        
        oldValue = opener.document.getElementById("revalidateText").value;
        
        var ensemblID = '';
        
        $('#gene_set_items a.choose').each(function(){
            ensemblID = $(this).html() +'\n' + ensemblID;
        
        });
        
        var original = $('#original').html();
        
        occurences = oldValue.split(original).length - 1;
        newValue = oldValue
        for (i=0; i < occurences;i++){
          newValue = newValue.replace(original,'');
        } 
        
        newValue = ensemblID + '\n' +newValue;
        
        opener.document.getElementById("revalidateText").value = newValue;
        
        CallParentWindowFunction();
        
        window.close();    
        
        
    });
    
    
});

/* helping to revalidate the list when leaving */
function CallParentWindowFunction()
{
    window.opener.CallAlert();
    return false;
}
