<%inherit file="/popup.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    
    <link href="${h.url('/css/contents/site_features_details.css')}" type="text/css" rel="stylesheet"> 
</%def>
    
    <div class="leftColumn">	
        
        
        <div class="mainTextColumn">
        
            <h2>Site Features - Line Graph <a id=calculationLink href="${h.url('/${c.site_name}_data_methods.pdf')}">Download data methods doc</a></h2>
            <div class="innerDiv">
                <img src="${h.url('/images/contents/siteFeatures/siteFeature_lineGraph.png')}" />
                <div id="legend">
                    <h3>Legend for Line Graph</h3>
                    <ol>
                        <li>Bread crumb allows you to navigate back to a previous stage.</li>
                        <li>Switch between datasets for the gene you are viewing.</li>
                        <li>Switch between genes for the dataset you are viewing. Auto complete will list matching results when 4 or more characters are entered.</li>
                        <li>Export the graphs data and/or share it with a colleague.</li>
                        <li>Contains options for changing the graph type and other display options.</li>
                        <li>Perform analyses of the graph data.</li>
                        <li>Access UCSC Genome Browser</li>
                        <li>Information on the current gene.</li>
                        <li>This help.</li>
                        <li>Line graphs are grouped by specific anotations provided by ${c.site_name}.</li>
                        <li>The x-axis is labelled based on the anotations provided by ${c.site_name}.</li>
                    </ol>
                </div>
                <div class="clear"></div>
            </div>
            
        </div>
    </div>

    
