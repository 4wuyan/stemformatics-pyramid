<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/genes/feature_search.js')}"></script>
   <link type="text/css" href="${h.url('/css/genes/search.css')}" rel="stylesheet" />
</%def>
<%def name="show_all_option()"></%def>

<div class="feature_search">



        ${Base.pre_enclosed_search_box()}
        <%
        text.title = "Search Feature in "+c.site_name
        text.help = "Enter miRBase identifier (mmu-miR-147) and any other miRBase identifier. You can even search on the sequence. Autocomplete is after 4 letters and both the autocomplete and the search result are limited to 100 rows."
        text.input_class = ""
        text.input_id = "featureSearch"
        text.search_button_id = "viewGenes"
        text.search_action = h.url('/genes/feature_search')
        text.search_value = c.feature_search_term if c.feature_search_term else ''
        %>
        ${Base.enclosed_search_box(text,self.show_all_option)}


        <div id="error_message" class="error_message hidden">${c.extra_message}</div>
        <div id="geneSearchDiv" class="searchDiv">


            <div class=clear></div>

            <div id="displayFeatureResults" class="">
                %if c.data != None:
                    <table id="searchFeatures" >
                        <thead>
                            <tr>
                                <th>Species</th><th>Type</th>
                                <th>Symbol</th><th>Accession ID</th>
                                <th>Aliases</th>
                                <th>Description</th>
                                <th style="width:120px;">Actions</th>
                                <!-- <th>Sequence</th> -->
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                % for feature in c.data:
                                    <tr>
                                        <%
                                            description = feature['description']
                                            feature_type = feature['feature_type']
                                            symbol = feature['symbol']
                                            feature_id = feature['feature_id']
                                            species = feature['species']
                                            aliases = feature['aliases']
                                            sequence = feature['sequence']
                                            if species == "Homo sapiens":
                                                db_id = "56"
                                            else:
                                                db_id = "46"
                                        %>
                                        <td>${species}</td><td>${feature_type}</td>
                                        <td>${symbol}</td><td>${feature_id}</td>
                                        <td>${aliases}</td>
                                        <!--<td><a href="">${symbol}</a></td> -->
                                        <td>${description}</td>
                                        <td>
                                            <ul class="buttonMenus">
                                                <li id="exportMenu">
                                                    <a class="button dropdown"><span>Actions</span><span class="arrow down"></span></a>
                                                    <ul class="submenu">
                                                        <li><a href="${h.url('/expressions/feature_result?graphType=default&feature_type='+feature_type+'&feature_id='+feature_id+'&db_id='+db_id)}" >View Expression Graph</a></li>
                                                        <li><a target="_blank" href="http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=${feature_id}" >miRBase Link</a></li>
                                                    </ul>
                                                </li>
                                            </ul>

                                       </td>
                                        <!--<td>${sequence}</td>-->
                                    </tr>
                                %endfor
                            </tr>
                        </tbody>
                    </table>
                %endif
            </div>

           <div class=clear></div>

        </div>
        <div class=clear></div>
</div>

