<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">

    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_annotation.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/jquery.treeview.css')}" >
    <script type="text/javascript" src="${h.url('/js/jquery.treeview.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_annotations.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/workbench/share_job_link.js')}"></script>
</%def>


    <div class="hidden" id="base_url" url="${c.url}"></div>
    <div class="hidden" id="url_with_filters" url="${c.url}"></div>
    <div class="hidden" id="url_with_filters_and_order" url="${c.url}"></div>
    <div class="hidden" id="url_filter_gene_set_id" url="${c.url_filter_gene_set_id}"></div>
    <div class="hidden" id="url_filter_id" url="${c.url_filter_id}"></div>
    <div class="hidden" id="url_sp_filter" url="${c.url_sp_filter}"></div>
    <div class="hidden" id="url_tm_filter" url="${c.url_tm_filter}"></div>
    <div class="hidden" id="url_order_by" url="${c.url_order_by}"></div>


    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            ${Base.wb_breadcrumbs()}

            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Gene List Annotation
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>Gene list annotation identifies biological features for the genes within your gene list, including transcript level, protein level and functional information.</p>
                                <br/>
                                <p>The filtered transcript details as well as the unfiltered Kegg Pathway information shown on the left hand side can be exported. The Kegg Pathway export information will not change regardless of the filters selected on this page.</p>
                                <br/>
                                <p>All genes can be seen on the one page by clicking on the 'SHOW ALL ON ONE PAGE' button.  The default is to show 50 genes on each page. There are options at the top and the bottom to navigate to the next page or subsequent pages.</p>
                                <br>
                                <p>The Tm Domain and Signal Peptide filter combinations can be saved. Due to the nature of the Kegg Pathway filtering, you cannot save this as part of your filtering option.</p>
                                <br>
                                <p>Clicking on the Kegg pathway filters on the left narrows down the genes in this list. The filter will be in bold. To remove the filter, simply click the <strong>(X)</strong>. Please note you can choose only one Kegg pathway at a time.</p>
                                <br/>
                                <p>The 'SAVE' button saves all the filtered genes as a new gene list, even if they are only shown in subsequent pages.  Genes can be individually selected for the current page and save them to a gene list.</p>
                                <br>
                                <p><strong>Filtered Genes</strong> is the number of genes found for this filter.</p>
                                <p><strong>Total Transcripts</strong> is the total number of transcripts found for all the genes in this filter.</p>
                                <p><strong>Number of SP</strong> is the total number of transcripts with Signal Peptides for all genes in this filter.</p>
                                <p><strong>Number of TM</strong> is the total number of transcripts with Transmembrane Domains for all genes in this filter.</p>
                                <br/>
                                <p>Clicking on the gene name or the + sign expands the rows to see a list of transcripts for that gene.</p>
                                <p>Clicking on the up and down arrow reorders the table at a gene level.</p>
                                <br/>
                                <p><strong>Transcript</strong> is the number of transcripts for this gene.</p>
                                <p><strong>aa Length</strong> is the protein length of the transcript. The gene level will show N/A. To see the protein lengths of the transcripts, click on the + sign for the appropriate gene.</p>
                                <p><strong>TM</strong> is the number of transcripts for this gene that have a Transmembrane Domain of True.</p>
                                <p><strong>SP</strong> is the number of transcripts for this gene that have a Signal Peptide of True.</p>
                                <br/>

                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>

            <div>

                    <table id="job_titles" class="job_titles">
                        <tbody>
                            <tr>
                                <td>Job#</td>
                                <td>${str(c.job_id) + ' [Shared by '+ c.shared_user.username +']' if c.job_shared else str(c.job_id)}</td>
                            </tr>
                            <tr>
                                <td>Gene List</td>
                                <td>${c.gene_set.gene_set_name}</td>
                            </tr>

                        </tbody>
                    </table>
                    <ul class="buttonMenus">
                        <li id="exportMenu">
                            <a class="button dropdown"><span><span class="icon go"></span>Export &amp; Share</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                                <li><a href="#" id="exportFilteredTxButton">Export Transcripts</a></li>
                                <li><a href="#" id="exportPathwaysButton">Export Pathways</a></li>
                                % if not c.job_shared:
                                    <li><a href="#" id="share_link">Share</a></li>
                                % endif
                                <li><a href="#" id="save_gene_set">Save as Gene List</a></li>
                            </ul>
                        </li>
                        <li id="helpMenu"> <a href="#" class="button help wb_open_help"><span><span class="icon quest"></span>Help</span><span class="arrow right"></span></a> </li>
                    </ul>


            </div>


            <div class="filter_options hidden">

                <select id="select_filter">
                    <option value="">--Select Filter--</option>
                % for filter in c.filter_list:

                    <option value="${filter.id}">${filter.name}</option>

                % endfor
                </select>

                <button id="save_filter">Save Current Filter</button>

                <button id="clear_all_filters">Clear all Filters</button>
            </div>

            <%
                if 'signal_peptide' not in c.filter:
                    all_signal_peptide = True
                    sp = ""
                else:
                    all_signal_peptide = False
                    sp = c.filter['signal_peptide']

                if 'tm_domain' not in c.filter:
                    all_tm_domain = True
                    tm = ""
                else:
                    all_tm_domain = False
                    tm = c.filter['tm_domain']



            %>


            <table id="transcriptTableStatistics">
                <thead>
                    <tr>
                        <th class="sp">Filtered Genes</th>
                        <th class="sp">Total transcripts</th>
                        <th class="sp">Number of SP</th>
                        <th class="sp">Number of TM</th>

                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${c.statistics['count_genes']}</td>
                        <td>${c.statistics['count_transcripts']}</td>
                        <td>${c.statistics['count_sp']}</td>
                        <td>${c.statistics['count_tm']}</td>
                    </tr>
                </tbody>
            </table>




            <ul id="browser" class="filetree">

                <li><span class="folder">TM Domain</span>
                    <ul>

                            % if 'tm_domain' in c.filter and c.filter['tm_domain'] == True:
                                <li>
                                    <span class="file selected">
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&tm=True&sp=${sp}"/>Yes (${c.statistics['count_tm_yes']})</a>
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&tm=&sp=${sp}"/>(x)</a>
                                    </span>

                                </li>
                            % elif 'tm_domain' not in c.filter:
                                <li>
                                    <span class="file">
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&tm=True&sp=${sp}"/>Yes (${c.statistics['count_tm_yes']})</a>
                                    </span>

                                </li>
                            %endif

                            % if 'tm_domain' in c.filter and c.filter['tm_domain'] == False:
                                <li>
                                    <span class="file selected">
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&tm=False&sp=${sp}"/>No (${c.statistics['count_tm_no']})</a>
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&tm=&sp=${sp}"/>(x)</a>
                                    </span>

                                </li>
                            % elif 'tm_domain' not in c.filter:
                                <li>
                                    <span class="file">
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&tm=False&sp=${sp}"/>No (${c.statistics['count_tm_no']})</a>
                                    </span>

                                </li>
                            %endif




                    </ul>
                </li>
                <li><span class="folder">Signal Peptide</span>
                    <ul>



                            % if 'signal_peptide' in c.filter and c.filter['signal_peptide'] == True:
                                <li>
                                    <span class="file selected">
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&sp=True&tm=${tm}"/>Yes (${c.statistics['count_sp_yes']})</a>
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&sp=&tm=${tm}"/>(x)</a>
                                    </span>
                                </li>

                            % elif 'signal_peptide' not in c.filter:
                                <li>
                                    <span class="file">
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&sp=True&tm=${tm}"/>Yes (${c.statistics['count_sp_yes']})</a>
                                    </span>
                                </li>

                            %endif



                            % if 'signal_peptide' in c.filter and c.filter['signal_peptide'] == False:
                                <li>
                                    <span class="file selected">
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&sp=False&tm=${tm}"/>No (${c.statistics['count_sp_no']})</a>
                                        <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&sp=&tm=${tm}"/>(x)</a>
                                    </span>
                                </li>
                            % elif 'signal_peptide' not in c.filter:
                                <li>
                                    <span class="file">
                                            <a href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}&sp=False&tm=${tm}"/>No (${c.statistics['count_sp_no']})</a>
                                    </span>
                                </li>
                            %endif










                    </ul>
                </li>

                % for gene_set_type in c.gene_set_details:
                    <li><span class="folder">${gene_set_type} Pathway (${len(c.gene_set_details[gene_set_type])})</span>

                    <%

                    sortBy = c.gene_set_details[gene_set_type]

                    sortBy.sort()
                    %>


                    % for gene_set in sortBy:
                        <%

                            name = gene_set[1].gene_set_name
                            type = gene_set[1].gene_set_type
                            description = gene_set[1].description
                            gene_set_id = gene_set[1].id

                            genes_found = c.pathway_statistics[str(gene_set_id)]['genes_found_in_pathway']


                            pvalue = float(c.pathway_statistics[str(gene_set_id)]['fisher_exact_pvalue'])

                            pvalue = "%.2E" % pvalue

                        %>

                        <ul>
                            <li>
                                % if c.filter_gene_set_name == name:
                                    <span class="file selected">
                                    <a href="${c.url}${c.url_pagination}&filter_gene_set_id=${gene_set_id}">${name.replace('KEGG_','')}<br/>[${genes_found} gene(s) - p value:${pvalue}]</a>
                                    <a href="${c.url}${c.url_pagination}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}"><span id="cancel">(X)</span></a>
                                % else:
                                    <span class="file">
                                    <a href="${c.url}${c.url_pagination}&filter_gene_set_id=${gene_set_id}">${name.replace('KEGG_','')}<br/>[${genes_found} gene(s) - p value:${pvalue}]</a>
                                %endif


                                </span>
                            </li>
                        </ul>


                    % endfor

                    </li>
                % endfor




            </ul>

            <table id="transcriptTable">
                <thead>
                    <tr>
                        <th class="select" id="select_all">Select</th>
                        <th class="short">Gene

                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=gene_name&descending=False">Λ</a>
                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=gene_name&descending=True">V</a>
                        </th>
                        <th class="long">Transcript

                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=count_tx&descending=False">Λ</a>
                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=count_tx&descending=True">V</a>
                        </th>
                        <th class="short">aa Length</th>
                        <th class="short">TM
                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=count_tm&descending=False">Λ</a>
                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=count_tm&descending=True">V</a>
                        </th>
                        <th class="short">SP
                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=count_sp&descending=False">Λ</a>
                            <a class="sort" href="${c.url}${c.url_pagination}${c.url_filter_gene_set_id}${c.url_filter_id}${c.url_sp_filter}${c.url_tm_filter}&order_by=count_sp&descending=True">V</a>
                        </th>

                    </tr>
                </thead>
                <tbody>
                    <% count = 0; %>
                    % for gene in c.genes:



                            <%
                            tm_domain = gene[1]['count_tm']
                            count_tx = gene[1]['count_tx']
                            sp = gene[1]['count_sp']
                            gene_name = gene[1]['gene_name']
                            gene_id = gene[1]['gene_id']

                            tx_details = c.tx_list[gene_id]
                            tx_details.sort()

                            %>

                            <tr>
                                <td><input type="checkbox" name="${gene_id}" id="${gene_name}"></a></td>
                                <td class="show"><img class="help" src="${h.url('/images/workbench/plus.png')}">${gene_name}<div class="gene_id hidden">${gene_id}</div></td>
                                <td>${count_tx}</td>
                                <td>N/A</td>
                                <td>${tm_domain}</td>
                                <td>${sp}</td>

                            </tr>

                            % for tx in tx_details:

                                <%
                                  tx_name = tx[1]['transcript_name']
                                  tm = tx[1]['tm_domain']
                                  sp = tx[1]['signal_peptide']
                                  protein_length = tx[1]['protein_length']
                                %>

                                <tr class="tx_${gene_id} transcripts hidden">
                                    <td></td>
                                    <td>${gene_name}</td>
                                    <td>${tx_name}</td>
                                    <td>${protein_length}</td>
                                    <td>${tm}</td>
                                    <td>${sp}</td>


                                </tr>


                            % endfor

                    % endfor


                </tbody>
            </table>

            <div class="clear"></div>


            % if c.paginate_on == True:
                ${h.print_paginate(c.paginate)}
                <a class="basic_link small_margin_top" href="#" id="removePagination">Show All One Page</a>
            % else:
                <a class = "basic_link small_margin_top" href="#" id="addPagination">Show All Pages</a>
            %endif

            <div class="clear"></div>

        </div>
    </div>


    <div id="save_filter_form" class="modal">

        <div class="wb_modal_title">
            Save Filter Name
        </div>
        <form id="form_save_filter" method="post">
            <label>New Filter Name:</label><input id="filter_name" name="filter_name" type="text" value="" />
            <br />
            <button id="submit_save_filter">Submit</button>

        </form>

    </div>



