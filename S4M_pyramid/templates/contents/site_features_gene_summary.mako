<%inherit file="/popup.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    
    <link href="${h.url('/css/contents/site_features_details.css')}" type="text/css" rel="stylesheet"> 
</%def>
    
    <div class="leftColumn">	
        
        
        <div class="mainTextColumn">
            <h2>Site Features - Gene Summary</h2>
            <div class="innerDiv">
                <img src="${h.url('/images/contents/siteFeatures/siteFeature_geneSumary.png')}" />
                <div id="legend">
                    <h3>Legend for Gene Summary</h3>
                    <ol>

                        <li>Bread crumb allows you to navigate back to a previous stage.</li>
                        <li>Clicking the dataset name takes you to the graph of this gene for this dataset</li>
                        <li>List of the probes that map to this gene for this dataset and the count of samples with detected probes versus the number of samples in the dataset.</li>
                        <li>"Choose Dataset" will take you to a larger graph. Here you can select alternative data sets to view expression results for this gene.</li>
                        <li>Clicking on the graph will take you to a larger graph. Here you can select alternative data sets to view expression results for this gene.</li>
                        <li>The legend describes the name of the dataset and sample types in the dataset.</li>
                        <li>A list of links to external websites for this gene.</li>
                        <li>"Export Annotation Data" downloads the gene information in csv format.</li>
                        <li>"Export Detected Data" downloads the probes detected tables in csv format.</li>
                        
                        
                        
                    </ol>
                </div>
                <div class="clear"></div>
            </div>
            
        </div>
        <div class="sideColumn">
            
        </div>
        
    </div>

    
