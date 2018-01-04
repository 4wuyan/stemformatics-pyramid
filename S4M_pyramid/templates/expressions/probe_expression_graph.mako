<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">   
    <script type="text/javascript" src="${h.url('/js/expressions/gene_expression_graph_triggers.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/expressions/probe_expression_graph.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/landing_pages.js')}"></script>
</%def>
        
<div class="content landing_page_graph">    
    <div class="baseMarginLeft" >
        <div class="hidden" id="show_help_flag">NO</div>
        <div id="ds_id" class="hidden">${c.ds_id}</div>
        <div id="db_id" class="hidden">${c.db_id}</div>
        <div class="landing_page_header graphs block">
            <div class="left_square">
<% 
graph_title = "Fake title"  # c.assay_platform_dict[c.chip_type]['probe_name']
    # I couldn't find where c.assay_platform_dict was set atm
%>
                <div class="header">Select Individual ${graph_title} </div>
                <div class="logo geg_logo"></div>
            </div>
            <div class="description centered">
                <p>
                Select individual ${graph_title} for Dataset ${c.handle}. </p><p>In this graph you can choose to view a boxplot graph, a bar graph, a scatterplot and if available, a time series graph.
               </p> 
               <p> 
                You can select one from the search below. 
               </p> 
            </div>
        </div>  

        <div class="clear"></div>  

        <%def name="show_all_option_null()"> </%def>
        ${Base.pre_enclosed_search_box()}
        <% 
        text.title = graph_title + " for " +c.handle
        text.help = "Enter an ID into the search box below. It will provide suggestions via an autocomplete after two characters."
        text.input_id = "probeSearch"
        text.search_button_id = "viewGenes"
        text.search_action ='#' 
        text.search_value = ''
        text.input_class = 'geg'
        %>
        ${Base.enclosed_search_box(text,self.show_all_option_null)}


    </div>
</div>
 
