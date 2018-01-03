<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/expressions/show_yugene_filter_dataset_breakdown.js')}"></script>
</%def>
<% data_length = len(c.data) %>
<div id="main_heading" class="title" style="text-align:center;">Dataset breakdown for YuGene ${c.symbol} graph showing "${c.generic_sample_type}" term</div>
</br>
<div class="dataset_results basic_help" style="text-align:center">
    Showing total of ${len(c.data)} Dataset(s) highlighted in YuGene graph.
</div>
</br>
<div class="dataset_results">
    <table id= "yugene_dataset_breakdown_table" >
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Title</th>
                <th>Species</th>
                <th>#Samples with annotation term/ total samples in dataset</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            %for ds_id in c.data:
                <%
                    try:
                        samples = len(c.data[ds_id])
                    except:
                        samples = 0
                %>
                <tr class="dataset">
                  <td>${ds_id}</td>
                  <td>${c.data[ds_id]['handle']}</td>
                  <td>${c.data[ds_id]['Title']}</td>
                  <td>${c.data[ds_id]['species']}</td>
                  <td><a class="toggle_samples" data-id="${ds_id}" href="#!"> ${c.data[ds_id]['sample_count']}/${c.data[ds_id]['number_of_samples']} </a></td>
                  <td class="actions">
                    <ul class="buttonMenus">
                        <li id="exportMenu">
                            <a class="button dropdown"><span>Actions .....</span><span class="arrow down"></span></a>
                            <ul class="submenu">
                            <%
                            url_summary = h.url('/datasets/search?ds_id='+str(ds_id))
                            url_gene_expression_graph = h.url('/expressions/result?graphType=box&datasetID='+str(ds_id)+'&gene='+str(c.ensembl_id)+'&db_id='+str(c.db_id))
                            %>
                               <li><a href="${url_summary}">View Dataset Summary</a></li>
                               <li><a href="${url_gene_expression_graph}">View Gene Expression Graph</a></li>
                           </ul>
                        </li>
                    </ul>
                  </td>
                </tr>
                %if samples != 0:
                    %for chip_id in c.data[ds_id]['chip_id_info']:
                        <%
                        chip_type = c.data[ds_id]['chip_id_info'][chip_id]
                        metadata_values = c.all_sample_metadata[chip_type][chip_id][ds_id]
                        %>
                    <tr class="hidden sample samples_of_${ds_id}">
                        <td>
                        </td>
                        <td colspan=1>
                            Sample Type : ${metadata_values['Generic sample type']}
                        </td>
                        <td colspan=2>
                            Sample ID : ${metadata_values['Replicate Group ID']}
                        </td>
                        <td colspan=1>
                            Disease : ${metadata_values['Disease State']}
                        </td>
                        <td colspan=1>
                          Chip ID : ${chip_id}
                        </td>
                    </tr>
                    <tr>
                    </tr>

                    %endfor
                %endif
        </tbody>
            %endfor
    </table>
</div>
