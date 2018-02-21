<%inherit file="/popup.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    
    <link href="${h.url('/css/contents/site_features_details.css')}" type="text/css" rel="stylesheet"> 
</%def>
    
    <div class="leftColumn">	
        
        
        <div class="mainTextColumn">
            <h2>Site Features - Boxplot Graph <a id=calculationLink href="${h.url('/${c.site_name}_data_methods.pdf')}">Download data methods doc</a></h2>
            
            <div class=clear> </div>
            
            <div class="innerDiv">
                <img src="${h.url('/images/contents/siteFeatures/siteFeature_boxPlot.png')}" />
                <div id="legend">
                    <h3>Legend for Boxplot Graph</h3>
                    <ol>
                        <li>Bread crumb allows you to navigate back to a previous stage</li>
                        <li>Change the graph type being displayed to a scatter plot, bar graph or box plot Note that there is no ability to turn off standard deviation for this graph type</li>
                        <li>Group samples by metadata categories (dataset specific)</li>
                        <li>Switch between datasets for the gene you are viewing</li>
                        <li>Switch between genes for the dataset you are viewing. Auto complete will list matching results when 4 or more characters are entered</li>
                        <li>Expand graph on x axis</li>
                        <li>Rescale y axis toggles between fixed scale and automatic scale</li>
                        <li>Toggle between showing and hiding the legend</li>
                        <li>Get this help page</li>
                        <li>Maximum expression value </li>
                        <li>Minimum expression value </li>
                        <li>Median expression value - hover over to show the label</li>
                        <li>3rd quartile </li>
                        <li>1st quartile </li>
                        <li>Detection threshold for the dataset</li>
                        <li>Median data set expression for the dataset</li>
                        <li>Labels for the data's metadata categories</li>
                        <li>"Export Graph Data" downloads the specific data used in the graphing in csv format</li>
                        <li>"Export Base Data" downloads the original data used to calculate the graphing data  in csv format</li>
                        <li>"Show/Hide Graph Data" Toggles between showing and hiding data used in the graph. An Expand button will be shown which increases the font size of the data shown</li>
                        <li>Red probe with underline and * denotes a probe that maps to multiple genes</li>
                        
                    </ol>
                </div>
                <div class="clear"></div>
            </div>
            
        </div>
        <div class="sideColumn">
            
        </div>
        
    </div>

    
