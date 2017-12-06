// make these variables global
var ds_id = 0;
var db_id = '';
var this_graph_data = {};

// Most of this is in expressions/graph.js
$(document).ready(function() {
    ds_id = $('#ds_id').html();    
    db_id = $('#db_id').html();
    graph_id = '#graph';
    this_graph_data = new graph_data(ds_id,graph_id,db_id);
    click_choose_datasets();
    check_choose_dataset_immediately();

    if (jQuery.isEmptyObject(this_graph_data.view_data.plot_data)){



        $('div.loading, div.backgroundGraph,div.view_table_content').hide();
        $('#no_data').modal({
            minHeight: 150
            /* minWidth: 400, */
       
        });
 
    } else {

        //set_large();	
        this_graph_data.view_data.expand_horizontally = false;   
        // gene_expression_graphs.js
        selectGraphToDraw();
        set_autocomplete();
      
        $('#graph_selection').draggable();
        $('div.graphControls').draggable();

    }
});



