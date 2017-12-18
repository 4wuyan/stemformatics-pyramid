
$(document).ready(function() {
    publish_gene_list_link();
    edit_gene_list_link();
    share_gene_list_link();
    delete_gene_list_link();
    /* aoColumns with bSortable False stops the column from being sortable */
    initial_filter = $('#initial_filter').html();
    if (initial_filter == undefined) {
        initial_filter = '';
    }
    $('#gene_set_items').dataTable( {
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "oSearch": {"sSearch":initial_filter},
		"aoColumns": [
			null,
            null,
            null,
			{ "bSortable": false },
			{ "bSortable": false }
		],

        "aaSorting": [[ 0, "asc" ]],
        "bAutoWidth": false } );


    $('#exportTableCSVButton').click(function(){
                $('#downloadGeneSetsTable').table2CSV();
            });


    $('a.popup').click(function(){

        window.open($(this).attr('href'), "PreviewGene", "status = 1, height = 860, width = 1024, resizable = 0, scrollbars=1" );
        return false;
    });








});
