<%inherit file="../default.html"/>\

<%def name="includes()">
   <link type="text/css" href="${h.url('/css/genes/search.css')}" rel="stylesheet" />
</%def>



        <div class="content one_column" >

                <div class="results">
        <div class="generic_orange_button margin_bottom_large "><a href="${h.url('/datasets/download_ds_id_mapping_id_file')}">Download dataset to mapping ids</a></div>
                    <table >
                        <thead>
                            <tr class="headers">
                                <th>Platform</th>
                                <th>Mappings</th>
                            </tr>
                        </thead>
                        <tbody>
                            %for platform in c.results:
                                <tr>
                                    <td>${platform.manufacturer} ${platform.platform} ${platform.version}</td>
                                    <td><a href="/mappings/mapping_${platform.mapping_id}.txt">Download Mappings</a> </td>
                                </tr>
                            %endfor
                        </tbody>
                    </table>
                </div>


            <div class=clear></div>
        </div>

        <div class=clear></div>
    </div>
