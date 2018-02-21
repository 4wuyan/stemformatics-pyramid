<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    <link href="${h.url('/css/contents/index.css')}" type="text/css" rel="stylesheet"> 
    <link href="${h.url('/css/contents/biologists.css')}" type="text/css" rel="stylesheet"> 
    <link href="${h.url('/css/contents/biology_article.css')}" type="text/css" rel="stylesheet"> 
</%def>
	
    <!-- links on the leftColumn -->
    ${Base.links()}  

    <div class="rightColumn">
        <div class="mainTextColumn">
            <div class="articleTitle">
                <span>PLURIPOTENT STEM CELLS</span>
            </div>
            <div class="date">13 May 2011</div>
            <div class="mainText">
                    <p>
                    Most cells in our body share the same genetic blueprint in the form of chromosomal DNA, but the information flow from DNA to cell function is contextual, and accessed according to the developmental state of that cell. Lineage commitment probably involves restricting the genetic information accessible to the cell, a process once thought to be irreversible. Induced pluripotent stem cells are 'reprogrammed' such that mature cells regain access to the genetic information required to generate different cell fates.
                    </p>
                    <p>
                    <div class="articleImageCaption">
                        <img class="small" src="${h.url('/images/contents/forBiologists/stemcell_hips.jpg')}" />
                        <div class="caption">
                            <div class="captionText">
                                A colony of human induced pluripotent stem cells. <em>(Courtesy: Sam Nayler &copy;)</em>
                            </div>
                        </div>
                    </div>
                    
                   The process of reprogramming is poorly understood, as most studies have focussed on relatively few exemplar lines. Even less well understood is the level of variation between cell lines, and how this might impact on their capacity to form different tissue types.  Christoph Bock and colleagues have systematically surveyed 12 human induced pluripotent cell lines (iPS) against 20 different human embryonic stem cell lines, measuring gene expression, chromatin state and differentiation potential of each cell line. The resulting 'scorecard' allows researchers to benchmark these cells against their potential to contribute to the three embryonic germlayers (mesoderm, ectoderm and endoderm); and derive part or all of the range of differentiated cell types required for normal human development.
                   </p>
                   <p>
                   Equally important, this study provides a first glimpse into the range of normal variation in gene expression in cells that share phenotypic characteristics, providing an important dataset for understanding the stem cell state as well as lineage commitment.
                   </p>
                    
            </div>
            <div class="biologistInfo">
                <h2>References</h2>
                <div class="ruler"></div>
                <p>
                Bock C, Kiskinis E, Verstappen G, Gu H, Boulting G, et al. (2011) "Reference Maps of Human ES and iPS Cell Variation Enable High-Throughput Characterization of Pluripotent Cell Lines." Cell 144: 439-452.
                </p>
            </div>

        </div>
        <div class="sideColumn">
            ${Base.sideColumnBiologists()}  
            
        </div>
    </div>

