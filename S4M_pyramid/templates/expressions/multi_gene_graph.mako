<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/landing_pages.js')}"></script>
</%def>

<div class="content landing_page_graph">
    <div class="baseMarginLeft" >
        <div class="hidden" id="show_help_flag">NO</div>

        <div class="landing_page_header graphs block">
            <div class="left_square">
                <div class="header">MultiGene Graph</div>
                <div class="logo mgeg_logo"></div>
            </div>
            <div class="description centered">
                <p>
            This is the MultiGene Graph. In this graph you select a gene list and a dataset and you can choose to view a boxplot graph,scatterplot or a bar graph.
               </p>
               <p>
                You can start the wizard from the "Start the Wizard" box below or follow the tutorials by clicking on the large boxes with arrows below. Anything that is clickable will change colour if you hover over the item.
               </p>

            </div>
        </div>

        <div class="clear"></div>

        <div class="tutorials">
            <div class="title" >Start the Wizard</div>
            <a href="${h.url('/workbench/histogram_wizard')}">
                <div class="display_box">
                    <div class="left">
                        <div class="header">Click here to start the MultiGene Graph Wizard</div>
                        <div class="description">The MultiGene Graph allows you to graph the expression value for a gene list from a single dataset. <br/><br/>You will need to be registered and logged in. For tutorials on registering and creating your own gene list, see below. </div>
                    </div>
                    <div class="snapshot big_arrow"></div>
                </div>
            </a>
            <div class="clear"></div>
        </div>



        <div class="tutorials base_middle_width">
            <div class="title" >Tutorials</div>

            ${Base.tutorial_create_gene_list()}
            ${Base.tutorial_registration()}

             <div class="clear"></div>
        </div>

    </div>
</div>
