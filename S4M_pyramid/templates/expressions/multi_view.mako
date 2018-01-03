<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/landing_pages.js')}"></script>
</%def>

<div class="content landing_page_graph">
    <div class="baseMarginLeft" >
        <div class="hidden" id="show_help_flag">NO</div>

        <div class="landing_page_header graphs block">
            <div class="left_square">
                <div class="header">Multiview</div>
                <div class="logo mv_logo"></div>
            </div>
            <div class="description centered">
            <p>
            This is the Multiview. In this graph you select a gene and from two to four dataset and you can choose to view a boxplot graph, a bar graph and a scatterplot. There is no time series graph available at the moment.
            </p>
            <p>
            You can select a gene from the gene search below or follow the tutorials by clicking on the large boxes with arrows below. Anything that is clickable will change colour if you hover over the item.
            </p>
            </div>
        </div>
        <div class="clear"></div>

        <%def name="show_all_option()"> </%def>
        ${Base.pre_enclosed_search_box()}
        <%
        text.title = "Gene Search for Multiview Graph"
        text.help = "Enter Symbol or Ensembl IDs for more precise results. It will provide suggestions via an autocomplete after four characters."
        text.input_id = "geneSearch"
        text.search_button_id = "viewGenes"
        text.search_action ='#'
        text.search_value = ''
        text.input_class = 'mv'
        %>
        ${Base.enclosed_search_box(text,self.show_all_option)}

        <div class="tutorials base_middle_width">
            <div class="title" >Tutorials</div>
            <a href="#" class="in_page_tutorial_link" data-tutorial="multiview" onclick="return audit_help_log ('multiview', 'help_tutorial_landing'); ">
            <div class="display_box">
                <div class="left">
                    <div class="header">Direct Access to Multiview</div>
                    <div class="description"> This link provides a tutorial to enter in a gene to take you directly to the Multiview Graph page. You will need to be registered. Registration is free. Please see below for details.<br/><br/>Please click to start.
                    </div>
                </div>
                <div class="snapshot big_arrow"></div>
            </div>
            </a>
            ${Base.tutorial_registration()}
            ${Base.tutorial_gene_search_single_gene_graphs()}
            <div class="clear"></div>
        </div>

    </div>
</div>
