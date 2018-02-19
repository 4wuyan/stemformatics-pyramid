<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/landing_pages.js')}"></script>
</%def>


<div class="content">
    <div class="landing_page_analyses" >
        <div class="hidden" id="show_help_flag">NO</div>

        <div class="landing_page_header analyses block">
            <div class="left_square">
                <div class="header">UCSC</div>
                <div class="logo ucsc_logo"></div>
            </div>
            <div class="description centered">
            <p>
            This is the UCSC Browser. There are several places where you can access the UCSC Browser, such as Gene Search and Gene Expression Graph.
            </p>
            <p>
            You can select a gene to take you to the YuGene Interactive Graph which has a link called "Genome Browser". This landing page also provides tutorials of where else to access the UCSC browser on ${c.site_name}.
            </p>
            </div>
        </div>

        <div class="clear"></div>
        <%def name="show_all_option()"> </%def>
        ${Base.pre_enclosed_search_box()}
        <%
        text.title = "View UCSC via YuGene Interactive Graph"
        text.help = "Enter Symbol or Ensembl IDs for more precise results. It will provide suggestions via an autocomplete after four characters. It will take you to the YuGene Graph and then you can select an option from the Genome Browser dropdown menu."
        text.input_id = "geneSearch"
        text.search_button_id = "viewGenes"
        text.search_action ='#'
        text.search_value = ''
        text.input_class='yugene'
        %>
        ${Base.enclosed_search_box(text,self.show_all_option)}


        <div class="tutorials base_middle_width">
            <div class="title" >Tutorials</div>
            ${Base.tutorial_gene_search_single_gene_graphs()}
            <div class="clear"></div>
        </div>

    </div>
</div>

