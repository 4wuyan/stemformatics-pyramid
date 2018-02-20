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
                <span>PEEKING INTO THE NOSE THROUGH THE BRAIN</span>
            </div>
            <div class="date">13 December 2010</div>
            <div class="mainText">
                    <p>
                    The mammalian nose represents one of the few regions of active neural regeneration in adults.  
                    Stem and progenitor cells isolated from the olfactory epithelium give rise to neurons, glia and surrounding stroma. 
                    Because stem cells from the nose are readily accessible, they provide an important patient-derived resource for studying neurological disorders. 
                    </p>
                    <p>
                    <div class="articleImageCaption">
                        <img class="small" src="${h.url('/images/contents/forBiologists/random_cell_2.png')}" />
                        <div class="caption">
                            <div class="captionText">
                                Cells derived from donors with Parkinson’s disease share differences 
                                in the pathways that process environmental toxins
                            </div>
                        </div>
                    </div>
                    <p>
                    Hyposmia, or loss of the sense of smell, is an early symptom of several neurodegenerative disorders, including Parkinson’s disease and Alzheimer’s. 
                    Researchers at the NCASCR led by Alan Mackay-sim have discovered gene expression signatures of Olfactory neurosphere-derived stem cells (hONS). 
                    Gene expression in hONS cell lines mirror the expression seen in the primary cells, indicating that they retain patient information. 
                    </p>
                    <p>
                    These signatures discriminate between different neurological disorders. Cells derived from donors with Parkinson’s disease share differences 
                    in the pathways that process environmental toxins. Cells derived from donors with Schizophrenia show differences in cell-cell and 
                    cell-environment interactions. They are being used to screen new cell-based and pharmaceutical based therapies.
                    </p>
            </div>
            <div class="biologistInfo">
                <h2>References</h2>
                <div class="ruler"></div>
                <p>
                Matigian, N., G. Abrahamsen, R. Sutharsan, A. L. Cook, A. M. Vitale, A. Nouwens, B. Bellette, J. An, M. Anderson, A. G. Beckhouse, 
                M. Bennebroek, R. Cecil, A. M. Chalk, J. Cochrane, Y. Fan, F. Feron, R. McCurdy, J. J. McGrath, W. Murrell, C. Perry, 
                J. Raju, S. Ravishankar, P. A. Silburn, G. T. Sutherland, S. Mahler, G. D. Mellick, S. A. Wood, C. M. Sue, 
                C. A. Wells, and A. Mackay-Sim (2010), "Disease-specific, neurosphere-derived cells as models for brain disorders", Dis Model Mech 3 (11-12):785-798.
                </p>
                <p>
                Murrell, W., F. Feron, A. Wetzig, N. Cameron, K. Splatt, B. Bellette, J. Bianco, C. Perry, G. Lee, and A. Mackay-Sim (2005), "Multipotent stem cells from adult olfactory mucosa", Dev Dyn 233 (2):496-515.
                </p>
                <p>
                Murrell, W., A. Wetzig, M. Donnellan, F. Feron, T. Burne, A. Meedeniya, J. Kesby, J. Bianco, C. Perry, P. Silburn, and A. Mackay-Sim (2008), "Olfactory mucosa is a potential source for autologous stem cell therapy for Parkinson's disease", Stem Cells 26 (8):2183-2192.
                </p>
            </div>

        </div>
        <div class="sideColumn">
            ${Base.sideColumnBiologists()}  
            
        </div>
    </div>


      

