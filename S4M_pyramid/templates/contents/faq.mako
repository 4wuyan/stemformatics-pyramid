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
This is the Help and Frequently Asked Questions page for ${c.site_name}
            </div>
            <div class="text">
            <p>This provides you with hands-on tutorials and frequently asked questions to help you get started or answer questions in ${c.site_name}.</p>
            </div>
        </div>
        <div class="content_box">
            <div class="content_links">
                <a href="#citation">How to Cite Us ></a>
                <a href="#tutorials">Tutorials to get started ></a>
                <a href="#faq">FAQ ></a>
                <div class="clear"></div>
            </div>
       </div>
       ${Base.citation_content()}
       <div id="more_tutorials" class="content_box">
            <a id="tutorials"></a>
            <div class="header_2">
                Tutorials
            </div>
            <div class="text">
                <ul class="tutorialList">
                % for tutorial, start_page in c.tutorials.iteritems():
                    <li><a href="${h.url(start_page + '#tutorial=' + tutorial)}" onclick="return audit_help_log ('${tutorial}', 'help_tutorial'); ">${tutorial.replace("_", " ").capitalize()}</a></li>
                % endfor
                </ul>
            </div>


       </div>



       <div class="content_box faq">
            <a id="faq"></a>
            <div class="header_2">
                FAQ
            </div>
            <div class="text">
                <p class="question">
What is the best screen resolution and browser to use with ${c.site_name}?
                </p>
                <p class="answer">
The minimum recommended screen resolution for ${c.site_name} is 1152px (width) x 864px (height). ${c.site_name} is 100% compatible with the latest Google Chrome and Mozilla Firefox. <br/><br/>Please note that only Internet Explorer 11 is currently supported.  All other Internet Explorers 10 and below are not supported. You can download Firefox for free at <a target = "_blank" href="http://www.mozilla.org/">Mozilla.org</a>. You can download Google Chrome for free at <a target="_blank" href="http://www.google.com/chrome">Google.com</a>.
                </p>

                <p class="question">
How can I get my favourite dataset into ${c.site_name}?
                </p>
                <p class="answer">
                You can suggest a dataset that goes straight into our dataset queue, Agile_org.
                <ul><li>
                    <a target="_blank" href="/main/suggest_dataset">Click here to go to Agile_org to add a new dataset</a>
                </ul></li>

We will then review your request and provide some feedback on when this might be put into ${c.site_name}. Unfortunately, due to limited resources and potential technical issues, we may not always be able to process your request.
                </p>

                <p class="question">
How can I get my private dataset into ${c.site_name}?
                </p>
                <p class="answer">
We are currently working on the ability to provide security to handle private datasets with access based on individual or group permisisons. In the meantime, please send us an email (our details are on the Contact page) with your details and we can keep you informed of our progress.
                </p>

                <p class="question">
Why do I get multiple genes back from a gene search?
                </p>
                <p class="answer">
We use gene annotations from Ensembl and Entrez. In cases where Ensembl have provided multiple Entrez IDs for their genes, we retrieve all associated gene symbols. The first gene symbol retrieved in such cases is the more trusted (canonical) symbol, usually sourced from HGNC (HUGO Gene) or MGI (Mouse Genome Informatics) for human and mouse gene annotations, respectively. For gene disambiguity, please refer to the Ensembl and Entrez links for your gene of interest.
                </p>

                <p class="question">
Why is there sometimes no data available for my favourite stem cell gene (such as NANOG, SOX2, OCT4, MYC), or other genes for a given dataset?
                </p>
                <p class="answer">
Currently, we rely on microarray probe mappings provided by Ensembl for the various microarray platforms used in the experiments associated with our expression datasets. On some platforms, there are no reliable probe mappings to the genomic sequences associated with these genes of interest. In such cases, we unfortunately cannot show expression for these genes. Note that this does not mean that these genes are not present or not expressed in the available data - only that we have no means to detect their presence (or absence) for a given platform.
                </p>

                <p class="question">
Are gene expression results accurate for my gene of interest?
                </p>
                <p class="answer">
The accuracy of gene detection and expression for a particular gene are constrained by the combination of the accuracy of a given microarray platform's probe sequences and probe set mappings to transcript sequences. Furthermore, we rely upon the accuracy of Ensembl's probe-to-transcript and transcript-to-gene mappings. Most probes map to a single gene, but some (about 7%) map to multiple genes (usually two, rarely more). If in doubt, refer to Ensembl's probe mapping pipeline for more information.
                </p>
                <p class="question">
How do you handle probes that map to multiple genes?
                </p>
                <p class="answer">
We show all probe expressions. Multi-mapping probes are highlighted in our graphs however; to see what other genes map to these probes, click on the probe IDs to access the multi-mapping probe summary page for this probe.
                </p>

                <p class="question">
How are biological sample replicates treated in our expression data and statistics?
                </p>
                <p class="answer">
Across the site, we use and display data pertaining to biological replicates that have been collapsed (averaged), with few exceptions. In our expression results, only scatter plots show un-collapsed sample expression, however the bar graphs and box plots aggregate biological replicate samples for a given sample or chip type (or other experimental metadata). In these cases, we provide error bars and standard deviations for sample expression.
                </p>

                <p class="question">
What do the lines in the expression graphs represent?
                </p>
                <p class="answer">
Two measures were taken for each dataset. The blue line is representative of the detection threshold (minimum level for this dataset where the gene is said to be detected) and the green line is representative of the median of normalized detection scores for all genes in the dataset.
                </p>

                <p class="question">
In the public gene lists, why are some genes missing from Kegg pathways?
                </p>
                <p class="answer">
These Kegg pathways were downloaded using the R Bioconductor library Kegg.db. This library used Entrez identifiers and these were converted to Ensembl identifiers via ${c.site_name} mapping and stored in the database. Around 5% of the mouse Entrez identifiers could not be converted to Ensembl and 2% of the human Entrez identifiers could not be converted to Ensembl.
                </p>
                <p class="question">
How can I access the probe-to-gene (or other reporter-to-gene) mappings for an assay platform?
                </p>
                <p class="answer">
You can download the mapping files from <a href="${h.url('/contents/download_mappings')}">here.</a>
                </p>
            </div>
       </div>


    </div>
</div>
