var AUTOCOMPLETE_TIMEOUT = 5000,
    GRAPH_TIMEOUT = 10000;

$(document).ready(function() {
    
   
   
    $('#geneSearch').focus();
    gene_and_feature_search_actions();
       
});


function gene_and_feature_search_actions(){

    $('#geneSearchForm').submit(function() {    
        $("#geneSearch").autocomplete('close');
        classes_on_input = $('#geneSearch').attr('class');
        db_id = ''; 
        gene = $('#geneSearch').val();        
        go_to_url(gene,db_id,classes_on_input)
        //window.location = BASE_PATH + 'genes/summary?gene=' + $("#geneSearch").val();
        return false;
    });
    if ( $( "#geneSearch" ).length ) {
        $("#geneSearch").autocomplete({
            source: BASE_PATH + 'genes/get_autocomplete',
            minLength: 4, // because the names are very small eg. STAT1
            timeout: AUTOCOMPLETE_TIMEOUT,
            appendTo: ".search_box",
            select: function(event, ui) {  
                classes_on_input = event.target.className;
                var gene = ui.item.ensembl_id;
                var db_id = ui.item.db_id;
                go_to_url(gene,db_id,classes_on_input)

            }
        }).data("ui-autocomplete")._renderItem = function( ul,item ){
            return $("<li></li>").append("<a> <div class='symbol'>" + item.symbol + "</div><div class='species'>"+item.species+"</div><div class='aliases'>"+item.aliases+"</div><div class='description'>"+item.description+"</div><div class='clear'></div></a>").appendTo(ul);
        };
    }  // if geneSearch Length

    $('#viewGenes').click(function(){ 
        classes_on_input = $('#geneSearch').attr('class');
        db_id = ''; 
        gene = $('#geneSearch').val();        
        go_to_url(gene,db_id,classes_on_input)
    });
 
}

function go_to_url(gene,db_id,classes_on_input){
        if (classes_on_input.indexOf('yugene') != -1){
            url = BASE_PATH + 'genes/summary?gene=' + gene + '&db_id='+db_id;          
        }
        if (classes_on_input.indexOf('geg') != -1){
            url = BASE_PATH + 'expressions/result?graphType=default&gene=' + gene + '&db_id='+db_id;          
        }
        if (classes_on_input.indexOf('mv') != -1){
            url = BASE_PATH + 'expressions/multi_dataset_result?graphType=default&gene=' + gene + '&db_id='+db_id;          
        }
        window.location = url;

}

