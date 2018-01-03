<%inherit file="/popup.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/wb_default.css')}" >
    <script type="text/javascript" src="${h.url('/js/expressions/choose_dataset.js')}"></script>
</%def>

        <div id="wb_background" class="wb_background_divs">
            <div id="wb_background_inner_div">


                <div id="form">
                    <div class="innerDiv">

                        <div class="title">Choose Dataset by clicking a link below</div>

                        <table id="chooseDatasetTable">
                            <thead>
                                <tr>
                                    <th class="th1">Name</th>
                                    <th>Title</th>
                                    <th>Sample/Cell Types</th>
                                    <th>Contact</th>

                                </tr>
                            </thead>
                            <tbody>
                                % for dataset in c.datasets:
                                    % if not c.datasets[dataset].has_key('has_data') or c.datasets[dataset]['has_data'] == 'yes':
                                        <%
                                            organism = c.datasets[dataset]['organism']
                                            datasetID = dataset
                                            name = c.datasets[dataset]['handle']
                                            title = c.datasets[dataset]['title']
                                            cells_samples_assayed = c.datasets[dataset]['cells_samples_assayed']
                                            contact = c.datasets[dataset]['name']
                                            url_link = "&datasetID="
                                        %>
                                        % if organism == c.species or c.species is None:
                                        <tr>
                                                <td><a href="${c.url}${url_link}${datasetID}">${name}</a></td>
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

                    <div class="clear" > </div>
                </div>
            </div>
        </div>
