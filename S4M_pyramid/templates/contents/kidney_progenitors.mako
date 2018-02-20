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
                <span>FROM STEM CELLS TO KIDNEY PROGENITORS</span>
            </div>
            <div class="date">13 May 2011</div>
            <div class="mainText">
                    <p>
                    Understanding kidney development is the first vital step towards improving outcomes for individuals with kidney disease. One approach taken by the laboratories of Melissa Little (UQ) and Andrew Laslett (CSIRO) is to identify and isolate cells capable of forming renal tissues from cultures of human embryonic stem cells which are differentiated in the presence of renal growth factors.
                    </p>
                    <p>
                    <div class="articleImageCaption">
                        <img class="small" src="${h.url('/images/contents/forBiologists/kidney_new.jpg')}" />
                        <div class="caption">
                            <div class="captionText">
                                Turning stem cells into kidney progenitors; a possible stem cell therapy for kidney repair.<br />
                            </div>
                            <div class="captionText"><em>(Image: Confocal analysis of a developing kidney highlighting the nephron progenitor and ureteric compartments. Courtesy: Alexander Combes and Adler Ju, Institute for Molecular Bioscience, The University of Queensland &copy;)</em>
                            </div>
                        </div>
                    </div>
                    
                   The kidney is a complex tissue made up of more than 26 specialised cell types. Many of these come from a developmental lineage known as mesoderm. In this study, Lin and colleagues grew embryonic stem cells (HES) under conditions known to give rise to mesoderm, and then sorted these based on cell-surface expression of proteins (Podocalyxin, CD24) thought to be important in kidney mesoderm. They also looked for the absence of the pluripotency marker GCTM-2, because its presence indicates poor commitment to kidney mesoderm.
                   </p>
                   <p>
                   They compared the gene expression of 4 different conditions: the original HES4; HES cultured under mesodermal conditions (HES/MD_low serum) ;  mesoderm-conditioned cells poorly committed (HES/MD_low serum PODXL+CD24+GCTM+); and mesoderm-conditioned cells enriched for renal progenitors, which were sorted for Podocalyxin, CD24 but no GCTM expression (HES/MD_Renal Progenitor-enriched).  They confirmed that it is possible to differentiate HES into mesoderm that contains kidney progenitors, which is an important first step towards using stem cell therapies for kidney repair.
                   </p>
                    
            </div>
            <div class="biologistInfo">
                <h2>References</h2>
                <div class="ruler"></div>
                <p>
               Lin, S.A., Kolle, G., Grimmond, S.M., Zhou, G., Doust, E., Little, M.H., Aronow, B., Ricardo, S., Martin, F., Pera, M.F., Bertram, J.F., and Laslett, A.L. (2010). "Subfractionation of differentiating hES populations allows the isolation of a mesodermal population enriched for intermediate mesoderm and renal progenitors.", Stem Cells and Development 19: 1637-1648.
               </p>
               <p>
                Little, M.H., Georgas, K., Pennisi, D., and Wilkinson, L. (2010). "Kidney development: two tales of tubulogenesis.", Current Topics in Developmental Biology 90: 193-229.
                </p>
            </div>

        </div>
        <div class="sideColumn">
            ${Base.sideColumnBiologists()}  
            
        </div>
    </div>

