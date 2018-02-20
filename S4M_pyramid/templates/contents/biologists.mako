<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
    <link href="${h.url('/css/contents/index.css')}" type="text/css" rel="stylesheet"> 
    <link href="${h.url('/css/contents/biologists.css')}" type="text/css" rel="stylesheet"> 
</%def>
	
    <!-- links on the leftColumn -->
    ${Base.links()}  

    <div class="rightColumn">
        <div class="mainTextColumn">
            <div class="imageText">
                <img class="large" src="${h.url('/images/contents/ST_Header_OverviewOfDatasets.png')}">
                
            </div>
            <div class="mainText">
              <p>In ${c.site_name} you'll find data from leading stem cell laboratories in a format that is easy to search, easy to visualise and easy to export. All data is publicly available (mainly sourced from Array Express).
              </p>
              <p>We've initially included a set of hand-picked experiments which we think are interesting to stem cell biologists, and indeed we take requests for new stem cell experiments to add to ${c.site_name} (please request via the Contact Us page).</p>
              <p>Browse experiment overviews below, for some of the datasets available in ${c.site_name}.</p>
            </div>
            <div class="biologistInfo">
                <h2>Article Summaries</h2>
                <div class="ruler"></div>
                <div class="showBiologists">
                    <img class="small" src="${h.url('/images/contents/forBiologists/random_cell_1.png')}" />
                    <div class="showText">
                        <h3><a href="${h.url('/contents/stem_cells_in_human_breast')}">STEM CELLS IN HUMAN BREAST</a></h3>
                        <div class="text"><a href="${h.url('/contents/stem_cells_in_human_breast')}">Breast is a tissue that requires dynamic remodelling
                            throughout the reproductive life of mammals. Adult stem
                            cells support this remodelling process. As well as
                            revealing information about the processes of cellular
                            differentiation, the study of mammary stem cells (MaSCs)
                            is also relevant to understanding the development of
                            breast cancers. The Visvader and Lindeman laboratories
                            at the WEHI report on the isolation of ... 
                            <span class="more">more ></a></span>
                        </div>
                    </div>
                    
                </div>
                <div class="showBiologists">
                    <img class="small" src="${h.url('/images/contents/forBiologists/nosePick.png')}" />
                    <div class="showText">
                        <h3><a href="${h.url('/contents/peeking_into_the_brain_through_the_nose')}">PEEKING INTO THE BRAIN THROUGH THE NOSE</a></h3>
                        <div class="text"><a href="${h.url('/contents/peeking_into_the_brain_through_the_nose')}">The mammalian nose represents one of the few regions
                            of active neural regeneration in adults. Stem and
                            progenitor cells isolated from the olfactory epithelium give
                            rise to neurons, glia and surrounding stroma. Because
                            stem cells from the nose are readily accessible, they
                            provide an important patient-derived resource for studying
                            neurological disorders. Hyposmia, or loss of the sense of
                            smell, is an early symptom of ... 
                            <span class="more">more ></a></span></a>
                        </div>
                    </div>
                </div>
                <div class="showBiologists">
                    <img class="small" src="${h.url('/images/contents/forBiologists/Blood.png')}" />
                    <div class="showText">
                        <h3><a href="${h.url('/contents/making_blood')}">MAKING BLOOD</a></h3>
                        <div class="text"><a href="${h.url('/contents/making_blood')}">Haemopoiesis – the generation of blood – provides the
                            archetypical model for hierarchical differentiation of adult
                            tissues. Model systems derive stem cells from adult bone
                            marrow or foetal cord blood. The datasets here profile
                            putative stem, progenitor and differentiated cell
                            populations. The gene expression signatures of
                            haemopoietic stem and progenitor cells, and their
                            differentiated progeny, provide ...
                            <span class="more">more ></a></span>
                        </div>
                    </div>
                </div>
                <div class="showBiologists">
                    <img class="small" src="${h.url('/images/contents/forBiologists/kidney_new.jpg')}" />
                    <div class="showText">
                        <h3><a href="${h.url('/contents/kidney_progenitors')}">FROM STEM CELLS TO KIDNEY PROGENITORS</a></h3>
                        <div class="text"><a href="${h.url('/contents/kidney_progenitors')}">Understanding kidney development is the first vital step
                           towards improving outcomes for individuals with kidney disease. 
                           One approach taken by the laboratories of Melissa Little (UQ) and 
                           Andrew Laslett (CSIRO) is to identify and isolate cells capable of 
                           forming renal tissues from cultures of human embryonic stem cells 
                           which are differentiated in the presence of renal growth factors ...
                            <span class="more">more ></a></span>
                        </div>
                    </div>
                </div>
                <div class="showBiologists">
                    <img class="small" src="${h.url('/images/contents/forBiologists/mesenchymal_stemcell.jpg')}" />
                    <div class="showText">
                        <h3><a href="${h.url('/contents/pluripotent_stem_cells')}">PLURIPOTENT STEM CELLS</a></h3>
                        <div class="text"><a href="${h.url('/contents/pluripotent_stem_cells')}">Most cells in our body share the same genetic
                            blueprint in the form of chromosomal DNA, but the information 
                            flow from DNA to cell function is contextual, and accessed 
                            according to the developmental state of that cell. Lineage 
                            commitment probably involves restricting the genetic 
                            information accessible to the cell, a process once thought 
                            to be irreversible. Induced pluripotent stem cells are 
                            'reprogrammed' such that mature cells regain access to the 
                            genetic information required to generate different cell fates ...
                            <span class="more">more ></a></span>
                        </div>
                    </div>
                </div>

            </div>            
        </div>
        <div class="sideColumn">
            ${Base.sideColumnBiologists()}  
        </div>
    </div>


      

