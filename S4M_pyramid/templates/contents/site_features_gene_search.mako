<%inherit file="/popup.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    
    <link href="${h.url('/css/contents/site_features_details.css')}" type="text/css" rel="stylesheet"> 
</%def>
    
    <div class="leftColumn">	
        
        
        <div class="mainTextColumn">
            <h2>Site Features - Gene Search</h2>
            <div class="innerDiv">
                <img src="${h.url('/images/contents/siteFeatures/siteFeature_geneSearch.png')}" />
                <div id="legend">
                    <h3>Legend for Gene Search</h3>
                    <ol>

                    <li>Bread crumb allows you to navigate back to a previous stage</li>
                    <li>Auto complete will list matching results when 4 or more characters are entered</li>
                    <li>Auto complete will list two or more gene symbols together, where multiple Entrez genes map to the same Ensembl gene</li>
                    <li>Clicking the search results table headers sorts that table on that column</li>
                    <li>Clicking a check boxes updates the gene information area and graph</li>
                    <li>Clicking the gene symbol in the search results will take you to Gene Summary page</li>
                    <li>Number of samples detected for the gene vs the number of Samples across all data sets. Where the Sample has probe(s) mapping to the gene</li>
                    <li>Multi gene descriptions are shown where multiple Entrez genes map to the same Ensembl gene</li>
                    <li>Clicking "Export Search Data" downloads the gene search results in csv format</li>
                    <li>Clicking "Choose Dataset" will take you to a larger graph. Here you can select alternative data sets to view expression results for this gene</li>
                    <li>Clicking "View Gene Summary" will take you to the summary view for the gene</li>
                    <li>The box plot displays the probe expression values of the selected gene for the default data set</li>
                    <li>Clicking on the graph will take you to a larger graph. Here you can select alternative data sets to view expression results for this gene</li>
                    <li>Identifiers links to external websites for this gene</li>
                        
                    </ol>
                </div>
                <div class="clear"></div>
            </div>
            
        </div>
        <div class="sideColumn">
            
        </div>
        
    </div>

    
