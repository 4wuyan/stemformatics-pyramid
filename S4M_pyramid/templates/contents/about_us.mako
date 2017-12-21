<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link href="${h.url('/css/contents/privacy_policy.css')}" type="text/css" rel="stylesheet">
    <link href="${h.url('/css/sass/stylesheets/screen.css')}" type="text/css" rel="stylesheet">
</%def>

<div class="content">
    <div class="content_left_column">
        ${Base.content_menu(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column">
        <div class="content_box">
            <div class="header_1">
${c.site_name} is a collaboration between the stem cell and bioinformatics community.
            </div>
            <div class="text">
 <p>We were motivated by the plethora of exciting cell models in the public and private domains, and the realisation that for many biologists these were mostly inaccessible. We wanted a fast way to find and visualise interesting genes in these exemplar stem cell datasets. We'd like you to explore. You'll find data from leading stem cell laboratories in a format that is easy to search, easy to visualise and easy to export.</p>
<p>${c.site_name} is not a substitute for good collaboration between bioinformaticians and stem cell biologists. We think of it as a stepping stone towards that collaboration.</p>
            </div>
        </div>
        <div class="content_box">
            <div class="content_links">
                <a href="#team">Our Core Team > </a>
                <a href="#annotators">Our Annotators ></a>
                <a href="#students">Our Students ></a>
                <a href="#citation">How to Cite Us ></a>
                <a href="#funding">Funding ></a>
                <a href="#suggest">Suggest a Dataset ></a>
                <a href="#partners">Partners ></a>
                <a href="#past_partners">Past Partners ></a>
                <a href="#links_we_like">Links we like ></a>
                <div class="clear"></div>
            </div>
        </div>
        <div class="content_box">
            <a id="team"></a>
            <div class="header_2">
                Our Core Team
            </div>
            <div>
                <div class="team">
                    <img src="/images/contents/team_photos/christine_s.jpg">
                    <div class="team_member">Christine Wells<br/>Project Leader</div>
                    <div class="clear"></div>
                </div>
                <div class="team">
                    <img src="/images/contents/team_photos/rowland_s.jpg">
                    <div class="team_member">Rowland Mosbergen<br/>Developer</div>
                    <div class="clear"></div>
                </div>
                <div class="team">
                    <img src="/images/contents/team_photos/othmar_s.jpg">
                    <div class="team_member">Othmar Korn<br/>Bioinformatician</div>
                    <div class="clear"></div>
                </div>
                <div class="clear"></div>
                <div class="team">
                    <img src="/images/contents/team_photos/tyrone_s.jpg">
                    <div class="team_member">Tyrone Chen<br/>Data importer</div>
                    <div class="clear"></div>
                </div>
		            <div class="team">
                    <img src="/images/contents/team_photos/isha_s.JPG">
                    <div class="team_member">Isha Nagpal<br/>Developer</div>
                    <div class="clear"></div>
                </div>
                <div class="team">
                    <img src="/images/contents/team_photos/chris_s.png">
                    <div class="team_member">Chris Pacheco Rivera<br/>Annotator</div>
                    <div class="clear"></div>
                </div>
                <div class="clear"></div>
            </div>
        </div>
        <div class="content_box">
            <a id="annotators"></a>
            <div class="header_2">
                Our Annotators
            </div>
            <div>
               <div class="text">

                    <div class="margin_top_small team_member">Chris Pacheco Rivera</div>

                    <div class="margin_top_small team_member">Jessica Schwarber (former)</div>
                    <div class="margin_top_small team_member">Suzanne Butcher (former)</div>
                    <div class="margin_top_small team_member">Elizabeth Mason (former)</div>
                    <div class="margin_top_small team_member">Alejandro Vitale (former)</div>
                    <div class="margin_top_small team_member">Jill Shepherd (former)</div>
                </div>
                <div class="clear"></div>
            </div>
        </div>
        <div class="content_box">
            <a id="students"></a>
            <div class="header_2">
                Our Students
            </div>
            <div>
               <div class="text">

                    <div class="margin_top_small team_member">Ariane Mora</div>
                    <div class="margin_top_small team_member">Sadia Waleem</div>
                    <div class="margin_top_small team_member">Huan Wang</div>
                    <div class="margin_top_small team_member">Isaac Virshup (former)</div>
                    <div class="margin_top_small team_member">Melinda Wang (former)</div>
                    <div class="margin_top_small team_member">Peter Zhang (former)</div>
                </div>
                <div class="clear"></div>
            </div>
        </div>
        ${Base.citation_content()}
        <div class="content_box">
            <a id="funding"></a>
            <div class="header_2">
                Funding
            </div>
            <div class="text">

                <p>Our current list of funders include:
                <ul>
                    <li>
                        ARC Special Research Initiative to Stem Cells Australia (SR1101002)
                    </li>
                    <li>
                        ARC Discovery Project (DP130100777)
                    </li>
                    <li>
                        ARC Future Fellowship (FT150100330)
                    </li>
                    <li>
                        JEM Research Foundation philanthropic funding
                    </li>
                    <li>
                        QLD Government Smart Futures Fellowship
                    </li>
                    <li>
                        University of Melbourne Centre for Stem Cell Systems
                    </li>

                </ul>
                </p>
            </div>
        </div>
        <div class="content_box">
            <a id="suggest"></a>
            <div class="header_2">
                Suggest a Dataset
            </div>
            <div class="text">

                <p>You can suggest a dataset that goes straight into our dataset queue, Agile_org.
                <ul><li>
                    <a target="_blank" href="/main/suggest_dataset">Click here to go to Agile_org to add a new dataset</a>
                </ul></li>
                </p>
            </div>
        </div>
        <div class="content_box partners">
            <a id="partners"></a>
            <div class="header_2">
                Partners
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.stemcellsaustralia.edu.au/">
                    <img src="/images/logos/STE_SCA.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.uq.edu.au/">
                <img src="/images/logos/STE_UQ.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.qcif.edu.au/">
                <img src="/images/logos/STE_QCIF_about_us.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.aibn.uq.edu.au/">
                <img src="/images/logos/STE_AIBN.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.wehi.edu.au/">
                <img src="/images/logos/STE_WEHI.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.qfab.org/">
                <img src="/images/logos/STE_QFAB.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a href="#partners">
                <img src="/images/logos/STE_JEM.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://nectar.org.au/">
                <img src="/images/logos/STE_NECTAR.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.unimelb.edu.au/">
                <img src="/images/logos/University_of_Melbourne_logo.png"></img>
                </a>
            </div>
             <div class="clear"></div>
        </div>
        <div class="content_box partners">
            <a id="past_partners"></a>
            <div class="header_2">
                Past Partners
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.imb.uq.edu.au/">
                <img src="/images/logos/STE_IMB.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.qcmg.org/">
                <img src="/images/logos/STE_QCMQ.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.griffith.edu.au/">
                <img src="/images/logos/STE_Griffith.png"></img>
                </a>
            </div>
            <div class="vertical_align">
                <a target="_blank" href="http://www.griffith.edu.au/science-aviation/eskitis-institute">
                <img src="/images/logos/STE_NCASCR.png"></img>
                </a>
            </div>
            <div class="clear"></div>
        </div>
        <div class="content_box">
            <a id="links_we_like"></a>
            <div class="header_2">
                Links we like
            </div>
            <div class="links_we_like">
                    <div><a target = "_blank" href="http://www.ebi.ac.uk/arrayexpress/">ArrayExpress</a></div>
                    <div><a target = "_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/">GenePattern</a></div>
                    <div><a target = "_blank" href="http://www.tm4.org/mev.html">MeV Multi-experiment viewer</a></div>
                    <div><a target = "_blank" href="http://www.ncbi.nlm.nih.gov/gene">Entrez Gene</a></div>
                    <div><a target = "_blank" href="http://www.ensembl.org/index.html">Ensembl genome</a></div>
                    <div><a target = "_blank" href="http://ensembl.org/info/data/biomart.html">Biomart - ENSEMBL tables of gene annotations</a></div>
                    <div><a target = "_blank" href="http://www.bioconductor.org/">Bioconductor - community driven analysis tools</a></div>
                    <div><a target = "_blank" href="http://bioinfogp.cnb.csic.es/tools/venny/index.html">Venny - Venn diagram generator</a></div>
                    <div><a target = "_blank" href="http://www.stembase.ca/?path=/">StemBase - large set of Stem Cell microarray experiments</a></div>
                    <div><a target = "_blank" href="http://biogps.org">BioGPS - tissue atlas of gene expression</a></div>
                    <div><a target = "_blank" href="http://bioinfo.wilmer.jhu.edu/tiger/">TiGER - analysis of cis-regulatory groups across an atlas of gene expression</a></div>
                    <div><a target = "_blank" href="http://fungene.cme.msu.edu/index.spr">FunGene - a great source for community driven gene annotations</a></div>
                    <div><a target = "_blank" href="http://www.stembook.org/">StemBook - The Harvard Stem Cell Institute's collection of stem cell e-books, protocols and opinions</a></div>
                    <div><a target = "_blank" href="http://www.wikigenes.org">WikiGenes - community driven gene annotation</a></div>
                    <div><a target = "_blank" href="http://www.wikipathways.org/index.php/WikiPathways">WikiPathway - community driven pathway annotation</a></div>
                    <div><a target = "_blank" href="http://www.genome.jp/kegg/">KEGG - Kyoto Encyclopaedia of Genes and Genomes</a></div>
                    <div><a target = "_blank" href="http://www.ncbi.nlm.nih.gov/">NCBI - the definitive source of information for genes and genomes</a></div>
                    <div><a target = "_blank" href="http://pb.apf.edu.au/phenbank/incidentalSNPs.html">The Australian Phenomics mouse strain archive</a></div>
                    <div><a target = "_blank" href="http://www.antibodypedia.com/">Antibodypedia - a collection of antibodies that cover most of the human protein-coding genes</a></div>
                    <div><a target = "_blank" href="http://www.cellreprogrammingaust.com/">Cell Reprogramming Australia</a></div>
                    <div><a target = "_blank" href="http://www.pantherdb.org/">Panther Classification System</a></div>

               <div class="clear"></div>
            </div>
        </div>
    </div>
</div>
