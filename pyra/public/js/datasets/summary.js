
$(document).ready(function() {
	contextHelpClick();

    var autocompleteTimeout = 5000;
    
    var db_id = $('#datasetDetails').attr('data-db_id'), 
        datasetID = $('#datasetDetails').attr('data-ds_id');
    
    $('#datasetGroupSamplesTable').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 0, "asc" ]],
        "bAutoWidth": false 
    });
    
    $("#geneSearch").autocomplete({
        source: BASE_PATH + 'genes/get_autocomplete?db_id='+db_id,
        minLength: 4, // because the names are very small eg. STAT1
        timeout: autocompleteTimeout,
        appendTo: ".geneSearch .searchBox",
        select: function(event, ui) {
            window.location = BASE_PATH + 'expressions/result?graphType=default&datasetID=' +datasetID+ '&gene=' +ui.item.value+ '&db_id=' +db_id;
        }
    });

    $("#probeSearch").autocomplete({
        source: BASE_PATH + 'datasets/autocomplete_probes_for_dataset?ds_id='+datasetID,
        minLength: 2, // because the names are very small eg. STAT1
        timeout: autocompleteTimeout,
        appendTo: ".probeSearch .searchBox",
        select: function(event, ui) {
            var probe = $('#probeSearch').val().replace('+','%2B');
            window.location = BASE_PATH + 'expressions/probe_result?graphType=default&datasetID=' +datasetID+'&probe=' +probe+ '&db_id=' +db_id;
        }
    });

    $('#geneSearchSubmit').click(function(){
		$('#geneSearchForm').submit();
	});
    
    $('#probeSearchSubmit').click(function(){
        $('#probeSearchForm').submit();
    });

    $('#geneSearchForm').submit(function(){ 
        $("#geneSearch").autocomplete('close');
        var gene = $('#geneSearch').val();
        window.location = BASE_PATH + 'expressions/result?graphType=default&datasetID='+datasetID+'&gene='+gene+'&db_id='+db_id;
        return false; 
    });

    $('#probeSearchForm').submit(function(){ 
        $("#probeSearch").autocomplete('close');
        var probe = $('#probeSearch').val().replace('+','%2B');
        window.location = BASE_PATH + 'expressions/probe_result?graphType=default&datasetID='+datasetID+'&probe='+probe+'&db_id='+db_id;
        return false;
    });
    
    $('#exportTableCSVButton').click(function(){
        $('#downloadDatasetSearch').table2CSV();    
    });
    
    $('#exportHighestGeneExpressedTableCSVButton').click(function(){
        $('#datasetHighlyExpressedTable').table2CSV();  
    });
    
    $('#exportGroupingSamplesTableCSVButton').click(function(){
        $('#datasetGroupSamplesTable').table2CSV(); 
    });
    
});
