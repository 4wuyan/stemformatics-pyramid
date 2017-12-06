$(document).ready(function() {


    var analysis = $('#analysis').html();

    if (analysis == 3){

        $('a.gene_set_link').click(function(){

            var object = $(this);

            var geneNumber = object.next().html();

            if (geneNumber > 50){

                $('#wb_modal_title').html('Histogram Error');
                $('#wb_modal_content').html('This gene set is too large for showing in a MultiGene Graph. The maximum number of genes allowed is 50');
                $('#modal_div').modal({minHeight: 100});
                return false;
            }

        });
    }

    $('a.popup').unbind('click');
    $('a.popup').click(function(){

            window.open($(this).attr('href'), "Preview Genes", "status = 1, height = 860, width = 1024, resizable = 0" );
            return false;
    });

        /* aoColumns with bSortable False stops the column from being sortable */
    $('#gene_set_items').dataTable( {
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "oLanguage": {
          "sSearch": "Filter: "
        },

		"aoColumns": [
			null,
            null,
            null,
			{ "bSortable": false },
			{ "bSortable": false }
		],

        "aaSorting": [[ 0, "asc" ]],
        "bAutoWidth": false } );


    $('#public_gene_set_items').dataTable( {
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": false,
        "oLanguage": {
          "sSearch": "Filter: "
        },

		"aoColumns": [
			null,
            null,
            null,
			{ "bSortable": false },
			{ "bSortable": false }
		],

        "aaSorting": [[ 0, "asc" ]],
        "bAutoWidth": false } );



    $('h2').click(function(){

        // want to show the table underneath and also change the + to a -

        var object = $(this);

        var header_id = object.attr('id');

        var table_id = header_id.replace('header','div');

        var div_object = $('#'+table_id);
        var showing = div_object.css('display');

        if (showing == 'none') {
            div_object.show();
            object.find('img').attr('src',BASE_PATH+'images/workbench/minus.png');
        } else {
            div_object.hide();
            object.find('img').attr('src',BASE_PATH+'images/workbench/plus.png');
        }


    });

    /* $('#select_probes_for_hc_div input').click(function(){
        var url = new URL(document.URL);
        var probes=$('#select_probes_for_hc_div textarea').val();
        probes = probes.replace(/\s{1,}/g,DELIMITER);
        url.get_data['select_probes'] = probes;
        new_url = url.get_url();

        window.location = new_url;

    });
    */

});
