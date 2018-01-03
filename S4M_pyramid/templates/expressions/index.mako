<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link type="text/css" href="${h.url('/css/workbench/index.css')}" rel="stylesheet" />
    <script type="text/javascript" src="${h.url('/js/expressions/choose_dataset.js')}"></script>
</%def>

<div class="content">
    <div class="baseMarginLeft base_width_minus_margin">
        <div class="hidden" id="show_help_flag">NO</div>

        <% hover_text = "This is the Gene Expression Graph. In this graph you select a gene and a dataset and you can choose to view a boxplot graph, a bar graph, a scatterplot and if available, a time series graph." %>
        ${Base.large_icon('graphs','geg_logo','Gene Expression Graph','One gene, one dataset',hover_text,h.url('/expressions/gene_expression_graph'))}

        <% hover_text = "This is the MultiGene Graph. In this graph you select a gene list and a dataset and you can choose to view the expression in a boxplot graph,scatterplot or a bar graph." %>
        ${Base.large_icon('graphs','mgeg_logo','MultiGene Graph','Multi gene, one dataset',hover_text,h.url('/expressions/multi_gene_graph'))}

        <% hover_text = "This is the Multiview. In this graph you select a gene and from two to nine datasets and you can choose to view a boxplot graph, a bar graph and a scatterplot. There is no time series graph available at the moment." %>
        ${Base.large_icon('graphs no_margin_right','mv_logo','Multiview','One gene, up to nine datasets',hover_text,h.url('/expressions/multi_view'))}

        <% hover_text = "This is the YuGene Interactive Graph. In this graph you select a gene and it will show you all the samples across all datasets that are mapped to this gene. It will show you the YuGene value, which is a value that is between 0 and 1, with 1 being the most expressed. "%>
        ${Base.large_icon('graphs','yugene_logo','YuGene','One gene, all datasets',hover_text,h.url('/expressions/yugene'))}

        <div class="clear"></div>


    </div>
</div>
