<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">

    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js','/js/external_asset_dependencies/d3-3.5.5.min.js')}"></script>
    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/d3-tip/0.6.3/d3-tip.min.js','/js/external_asset_dependencies/d3-tip-0.6.3.min.js')}"></script>

    <script type="text/javascript" src="${h.web_asset_url('/js/genes/search.js')}"></script>
    <script type="text/javascript" src="${h.web_asset_url('/js/expressions/biojs-vis-yugene-graph.js')}"></script>
    <link type="text/css" href="${h.web_asset_url('/css/expressions/biojs-vis-yugene-graph.css')}" rel="stylesheet" />



</%def>

   <%
        try:
            c.num_of_genes = len(c.results)
        except:
            c.num_of_genes = 0
    %>
<%def name="show_all_option()">


    %if c.num_of_genes > 0:
    <div class="show_all_button"><a href="#">Select from ${c.num_of_genes} genes found</a></div>
    %endif
</%def>
<div class="content">

    <div id="yugene_graph_data" class="hidden">${c.yugene_graph_data}</div>
    <div id="show_selections" class="hidden">${c.show_selections}</div>
    <div id="num_of_genes" class="hidden">${c.num_of_genes}</div>
    <div id="ensembl_id" class="hidden">${c.ensembl_id}</div>
    <div id="db_id" class="hidden">${c.db_id}</div>

    ${Base.pre_enclosed_search_box()}
    <%
    text.title = "Search Gene in "+c.site_name
    text.help = "Enter Symbol, Ensembl, Entrez, HGNC, MGI or RefSeq IDs for more precise results. It will provide suggestions via an autocomplete after four characters."
    text.input_id = "geneSearch"
    text.search_button_id = "viewGenes"
    text.search_action = h.url('/genes/search')
    text.search_value = c.searchQuery if c.searchQuery else ''
    text.input_class = ""
    %>
    ${Base.enclosed_search_box(text,self.show_all_option)}


    <% ensembl_id = str(c.ensembl_id) %>
    %if c.searchQuery and c.firstResult:
        <%
            db_id = str(c.firstResult['db_id'])
            symbol = str(c.firstResult['symbol'])
            aliases = str(c.firstResult['aliases'])
            description = str(c.firstResult['description']).replace('<br />','')
            species = str(c.firstResult['species'])
            entrez_id = str(c.firstResult['EntrezID'])

        %>
        <div class="gene_summary_box" >
            <a href="${h.url('/genes/summary?gene='+ensembl_id+'&db_id='+db_id)}">
                <div class="yugene_preview">
                    <div id="yugene_graph" class="graph" style="height: 240px; width: 310px;"></div>
                </div>
            </a>
            <div class="summary">
                <div class="title">${ensembl_id} ${symbol}</div>
                <div class="aliases">${aliases}</div>
                <div class="description">${description}</div>
                <div class="clear"></div>
                <div class="export_more_info generic_orange_button margin_top_small "><a href="#">Export / More Information</a></div>
            </div>
            <div class="clear"></div>
         </div>

        <div class="graph_icons">
            <div class="title gene_search_headers">Graphs</div>
                <% hover_text = "Click to view a Gene Expression Graph using this gene. In the next step you will be asked to choose a dataset." %>
            ${Base.large_icon('graphs','geg_logo','Gene Expression Graph','One gene, one dataset',hover_text,h.url('/expressions/result?graphType=default&db_id='+db_id+'&gene='+ensembl_id))}
                <% hover_text = "Click to view the Multiview using this gene. In the next step you will be asked to choose from two to four datasets, if you haven't chosen them already. You will need to be logged in to access this functionality." %>
            ${Base.large_icon('graphs','mv_logo','Multiview','One gene, up to four datasets',hover_text,h.url('/expressions/multi_dataset_result?graphType=scatter&gene='+ensembl_id+'&db_id='+db_id))}
            <% hover_text = "Click to view the YuGene Interactive Graph. This graph will show you all the samples across all datasets that are mapped to this gene. It will show you the YuGene value, which is a value that is between 0 and 1, with 1 being the most expressed. "%>
            ${Base.large_icon('graphs no_margin_right','yugene_logo','YuGene','One gene, all datasets',hover_text,h.url('/genes/summary?gene='+ensembl_id+'&db_id='+db_id))}
            <div class="clear"></div>
        </div>
    %endif
    <div class="analyses_icons base_width_minus_margin">
        <div class="title gene_search_headers">Analyses</div>
        <%
            gene_filter = ""
            my_gene_list_description = "Browse my gene lists"
            kegg_gene_list_description = "Browse Kegg pathways"
            public_gene_list_description = "Browse Public gene lists"
            my_gene_lists_found = 0
            kegg_gene_lists_found = 0
            public_gene_lists_found = 0

        %>
        %if c.searchQuery:
            <% gene_filter = "&ensembl_id="+ensembl_id %>
            %if c.gene_set_results is not None:
            <%
                gene_lists_found_breakdown = c.gene_set_results[1]
                try:
                    my_gene_lists_found = len(gene_lists_found_breakdown['uid'])
                except:
                    pass
                try:
                    kegg_gene_lists_found = len(gene_lists_found_breakdown['Kegg'])
                except:
                    pass
                try:
                    public_gene_lists_found = len(gene_lists_found_breakdown['Public'])
                except:
                    pass
            %>
            %endif
            <%

                my_gene_list_description = str(my_gene_lists_found) +" gene lists found"
                kegg_gene_list_description = str(kegg_gene_lists_found) + " Kegg pathways found"
                public_gene_list_description = str(public_gene_lists_found) + " Public gene lists found"

            %>
        %endif

            <% hover_text = "Show all your private and shared gene lists. You can then filter by gene list name and description. If you have selected a gene, it shows the number of gene lists found with the gene you selected." %>
        ${Base.large_icon('analyses','gla_logo','My Gene Lists',my_gene_list_description,hover_text,h.url('/workbench/gene_set_index?filter='+gene_filter))}
            <% hover_text = "Show all Kegg Pathway gene lists. You can then filter by gene list name and description. If you have selected a gene, it shows the number of gene lists found with the gene you selected." %>
        ${Base.large_icon('analyses','gla_logo','Kegg Pathways',kegg_gene_list_description,hover_text,h.url('/workbench/public_gene_set_index?filter=kegg'+gene_filter))}
            <% hover_text = "Show all Public gene lists. You can then filter by gene list name and description. If you have selected a gene, it shows the number of gene lists found with the gene you selected." %>
        ${Base.large_icon('analyses no_margin_right','gla_logo','Public Gene Lists',public_gene_list_description,hover_text,h.url('/workbench/public_gene_set_index?filter=public'+gene_filter))}
        %if not c.searchQuery:
            <% hover_text = "Click to do an easy search of all the non-coding RNA available in "+c.site_name %>
            ${Base.large_icon('analyses','ucsc_logo','Feature Search','Search miRNA',hover_text,h.url('/genes/feature_search'))}
        %endif

        %if c.searchQuery and c.firstResult:
            <% hover_text = "Click to do an analysis of the fold change for this gene. In the next step you will be asked to choose from a dataset in "+c.site_name %>
            ${Base.large_icon('analyses','fc_logo','Fold Change Viewer','Avg fold change',hover_text,h.url('/workbench/fold_change_viewer_wizard?gene='+ensembl_id+'&db_id='+db_id))}
            <% hover_text = "Click to do an analysis of the gene expression profile for this gene. In the next step you will be asked to choose from a dataset in "+c.site_name %>
            ${Base.large_icon('analyses','gep_logo','Gene Expression Profile','Find similar profiles',hover_text,h.url('/workbench/gene_neighbour_wizard?gene='+ensembl_id+'&db_id='+db_id))}
            <% hover_text = "Click to view the UCSC Browser for this gene." %>
            ${Base.large_icon('analyses no_margin_right','ucsc_logo','UCSC Browser','Browsing UCSC',hover_text,c.ucsc_data['base_url']+'?position=chr' + str(c.ucsc_data['chr'])+':'+str(c.ucsc_data['start'])+'-'+str(c.ucsc_data['end'])+'&db='+str(c.ucsc_data['ucsc_db_id']))}

        %endif
        <div class="clear"></div>
    </div>






    %if c.searchQuery and c.firstResult:
    <div class="more_info">
        <div class="title">Export / More Information</div>
        <div class="export">
           <ul class="buttonMenus">
                <li id="exportMenu">
                    <a class="button dropdown">
                        <span><span class="icon go"></span>Export</span><span class="arrow down"></span>
                    </a>
                    <ul class="submenu">
                        <li><a href="${request.url}&export=true" id="exportTableCSVButton">Export Gene Data</a></li>
                    </ul>
                </li>
            </ul>

        </div>
        <div class="clear"></div>
        ${Base.large_icon('analyses','gla_logo','Ensembl Browser','Click for Ensembl link','Link to the Ensembl website','http://www.ensembl.org/'+species+'/Gene/Summary?g='+ensembl_id)}
        ${Base.large_icon('analyses no_margin_right','gla_logo','Entrez Browser','Click for Entrez link','Link to the NCBI Entrez website','http://www.ncbi.nlm.nih.gov/gene/'+entrez_id)}
        ${Base.large_icon('analyses','gla_logo','Diseases via OMIM','Click for Omim link','Link to Omim for all diseases that have this Entrez ID','http://www.ncbi.nlm.nih.gov/gene?Db=omim&DbFrom=gene&Cmd=Link&LinkName=gene_omim&LinkReadableName=OMIM&IdsFromResult='+entrez_id)}
        ${Base.large_icon('analyses no_margin_right','gla_logo','Pubmed Links','Click for Pubmed link','Link to Pubmed for all publications that have this Entrez ID','http://www.ncbi.nlm.nih.gov/gene?Db=pubmed&DbFrom=gene&Cmd=Link&LinkName=gene_pubmed&LinkReadableName=PubMed&IdsFromResult='+entrez_id)}
        ${Base.large_icon('analyses no_margin_bottom ','gla_logo','InnateDB Link','Click for InnateDB link','Link to InnateDB',c.innate_db_object.get_single_gene_url(ensembl_id))}
        ${Base.large_icon('analyses no_margin_bottom no_margin_right','gla_logo','StringDB Link','Click for StringDB link','Link to StringDB',c.string_db_object.get_single_gene_url(ensembl_id))}


        <div class="clear"></div>
    </div>





    %endif


</div>
