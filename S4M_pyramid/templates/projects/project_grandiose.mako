<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
	<script type="text/javascript" src="${h.url('/js/projects/project_grandiose.js')}"></script>
</%def>
<%def name="nagy_lab()">
    <li><a target = "_blank" href="http://research.lunenfeld.ca/nagy/">Nagy Lab </a></li>
</%def>
<%def name="cloonan_lab()">
    <li><a target = "_blank" href="https://unidirectory.auckland.ac.nz/profile/n-cloonan">Cloonan Lab </a></li>
</%def>
<%def name="grimmond_lab()">
    <li><a target = "_blank" href="http://www.imb.uq.edu.au/sean-grimmond">Grimmond Lab </a></li>
</%def>
<%def name="heck_lab()">
    <li><a target = "_blank" href="http://hecklab.com">Heck Lab </a></li>
</%def>
<%def name="zandstra_lab()">
    <li><a target = "_blank" href="http://stemcell.ibme.utoronto.ca/about_us.html">Zandstra Lab </a></li>
</%def>
<%def name="preiss_lab()">
    <li><a target = "_blank" href="http://jcsmr.anu.edu.au/research/genome-biology/rna-biology">Preiss Lab </a></li>
</%def>
<%def name="seo_lab()">
    <li><a target = "_blank" href="http://www.gmi.ac.kr">Seo Lab </a></li>
</%def>
<%def name="s4m()">
    <li><a target = "_blank" href="http://www.stemformatics.org/contents/about_us">${c.site_name} Team Page</a></li>
</%def>
<%def name="wells_lab()">
    <li><a target = "_blank" href="http://www.aibn.uq.edu.au/christine-wells">Wells Lab </a></li>
</%def>
<%def name="rasko_lab()">
    <li><a target = "_blank" href="http://sydney.edu.au/medicine/people/academics/profiles/john.rasko.php">Rasko Lab </a></li>
</%def>

<%def name="nagy_contact()">
    <li><a href="mailto:nagy@lunenfeld.ca">Contact Andras Nagy</a></li>
</%def>

<%def name="generic_contact(email,name)">
    <li><a href="mailto:${email}">Contact ${name}</a></li>
</%def>

<%def name="umbrella_paper()">
<% ds_id = 6197 %>
${h.get_citations(ds_id,c.citations)}
</%def>
<%def name="cell_state_paper()">
<% ds_id = 6198 %>
${h.get_citations(ds_id,c.citations)}
</%def>
<%def name="miRNA_paper()">
<% ds_id = 6128 %>
${h.get_citations(ds_id,c.citations)}
</%def>
<%def name="methylation_paper()">
<% ds_id = 6131 %>
${h.get_citations(ds_id,c.citations)}
</%def>
<%def name="proteome_paper()">
<% ds_id = 6130 %>
${h.get_citations(ds_id,c.citations)}
</%def>

<%def name="umbrella_citation_only()">
<% ds_id = 6197 %>
${h.get_citations_part(ds_id,c.citations,"Publication Citation")}
</%def>
<%def name="methylation_citation_only()">
<% ds_id = 6131 %>
${h.get_citations_part(ds_id,c.citations,"Publication Citation")}
</%def>


<%def name="methods()">
<a target="_blank" href="${h.url('/Project Grandiose methods.pdf')}">Project Grandiose Detailed methods.</a>
</%def>



<%def name="content_menu_pg()">
        <a href="${h.url('/projects/project_grandiose#introduction')}"> 
            <div class="contact_menu selected">
                <div class="contact_menu_title">Introduction</div>
            </div>
        </a>
        <a href="${h.url('/projects/project_grandiose#chromatin')}"> 
            <div class="contact_menu" >
                <div class="contact_menu_title">Epigenome</div>
            </div>
        </a>
        <a href="${h.url('/projects/project_grandiose#transcriptome')}"> 
            <div class="contact_menu" >
                <div class="contact_menu_title">Transcriptome</div>
            </div>
        </a>
        <a href="${h.url('/projects/project_grandiose#proteome')}"> 
            <div class="contact_menu" >
                <div class="contact_menu_title">Proteome</div>
            </div>
        </a>
        <a href="${h.url('/projects/project_grandiose#visualisation')}"> 
            <div class="contact_menu" >
                <div class="contact_menu_title">Data Visualisation</div>
            </div>
        </a>

</%def>


<div class="content project_grandiose">
    <div class="content_left_column">
        ${self.content_menu_pg()}
    </div>
    <div class="content_right_column ">
        <div class="box display">
            <div id="introduction" class="content_box">
                <a id="introduction"></a>
                <div class="header_1">
    Project Grandiose
                </div>
                <div class="text">
                <p>
Differentiated cells are presumed to have a molecular network that is 'hard-wired' to dictate the restricted phenotype of that cell. The discovery that the over-expression of four transcription factors (reprogramming factors), Oct4, Sox2, Klf4 and c-Myc (OSKM) could disrupt this hard-wiring, and revert cells to stem-cell-like phenotypes (induced pluripotent stem cells or iPSCs) challenged many of our assumptions about cell fate. 
</p>
<p>
Project Grandiose defines two reprogramming trajectories, which arrive at distinct pluripotent states: the "F-class" and embryonic stem cell (ESC)-like iPSCs. The F-class state represents reprogramming factor dependent cells, whilst the (ESC)-like iPSCs state represent reprogramming factor independent cells.
</p>
<p>
A highly efficient mouse secondary reprogramming system was used to characterise the molecular trajectories leading to these two distinct pluripotent cell types at multiple omic levels. NGS was used to profile the transcriptome (miRNA, lncRNA, mRNA), genome wide CpG methylation and chromatin marks (H3K4me3, H3K27me3 and H3K36me3) in addition to quantitative mass spectrometry profiling of the global and cell surface proteome. These analyses were coordinated to be performed in parallel on the same cell collections at the same time points and cell states indicated in Figure 1.
</p>
<img style="width:570px;important;max-width:570px;max-height: 200px" src="${h.url('/images/grandiose/ips_path.png')}"></img>
<p><span style="font-weight:bold">Figure 1</span> | Samples taken from trajectories leading to F-class and ES cell-like pluripotency for “omics” analyses. 
2ºMEF = secondary mouse embryonic fibroblasts containing doxycycline inducible reprograming transgenes, H = high reprogramming factor expression, L/0 = low or no reprogramming factor expression, 1ºiPSCs and 2ºiPSCs = ESC-like iPSCs.
</p>
<p>
The data is fully implemented into the ${c.site_name} platform for presentation and mining with user-friendly bioinformatics and statistical tools.
</p>
<p>
</p>
                  <p>Current publications from Project Grandiose:
                        <ul>
                            <li>${self.umbrella_paper()}</li>
                            <li>${self.cell_state_paper()}</li>
                            <li>${self.miRNA_paper()}</li>
                            <li>${self.methylation_paper()}</li>
                            <li>${self.proteome_paper()}</li>
</ul></p><p>Additional Information:<ul>
                            <li>${self.methods()}</li>
                            
                        
                        </ul>   
                    </p>
<p>
We invite you to explore specific datasets using the menu on the left, alternatively look at the collection of Project datasets here:
</p>
                  <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?filter=project grandiose:')}">All Project Grandiose Datasets in ${c.site_name}</a></li>

                        </ul>   
                    </p>
<!--
<p>
Visualise, analyse and download published gene lists here:
</p>
                  <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=project grandiose')}">All Project Grandiose Gene Lists in ${c.site_name}</a></li>
                        
                        </ul>   
                    </p> 
-->                   
<p>
The Project Grandiose collaboration spans groups in Canada, Australia, South Korea, and The Netherlands, and includes members of:
</p>
                  <p>
                        <ul>
                            ${self.cloonan_lab()} 
${self.generic_contact('n.cloonan@auckland.ac.nz','Nicole Cloonan')}
                            ${self.heck_lab()}
${self.generic_contact('a.j.r.heck@uu.nl','Albert Heck')}
                            ${self.grimmond_lab()} 
${self.generic_contact('sean.grimmond@glasgow.ac.uk','Sean Grimmond')}
                            ${self.nagy_lab()} 
                            ${self.nagy_contact()}
                            ${self.preiss_lab()} 
${self.generic_contact('thomas.preiss@anu.edu.au','Thomas Preiss')}
                            ${self.rasko_lab()} 
${self.generic_contact('j.rasko@centenary.usyd.edu.au','John Rasko')}
                            ${self.seo_lab()} 
${self.generic_contact('jeongsun@snu.ac.kr','Jeong-Sun Seo')}
                            ${self.s4m()} 
                            ${self.wells_lab()} 
${self.generic_contact('c.wells@uq.edu.au','Christine Wells')}
                            ${self.zandstra_lab()}
${self.generic_contact('peter.zandstra@utoronto.ca','Peter Zandstra')}

 
                        </ul>   
                    </p>                         
                    <div class="clear"></div>
                  </div>
            </div>
        </div>
        <div class="box hidden">
            <div  class="content_box">
                <a id="chromatin"></a>
                <div class="header_1">
Project Grandiose Epigenome Datasets - CpG Methylation
                </div>
                <div class="text">
                    <p>
Project Grandiose interrogated the methylome by sequencing bisulfite-treated genomic DNA to determine the methylation status of CpG dinucleotides. 

                    </p>
                    <p>
Genomic DNA purification was carried out by the Nagy laboratory, and bisulfite treatment and sequencing were performed in the Seo laboratory at the Genomic Medicine Institute, South Korea. Two datasets are provided here since the mapped sequencing reads were analyzed using two approaches in Lee <em style="font-style:italic">et al</em> (${self.methylation_citation_only()}) and Hussein <em style="font-style:italic">et al</em> (${self.umbrella_citation_only()}).
                    </p>
                    <p>
If the user is looking for average methylation level within 5kb upstream and 1kb downstream of the TSS (transcriptional start site) of annotated genes, and searching using a gene name to assess how they change during reprogramming, then use <a href="${h.url('/datasets/search?ds_id=6131')}" target="_blank">Lee<em style="font-style:italic"> et al</em></a>.
                    </p>
                    <p>
If the user is looking for average methylation +/- 1kb from the TSS of genes including any of the novel transcripts described by the consortium, then use <a href="${h.url('/datasets/search?ds_id=6368')}" target="_blank">Hussein<em style="font-style:italic"> et al</em></a> data.
</p>
                    <p>
Refer to methods <a target="_blank" href="${h.url('/Project Grandiose methods.pdf')}">PDF</a> for more information.
                    </p>

                    <p>
                        <ul>
                            <li>Please note that to view novel genes (like PG_lncRNA_3770) you must use the ${c.samer_methylation_probe_name} Search below the Gene Search in the link below.</li>
                            <li><a target="_blank" href="${h.url('/datasets/search?filter=PGMethylationCpG')}">Project Grandiose CpG Methylation Datasets in ${c.site_name}</a></li>
                            <!-- <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=project grandiose chromatin')}">All Project Grandiose CpG methylation Gene Lists in ${c.site_name}</a></li> -->
</ul></p><p>Publications<ul>
                            <li>${self.methylation_paper()}</li>
                            <li>${self.umbrella_paper()}</li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>

            <div  class="content_box">
                <a id="chromatin"></a>
                <div class="header_1">
Project Grandiose Epigenome Datasets - Chromatin Marks
                </div>
                <div class="text">
                    <p>
Project Grandiose interrogated chromatin status by ChIP-Seq for histone marks: H3K27me3, H3K4me3 and H3K36me3. 
                    </p>
                    <p>
Chromatin pull downs were performed by the Nagy laboratory and sequenced by the Seo laboratory at the Genomic Medicine Institute, South Korea. 
                    </p>


                    <p>
                        <ul>
                            <li>Please note that to view novel genes (like PG_lncRNA_3770) you must use the Histone ChIPSeq Search below the Gene Search in the link below.</li>
                            <li><a target = "_blank" href="${h.url('/datasets/search?filter=PGChromatin')}">All Project Grandiose Chromatin Mark Datasets in ${c.site_name}</a></li>
                            <!-- <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=project grandiose chromatin')}">All Project Grandiose Chromatin Mark Gene Lists in ${c.site_name}</a></li> -->
</ul></p><p>Publications<ul>
                            <li>${self.umbrella_paper()}</li>
                            <li>${self.methylation_paper()}</li>
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Contributing Laboratories 
                </div>
                <div class="text">
                    <p>
                        <ul>
                            ${self.seo_lab()}
${self.generic_contact('jeongsun@snu.ac.kr','Jeong-Sun Seo')}
                            ${self.nagy_lab()}
                            ${self.nagy_contact()}
            
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
       </div>
        <div class="box hidden">

            <div  class="content_box">
                <a id="transcriptome"></a>

                <div class="header_1">
Project Grandiose Transcriptome Datasets - miRNA
                </div>
                <div class="text">
                    <p>
Project Grandiose interrogated the miRNA expression profiles of the samples leading to the two pluripotent stem cell states (described in the Introduction) by NGS of the small RNA fraction (20-35 nt) of the total RNA. 
                    </p>
                    <p>
The libraries were generated and sequenced by the Nagy lab. The Preiss lab performed the mapping of the reads and further data analyses.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?ds_id=6128')}">Project Grandiose miRNA Dataset in ${c.site_name}</a></li>
                            <!-- <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=grandiose and mrna')}">Project Grandiose miRNA Gene Lists in ${c.site_name}</a></li> -->
</ul></p><p>Publications<ul>
<li>${self.miRNA_paper()}</li>
<li>${self.umbrella_paper()}</li>
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
            </div> 
            <div  class="content_box">

                <div class="header_1">
Project Grandiose Transcriptome Datasets - RNASeq
                </div>
                <div class="text">
                    <p>
Project Grandiose interrogated the mRNA expression profiles of the samples leading to the two pluripotent stem cell states described in the Introduction by NGS of the large RNA fraction (>35 bp) of the total RNA. 
                    </p>
                    <p>
The RNA was isolated by the Nagy lab, the libraries were generated and the sequencing was performed by the Grimmond lab. The mapping and the analysis were done in both the Nagy and Grimmond labs.
                    </p>

                    <p>
                    </p>

                    <p>
                        <ul>
                            <li>Please note that to view novel genes (like PG_lncRNA_3770) you must use the Feature Search below the Gene Search in the link below.</li>
                            <li><a target = "_blank" href="${h.url('/datasets/search?ds_id=6197')}">Project Grandiose RNASeq Dataset in ${c.site_name}</a></li>
                            <!-- <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=grandiose and mrna')}">Project Grandiose RNASeq Gene Lists in ${c.site_name}</a></li> -->
                        </ul>
                   </p>
                   <p>Publications
                       <ul>
                           <li>${self.umbrella_paper()}</li>
                           <li>${self.methylation_paper()}</li>
                       </ul>   
                   </p>
                   <div class="clear"></div>
                    
                </div>

            </div> 

            <div  class="content_box">

                <div class="header_1">
Project Grandiose Transcriptome Datasets - Microarray
                </div>
                <div class="text">
                    <p>
Before NGS the samples were microarray profiled on the Illumina MouseRef-8 V2 platform as part of the quality control. The library construction and microarray were performed by the Grimmond lab. 
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?ds_id=6126')}">Project Grandiose Microarray Dataset in ${c.site_name}</a></li>
                            <!-- <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=grandiose and mrna')}">Project Grandiose Microarray Gene Lists in ${c.site_name}</a></li> -->
</ul></p><p>Publications<ul>
<li>${self.umbrella_paper()}</li>
<li>${self.cell_state_paper()}</li>
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
            </div> 
            <div  class="content_box">

                <div class="header_1">
Project Grandiose Transcriptome Datasets – primary iPS cell lines (F-class and ES cell like) – Microarray
                </div>
                <div class="text">
                    <p>
The primary iPS cell lines analysed by Tonge <span style="font-style:italic;">et al.</span>were subjected to microarray expression profiling on the Illumina MouseRef-8 V2 platform.
                    </p>
                    <p>
The RNA preparation and microarray analysis was performed by the Nagy lab. 
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?filter=PGCellState')}">Project Grandiose Microarray Dataset of primary F-class and ES cell-like clones in ${c.site_name}</a></li>
                            <!-- <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=grandiose and mrna')}">Project Grandiose Gene Lists of the primary iPS cell clones of Tonge, <span style="font-style:italic;">et al.</span>in ${c.site_name}</a></li> -->
</ul></p><p>Publications<ul>
<li>${self.cell_state_paper()}</li>
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
            </div> 
            <div class="content_box">
                <div class="header_2">
                    Contributing Laboratories 
                </div>
                <div class="text">
                    <p>
                        <ul>
                            ${self.nagy_lab()}
                            ${self.nagy_contact()}
                            ${self.preiss_lab()}
${self.generic_contact('thomas.preiss@anu.edu.au','Thomas Preiss')}
                            ${self.cloonan_lab()}
${self.generic_contact('n.cloonan@auckland.ac.nz','Nicole Cloonan')}
                            ${self.grimmond_lab()}
${self.generic_contact('sean.grimmond@glasgow.ac.uk','Sean Grimmond')}
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
        </div>
        <div class="box hidden">
            <div  class="content_box">
                <a id="proteome"></a>
                <div class="header_1">
Project Grandiose Proteome Datasets - Global
                </div>
                <div class="text">
                    <p>
Project Grandiose surveyed global protein expression of the samples by quantitative mass spectrometry.
                    </p>
                    <p>
The Nagy laboratory collected the cells and the Heck laboratory performed the quantitative mass spectrometry using a combination of isobaric peptide labeling, strong cation exchange (SCX) chromatography and high-resolution LC-MS/MS analysis.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?ds_id=6130')}">Project Grandiose Global Proteome Dataset in ${c.site_name}</a></li>
                            <!-- <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=grandiose proteome')}">Project Grandiose Global Proteome Gene Lists in ${c.site_name}</a></li> -->
</ul></p><p>Publications<ul>
<li>${self.proteome_paper()}</li>
<li>${self.umbrella_paper()}</li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div  class="content_box">
                <div class="header_1">
Project Grandiose Proteome Datasets - Cell Surface 
                </div>
                <div class="text">
                    <p>
Under construction, publication is in preparation.
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Contributing Laboratories
                </div>
                <div class="text">
                    <p>
                        <ul>
                            ${self.heck_lab()}
${self.generic_contact('a.j.r.heck@uu.nl','Albert Heck')}
                            ${self.zandstra_lab()}
${self.generic_contact('peter.zandstra@utoronto.ca','Peter Zandstra')}
                            ${self.nagy_lab()}
                            ${self.nagy_contact()}
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
        </div>
        <div class="box hidden">

            <div  class="content_box">
                <a id="visualisation"></a>
                <div class="header_1">
                    Data Visualisation support and support was provided by various labs.
                </div>
                <div class="text">
                    <p>
    In this project, new ways of visualising data both in ${c.site_name} and by more commonly used bioinformatics methods were tested and improved.
                    </p>
                    <p>
    Dr. Kim-Anh Lê Cao provided statistical analysis and new ways of visualizing the data using data integration statistical approaches by the mean of multivariate analysis. These approaches are available in the mixOmics R package (<a href="http://perso.math.univ-toulouse.fr/mixomics">http://www.math.univ-toulouse.fr/~biostat/mixOmics</a>).</p><p>Dr. Jessica Mar provided assistance with normalization of data sets and bioinformatics support. </p>
                   
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Contributing Laboratories
                </div>
                <div class="text">
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://perso.math.univ-toulouse.fr/mixomics/">Dr. Kim-Anh Lê Cao website</a></li>
                            <li><a target = "_blank" href="https://sites.google.com/site/marlabeinstein/">Mar Lab website</a></li>
                            ${self.wells_lab()} 
${self.generic_contact('c.wells@uq.edu.au','Christine Wells')}
                            ${self.s4m()} 
                            ${self.nagy_contact()}
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
        </div>
               
            
    </div>
</div>

