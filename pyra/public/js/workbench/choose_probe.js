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
    probe_list = this_graph_data.view_data.probe_list;

    for ( var probe_count in probe_list){
        graph_id = '#graph'+probe_count;
        this_graph_data = new graph_data(ds_id,graph_id,db_id);
        this_graph_data.view_data.draw_scatter_with_lines = true;

        var probe_name = this_graph_data.view_data.probe_list[probe_count];
        var save_plot_data = this_graph_data.view_data.plot_data[probe_name]
        this_graph_data.view_data.title = "Expression Graph for "+probe_name + " for Dataset " + this_graph_data.view_data.handle;
        this_graph_data.view_data.plot_data = {};
        this_graph_data.view_data.plot_data[probe_name] = save_plot_data;

        //filter_gene_symbol();
     
        //set_sort_by();
        set_large();	
       
        // gene_expression_graphs.js
        selectGraphToDraw();
    } 
});

