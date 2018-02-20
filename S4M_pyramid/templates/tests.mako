<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/tests.js')}"></script>
</%def>
<style> td:nth-child(2){ text-align: right; } </style>
<%
tests = [
["Graphs", "Large number of samples and probes Novershtern PSG4 ", "/expressions/result?graphType=scatter&datasetID=5003&gene=ENSG00000243137&db_id=56"],
["PG non-microarray", "miRNA  ", "/expressions/feature_result?graphType=default&db_id=46&feature_type=miRNA&feature_id=mmu-mir-205&datasetID=6128"],
["PG non-microarray", "Global Protein ", "/expressions/result?graphType=default&gene=ENSMUSG00000027547&db_id=46&datasetID=6130#"],
["PG non-microarray", "Histone ChIPSeq ", "/expressions/result?graphType=default&datasetID=6151&gene=ENSMUSG00000035206&db_id=46#"],
["PG non-microarray", "DNA Methylation ", "/expressions/result?graphType=default&gene=ENSMUSG00000074637&db_id=46&datasetID=6131"],
["General", "Speed Tests ", "/contents/speed_test"],
["Private datasets", "Logout and then run this ", "/datasets/search?filter=private"],
["Genes", "Partial gene search mincl", "/genes/search?gene=mincl"],
["Genes", "Gene found with search ", "/genes/search?gene=mincl&ensembl_id=ENSG00000166523"],
["Genes", "Adding a Gene list ", "/workbench/gene_set_bulk_import_manager"],
["Genes", "Feature Search - should select a dataset ", "/expressions/feature_result?graphType=default&feature_type=miRNA&feature_id=mmu-mir-148b&db_id=46"],
["Probes", "Multi-mapping probes page ", "/probes/multi_map_summary?probe_id=ILMN_1679060&ds_id=5005&db_id=56"],
["Graphs", "Partial gene entered into Gene Expression Graphs ", "/expressions/result?graphType=box&datasetID=5005&gene=POU&db_id=56&sortBy=Sample%20Type"],
["Genes", "Gene Search not found jjjjj ", "/genes/search?gene=jjjjj"],
["Datasets", "Dataset Search not found jjjj ", "/datasets/search?filter=jjjj"],
["Hamlet", "Hamlet small ", "/hamlet/index?dataset=5032"],
["Graphs", "Multi-mapping probes Oct4 -  Gene Expression Graphs - Hough ", "/expressions/result?graphType=default&gene=ENSG00000204531&db_id=56&datasetID=5005"],
["Graphs", "Line Graphs -  Gene Expression Graphs - Hitchens ", "/expressions/result?graphType=default&datasetID=6124&gene=ENSMUSG00000030142&db_id=46"],
["Projects", "Project Grandiose ", "/project_grandiose"],
["Graphs/Genes", "Gene Search ", "/genes/search?gene=POU5F1"],
["Graphs", "Gene Expression Graphs - with example from RNASeq negative numbers ", "/expressions/result?graphType=box&datasetID=6197&gene=ENSMUSG00000030142&db_id=46"],
["Graphs", "Gene Expression Graphs with values less than 1 - Pera Dataset ", "/expressions/probe_result?graphType=default&datasetID=6081&probe=ACVR2B&db_id=56"],
["Graphs", "Gene Expression Graphs ", "/expressions/result?graphType=default&datasetID=5005&gene=ENSG00000229094&db_id=56"],
["Datasets", "Datasets Select Matigian ", "/datasets/search?filter=2000&ds_id=2000"],
["Graphs", "Probe Expression Graphs ", "/expressions/probe_result?graphType=default&datasetID=5005&probe=ILMN_1912512&db_id=56"],
["Graphs", "Feature Expression Graphs ", "/expressions/feature_result?graphType=default&feature_type=miRNA&feature_id=mmu-mir-27b&db_id=46&datasetID=6128"],
["Graphs", "Multi-Gene Expression Graphs ", "/workbench/histogram_wizard?graphType=default&db_id=56&gene_set_id=779&datasetID=5005"],
["Graphs", "Multiview Graphs ", "/expressions/multi_dataset_result?graphType=scatter&gene=ENSG00000229094&db_id=56"],
["Graphs", "Yugene Graphs ", "/genes/summary?gene=ENSG00000229094&db_id=56"],
["Graphs", "Gene Neighbourhood Choose Probe Graphs", "/workbench/gene_neighbour_wizard?gene=ENSG00000115415&db_id=56&datasetID=5005"],
["Graphs", "Select Probes GEG ", "/expressions/result?graphType=default&datasetID=5005&gene=ENSG00000229094&db_id=56&select_probes=ILMN_1679060"],
["Graphs", "Select Probes MGEG ", "/workbench/histogram_wizard?graphType=default&db_id=56&gene_set_id=779&datasetID=5005&select_probes=ILMN_1711899 ILMN_1740938 ILMN_1694877"],
["Graphs", "Rohart MSC Test", "/workbench/rohart_msc_graph?ds_id=6037"],
["New Graphs", "GEG Expression value none, some samples are null, line graph plots are not connected properly", "/expressions/result?graphType=default&datasetID=6729&gene=ENSG00000115415&db_id=56"],
["New Graphs", "GEG Expression value none/also check bar graph/ largets no. of samples", "/expressions/result?graphType=default&gene=ENSG00000107485&db_id=56&datasetID=6936"],
["New Graphs", "GEG gene with 191 probes, check all the graphs/ legend position", "/expressions/result?graphType=default&gene=ENSG00000155657&db_id=56&datasetID=6385"],
["New Graphs", "GEG horizontal lines in graph should be calculated", "/expressions/result?graphType=default&datasetID=6071&gene=ENSMUSG00000026104&db_id=46"],
["New Graphs", "GEG MD value is not an integer", "/expressions/result?graphType=default&gene=ENSG00000169884&db_id=56&datasetID=6370"],
["New Graphs", "GEG MD/DT both are NULL", "/expressions/result?graphType=default&gene=ENSG00000204287&db_id=56&datasetID=6837"],
["New Graphs", "GEG should be grouped by sample type on page load", "/expressions/result?graphType=default&datasetID=6370&gene=ENSG00000169884&db_id=56"],
["New Graphs", "GEG scatter plots are ordered by sample type", "/expressions/result?graphType=default&gene=ENSG00000204531&db_id=56"],
["New Graphs", "GEG DT < .05", "/expressions/result?graphType=default&datasetID=6309&gene=ENSG00000115415&db_id=56"],
["New Graphs", "GEG colour for box/bar/violin plots should iterate", "/expressions/result?graphType=default&gene=ENSG00000132535&db_id=56&datasetID=6468"],
["New Graphs", "GEG bars in bar graph should be properly placed", "/expressions/result?graphType=default&datasetID=6124&gene=ENSMUSG00000026104&db_id=46"],
["New Graphs", "GEG bars in bar graph should be proper", "/expressions/result?graphType=default&gene=ENSG00000184481&db_id=56&datasetID=5003"],
["New Graphs", "GEG not all probes have valid expression values/ Graph width issue", "/expressions/result?graphType=default&datasetID=6128&gene=ENSMUSG00000061186&db_id=46"],
["New Graphs", "GEG box plots for negative values should be proper x axis for line graph should be proper", "/expressions/result?graphType=box&datasetID=6197&gene=ENSMUSG00000030142&db_id=46"],
["New Graphs", "GEG largest number of sample types/ check all graphs", "/expressions/probe_result?graphType=box&datasetID=6353&probe=A_19_P00321466&db_id=56"],
["New Graphs", "GEG line graph has missing plot/sactter plot at 0 was missing", "/expressions/result?graphType=default&gene=ENSMUSG00000000303&db_id=46&datasetID=6150"],
["New Graphs", "GEG graph box width issue", "/expressions/result?graphType=default&gene=ENSG00000245680&db_id=56&datasetID=5025"],
["New Graphs", "GEG bars in bar graph out of box/line graph is improper, check group by for all options", "/expressions/result?graphType=default&datasetID=6076&gene=ENSG00000115415&db_id=56"],
["New Graphs", "GEG box plot should be hoverable with scatter off", "/expressions/result?graphType=box&datasetID=6128&gene=ENSMUSG00000061186&db_id=46"],
["New Graphs", "GEG box plot should not be on top of each other when grouped by sample type and time", "/expressions/result?graphType=box&datasetID=6152&gene=ENSMUSG00000026104&db_id=46"],
["New Graphs", "GEG missing bar plots", "/expressions/result?graphType=box&gene=ENSG00000181449&db_id=56&datasetID=6145"],
["New Graphs", "y_axis_max value not correct", "/expressions/result?graphType=bar&gene=ENSG00000125378&db_id=56&datasetID=6081"],
["New Graphs", "error being thrown in graph", "/workbench/gene_neighbour_wizard?gene=ENSG00000115415&db_id=56&datasetID=6729"],
["New Graphs", "chipsque scatter plot not working", "/expressions/probe_result?graphType=scatter&datasetID=6135&probe=chr10:111404619-111406650&db_id=46"],
["New Graphs", "multiview should throw error when no data found","/expressions/multi_dataset_result?gene=ENSG00000206454&db_id=56&graphType=box&datasets=6362,6058,6468"],
["New Graphs", "plots lying not 0 axis not present in box plot when compared to www ", "/expressions/probe_result?graphType=box&datasetID=6135&probe=chr10:111404619-111406650&db_id=46"],
["New Graphs", "download image for multi mapped probe in probe graph ", "/expressions/probe_result?graphType=box&datasetID=5003&probe=211245_x_at&db_id=56#"],
["New Graphs", "Long sample type names ", "/expressions/result?graphType=box&gene=ENSG00000116132&db_id=56&datasetID=6253"],
["New Graphs", "Public dataset line graph", "/expressions/result?graphType=line&gene=ENSG00000125398&db_id=56&datasetID=5008"],
["New Graphs", "violin plots", "/expressions/result?graphType=violin&gene=ENSG00000101076&db_id=56&datasetID=6936"],
["Mappings", "Download mapping id #1", "/mappings/mapping_1.txt"]
]

%>
%if c.debug:

<textarea style="width:1000px;height:500px;">
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head profile="http://selenium-ide.openqa.org/profiles/test-case">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<link rel="selenium.base" href="${c.external_base_url}" />
<title>test</title>
</head>
<body>
<table cellpadding="1" cellspacing="1" border="1">
<thead>
<tr><td rowspan="1" colspan="3">test</td></tr>
</thead><tbody>
% for row in tests:
    <%
        type  = row[0]
        test = row[1]
        url = row[2]

    %>
    <tr>
        <td>open</td>
        <td>${url}</td>
        <td></td>
    </tr>
    <tr>
        <td>pause</td>
        <td>2000</td>
        <td></td>
    </tr>
%endfor


</tbody></table>
</body>
</html>
</textarea>

%else:
<div class="content">
    <a href="${h.url('/main/tests?debug=true')}">Get code for Selenium</a>
    <div class="baseMarginLeft base_width_minus_margin">
        <button id="open_all_links">Open All</button>
        <table id="tests">
            <thead>
                <tr>
                    <th class="long">Type</th>
                    <th class="long">Test</th>
                    <th class="short">Click</th>

                </tr>
            </thead>
            <tbody>

            % for row in tests:
            <%
                type  = row[0]
                test = row[1]
                url = row[2]

            %>

            <tr>
                <td>${type}</td>
                <td>${test}</td>
                <td><a href="${url}"> Click here </a></td>
            </tr>

            %endfor

            </tbody>
        </table>


    </div>
</div>

%endif
