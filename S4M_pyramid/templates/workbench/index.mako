<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link type="text/css" href="${h.url('/css/workbench/index.css')}" rel="stylesheet" />
    <script type="text/javascript" src="${h.url('/js/workbench/index.js')}"></script>
</%def>

    <div class="hidden" id="show_help_flag">NO</div>
    <div class="content">
        <div class="baseMarginLeft base_width_minus_margin">

            <!-- ########################## First Row ################################### -->

            <% hover_text = "This is the Hierarchical Cluster. In this analysis you select a gene list,a dataset and some graphing options like grouping by genes or samples or both. It returns a heatmap with the clustering specified along with options to export the image and the table in order." %>
            ${Base.large_icon('analyses','hc_logo','Hierarchical Cluster','Clustering',hover_text,h.url('/workbench/hierarchical_cluster_wizard'))}

            <% hover_text = "This is the Gene Expression Profile. In this analysis you select a gene for it's expression profile (Gene Neighbourhood) or provide your own expression profile (User Defined Expression Profile), then you select a dataset. It then returns all other genes that are in that dataset that have a similar expression profile." %>
            ${Base.large_icon('analyses','gep_logo','Gene Expression Profile','Find similar profiles',hover_text,h.url('/workbench/gene_expression_profile_wizard'))}

            <% hover_text = "This is the Rohart MSC Test. You can view whether the samples in a dataset are considered MSC or non-MSC."  %>
            ${Base.large_icon('analyses no_margin_right','mdd_logo','Rohart MSC Test','View MSC and non-MSC status',hover_text,h.url('/workbench/rohart_msc_test'))}

            <!-- ########################## Second Row ################################### -->
            <% hover_text = "This is the Multiple Dataset Downloader. You can search on the metadata of samples and datasets to find datasets that you can then download in the one place."  %>
            ${Base.large_icon('analyses','mdd_logo','Multiple Dataset Downloader','Search and download datasets',hover_text,h.url('/workbench/download_multiple_datasets'))}
            <% hover_text = "This is the Fold Change Viewer. In this analysis you select a gene and a dataset and you can then select the fold change between two groups of samples. This fold change is based off the average of the sample groups." %>
            ${Base.large_icon('analyses','fc_logo','Fold Change Viewer','Avg fold change',hover_text,h.url('/workbench/fold_change_viewer_wizard'))}



            <% hover_text = "This is the UCSC Browser. There are several places where you can access the UCSC Browser, such as Gene Search and Gene Expression Graph. This takes you to a landing page where you can see some tutorials of where to access the UCSC browser on "+c.site_name+"." %>
            ${Base.large_icon('analyses no_margin_right','ucsc_logo','UCSC Browser','Browsing UCSC',hover_text,h.url('/workbench/ucsc'))}

            <!-- ########################## Third Row ################################### -->
            <% hover_text = "This is the Gene List Annotation. In this analysis you select a gene list and it returns a list of Kegg Pathways, Signal Peptide,Transcript and Transmembrane information." %>
            ${Base.large_icon('analyses ','gla_logo','Gene List Annotation','Find Kegg Pathways',hover_text,h.url('/workbench/gene_set_annotation_wizard'))}

            <% hover_text = "This is a link to all the completed and in-progress analyses. You can filter based on the name of the analysis or the content. All analyses have an expiry period." %>
            ${Base.large_icon('analyses','jobs_logo','My Jobs','Pending and finished jobs',hover_text,h.url('/workbench/jobs_index'))}

            <!--
            <% hover_text = "This is a link to login as a guest account so that you can check out the functionality of "+c.site_name+". Please note that everything you generate is public and can be viewed by anyone. You can register for free via the registration link in the top right hand corner." %>
            ${Base.large_icon('analyses no_margin_right','user_logo','Guest Account','Publically accessible demo account' ,hover_text,h.url('/auth/guest'))}
            -->
             <div class="clear"></div>

        </div>
    </div>



