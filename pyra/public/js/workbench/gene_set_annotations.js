$(document).ready(function(){

    
    var base_url = $('#base_url').attr('url');
            
    var url_filter_gene_set_id = $('#url_filter_gene_set_id').attr('url');
    var url_filter_id = $('#url_filter_id').attr('url');
    var url_sp_filter = $('#url_sp_filter').attr('url');
    var url_tm_filter = $('#url_tm_filter').attr('url');
    var url_order_by = $('#url_order_by').attr('url');
    
    
    $('#select_filter').change(function(){
            
        var value = $("#select_filter option:selected").val();
        
        if (value != ""){
            
            window.location = base_url + url_filter_gene_set_id+ '&filter_id='+value;
        }
        
    });
    
    
    $('#save_filter').click(function(){
        $('#save_filter_form').modal();
    });
    
    
    $('#clear_all_filters').click(function(){
        window.location = base_url;
    });


    $('.select_page').change(function(){
        
            var value = $(this).children("option:selected").val();
        
            
            window.location = base_url + url_filter_gene_set_id + url_filter_id + url_sp_filter + url_tm_filter + '&page='+value;
        
        });


    $('#save_gene_set').click(function(){
        
        var new_url = base_url.replace(/view/i,'save');
        var genes_selected = "";
        var nice_gene_names_selected = "";
        $('#transcriptTable input:checked').each(function(){
            var name = $(this).attr('name');
            var nice_gene_name = $(this).attr('id');
            
            genes_selected = genes_selected + ',' + name;
            nice_gene_names_selected = nice_gene_names_selected + "," + nice_gene_name;
        });
        
        if (genes_selected != ""){
            var url_genes_selected = '&genes_selected=' + genes_selected.substring(1);
            var url_nice_gene_names_selected = '&nice_gene_names_selected=' + nice_gene_names_selected.substring(1);
            
        } else {
            var url_genes_selected = '';
            var url_nice_gene_names_selected = '';
        }
        
        
        var redirect_url = new_url + url_filter_gene_set_id + url_filter_id + url_sp_filter + url_tm_filter +url_genes_selected + url_nice_gene_names_selected;
        
        window.location = redirect_url;
    });
    
    
    
    $('#exportFilteredTxButton').click(function(){
        
        var new_url = base_url.replace(/view/i,'export_tx');
        var genes_selected = "";
        var nice_gene_names_selected = "";
        $('#transcriptTable input:checked').each(function(){
            var name = $(this).attr('name');
            var nice_gene_name = $(this).attr('id');
            
            genes_selected = genes_selected + ',' + name;
            nice_gene_names_selected = nice_gene_names_selected + "," + nice_gene_name;
        });
        
        if (genes_selected != ""){
            var url_genes_selected = '&genes_selected=' + genes_selected.substring(1);
            var url_nice_gene_names_selected = '&nice_gene_names_selected=' + nice_gene_names_selected.substring(1);
            
        } else {
            var url_genes_selected = '';
            var url_nice_gene_names_selected = '';
        }
        
        
        var redirect_url = new_url + url_filter_gene_set_id + url_filter_id + url_sp_filter + url_tm_filter +url_genes_selected + url_nice_gene_names_selected;
        
        window.location = redirect_url;
    });
    
    $('#removePagination').click(function(){
        
        var redirect_url = base_url + url_filter_gene_set_id + url_filter_id + url_sp_filter + url_tm_filter + url_order_by;
        
        window.location = redirect_url + '&remove_pagination=True';
    });
    
    
    $('#addPagination').click(function(){
        
        var redirect_url = base_url + url_filter_gene_set_id + url_filter_id + url_sp_filter + url_tm_filter + url_order_by;
        
        window.location = redirect_url + '&remove_pagination=False';
    });
    
    
    $('#exportPathwaysButton').click(function(){
        
        var new_url = base_url.replace(/view/i,'export_pathways');
        
        var redirect_url = new_url + url_filter_gene_set_id + url_filter_id + url_sp_filter + url_tm_filter;
        
        window.location = redirect_url;
    });
    
    
    $('td.show').click(function(){
        
        var gene_id = $(this).find('.gene_id').html();
        
        $('tr.tx_'+gene_id).toggle();
        
        var old_html = $(this).html();
        
        var isThere = old_html.indexOf('plus.png');
        
        if (isThere == -1){
            var new_html = old_html.replace('minus.png','plus.png');
            
        } else {
            var new_html = old_html.replace('plus.png','minus.png');
        }
        
        $(this).html(new_html);
        
        
    });
    
    $('#select_all').click(function(){
        
        var checkboxes_checked = $('#transcriptTable input:checked').length;
        
        $('#transcriptTable input:checkbox').each(function(){
            if (checkboxes_checked == 0){
                $(this).attr('checked','checked');            
            } else {
                $(this).attr('checked','');            
            }
        });
    });

    /* tree view */
    $("#browser").treeview();

});
