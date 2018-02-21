<%inherit file="/popup.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    
    <link href="${h.url('/css/contents/site_features_details.css')}" type="text/css" rel="stylesheet"> 
</%def>
    
    <div class="leftColumn">	
        
        
        <div class="mainTextColumn">
            <h2>Site Features - Dataset Listings</h2>
            <div class="innerDiv">
                <img src="${h.url('/images/contents/siteFeatures/siteFeature_datasetListing.png')}" />
                <div id="legend">
                    <h3>Legend for Dataset Listings</h3>
                    <ol>

                        <li>Clicking the gene name takes you to the gene's expression results graph for this dataset</li>
                        <li>Indicates the number of unique probes identifiers detected in the dataset</li>
                        <li>Clicking a check box updates the dataset information area</li>
                        <li>Clicking the thumbnail of the hierarchical cluster image takes you to the Dataset Summary page</li>
                        <li>Identifiers link to external websites for this dataset.</li>
                        <li>The number of Minimum and Maximum techinal replicates in the dataset</li>
                        <li>"Export Search Data" downloads the dataset search results in csv format.</li>
                        
                        
                    </ol>
                </div>
                <div class="clear"></div>
            </div>
            
        </div>
        <div class="sideColumn">
            
        </div>
        
    </div>

    
