<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.web_asset_url('/js/datasets/search.js')}"></script>
</%def>

<script type="text/javascript">
$(document).ready(function(){
    // https://stackoverflow.com/questions/13755563/how-to-add-an-overlay-div-to-cover-an-existing-div-using-jquery
    $("<div class='div_to_disable' />").css({
        position: "absolute",
        width: "100%",
        height: "100%",
        "background-color": "#000000",
        opacity: 0.3,
        left: 0,
        zIndex: 1000000,  // to be on the safe side
        top: 0
    }).appendTo($(".disabled").css("position", "relative"));

});
</script>
<style>
#dataset_status {

    background-color: #68228B;
    margin-bottom: 20px;
    height: 60px;
    color: #FFFFFF;
}
#dataset_status_text {
    font-family: Arial;
    font-size: 17px;
    line-height: 17px;
    margin-top: 22px;
    margin-left: 20px;
    float:left;
}
#report_summary td{
  width: 80% !important; /* changes for IE to explicitly set width for td*/
}
</style>


<%
        try:
            c.num_of_ds = len(c.dataset)
        except:
            c.num_of_ds = 0
%>

<%def name="show_all_option()">
</%def>

<div id="selected_ds_id" class="hidden">${c.selected_ds_id}</div>
<div id="ds_id" class="hidden">${c.ds_id}</div>
<div id="db_id" class="hidden">${c.db_id}</div>
<div id="num_of_datasets" class="hidden">${c.num_of_ds}</div>
<!-- Python code that returns this has default has_data = yes -->
% if c.ds_id:
  <div id="has_data" class="hidden">${c.dataset[c.ds_id]['has_data']}</div>
% endif



<div class="content">

    ${Base.pre_enclosed_search_box()}
    <%
    text.title = "Search Dataset in "+c.site_name
    text.help = "Keyword Search to filter available datasets: Filter on cell type, author name, publication title or dataset ID"
    text.input_id = "dataset_search"
    text.search_button_id = "view_datasets"
    text.search_action = "/datasets/search"
    text.search_value = c.searchQuery
    text.input_name = "filter"
    text.input_class = ""

    # note that the text.extra_class in pre_enclosed_search_box doesn't
    # reset if this has already been used. Have to set the blank value to be sure
    text.extra_class = ""
    %>
    ${Base.enclosed_search_box(text,self.show_all_option)}

    %if c.ds_id and 'datasetStatus' in c.dataset[c.ds_id] and c.dataset[c.ds_id]['datasetStatus'] != None and c.dataset[c.ds_id]['datasetStatus'] != '':
        <div id="dataset_status">
            <div id="dataset_status_text">${c.dataset[c.ds_id]['datasetStatus']} </div>
        </div>
    %endif

    %if c.num_of_ds == 0:
        <div class="base_width_minus_margin">
            <div class="title gene_search_headers">Quick Search Terms</div>
            <% hover_text = "Click to do an easy search for all the Project Grandiose datasets in "+c.site_name %>
            ${Base.large_icon('analyses','gla_logo','All Project Grandiose Datasets','Click for all Project Grandiose datasets',hover_text,h.url('/datasets/search?filter=Project Grandiose:'))}
            <% hover_text = "Click to do an easy search for all the LEUKomics datasets in "+c.site_name %>
            ${Base.large_icon('analyses','gla_logo','All LEUKomics Datasets','Click for all LEUKomics datasets',hover_text,h.url('/datasets/search?filter=leukomics'))}
            <% hover_text = "Click to do an easy search for all the human msc datasets in "+c.site_name %>
            ${Base.large_icon('analyses no_margin_right','gla_logo','All Human MSC Datasets','Click for all MSC human datasets',hover_text,h.url('/datasets/search?filter=Homo sapiens and MSC'))}
            <% hover_text = "Click to do an easy search for all the mouse datasets in "+c.site_name %>
            ${Base.large_icon('analyses','gla_logo','All Mouse Datasets','Click for all mouse datasets',hover_text,h.url('/datasets/search?filter=Mus musculus'))}
            <% hover_text = "This is the Multiple Dataset Downloader. You can search on the metadata of samples and datasets to find datasets that you can then download in the one place."  %>
            ${Base.large_icon('analyses','mdd_logo','Multiple Dataset Downloader','Search and download datasets',hover_text,h.url('/workbench/download_multiple_datasets'))}
            <% hover_text = "Click to make a suggestion for a dataset in "+c.site_name %>
            ${Base.large_icon('analyses no_margin_right','gla_logo','Suggest a Dataset','Click to suggest a public dataset',hover_text,h.url('/main/suggest_dataset'))}
        </div>
        <div class="clear"></div>
        <div class="two_cols links_we_like light_background hidden">
            <div class="title analyses_text">Human Datasets</div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Homo sapiens')}">Filter All Human Datasets ></a></div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Homo sapiens and Kidney')}">Filter All Human Kidney Datasets ></a></div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Homo sapiens and iPSC')}">Filter All Human iPSC Datasets ></a></div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Homo sapiens and MSC')}">Filter All Human MSC Datasets ></a></div>
        </div>
        <div class="two_cols links_we_like no_margin_right light_background hidden">
            <div class="title analyses_text">Mouse Datasets</div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Mus musculus')}">All Mouse Datasets ></a></div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Mus musculus and Kidney')}">All Mouse Kidney Datasets ></a></div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Mus musculus and iPSC')}">All Mouse iPSC Datasets ></a></div>
            <div class="initial_search"><a href="${h.url('/datasets/search?filter=Mus musculus and MSC')}">All Mouse MSC Datasets ></a></div>
        </div>
    %else:
        <% ds_id = c.ds_id %>
        <%
        chip_type =c.dataset[c.ds_id]['chip_type']
        platform_type = '' # not sure if this is even being used RM
        probe_name = c.dataset[c.ds_id]['probeName']

        %>
        <div class="hidden" id="platform_type">${platform_type}</div>
        <div class="hidden" id="probe_name">${probe_name}</div>
         <div class="dataset_summary_box" style="display:inline-block">
            %if c.role =="admin" or c.role=="annotator":
            <div class="admin">
                <a href="${h.url('/admin/annotate_dataset?ds_id='+str(c.ds_id))}">Annotate this Dataset</a>
                %if c.role=="admin":
                <a href="${h.url('/admin/update_datasets?ds_id='+str(c.ds_id))}">Update this Dataset</a>
                <a href="${h.url('/admin/setup_new_dataset/'+str(c.ds_id))}">Setup this Dataset in Redis</a>
                %endif
            </div>
            %endif
            <div class="title">${c.dataset[ds_id]['title']}</div>
            <div class="handle">${c.dataset[ds_id]['handle']} (${c.dataset[ds_id]['organism']})</div>
            <div class="cells">${c.dataset[ds_id]['cells_samples_assayed']}</div>
            <div class="clear"></div>
            <div class="description">${c.dataset[ds_id]['authors']}</div>
            <div class="description">${c.dataset[ds_id]['description']}</div>
            <div class="clear"></div>
            <div class="dataset_links_col no_margin_left">
                <table id="datasetDetails"  class="fixed" data-ds_id="${c.ds_id}" >
                    <tr class="pubMedID">
                        <td>Pubmed ID:</td>
                        <td class="detail"><a target="_blank" href="${'http://www.ncbi.nlm.nih.gov/pubmed/' + c.dataset[ds_id]['pub_med_id']}">${c.dataset[ds_id]['pub_med_id']}</a>
                        </td>
                    </tr>
                    <tr class="accessionID">
                        <td>Accession IDs:  </td>
                        <td class="detail">
                            ${h.setup_accession_ids_for_viewing(c.dataset[ds_id])}
                            %if False == True:
                            %endif
                        </td>
                    </tr>
%if c.dataset[ds_id]['has_data'] != 'no':
    %if platform_type == 'miRNA':
        %if c.dataset[ds_id]["top_miRNA"] != {}:
                        <tr class="platform">
                            <td>miRNA of Interest:</td>
                            <td class="genes_of_interest">
                                <% miRNA_of_interest = c.dataset[ds_id]["top_miRNA"].split(',')%>
                                % for row in miRNA_of_interest:

                                        <%
                                        miRNA = row
                                        main_url =  h.url('/expressions/feature_result?graphType=default&feature_type=miRNA&feature_id=' + str(miRNA) + '&db_id=' + str(c.db_id) + '&datasetID=' + str(c.ds_id))
                                        %>
                                        <a href="${main_url}">${miRNA}</a>
                                % endfor
                            </td>
                        </tr>
        %endif
    %else:
        %if c.dataset[ds_id]["top_diff_exp_genes"] != {}:
                        <tr class="platform">
                            <td>Genes of Interest:</td>
                            <td class="genes_of_interest">
                                <% genes_of_interest = c.dataset[ds_id]["top_diff_exp_genes"] %>
                                <% default_url_geg = "" %>
                                % for gene, gene_details in genes_of_interest.iteritems():

                                        <%
                                        main_url =  h.url('/expressions/result?graphType=default&gene=' + str(gene_details['ensemblID']) + '&db_id=' + str(gene_details['db_id']) + '&datasetID=' + str(c.ds_id))
                                        if default_url_geg == "":
                                            default_url_geg = main_url
                                        %>
                                        <a href="${main_url}">${gene}</a>
                                % endfor
                            </td>
                        </tr>
        %endif
    %endif
%endif
                    <tr class="name">
                        <td>Name:</td>
                        <td class="detail">${c.dataset[ds_id]['name']}</td>
                    </tr>
                    <tr class="email">
                        <td>Email:</td>
                        <td class="detail">${c.dataset[ds_id]['email']}</td>
                    </tr>
                    <tr class="affiliation">
                        <td>Affiliation:</td>
                        <td class="detail">${c.dataset[ds_id]['affiliation']}</td>
                    </tr>
                    %if c.dataset[ds_id]['has_data'] != 'no':
                    <tr class="platform">
                        <td>Number of Samples:</td>
                        <td class="detail">${c.dataset[ds_id]['number_of_samples']}</td>
                    </tr>
                    %endif
                    <tr class="platform">
                        <td>Platform:</td>
                        <td class="detail">${c.dataset[ds_id]['platform']}</td>
                    </tr>
%if True == False:
                    <tr class="probes-detected">
                        <td>${Base.print_plural(probe_name)} Detected:</td>
                        <td class="detail">${c.dataset[ds_id]['probes detected']}</td>
                    </tr>
                    <tr class="probes">
                        <td>${Base.print_plural(probe_name)}:</td>
                        <td class="detail">${c.dataset[ds_id]['probes']}</td>
                    </tr>
%endif
                </table>

            </div>
            <div class="clear"></div>


            <div class="clear"></div>
       </div>
            <div class="column2" style="display:inline-block;margin-left:25px;width:43.5%;vertical-align:top">
              <div class="enclosed_search_box" >
                  <div class="title">
                      Reports
                  </div>
                  <div class="breakdown">
                  <table id="report_summary" class="dataTable" style="border:2px solid #ddd">
                    <thead>
                      <tr>
                        <td style="border-right:2px solid #ddd">
                          Report
                        </td>
                        <td >
                          Link to Report
                        </td>
                      </tr>
                    </thead>
                      <tbody>
                          %if c.dataset[ds_id]['has_data'] != 'no':
                              <tr>
                                <td>
                                  Export Metadata / View Sample Summary
                                </td>
                                <td>
                                  <div class="export_more_info"><a href="#">View</a></div>
                                </td>
                              </tr>

                              % if c.msc_values_access in c.dataset[ds_id] and c.dataset[ds_id][c.msc_values_access] == 'True':
                              <tr>
                                <td>
                                  Rohart MSC Test
                                </td>
                                <td>
                                  <div><a target="_blank" href="${h.url('/workbench/rohart_msc_graph?ds_id=')}${c.ds_id}">View</a></div>
                                </td>
                              </tr>

                              %endif
                          %endif
                          % for button_name,button_url in c.dataset[ds_id]['showReportOnDatasetSummaryPage']:
                                  <tr>
                                      <td style="border-right:2px solid #ddd">${button_name}</td>
                                      <td><a href="/reports/${ds_id}${button_url}">view</a></td>
                                  </tr>
                          % endfor
                          % for button_name,button_url in c.dataset[ds_id]['ShowExternalLinksOnDatasetSummaryPage']:
                                  <tr>
                                      <td style="border-right:2px solid #ddd">${button_name}</td>
                                      <td><a target="_blank" href="${button_url}">view</a></td>
                                  </tr>
                          % endfor
                          % for button_name,button_url in c.dataset[ds_id]['ShowPCALinksOnDatasetSummaryPage']:
                                  <tr>
                                      <td style="border-right:2px solid #ddd">${button_name} PCA Plots</td>
                                      <td><a target="_blank" href="${button_url}">view</a></td>
                                  </tr>
                          % endfor


                      </tbody>
                  </table>
                  </div>
              </div>

            <div class="clear"></div>
         <%def name="show_all_option_null()"> </%def>

        %if platform_type == 'miRNA':
            ${Base.pre_enclosed_search_box()}
            <%
            text.title = "miRNA Search for Expression Graph"
            text.help = "Enter miRBASE v18 details for more precise results. It will provide suggestions via an autocomplete after four characters."
            text.input_id = "miRNASearch"
            text.search_button_id = "viewmiRNA"
            text.search_action ='#'
            text.search_value = ''
            text.input_class = 'geg'
            if c.dataset[c.ds_id]['has_data'] == 'no':
                text.extra_class = 'disabled'
            %>
            ${Base.enclosed_search_box(text,self.show_all_option_null)}
        %endif

        ${Base.pre_enclosed_search_box()}
        %if platform_type == 'NGS methylome':
            <%
            text.title = "Gene Search for Promoter Methylation Graph"
            %>
        %else:
            <%
            text.title = "Gene Search for Gene Expression Graph"
            %>
        %endif
        <%
        text.help = "Enter Symbol or Ensembl IDs for more precise results. It will provide suggestions via an autocomplete after four characters."
        text.input_id = "geneSearch"
        text.search_button_id = "viewGenes"
        text.search_action ='#'
        text.search_value = ''
        text.input_class = 'geg'
        if c.dataset[c.ds_id]['has_data'] == 'no':
            text.extra_class = 'disabled'
        %>
        ${Base.enclosed_search_box(text,self.show_all_option_null)}

        %if probe_name != 'miRNA' and probe_name != 'Gene':
            ${Base.pre_enclosed_search_box()}
            <%
            text.title = probe_name + " Search for Expression Graph"
            text.help = "Enter an ID into the search box below. It will provide suggestions via an autocomplete after two characters."
            text.input_id = "probeSearch"
            text.search_button_id = "viewProbes"
            text.search_action ='#'
            text.search_value = ''
            text.input_class = 'miRNA'
            if c.dataset[c.ds_id]['has_data'] == 'no':
                text.extra_class = 'disabled'
            %>
            ${Base.enclosed_search_box(text,self.show_all_option_null)}
        %endif


      </div>
       <div class="clear"></div>



        <div class="more_info">
            <div class="title">Export / View Sample Summary</div>
            <div class="export">
               <ul class="buttonMenus">
                    <li id="exportMenu">
                        <a class="button dropdown">
                            <span><span class="icon go"></span>Export</span><span class="arrow down"></span>
                        </a>
                        <ul class="submenu">
                            %if c.dataset_status != 'Limited':

                            <li><a href="${h.url('/datasets/download_gct/' + str(c.ds_id))}">Download GCT expression file</a></li>
                            %if 'show_yugene' in c.dataset[ds_id] and c.dataset[ds_id]['show_yugene'] == True:
                            <li><a href="${h.url('/datasets/download_yugene/' + str(c.ds_id))}">Download Yugene expression file</a></li>
                            %endif
                            <li><a href="${h.url('/datasets/download_cls/' + str(c.ds_id))}">Download CLS sample annotation file</a></li>
                            %endif
                            <li><a href="${request.url}&export=true" id="exportTableCSVButton">Export Metadata</a></li>
                            <li><a href="#" id="exportSampleSummaryButton">Export Sample Summary</a></li>
                        </ul>
                    </li>
                </ul>

            </div>
            <div class="clear"></div>
            <div class="breakdown">
                <table id="dataset_sample_summary" class="fixed">
                    <thead>
                        <tr>
                            <th>Sample Grouping</th>
                            <th>Sample Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for grouping, count in c.dataset[ds_id]["breakDown"].iteritems():
                            % if grouping.split(': ')[1] != 'NULL':
                                <tr>
                                    <td>${grouping}</td>
                                    <td>${count}</td>
                                </tr>
                            % endif
                        % endfor
                    </tbody>
                </table>
            </div>

        </div>



    %endif

</div>
