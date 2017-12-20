AUTOCOMPLETE_TIMEOUT = 5000;
$(document).ready(function() {

    var datasetID = $('#datasetID').html();
    var db_id = $('#db_id').html();

    var url = $('#url_to_post').attr('href');


    $("#geneSearch").autocomplete({
        source: BASE_PATH + 'genes/get_autocomplete',
        minLength: 4, // because the names are very small eg. STAT1
        timeout: AUTOCOMPLETE_TIMEOUT,
        appendTo: ".search_box",
        select: function(event, ui) {  
            var ensembl_id = ui.item.ensembl_id;
            var db_id = ui.item.db_id;
            window.location = url + '?gene='+ensembl_id+'&db_id='+db_id;
        }
    }).data("ui-autocomplete")._renderItem = function( ul,item ){
        return $("<li></li>").append("<a> <div class='symbol'>" + item.symbol + "</div><div class='species'>"+item.species+"</div><div class='aliases'>"+item.aliases+"</div><div class='description'>"+item.description+"</div><div class='clear'></div></a>").appendTo(ul);
    };
 

    $('#viewGenes').click(function(){
        $("#geneSearch").autocomplete('close');
        window.location = url + '?gene=' + $("#geneSearch").val();          
        // window.location = BASE_PATH + 'workbench/gene_neighbour_wizard?datasetID='+datasetID+'&gene=' + $("#geneSearch").val();          
    });
    

});
