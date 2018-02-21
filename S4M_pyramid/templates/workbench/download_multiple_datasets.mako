<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/workbench/download_multiple_datasets.js')}"></script>
</%def>

<div class="content">
    <div class="landing_page_analyses" >
        <div class="hidden" id="show_help_flag">NO</div>

        <div class="clear"></div>
        <%def name="show_all_option()"> </%def>
        ${Base.pre_enclosed_search_box()}
        <%
        text.title = "Download Multiple Datasets"
        text.help = "Enter search terms"
        text.input_id = "search"
        text.search_button_id = "search_button"
        text.search_action ='#'
        if c.search is not None:
            text.search_value = c.search
        else:
            text.search_value = ''
        text.input_class='yugene'
        %>
        ${Base.enclosed_search_box(text,self.show_all_option)}

    </div>
    %if c.search is not None and c.search != "":
    <div class="export_buttons">
        <div class="generic_orange_button metadata_dataset_export"><a class="export" href="${h.url('/workbench/download_multiple_datasets?filter=')}${c.search}&export=datasets">Export selected dataset metadata</a></div>
        <div class="generic_orange_button metadata_sample_export margin_bottom_large"><a class="export" href="${h.url('/workbench/download_multiple_datasets?filter=')}${c.search}&export=samples">Export selected sample metadata</a></div>
        <div class="generic_orange_button margin_bottom_large script_to_download"><a class="export" href="${h.url('/workbench/download_multiple_datasets?filter=')}${c.search}&export=download_script">Export download script for selected datasets</a></div>
        <div class="generic_orange_button probe_mappings"><a href="${h.url('/contents/download_mappings')}">Link to probe mappings</a></div>
    </div>
    %endif

    %if c.datasets is not None:
    <div class="dataset_results">
        <table>
            <thead>
                <tr>
                    <th class="toggle_select_all">Click to toggle</th>
                    <th>ID</th>
                    <th>Handle</th>
                    <th>Title</th>
                    <th>Species</th>
                    <th class="samples_header">Samples/Total</th>
                    <th class="actions_header">Actions</th>
                </tr>
            </thead>
            <tbody>
                %for ds_id in c.datasets:
                    <%
                        try:
                            samples = len(c.all_samples_by_ds_id[ds_id])
                        except:
                            samples = 0
                    %>
                    <tr class="dataset">
                        <td><input name="${ds_id}" type="checkbox" checked></input></td>
                        <td>${ds_id}</td>
                        <td>${c.datasets[ds_id]['handle']}</td>
                        <td>${c.datasets[ds_id]['title']}</td>
                        <td>${c.datasets[ds_id]['organism']}</td>
                        %if samples > c.datasets[ds_id]['number_of_samples']:
                          <td><a class="toggle_samples" data-id="${ds_id}" href="#!">${samples}/${samples}</a></td>
                        %else:
                          <td><a class="toggle_samples" data-id="${ds_id}" href="#!">${samples}/${c.datasets[ds_id]['number_of_samples']}</a></td>
                        %endif
                        <td class="actions">
                            <ul class="buttonMenus">
                                <li id="exportMenu">
                                    <a class="button dropdown"><span>Actions .....</span><span class="arrow down"></span></a>
                                    <ul class="submenu">
                                    <%
                                    url_summary = h.url('/datasets/search?ds_id='+str(ds_id))
                                    url_yugene = h.url('/datasets/download_yugene/'+str(ds_id))
                                    url_gct = h.url('/datasets/download_gct/'+str(ds_id))
                                    %>
                                       <li><a href="${url_summary}">View Dataset Summary</a></li>
                                       <li><a class="toggle_samples" href="#" data-id="${ds_id}">Toggle Samples View</a></li>
                                       <li><a href="${url_gct}">Download Normalised</a></li>
                                       <li><a href="${url_yugene}">Download Yugene</a></li>
                                   </ul>
                                </li>
                            </ul>

                        </td>
                    </tr>
                    %if samples != 0:
                        %for sample in c.all_samples_by_ds_id[ds_id]:
                            <%
                            chip_type = sample[1]
                            chip_id = sample[2]
                            try:
                                metadata_values = c.all_sample_metadata[chip_type][chip_id][ds_id]
                            except:
                                metadata_values={"Replicate Group ID":"Error accessing data","Sample Type":"Error accessing data"}
                            %>
                        <tr class="sample hidden samples_of_${ds_id}">
                            <td>
                            </td>
                            <td colspan=2>
                                Chip ID : ${chip_id}
                            </td>
                            <td colspan=2>
                                Sample ID : ${metadata_values['Replicate Group ID']}
                            </td>
                            <td colspan=2>
                                Sample Type : ${metadata_values['Sample Type']}
                            </td>
                        </tr>

                        %endfor
                    %endif


                %endfor
            </tbody>

        </table>
    </div>
    %endif
</div>
