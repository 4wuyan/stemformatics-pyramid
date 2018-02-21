<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
	<script type="text/javascript" src="${h.url('/js/projects/project_grandiose.js')}"></script>
</%def>

<%def name="content_menu_pg()">
        <a href="${h.url('/projects/project_grandiose#introduction')}"> 
            <div class="contact_menu selected">
                <div class="contact_menu_title">Introduction</div>
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
    Welcome to the reviewer page for Project Grandiose and ${c.site_name}.
                </div>
                <div class="text">
                  <p>
                        This page is specifically designed to take you to the datasets quickly. It is a cut-down version of what the landing page proper will look like in ${c.site_name} after publication. </p><p>This site is best viewed with the latest Google Chrome or Mozilla Firefox.  For Internet Explorer users, ${c.site_name} only supports Internet Explorer 9+ due to limitations with previous Internet Explorer versions.</p><p>To view all datasets via the datasets search, please search on "Project Grandiose". A quick link of this search is below:
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?filter=project grandiose')}">All Project Grandiose Datasets in ${c.site_name}</a></li>
                        
                        </ul>   
                    </p>
<p>
Visualise, analyse and download published gene lists here:
</p>
                  <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=project grandiose')}">All Project Grandiose Gene Lists in ${c.site_name}</a></li>
                        
                        </ul>   
                    </p>                    
                
<p>
Contact Andras Nagy or visit his lab's homepage here:
</p>
                  <p>
                        <ul>
                            <li><a target = "_blank" href="http://research.lunenfeld.ca/nagy/contactus.html">Contact Andras Nagy</a></li>
                            <li><a target = "_blank" href="http://research.lunenfeld.ca/nagy/">Nagy Lab Website</a></li>
                        
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
    There are four chromatin datasets: three ChIP directed at Histone H3 trimethylation marks (H3K27me3; H3K4me3; H3K36me3), as well as bisulfite sequencing of methylated CpG DNA.
                </div>
                <div class="text">
                    <p>
Project Grandiose interrogated the transitioning chromatin states of reprogrammed cells using Chromatin Immunoprecipitation methods (pdf link) with antibodies to Histone H3K27me3; H3K4me3 and H3K36me3.
                    </p>
                    <p>
H3K27me3 is typically a repressive mark directed by the polycomb repressive complex, but also identifies a subset of  bivalent promoters when colocalised with H3K4me3
H3K4me3 is typically associated with actively transcribed chromatin as it facilitates TFIID, but also identifies a subset of bivalent promoters when present with H3K27me3.
H3K36me3 is a co-transcriptional event that marks transcript elongation, suppresses histone acetylation and reduces histone exchange.
                    </p>

                    <p>
DNA methylation was also assessed across the reprogramming time course.
                    </p>

                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?filter=grandiose and methylation')}">All Project Grandiose Chromatin Datasets in ${c.site_name}</a></li>
                            <li><a target = "_blank" href="${h.url('/workbench/public_gene_set_index?filter=project grandiose chromatin')}">All Project Grandiose Chromatin Gene Lists in ${c.site_name}</a></li>
                            <li><a target = "_blank" href="#">Go to the "An epigenomic roadmap to induced pluripotency" paper</a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Seo Lab 
                </div>
                <div class="text">
                    <p>
                        Chromatin datasets were generated by Professor Jeong-Sun Seo at the Genomic Medicine Institute, South Korea.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Genomic Medicine Institute website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Contact Jeong-Sun Seo</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Contact Andras Nagy</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
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
                    There are 5 datasets to do with the transcriptome
                </div>
                <div class="text">
                    <p>
                        There are two datasets, the original microarray and a new microarry by Peter Tonge.
                    </p>
                    <p>
                        You can access both datasets by clicking on the link below and there is also a link to the Cell State satellite paper.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?filter=grandiose and mrna')}">All Project Grandiose Transcriptome Datasets in ${c.site_name}</a></li>
                            <li><a target = "_blank" href="#">Project Grandiose Cell State Paper</a></li>
                            <li><a target = "_blank" href="#">Project Grandiose miRNA Paper</a></li>
                            <li><a target = "_blank" href="#">Project Grandiose RNASeq Paper</a></li>
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Nagy Lab 
                </div>
                <div class="text">
                    <p>
                        This is the Nagy lab at the Samuel Lunenfeld Research Institute,Mount Sinai Hospital. 
                    </p>
                    <p>
Lorem Ipsumn
                    </p>
                    <p>
                    <p>
    Please click below to see the Nagy website.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://research.lunenfeld.ca/nagy/">Nagy Lab Website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Grimmond Lab 
                </div>
                <div class="text">
                    <p>
                        This is the QCMG lab at IMB.
                    </p>
                    <p>
                    Lorem Ipsum
                    </p>
                    <p>
                    <p>
    Please click on the link below to access the QCMG website.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://www.qcmg.org/">Queensland Centre for Medical Genomics</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Preiss Lab 
                </div>
                <div class="text">
                    <p>
                        This is the Preiss lab at the John Curtin School of Medical Reasearch, Australian National University
                    </p>
                    <p>
Lorem Ipsum

                    </p>
                    <p>
                    <p>
        You can access the Preiss lab website below.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://jcsmr.anu.edu.au/research/genome-biology/rna-biology">Preiss Lab Website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>            <div class="content_box">
                <div class="header_2">
                    Cloonan Lab 
                </div>
                <div class="text">
                    <p>
                        This is the Cloonan Lab
                    </p>
                    <p>
Lorem Ipsum

                    </p>
                    <p>
                    <p>
Blah
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://www.qimr.edu.au/page/Lab/Genomic-Biology/">Cloonan Lab Website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
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
                    There were two types of protein data, the cell surface and a global preteome
                </div>
                <div class="text">
                    <p>
                        The Cell Surface Proteome data was provided by the Zandstra lab and the Global Proteome data was provided by the Heck lab.
                    </p>
                    <p>
                        There were over 400 proteins and 6000 proteins looked at in the Cell Surface and Global data respectively.
                    </p>
                    <p>
                    <p>
                    From this page you can view all the Project Grandiose Proteome datasets and the satellite papers with the links below.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/datasets/search?filter=grandiose and proteome')}">All Project Grandiose Proteome Datasets in ${c.site_name}</a></li>
                            <li><a target = "_blank" href="#">Project Grandiose Global Proteome Paper</a></li>
                            <li><a target = "_blank" href="#">Project Grandiose Cell Surface Proteome Paper</a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Heck Lab 
                </div>
                <div class="text">
                    <p>
                        This is Heck lab in Utrect University
                    </p>
                    <p>
Lorem Ipsum

                    </p>
                    <p>
                    <p>
                    Please click on the link below to view the Heck lab website.    
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://hecklab.com">Heck Lab Website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Zandstra Lab 
                </div>
                <div class="text">
                    <p>
                        This is Zandstra lab in University of Toronto
                    </p>
                    <p>
Lorem Ipsum

                    </p>
                    <p>
                    <p>
                        Please click on the link below to view the Zandstra lab website.    
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://stemcell.ibme.utoronto.ca/about_us.html">Zandstra Lab Website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
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
                    Data Visualation support and support was provided by various labs.
                </div>
                <div class="text">
                    <p>
    In this project, new ways of visualising data both in ${c.site_name} and by more normal bioinformatics methods were tested and improved.
                    </p>
                    <p>
    To see the satellite paper, you can click on the link below.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="#">Project Grandiose ${c.site_name} Paper</a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    QFAB
                </div>
                <div class="text">
                    <p>
                        This is the QFAB located in IMB.
                    </p>
                    <p>
Lorem ipsum
                    </p>
                    <p>
                    <p>
    Please click on the link below to access the About Us on ${c.site_name}.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="http://mixology.qfab.org/lecao/">Dr. Kim-Anh Lê Cao website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Wells Lab 
                </div>
                <div class="text">
                    <p>
                        This is the Wells lab at AIBN.
                    </p>
                    <p>
Lorem ipsum
                    </p>
                    <p>
                    <p>
    Please click on the link below to access the About Us on ${c.site_name}.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="${h.url('/contents/about_us')}">${c.site_name} About Us</a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>
            <div class="content_box">
                <div class="header_2">
                    Mar Lab 
                </div>
                <div class="text">
                    <p>
                        This is the Mar lab at NY.
                    </p>
                    <p>
    She knows Albert Einstein. 
                    </p>
                    <p>
                    <p>
    Please click on the link below to access the About Us on ${c.site_name}.
                    </p>
                    <p>
                        <ul>
                            <li><a target = "_blank" href="https://sites.google.com/site/marlabeinstein/">Mar Lab website</a></li>
                            <li><a target = "_blank" href="http://www.gmi.ac.kr/">Methods used </a></li>
                        
                        </ul>   
                    </p>
                    <div class="clear"></div>
                    
                </div>
                
            </div>        </div>
    </div>
</div>

