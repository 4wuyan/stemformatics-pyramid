<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/admin/annotate_dataset.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/jquery.handsontable.css')}" >
    <script type="text/javascript" src="${h.url('/js/jquery.handsontable.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/admin/annotate_dataset.js')}"></script>
    <script type="text/javascript" src="${h.url('/js/keymaster.js')}"></script>
</%def>



    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">



            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Annotate Dataset #${c.ds_id} ${c.handle}
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                Please click on the steps on the Control Bar for more details. Once selected, you can click on the help icon at the top right for help when hovering over elements. To copy the annotations from one instance to another, please use JSON Export. Then you can use JSON Import to import the data you copied from the previous instance.
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>
<a name="home"/></a>
<div id="annotate_biosamples_metadata_div" class="datasets form">

    <div id="ds_id" class="hidden" >${c.ds_id}</div>
    <div id="db_id" class="hidden" >${c.db_id}</div>
    <div id="chip_type" class="hidden" >${c.chip_type}</div>
    <div id="chip_ids" class="hidden" >${c.chip_ids}</div>
    <div id="json_headers" class="hidden" >${c.json_headers}</div>
    <div id="json_metastore" class="hidden" >${c.json_ds_md}</div>
    <div id="json_biosamples_metadata" class="hidden" >${c.json_bs_md}</div>
    <div class="title hidden" id="old_samples_header">Samples Metadata <img class="expand" src="/images/workbench/plus.png" ></div>
    <div id="sample_help" class="content hidden toggleable sample_metadata">
        <table>
            <thead>
                <tr>
                    <th>Steps to Annotate the Samples Metadata</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <ul>
                            <li>Start with the Sample Type, which is the default grouping for ${c.site_name}.</li>
                            <li>You can get in-page help for this page at the top right help icon (that changes colour). Hover over the icon and click "Toggle in-page help".  You will be able to hover over the Samples Metadata table column headers and get information on how to fill out the column.</li>
                            <li>You can click on the columns and they will be ordered alphabetically.</li>
                            <li>You can also CTRL+V and CTRL+C and select multiple rows just like Excel.</li>
                            <li>If you want to start again, simply refresh the page.</li>
                            <li>After editing and saving the inital columns, you can then check the rest of the columns by selecting "Select columns individually" to see the ones that are unticked and see if they would be useful for this dataset. By ticking the labels they will be added as columns in the table for editing.</li>
                            <li>You can also select "Select columns by Group" button to see if there are any groups you belong to that have important columns you need to fill out. It works the same way and will add extra columns in the table for editing.</li>
                            <li>If you want to save, simply click on Save in the Control Bar in the top right. A message will appear below with details of the save.</li>
                            <li>Once you have saved, you can go onto step #2 - Sample Type ordering. Simply click on the link in the Control Bar.</li>
                        </ul>
                    </td>
                </tr>
        </table>
    </div>

    <div id="button_select_columns_individually" class="dataset_summary_button sample_metadata hidden toggleable"><a href="#">Select columns individually</a></div>
    <div id="button_select_columns_by_group" class="dataset_summary_button margin_left_small hidden sample_metadata toggleable margin_bottom_small "><a href="#">Select columns by Group</a></div>


    <div id="biosamples_metadata_grid" class="clear dataTable toggleable sample_metadata">
        <div id="json_columns_default" class="hidden">${c.columns_default_json}</div>
    </div>



    <div class="title hidden toggleable" id="old_dataset_header">Dataset Metadata <img class="expand" src="/images/workbench/plus.png" ></div>
    <div id="metastore_div" class="content toggleable">
        <table>
            <thead>
                <tr>
                    <th>Steps to Annotate the Dataset metadata</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <ul>
                            <li>Make sure you have already saved what you have changed.</li>
                            <li>No need to change the handle in most cases.</li>
                            <li>Publication Title is the actual title of the publication. Title is the specific title of this dataset. Normally they are identical. They can be made different if there are multiple datasets for the one Publication.</li>
                            <li>First Authors is the list of first authors that you would use in a citation, without the et al. eg. Wells CA (for the citation for Stemformatics Wells CA et al Stemformatics: Visualisation and sharing of stem cell gene expression. Stem Cell Research, DOI http://dx.doi.org/10.1016/j.scr.2012.12.003)
                            <li>Publication Citation is the citation of the actual publication. eg. Stem Cell Research, DOI http://dx.doi.org/10.1016/j.scr.2012.12.003</li>
                            <li>Show All will show all the hidden metadata - usually this is not needed</li>
                            <li>Order the columns alphabetically by clicking on Type.</li>
                            <li>AE Accession is the Array Express Accession ID. Leave blank if unavailable.</li>
                            <li>Affiliation is the University and/or Institute</li>
                            <li>Contact Email and Contact Name is usually the corresponding author or the main person to discuss the data with</li>
                            <li>Description is really the abstract.</li>
                            <li>To get this dataset onto the "Our Publications" Page, you need to set "showAsPublication" to be True. Then you need to update "Publication Date" using YYYY-MM to keep the publications in order. Finally, you need to ensure all the Publication fields are set, including Authors,Description, Publication Title and Publication Citation.</li>
                            <li>cellsSamplesAssayed is a human-readable, short list of cell and sample types of interest in the study.  This field is used in the Dataset Browser table within ${c.site_name} web site and gives a summary view of the cell and sample types in the study. eg. human olfactory neurosphere (hONS),fibroblast </li>
                            <li>If you want to troubleshoot a problem, simply click on Troubleshoot in the Control Bar on the top right. A message will appear below with details of the test.</li>
                            <li>If you want to save, simply click on Save in the Control Bar on the top right. A message will appear below with details of the save.</li>
                            <li>If you want to see your changes in the front end, simply click on "Set Front End" in the Control Bar on the top right. A message will appear below with details of setting the front end.</li>
                            <li>Next, go to the Genes of Interest step in the Control Bar</li>
                        </ul>

                    </td>
                </tr>
        </table>

        <input id="handle" type="text" value="${c.handle}" style="width:400px;">
        <input id="update_handle" type="button" value="Update Handle"/>
        <div class="clear"></div>
        <input id="show_all" type="button" value="Show All"/>
        <div id="metastore_grid" class="dataTable">
        </div>
    </div>
    <div class="hidden content toggleable" id="genes_info">
        <table>
            <thead>
                <tr>
                    <th>Steps to Annotate the Dataset metadata</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <ul>
                            <li>Make sure you have already saved what you have changed.</li>
                            <li>Genes of Interest are a comma separated list of interesting Ensembl gene ids from the paper that allow users to easily click and view the gene in a graph for this dataset. The expected number of genes in this list is 5, but you can have more or less.</li>
                            <li>First, enter in the ensembl gene id or symbols (eg. mincle or oct4) into the text area below and then click on submit</li>
                            <li>Then you will see a list of genes that have been returned. Select the genes you want to be a part of this list and then click on the submit button below the table. This will save it to the database.</li>
                            <li>Next, go to the testing step in the Control Bar</li>
                        </ul>

                    </td>
                </tr>
        </table>


        <textarea></textarea>
        <input type="submit"></submit>
        <div class="display" id="view_genes_found">
        </div>
    </div>


    <div class="hidden content toggleable" id="test_info">

        <table>
            <thead>
                <tr>
                    <th>Testing the Annotations</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <ul>
                            <li>Check dataset details are correct including Export/View Sample Summary: <a class="large_link" target=_blank href="${h.url('/datasets/summary?datasetID=')}${c.ds_id}">Dataset Summary</a></li>
                            <li>Check Gene Graph: <a class="large_link" target=_blank href="">Gapdh Graph</a></li>
                            <li>Check Hierarchical Cluster: <a class="large_link" target=_blank href="">Hierarchical Cluster Wizard</a></li>
                            <li>Send ${c.feedback_email} an email to let us know that you are happy with the dataset. ${c.site_name} will then check it for details and if it is a public dataset will make it publically available.</li>
                        </ul>

                      </td>
                </tr>
        </table>


    </div>



    <div id="controls" class="content normal_top_margin normal_bottom_margin">
        <div>
          <img id="toogle_controls_expand_image" class="toggle_controls_expand" src="/images/workbench/minus.png" alt="" />
          <h1 id="main_control_bar_heading">Control Bar (Click and drag to move)</h1>
        </div>
      </br>
        <table id="steps" >
            <tr>
                <th>Step Name</th><th>Open</th>
            </tr>
            <tr>
                <td>#1 - Samples metadata</td><td><a href="#" id="samples_header">Click here</a></td>
            </tr>
            <tr>
                <td>#2 - Sample Type Order</td><td><a href="#" id="sample_type_ordering" class="sample_type_ui">Click here</a></td>
            </tr>
            <tr>
                <td>#3 - Dataset metadata</td><td><a href="#" id="dataset_header">Click here</a></td>
            </tr>
            <tr>
                <td>#4 - Genes of Interest</td><td><a href="#" id="genes_header">Click here</a></td>
            </tr>
            <tr>
                <td>#5 - Test Dataset summary<br/>Check text, gene select, links etc.</td><td><a target="_blank" href="${h.url('/datasets/summary?datasetID=')}${c.ds_id}">Click here</a></td>

            </tr>
            <tr>
                <td>#6 - Test Gene Graph<br/>Use any gene to display graph. eg. Gapdh <br/>Some genes may be unavailable.</td><td><a target="_blank" href="${h.url('/expressions/result?graphType=default&db_id='+str(c.db_id)+'&gene=gapdh&datasetID=')}${c.ds_id}">Click here</a></td>
            </tr>
            <tr>
                <td>#7 - Test Hierarchical Cluster<br/>Check job runs correctly.</td><td><a target="_blank" href="${h.url('/workbench/hierarchical_cluster_wizard')}">Click here</a></td>
            </tr>
            <tr>
                <td colspan=2>#8 - Email us at ${c.feedback_email}</td>
            </tr>
        </table>
        <table id="other">
            <tr>
                <th>Other Info</th>
            </tr>
            <tr>
                <td>Accession IDs: ${h.setup_accession_ids_for_viewing(c.ds_md)}</td>
            </tr>
            %if 'pub_med_id' in c.ds_md:
            <tr>
                <td><a target="_blank" href="http://www.ncbi.nlm.nih.gov/pubmed/${c.ds_md['pub_med_id']}" >Pubmed Link</a></td>
            </tr>
            %endif
            <tr>
                <td><a target="_blank" href="${config['agile_org_base_url']}datasets/view/${c.ds_id}" >Agile_org dataset Link</a></td>
            </tr>
            <tr>
                <td><a target="_blank" href="${config['qcplots_base_url']}${c.ds_id}/source/normalized/qc_plots.PDF" >Agile_org QC Plot Link</a></td>
            </tr>
            %if c.role in ('admin','annotator'):
                <tr>
                    <td><a target="_blank" href="${h.url('/admin/add_msc_project?ds_id=')}${c.ds_id}" >Add MSC Signature Metadata</a></td>
                </tr>
                <tr>
                    <td><a target="_blank" href="${h.url('/msc_signature/index')}" >MSC Signature Statistics</a></td>
                </tr>
            %endif
            %if c.role == 'admin':
                <tr>
                    <td><a target="_blank" href="${h.url('/admin/add_project_banner?ds_id=')}${c.ds_id}" >Add Project Banner Metadata</a></td>
                </tr>
                <tr>
                    <td><a target="_blank" href="${h.url('/admin/update_datasets?ds_id=')}${c.ds_id}" >Update Dataset</a></td>
                </tr>
                <tr>
                    <td><a target="_blank" href="${h.url('/admin/add_line_graph?ds_id=')}${c.ds_id}" >Add Line Graph Metadata</a></td>
                </tr>
                <tr>
                    <td><a target="_blank" href="${h.url('/admin/change_user_to_annotator_for_dataset')}" >Add Annotator for a dataset</a></td>
                </tr>
            %endif
        </table>
        <div class="clear"></div>
        <div id="other_buttons">
          <button id="clear" class="big ">Clear Messages</button>
          <button class="big send">Troubleshoot</button>
          <button class="big send">Save</button>
          <button class="big send">Set Front End</button>
          <button class= "big " id='create_json'>JSON Export</button>
          <button class= "big " id='save_json'>JSON Import</button>
          <button class= "big margin_top_small" id='export_biosamples'>Export Samples</button>
          <div id="ajax_message"></div>
          <div class="clear"></div>
        </div>
    </div>
</div>

<div id="div_select_columns_individually" class="hidden">
    <form class="" id="choose_columns">
        <div class="title margin_bottom_small">Select columns individually</div>
        %for header in c.headers:
            <% count = c.headers.index(header) + 1  %>
            % if count > 3:

                % if header in c.columns_default:
                    <% checked = "checked" %>
                % else:
                    <% checked = "" %>

                % endif
                <div class="select_column"><div>${header}</div><input type="checkbox"  name="${header}" data-order="${count}" ${checked}></input> </div>

            %endif
        %endfor
    </form>
    <div class="clear"></div>
</div>

<div id="div_select_columns_by_group" class="hidden">

    <form class="" id="choose_groups">
        <div class="title margin_bottom_small">Select columns by Group</div>
        <div class="margin_bottom_large">Select the groups that you want to use for this dataset. The annotation columns are in parentheses.</div>
        %if len(c.group_configs) > 0:
            %for row in c.group_configs:
                <% config_value = row['config_value'] %>
                <% group_name = c.list_of_groups[row['gid']] %>
                <%
                    try:
                        c.gid = int(c.gid)
                    except:
                        c.gid = None
                %>
                % if c.gid is not None and row['gid'] == c.gid :
                    <% checked = "checked" %>
                % else:
                    <% checked = "" %>

                % endif

                <div class="select_group"><div>${group_name} (${config_value})</div><input type="checkbox" name="${group_name}" data-gid="${row['gid']}" data-value="${config_value}" ${checked}></input> </div>
            %endfor
        %else:
            <div class="">You are not in any groups that need specific annotations.</div>
        %endif
        <div class="clear"></div>
    </form>
</div>
