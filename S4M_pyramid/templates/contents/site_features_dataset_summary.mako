<%inherit file="/popup.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    
    <link href="${h.url('/css/contents/site_features_details.css')}" type="text/css" rel="stylesheet"> 
</%def>
    
    <div class="leftColumn">	
        
        
        <div class="mainTextColumn">
            <h2>Site Features - Dataset Summary</h2>
            <div class="innerDiv">
                <img src="${h.url('/images/contents/siteFeatures/siteFeature_datasetSummary.png')}" />
                <div id="legend">
                    <h3>Legend for Dataset Summary</h3>
                    <ol>

                        <li>Bread crumb allows you to navigate back to a previous stage.</li>
                        <li>Identifiers link to external websites for this dataset.</li>
                        <li>This thumb nail takes you to the full size principal component analysis image.</li>
                        <li>This thumb nail takes you to the full size hierarchical cluster image.</li>
                        <li>Lists the most highly differentially expressed genes as described by the publication. </li>
                        <li>Clicking the gene name takes you to the gene's expression results graph for this dataset.</li>
                        <li>The Sample Grouping table shows the number of samples in each sub-category.</li>
                        <li>Clicking the Sample Grouping table headers sorts that table on that column.</li>
                        <li>"Export Summary Data" downloads the summary data for the data set area in csv format.</li>
                        <li>"Export Gene Expressed Data" downloads the highly differentially expressed genes table in csv format.</li>
                        <li>"Export Sample Grouping Data" downloads the Sample Grouping table in csv format.</li>
                        
                     
                        
                        
                    </ol>
                </div>
                <div class="clear"></div>
            </div>
            
        </div>
        <div class="sideColumn">
            
        </div>
        
    </div>

    
