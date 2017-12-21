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
${c.site_name} is driven by the desire to help researchers publish papers
            </div>
            <div class="text">
            <p>${c.site_name} was designed to allow researchers the ability to visually analyze and explore their data and high class datasets quickly and easily to allow them to get on with the serious job of publishing papers.</p>
            <p>Please cite us appropriately and have a look at the publications we have been associated with or helped with so far.</p>
            </div>
        </div>
        <div class="content_box">
            <div class="content_links">
                <a href="#citation">How to Cite Us ></a>
                <a href="#publications">Data Publications ></a>
                <a href="#bioinformatics_publications">Bioinformatics Publications ></a>
                <div class="clear"></div>
            </div>
       </div>
       ${Base.citation_content()}
       <div class="content_box publications">
            <a id="publications"></a>
            <div class="header_2">
                Data Publications
            </div>

            %for row in c.data_publications:

                <%
                ds_id = row['ds_id']
                try:
                    title = row['Publication Title']
                except:
                    title = ""
                try:
                    citation = row['Publication Citation']
                except:
                    citation = ""
                try:
                    authors = row['Authors']
                except:
                    authors = ""
                try:
                    abstract = row['Description']
                except:
                    abstract = ""
                try:
                    pub_med_id = row['PubMed ID']
                except:
                    pub_med_id = ""


                %>
                <div class="text">
                    <p class="title">${title}</p>
                    <p class="authors">${authors}</p>
                    <p class="publication">${citation}</p>
                    <p class="abstract">${abstract}</p>
%if pub_med_id != None and pub_med_id != "NULL" and pub_med_id != "":
                    <p class="link"><a target="_blank" href="http://www.ncbi.nlm.nih.gov/pubmed/${pub_med_id}">View article in PubMed</a>
%endif
                    <p class="link"><a href="${h.url('/datasets/search?ds_id=')}${ds_id}">View data in ${c.site_name}</a>
                    </p>

                </div>




            %endfor
        </div>
        <div class="content_box publications">
            <a id="bioinformatics_publications"></a>
            <div class="header_2">
                Bioinformatics Publications
            </div>

            <div class="text">

            <div class="text">
                <a id="msc_paper"></a>
                <p class="title">
A molecular classification of human mesenchymal stromal cells</p>
                <p class="authors">
Florian Rohart, Elizabeth A. Mason, Nicholas Matigian, Rowland Mosbergen, Othmar Korn, Tyrone Chen, Suzanne Butcher, Jatin Patel, Kerry Atkinson, Kiarash Khosrotehrani, Nicholas M. Fisk, Kim-Anh Lê Cao, Christine A. Wells
                </p>
                <p class="publication">
PeerJ. 2016 Mar 24;4:e1845. doi: 10.7717/peerj.1845. eCollection 2016.
                </p>
                <p class="abstract">
Mesenchymal stromal cells (MSC) are widely used for the study of mesenchymal tissue repair, and increasingly adopted for cell therapy, despite the lack of consensus on the identity of these cells. In part this is due to the lack of specificity of MSC markers. Distinguishing MSC from other stromal cells such as fibroblasts is particularly difficult using standard analysis of surface proteins, and there is an urgent need for improved classification approaches. Transcriptome profiling is commonly used to describe and compare different cell types; however, efforts to identify specific markers of rare cellular subsets may be confounded by the small sample sizes of most studies. Consequently, it is difficult to derive reproducible, and therefore useful markers. We addressed the question of MSC classification with a large integrative analysis of many public MSC datasets. We derived a sparse classifier (The Rohart MSC test) that accurately distinguished MSC from non-MSC samples with >97% accuracy on an internal training set of 635 samples from 41 studies derived on 10 different microarray platforms. The classifier was validated on an external test set of 1,291 samples from 65 studies derived on 15 different platforms, with >95% accuracy. The genes that contribute to the MSC classifier formed a protein-interaction network that included known MSC markers. Further evidence of the relevance of this new MSC panel came from the high number of Mendelian disorders associated with mutations in more than 65% of the network. These result in mesenchymal defects, particularly impacting on skeletal growth and function. The Rohart MSC test is a simple in silico test that accurately discriminates MSC from fibroblasts, other adult stem/progenitor cell types or differentiated stromal cells. It has been implemented in the www.stemformatics.org resource, to assist researchers wishing to benchmark their own MSC datasets or data from the public domain. The code is available from the CRAN repository and all data used to generate the MSC test is available to download via the Gene Expression Omnibus or the Stemformatics resource.
                </p>
                <p class="link">
                    <a href="https://peerj.com/articles/1845/">View article here</a>
                </p>
            </div>

            <div class="text">
                <p class="title">
Stemformatics: Visualisation and sharing of stem cell gene expression
                </p>
                <p class="authors">
Wells CA, Mosbergen R, Korn O, Choi J, Seidenman N, Matigian NA, Vitale AM, Shepherd J.
                </p>
                <p class="publication">
Stem Cell Research May 2013
                </p>
                <p class="abstract">
Genome-scale technologies are increasingly adopted by the stem cell research community, because of the potential to uncover the molecular events most informative about a stem cell state. These technologies also present enormous challenges around the sharing and visualisation of data derived from different laboratories or under different experimental conditions. Stemformatics is an easy to use, publicly accessible portal that hosts a large collection of exemplar stem cell data. It provides fast visualisation of gene expression across a range of mouse and human datasets, with transparent links back to the original studies. One difficulty in the analysis of stem cell signatures is the paucity of public pathways/gene lists relevant to stem cell or developmental biology. Stemformatics provides a simple mechanism to create, share and analyse gene sets, providing a repository of community-annotated stem cell gene lists that are informative about pathways, lineage commitment, and common technical artefacts. Stemformatics can be accessed at stemformatics.org.
                </p>
                <p class="link">
                    <a href="http://www.sciencedirect.com/science/article/pii/S1873506112001262">View article here</a>
                </p>
            </div>
            <div class="text">
                <p class="title">
Method: "attract" A method for identifying core pathways that define cellular phenotypes
                </p>
                <p class="authors">
Mar JC, Matigian NA, Quackenbush J, Wells CA.
                </p>
                <p class="publication">
PLoS ONE October 14 2011
                </p>
                <p class="abstract">
attract is a knowledge-driven analytical approach for identifying and annotating the gene-sets that best discriminate between cell phenotypes. attract finds distinguishing patterns within pathways, decomposes pathways into meta-genes representative of these patterns, and then generates synexpression groups of highly correlated genes from the entire transcriptome dataset. attract can be applied to a wide range of biological systems and is freely available as a Bioconductor package, has been incorporated into the MeV software system.
                </p>
                <p class="link">
                    <a href="http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0025445">View article here</a>
                </p>
            </div>
            <div class="text">
                <p class="title">
Variance of Gene Expression Identifies Altered Network Constraints in Neurological Disease.
                </p>
                <p class="authors">
Mar JC, Matigian NA, Mackay-Sim A, Mellick GD, Sue CM, Silburn PA, McGrath JJ, Quackenbush J, Wells CA.
                </p>
                <p class="publication">
PLoS Genetics 2011 August 11
                </p>
                <p class="abstract">
Gene expression analysis has become a ubiquitous tool for studying a wide range of human diseases. In a typical analysis we compare distinct phenotypic groups and attempt to identify genes that are, on average, significantly different between them. Here we describe an innovative approach to the analysis of gene expression data, one that identifies differences in expression variance between groups as an informative metric of the group phenotype. We find that genes with different expression variance profiles are not randomly distributed across cell signaling networks. Genes with low-expression variance, or higher constraint, are significantly more connected to other network members and tend to function as core members of signal transduction pathways. Genes with higher expression variance have fewer network connections and also tend to sit on the periphery of the cell. Using neural stem cells derived from patients suffering from Schizophrenia (SZ), Parkinson's disease (PD), and a healthy control group, we find marked differences in expression variance in cell signaling pathways that shed new light on potential mechanisms associated with these diverse neurological disorders. In particular, we find that expression variance of core networks in the SZ patient group was considerably constrained, while in contrast the PD patient group demonstrated much greater variance than expected. One hypothesis is that diminished variance in SZ patients corresponds to an increased degree of constraint in these pathways and a corresponding reduction in robustness of the stem cell networks. These results underscore the role that variation plays in biological systems and suggest that analysis of expression variance is far more important in disease than previously recognized. Furthermore, modeling patterns of variability in gene expression could fundamentally alter the way in which we think about how cellular networks are affected by disease processes.
                </p>
                <p class="link">
                    <a href="http://www.plosgenetics.org/article/info%3Adoi%2F10.1371%2Fjournal.pgen.1002207">View article here</a>
                </p>
            </div>
            <div class="text">
                <p class="title">
Defining an informativeness metric for clustering gene expression data.
                </p>
                <p class="authors">
Mar JC, Wells CA, Quackenbush J.
                </p>
                <p class="publication">
Bioinformatics 2011 April 15
                </p>
                <p class="abstract">
MOTIVATION: Unsupervised 'cluster' analysis is an invaluable tool for exploratory microarray data analysis, as it organizes the data into groups of genes or samples in which the elements share common patterns. Once the data are clustered, finding the optimal number of informative subgroups within a dataset is a problem that, while important for understanding the underlying phenotypes, is one for which there is no robust, widely accepted solution.

RESULTS: To address this problem we developed an 'informativeness metric' based on a simple analysis of variance statistic that identifies the number of clusters which best separate phenotypic groups. The performance of the informativeness metric has been tested on both experimental and simulated datasets, and we contrast these results with those obtained using alternative methods such as the gap statistic.
                </p>
                <p class="link">
                    <a href="http://www.ncbi.nlm.nih.gov/pubmed/21330289">View article here</a>
                </p>
            </div>
        </div>

    </div>
</div>

<div class="hidden">
            <div class="text">
                <p class="title">
                </p>
                <p class="authors">
                </p>
                <p class="publication">
                </p>
                <p class="abstract">
                </p>
                <p class="link">
                    <a href="">View article here</a>
                </p>
            </div>
</div>
