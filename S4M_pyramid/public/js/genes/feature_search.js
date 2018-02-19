var autocompleteTimeout = 5000;
var genesearchTimeout = 5000;
var graphTimeout = 10000;
var graphWidth = 340;
var graphHeight = 275;


$(document).ready(function() {

    // error if more than X found, only displayX
    var error_div = $('#error_message');
    var error_message = error_div.html().length;
    if (error_message > 0) {
        error_div.removeClass('hidden');
    }

    $('body').on('click','exportTableCSVButton',function(){
        $('#downloadGeneSearch').table2CSV();
    });



    $('#searchGenes').dataTable( {
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "aaSorting": [[ 1, "asc" ]],
        "bAutoWidth": false } );



    // **************** All the auto complete functions **************************
    var details = new Object();
    details.id = "#featureSearch";
    details.data_url = BASE_PATH + 'genes/get_feature_search_autocomplete?feature_type=all&db_id=';
    details.target_url = BASE_PATH + 'genes/feature_search?feature_search_term=';
    details.append_to = ".searchBox";
    setup_feature_search_autocomplete(details);


    // **************** Cancel Form submit **************************



    // each time the enter key pressed, get the gene details
    $('form').submit(function(){


        $("#featureSearch").autocomplete('close');

        // getGeneDetails();
        window.location = BASE_PATH + 'genes/feature_search?feature_search_term=' + $("#featureSearch").val();

        return false;
    });


    /* *************** Initial actions ******************** */

    // choose Gene Selection first

    // have to fix firefox issue with focus not highlighting all text
    // Set the focus up on gene search straight away
    $('#featureSearch').focus();




});
