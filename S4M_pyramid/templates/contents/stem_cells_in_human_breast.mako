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
                <span>STEM CELLS IN HUMAN BREAST</span>
            </div>
            <div class="date">13 December 2010</div>
            <div class="mainText">
                    <p>
                    Breast is a tissue that requires dynamic remodelling throughout the reproductive life
                    of mammals. Adult stem cells support this remodelling process. As well as revealing
                    information about the processes of cellular differentiation, the study of mammary
                    stem cells (MaSC) is also relevant to understanding the development of breast
                    cancers.
                    </p>
                    <p>
                    <div class="articleImageCaption">
                        <img class="small" src="${h.url('/images/contents/forBiologists/random_cell_1.png')}" />
                        <div class="caption">
                            <div class="captionText">
                                The study of mammary stem cells (MaSC) is also relevant to understanding the development of breast cancers
                            </div>
                        </div>
                    </div>
                    
                    The Visvader and Lindeman laboratories
                    at the WEHI report on the isolation of
                    three epithelial subsets from human
                    breast tissue. These form a hierarchy of
                    differentiation potential and include basal
                    stem/progenitor, luminal progenitor and
                    mature luminal cells. Each subset was
                    defined by their expression of
                    differentiation markers. The population
                    defined as CD49f (α6 integrin)-high but
                    Digital mammogram scan of breast cancer in
                    CD326 (EpCAM)-negative could
                    regenerate breast epithelium in mouse
                    models, although at low efficiency and
                    were termed MaSC-enriched. Although representing a heterogeneous cell population,
                    these datasets provide gene expression signatures enriched for MaSC.
                    </p>
                    <p>
                    While the cancer-stem cell theory remains controversial, there is no doubt that many
                    breast tumours share phenotypes reminiscent of MaSC populations; and individuals
                    with predisposition to breast cancer (for example, carriers of BRCA1 mutations) have
                    abnormal MaSC phenotypes. Bench-marking tumours against the MaSC gene
                    signature allowed researchers to identify tumour lineage and provide insight into the
                    processes predisposing individuals to the development of cancers.
                    </p>
                    
            </div>
            <div class="biologistInfo">
                <h2>References</h2>
                <div class="ruler"></div>
                <p>
                Lim, E., F. Vaillant, D. Wu, N. C. Forrest, B. Pal, A. H. Hart, M. L. Asselin-Labat, D. E. Gyorki, T.
                Ward, A. Partanen, F. Feleppa, L. I. Huschtscha, H. J. Thorne, S. B. Fox, M. Yan, J. D. French, M. A.
                Brown, G. K. Smyth, J. E. Visvader, and G. J. Lindeman (2009), "Aberrant luminal progenitors as the
                candidate target population for basal tumor development in BRCA1 mutation carriers", Nat Med 15
                (8):907-913.
                </p>
                <p>
                Lim, E., D. Wu, B. Pal, T. Bouras, M. L. Asselin-Labat, F. Vaillant, H. Yagita, G. J. Lindeman, G. K.
                Smyth, and J. E. Visvader (2010), "Transcriptome analyses of mouse and human mammary cell
                subpopulations reveal multiple conserved genes and pathways", Breast Cancer Res 12 (2):R21.
                Visvader, J. E., and G. J. Lindeman (2010), "Stem cells and cancer - the promise and puzzles", Mol
                Oncol 4 (5):369-372.
                </p>
                <p>
                Visvader, J. E., and G. H. Smith (2010), "Murine Mammary Epithelial Stem Cells: Discovery,
                Function, and Current Status", Cold Spring Harb Perspect Biol.
                Asselin-Labat, M. L., F. Vaillant, J. M. Sheridan, B. Pal, D. Wu, E. R. Simpson, H. Yasuda, G. K.
                Smyth, T. J. Martin, G. J. Lindeman, and J. E. Visvader (2010), "Contro
                </p>
            </div>

        </div>
        <div class="sideColumn">
            ${Base.sideColumnBiologists()}  
            
        </div>
    </div>


      

