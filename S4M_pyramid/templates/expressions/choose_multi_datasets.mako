<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/choose_dataset.css')}" >
    <link rel="stylesheet" type="text/css" href="${h.url('/css/expressions/choose_multi_datasets.css')}" >
    <script type="text/javascript" src="${h.url('/js/expressions/choose_multi_datasets.js')}"></script>
</%def>



<div id="wb_background" class="wb_background_divs">
    <div id="wb_background_inner_div">

        ${Base.wb_breadcrumbs()}
        <div id="data" class="hidden">
            <a id=base_url class="hidden" href="${c.base_url}"></a>
            <div id=loaded_datasets class="hidden">${c.loaded_datasets}</div>
        </div>
        <div class="wb_question_groups_selected">

            <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                ${c.purple_title}
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                ${c.help_text}
                            </div>
                        </div>



                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <div id="chosenDatasets">

                <input type="submit" class="save" id="save1" value="Save"/>
                <table id="chosenDatasetTable">
                    <thead>
                        <tr>
                            <th class="select">Delete</th>
                            <th class="name">Name</th>
                            <th class="title">Title</th>
                            <th class="sample_types">Sample/Cell Types</th>
                            <th class="contact">Contact</th>

                        </tr>
                    </thead>
                    <tbody>
                        <tr id="table_chosen_none_row"><td colspan=5>None</td></tr>
                    </tbody>
                </table>

                <input type="submit" class="save" id="save2" value="Save"/>
            </div>
            <div id="chooseMultiDataset">
                <table id="chooseDatasetTable">
                    <thead>
                        <tr>
                            <th class="select">Select</th>
                            <th class="name">Name</th>
                            <th class="title">Title</th>
                            <th class="sample_types">Sample/Cell Types</th>
                            <th class="contact">Contact</th>

                        </tr>
                    </thead>
                    <tbody>
                        % for dataset in c.all_datasets:
                            % if not c.all_datasets[dataset].has_key('has_data') or c.all_datasets[dataset]['has_data'] == 'yes':
                                <%
                                    organism = c.all_datasets[dataset]['organism']
                                    datasetID = dataset
                                    name = c.all_datasets[dataset]['handle']
                                    title = c.all_datasets[dataset]['title']
                                    cells_samples_assayed = c.all_datasets[dataset]['cells_samples_assayed']
                                    contact = c.all_datasets[dataset]['name']
                                %>

                                % if organism == c.species or c.species is None:
                                <tr>
                                        <td><input id="${datasetID}" name="${datasetID}" type="checkbox"/></td>
                                        <td>${name}</td>
                                        <td>${title}</td>
                                        <td>${cells_samples_assayed}</td>
                                        <td>${contact}</td>


                                </tr>
                                % endif
                            % endif
                        % endfor

                    </tbody>
                </table>

                <div class="clear" > </div>
            </div>
            <input type="submit" class="save" id="save3" value="Save"/>
        </div>

        <div class="clear" > </div>

    </div>
</div>
