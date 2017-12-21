<%def name="default_inclusions()">
    <% from S4M_pyramid.config import config %>
    <title>${c.title}</title>
    <meta name="google-site-verification" content="eKfRHsSQKFfEQDBulOvJy8P1H6d5PpjgRp8IoMXgE0A"/>
	<!-- <meta http-equiv="content-language" content="en-us" /> -->
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />

        <meta name="author" content="Australian Institute of Bioengineering and Nanotechnology (AIBN)" />
        <meta name="description" content="" />
        <meta name="keywords" content="microarray, gene expression" />

    <!-- Task #426 Safari iPhone issue -->
    <meta name="format-detection" content="telephone=no"/>
    <!-- jQuery, jQuery-UI and additional plug-ins should go here. -->
    <script type="text/javascript" src="${h.external_dependency_url('ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js','/js/external_asset_dependencies/jquery-1.8.2.min.js')}"></script>



    <!-- jQuery css is included first.  Add other .css files after this line. -->
    % if not hasattr(c,'speed_up_page') or (hasattr(c,'speed_up_page') and c.speed_up_page != 'true'):
        <link rel="stylesheet" type="text/css" href="${h.external_dependency_url('ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/css/jquery.dataTables.css','/css/external_asset_dependencies/jquery-1.9.4.dataTables.css')}">
        <script type="text/javascript" charset="utf8" src="${h.external_dependency_url('ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js','/js/external_asset_dependencies/jquery-1.9.4.dataTables.min.js')}" ></script>
        <script src="${h.external_dependency_url('cdn.jsdelivr.net/simplemodal/1.4.4/jquery.simplemodal.min.js','/js/external_asset_dependencies/jquery-1.4.4.simplemodal.min.js')}" ></script>

        <link href="${h.web_asset_url('/css/combined_jquery_ui_tripoli_full.min.css')}" type="text/css" rel="stylesheet"/>

    % endif

    % if c.production != 'true':
        % if c.production == "local":
            <link type="text/css" href="${h.url('/css/local-development.css')}"} rel="stylesheet" />
        % else:
            <link type="text/css" href="${h.url('/css/development.css')}"} rel="stylesheet" />
        %endif
    % endif

    % if c.production != 'true' or c.debug is not None:
        <script type="text/javascript" src="${h.url('/js/main.js')}"></script>
        <script type="text/javascript" src="${h.url('/js/table2CSV.js')}"></script>
    %else:
        <script src="${h.web_asset_url('/js/main_table2CSV_help_min.js')}" type="text/javascript"></script>
    %endif


    <link href="${h.web_asset_url('/css/sass/stylesheets/screen.css')}" type="text/css" rel="stylesheet"/>


    <script type="text/javascript">
    <%
      basePath = config['proxy-path'] if 'proxy-path' in config and config['proxy-path'] is not None else '/'
      basePath += '/' if basePath[-1] != '/' else ''
    %>
        var BASE_PATH = "${basePath}";
    var DELIMITER = "${config['delimiter']}";
    var SITE_NAME = "${c.site_name}";
    check_browser(); // this relies on main.js
    </script>




    <script type="text/javascript" src="${h.external_dependency_url('ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js','/js/external_asset_dependencies/jquery-1.10.2-ui.min.js')}" ></script>
    <script type="text/javascript" src="${h.external_dependency_url('cdnjs.cloudflare.com/ajax/libs/marked/0.3.1/marked.min.js','/js/external_asset_dependencies/marked-0.3.1.min.js')}" ></script>
    <script src="${h.external_dependency_url('cdn.jsdelivr.net/jquery.cookie/1.3/jquery.cookie.js','/js/external_asset_dependencies/jquery-1.3.cookie.js')}" ></script>
    <script src="${h.external_dependency_url('cdn.jsdelivr.net/guiders.js/1.3.0/guiders-1.3.0.js','/js/external_asset_dependencies/guiders-1.3.0.js')}" ></script>


    <script src="${h.web_asset_url('/help/helpsystem.js')}" type="text/javascript"></script>



    % if 'turn_on_google_analytics' in config and config['turn_on_google_analytics'] == 'true':
	<script type="text/javascript" >
      var _gaq = _gaq || [];

      _gaq.push(['_setAccount', '${config['google_analytics_tracking_id']}']);
      _gaq.push(['_setDomainName', 'none']);
      _gaq.push(['_setAllowLinker', true]);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script>
    % endif

% if 'turn_on_cookie_consent_plugin' in config and config['turn_on_cookie_consent_plugin'] == 'true':

<!-- Begin Cookie Consent plugin by Silktide - http://silktide.com/cookieconsent -->
<script type="text/javascript">
// <![CDATA[
cc.initialise({
 cookies: {
 analytics: {}
 },
 settings: {
 consenttype: "implicit",
 onlyshowbanneronce: true,
 hideallsitesbutton: true,
 hideprivacysettingstab: true,
 disableallsites: true,
 bannerPosition: "push",
 tagPosition: "vertical-right",
 useSSL: true
 }
});
// ]]>

</script>

<!-- End Cookie Consent plugin -->

%endif


</%def>

<%def name="help_icon()">
    <div class="help_icon"><a href="${h.url('/contents/faq')}"><img src="/images/icons/help_icon.png"></img></a>
        <ul class="main_help_menu" >
        %try:
            %if  c.tutorials_for_page['page_guide'] is not None:
                <li><a class="page_guide" href="#">Toggle in-page help</a></li>
            %else:
                <li><a  href="#">No in-page help for this page</a></li>
            %endif
        %except:
                <li><a  href="#">No in-page help for this page</a></li>
        %endtry


            <li class="sep"></li>
<%
this_path = '/'+url.environ['pylons.routes_dict']['controller'] + '/' + url.environ['pylons.routes_dict']['action']
 %>
                % for tutorial, start_page in c.tutorials.items():
        <%
class_text= 'class = in_page_tutorial_link' if this_path == start_page else ''
import string
        %>


                    <li><a ${class_text} href="${h.url(start_page + '#tutorial=' + tutorial)}" onclick = "return audit_help_log('${tutorial}','help_tutorial');" data-tutorial='${tutorial}'>${string.capwords(tutorial.replace("_", " "))} Tutorial</a></li>
                % endfor
                                                <li class="sep"></li>
                                                <li><a href="${h.url('/contents/faq')}">General Help &amp; FAQ</a></li>

                                           </ul>
    </div>
</%def>

<%def name="default_inclusions_wb()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/wb_default.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/wb_main.js')}"></script>
</%def>

<%def name="wb_breadcrumbs()">
    <div id="breadcrumb">
        <%
            try:
                c.breadcrumbs
            except:
                c.breadcrumbs = []

        %>

        % for link in c.breadcrumbs:

            <%
                lastIndex = len(c.breadcrumbs) -1
                currentIndex = c.breadcrumbs.index(link)
                linkUrl = link[0]
                linkName = link[1]

            %>

            % if lastIndex == currentIndex:
                <span class="current">${linkName}</span>
            % else:
                <a class="basic_link" href="${linkUrl}">${linkName}</a> >>
            % endif


        % endfor

    </div>
    <div class="clear"></div>

</%def>

<%def name="header()">
        % try:
            %if c.header is not None and c.header != '':
                <div id="header" class="other_banner ${c.header}">
                <% project_url ='/projects/'+c.header %>
            %else:
                <div id="header" >
                <% project_url ='/' %>
            %endif
        % except AttributeError:
            <div id="header">
        % endtry
                <div class="limitedHeader">
                    ##% if c.production:
                        <a class="logo" href="${h.url('/')}" data_hover_text="Click for home page"></a>
                    ##% else:
                    ##    <div id=warning>${c.site_name} Development - this is only for testing datasets and functionality</div>
                    ##% endif
                    <a href="${h.url(project_url)}"><div id="project_logo" class="${c.header}"></div></a>

                    % if c.user == "" :
                    <div class="rightHeader">
                    % else:
                    <div class="rightHeader logged_in">
                    %endif
                        <div class="user-info">
                            <div class="hidden" id="user">${c.user}</div>
                            <div class="full_name" id="full_name">${c.full_name}</div>
                            <div class="hidden" id="uid">${c.uid}</div>
                        </div>
                        <div class="login-tasks">
                            % if c.user == "" :
                                <a class="no_padding_right" href="${h.url('/auth/login')}">Login</a><br/><a class="no_padding_right" href="${h.url('/auth/register')}">Register</a><br/><a href="${h.url('/auth/forgot_password')}">Forgot pass phrase</a>
                            % else:
                                <a id="logout_link" href="${h.url('/auth/logout')}">Logout </a>|<a href="${h.url('/auth/history/show')}">History</a>|<a class="no_padding_right" href="${h.url('/auth/update_details')}">My account</a><br/><a href="${h.url('/ensembl_upgrade/index')}">Ensembl upgrade</a>|<a class="no_padding_right"
href="${h.url('/auth/show_private_datasets')}">My datasets</a>
                                <!-- |<a ${'id=unread_notifications' if c.notifications > 0 else ''} href="${h.url('/auth/notifications')}">My Notifications (${c.notifications})</a> -->
                            % endif
                        </div>

                    </div>
                   ${self.help_icon()}
                </div>
            </div>
            <div id="menus">
                <div id="main_headers" >

<% select_text = " class=selected " %>

                    <div class="header"><a
                        %if c.header_selected == 'genes':
                            class='selected'
                        %endif
                        id="header-genesearch-button" href="${h.url('/genes/search')}">GENES ></a>
                    </div>
                    <div class="header">
                        <a
                        %if c.header_selected == 'datasets':
                            class='selected'
                        %endif
                        id="header-datasetsearch-button" href="${h.url('/datasets/search')}">DATASETS ></a>
                    </div>
                    <div class="header"><a
                        %if c.header_selected == 'expressions':
                            class='selected'
                        %endif
                    id="header-graphs-button" href="${h.url('/expressions/index')}">GRAPHS ></a></div>
                    <div class="header"><a
                        %if c.header_selected == 'workbench':
                            class='selected'
                        %endif
                    id="header-analyses-button" href="${h.url('/workbench/index')}">ANALYSES ></a></div>
                    <div class="header"><a id="header-analyses-button" href="${h.url('/workbench/jobs_index')}">MY JOBS ></a></div>
                    <div class="header"><a
                        %if c.header_selected == 'contents':
                            class='selected'
                        %endif
                    id="header-about-us-button" href="${h.url('/contents/about_us')}">ABOUT US ></a></div>
                    <div class="header"><a id="header-analyses-button" href="${h.url('/contents/faq')}">FAQ ></a></div>
                    % if c.role=="admin":
                    <div class="header"><a
                        %if c.header_selected == 'admin':
                            class='selected'
                        %endif
                    href="${h.url('/admin/index')}">ADMIN ></a></div>
                    <div class="header"><a id="header-workbench-button" href="${h.url('/main/tests')}">TESTS ></a></div>

                    %endif
                    <!-- <div class="search"><a href="/datasets/search">CELL SEARCH ></a></div>
                    <div class="search"><a href="/datasets/search">LOCATION SEARCH ></a></div> -->
                </div>
            </div>


            %if c.role=="admin":
            <%
                query = request.environ['QUERY_STRING']
                path =  request.environ['PATH_INFO']
                if query is not None and query != "":
                    path = path + '?' + query
                other_urls = [{'name':'www1','url':'http://www1.stemformatics.org'},
{'name':'www3','url':'http://www3.stemformatics.org'},
{'name':'www5','url':'http://www5.stemformatics.org'},
{'name':'dev','url':'http://dev.stemformatics.org'},
{'name':'dev2','url':'http://dev2.stemformatics.org'},
{'name':'dev3','url':'http://dev3.stemformatics.org'}]

            %>
            <div class="admin">
                <div class="admin_top" >
                    %for url_data in other_urls:
                        <a href="${url_data['url']}${path}"  style="text-align:center;width:50px;" >${url_data['name']}</a>
                    %endfor
                    %if hasattr(c,'ds_id'):
                        <a target="_blank" href="${config['agile_org_base_url']}datasets/view/${c.ds_id}">Agile_org Dataset</a>
                    %endif
                    %if hasattr(c,'graphType') :
                        <a target="_blank" href="/admin/troubleshoot_geg?ds_id=${c.ds_id}">Troubleshoot GEG</a>
                    %endif
                        <a href="#"  style="text-align:center;width:50px;" onclick="$('div.admin').hide();">Hide</a>
                    <div class="clear"></div>
                </div>
            </div>
            <div class="clear"></div>
            %endif




</%def>


<%def name="footer()">
            <div class="clear"></div>
            <div id="footer">
                <div class="footer_central">
                    <div class="leftfooterText">
                        <span>© 2015 ${c.site_name}</span><span>${c.stemformatics_version}</span><span><a href="${h.url('/contents/disclaimer')}">Disclaimer</a></span><span><a href="${h.url('/contents/privacy_policy')}">Privacy Policy</a></span><span>${c.hostname} </span>
                    </div>
                    <div class="rightfooterText">
                        <span class="website">Website hosted by </span><a class="qcif" href="http://www.qcif.edu.au"></a>  <a class="nectar" href="http://nectar.org.au"></a>
                    </div>
                </div>
            </div>

            <div id="modal_div" class="modal">

                <div id="wb_modal_title" class="wb_modal_title">

                </div>
                <div id="wb_modal_content" class="wb_modal_content">

                </div>

            </div>
            <div id='guide-wrapper'></div>
            <div id='generic_tooltip'></div>
            <div id='tutorials_for_page' class="hidden">${c.json_tutorials_for_page}</div>
</%def>


<%def name="sideColumnHelpAboutUs()">
            <h1>How to cite us</h1>
            <div class="ruler"></div>
            <div class="text">
               Please ensure that you cite the original publications describing the datasets hosted by ${c.site_name}.
<br/>
<br/>
To cite Stemforamtics, please use:
<br/>
Wells CA et al Stemformatics: Visualisation and sharing of stem cell gene expression. Stem Cell Research, DOI http://dx.doi.org/10.1016/j.scr.2012.12.003
<br/>
<br/>
<a href="http://www.sciencedirect.com/science/article/pii/S1873506112001262">Link to the article is here</a>
<br/>
<br/>

Updated citation to follow.
            </div>

            <h1>Data sources</h1>
            <div class="ruler"></div>
            <div class="text">
                <ul>
                    <li><span>We share all of our published datasets with <a target="_blank" href="http://www.ebi.ac.uk/arrayexpress/">ArrayExpress</a></span></li>
                    <li><span>Links to publications are provided through </span><a target="_blank" href="http://www.ncbi.nlm.nih.gov/pubmed/">PubMed</a></li>
                    <li><span>We source statistical packages from </span><a target="_blank" href="http://www.bioconductor.org/">R/Bioconductor</a></li>
                </ul>
            </div>

            <h1>Academic standards</h1>
            <div class="ruler"></div>
            <div class="text">
                Our team is committed to using the highest academic standards for sharing of data. We are members of The Functional Genomics Data Society and use: <br><br>
                <ul>
                    <li><a target="_blank" href="http://www.mged.org/Workgroups/MIAME/miame.html">MIAME standards</a> <span>for gene expression datasets</span></li>
                    <li><a target="_blank" href="http://www.mged.org/Workgroups/MAGE/mage.html">MAGE formats</a> <span>for data exchange</span></li>
                    <li><span>We subscribe to </span><a target="_blank" href="http://obi-ontology.org/page/Main_Page">The Ontology for Biomedical Investigations</a><span> (OBI) project</span></li>
                </ul>
            </div>

            <h1>Protocols description</h1>
            <div class="ruler"></div>
            <div class="text">
                <a href="${h.url('/'+c.site_name+'_data_methods.pdf')}">${c.site_name} Data Methods (pdf)</a>
            </div>

            <H1>
                Links we like
            </H1>
            <div class="ruler"></div>
            <div class="text">We are not affiliated with any of the following sites, but that they are shown because we find them useful.</div>
            <div class="list">
                <ul>
                    <li><a target = "_blank" href="http://www.ebi.ac.uk/arrayexpress/">ArrayExpress</a></li>
                    <li><a target = "_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/">GenePattern</a></li>
                    <li><a target = "_blank" href="http://www.tm4.org/mev/?q=about">MeV Multi-experiment viewer</a></li>
                    <li><a target = "_blank" href="http://www.ncbi.nlm.nih.gov/gene">Entrez Gene</a></li>
                    <li><a target = "_blank" href="http://www.ensembl.org/index.html">Ensembl genome</a></li>
                    <li><a target = "_blank" href="http://www.bioconductor.org/">Bioconductor - community driven analysis tools</a></li>
                    <li><a target = "_blank" href="http://david.abcc.ncifcrf.gov/">NIH DAVID - Comprehensive geneset annotations</a></li>
                    <li><a target = "_blank" href="http://bioinfogp.cnb.csic.es/tools/venny/index.html">Venny - Venn diagram generator</a></li>
                    <li><a target = "_blank" href="http://www.stembase.ca/?path=/">StemBase - large set of Stem Cell microarray experiments</a></li>
                    <li><a target = "_blank" href="http://biogps.org">BioGPS - tissue atlas of gene expression</a></li>
                    <li><a target = "_blank" href="http://bioinfo.wilmer.jhu.edu/tiger/">TiGER - analysis of cis-regulatory groups and transcription factor pairs across an atlas of gene expression</a></li>
                    <li><a target = "_blank" href="http://fungene.cme.msu.edu/index.spr">FunGene - a great source for community driven gene annotations</a></li>
                    <li><a target = "_blank" href="http://www.stembook.org/">StemBook - The Harvard Stem Cell Institute's collection of stem cell e-books, protocols and opinions</a></li>
                    <li><a target = "_blank" href="http://stemcell.mssm.edu/v2/">SCDb - The Stem Cell Database, with a focus on the hematopoietic stem cell system</a></li>
                    <li><a target = "_blank" href="http://www.wikigenes.org">WikiGenes - community driven gene annotation</a></li>
                    <li><a target = "_blank" href="http://www.wikipathways.org/index.php/WikiPathways">WikiPathway - community driven pathway annotation</a></li>
                    <li><a target = "_blank" href="http://www.genome.jp/kegg/">KEGG - Kyoto Encyclopaedia of Genes and Genomes</a></li>
                    <li><a target = "_blank" href="http://www.ncbi.nlm.nih.gov/">NCBI - the definitive source of information for genes and genomes</a></li>
                    <li><a target = "_blank" href="http://ensembl.org/info/data/biomart.html">Biomart - ENSEMBL tables of gene annotations</a></li>
                    <li><a target = "_blank" href="http://pb.apf.edu.au/phenbank/incidentalSNPs.html">The Australian Phenomics mouse strain archive</a></li>
                    <li><a target = "_blank" href="http://www.antibodypedia.com/">Antibodypedia - a collection of antibodies from various sources that cover most of the human protein-coding genes</a></li>
                    <li><a target = "_blank" href="http://www.cellreprogrammingaust.com/">Cell Reprogramming Australia</a></li>




                </ul>
            </div>


</%def>

<%def name="sideColumnBiologists()">
            <div id="searchListSide" class="clear">
                <div class="search"><a href="${h.url('/contents/site_features')}">SITE FEATURES >></a></div>
                <div class="search"><a href="${h.url('/contents/dataset_articles')}">OVERVIEW OF DATASETS >></a></div>
                <!-- <div class="search"><a href="/contents/public">INFORMATION FOR <span>GENERAL PUBLIC</span> >> </a></div> -->

            </div>
            <div class="sideColumnList">
                <h1>Short List of Publications</h1>
                <div class="ruler"></div>
                <div class=news>
                    <div class="showText">
                        <h3><a href="${h.url('/contents/publications')}">DISEASE-SPECIFIC, NEUROSPHERE-DERIVED CELLS AS MODELS FOR BRAIN DISORDER</a></h3>
                        <div class="name"><a href="${h.url('/contents/publications')}"></a>Dis Model Mech</div>
                        <div class="date"><a href="${h.url('/contents/publications')}">November-December 2010</a></div>
                        <div class="text"><a href="${h.url('/contents/publications')}">
                           There is a pressing need for patient-derived cell models of brain diseases that are relevant and robust enough to produce the large quantities of cells required for molecular and functional analyses. We describe here a new cell model based on patient-derived cells from the human olfactory mucosa, the organ of smell, which regenerates throughout life from neural stem cells ...
                            <span class="more">read article ></span></a>
                        </div>
                    </div>

                </div>
                <div class=news>
                    <div class="showText">
                        <h3><a href="${h.url('/contents/publications')}">DEFINING AN INFORMATIVENESS METRIC FOR CLUSTERING GENE EXPRESSION DATA.</a></h3>
                        <div class="name"><a href="${h.url('/contents/publications')}"></a>Bioinformatics</div>
                        <div class="date"><a href="${h.url('/contents/publications')}">2011 April 15</a></div>
                        <div class="text"><a href="${h.url('/contents/publications')}">
                           MOTIVATION: Unsupervised 'cluster' analysis is an invaluable tool for exploratory microarray data analysis, as it organizes the data into groups of genes or samples in which the elements share common patterns. Once the data are clustered, finding the optimal number of informative subgroups within a dataset is a problem that....
                            <span class="more">read article ></span></a>
                        </div>
                    </div>

                </div>
                <div class=news>
                    <div class="showText">
                        <h3><a href="${h.url('/contents/publications')}">METHOD: "<I>ATTRACT</I>" A METHOD FOR IDENTIFYING CORE PATHWAYS THAT DEFINE CELLULAR PHENOTYPES</a></h3>
                        <div class="name"><a href="${h.url('/contents/publications')}"></a>To be announced</div>
                        <div class="date"><a href="${h.url('/contents/publications')}">To be announced</a></div>
                        <div class="text"><a href="${h.url('/contents/publications')}">
                           <i>attract</i> is a knowledge-driven analytical approach for identifying and annotating the gene-sets that best discriminate between cell phenotypes. <i>attract</i> finds distinguishing patterns within pathways, decomposes pathways into meta-genes representative of these patterns, and then generates...
                            <span class="more">read article ></span></a>
                        </div>
                    </div>

                </div>
            </div>
</%def>


<%def name="noCache()">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
</%def>

<%def name="genomeMenu()">
     <li id="genomeMenu" class="genomeMenu">
        <a class="button dropdown"><span><span class="icon helix"></span>Genome Browser</span><span class="arrow down"></span></a>
        <ul class="submenu">
            <li><a target="_blank" href="${c.ucsc_data['base_url']}?position=chr${c.ucsc_data['chr']}:${c.ucsc_data['start']}-${c.ucsc_data['end']}&db=${c.ucsc_data['ucsc_db_id']}" id="otheh_link">UCSC Genome Browser</a></li>
        % if len(c.ucsc_links) > 0:
            <%
            ## Build dict keyed by link name for next step with lambda lower-case sort order
            name_sorted = {}
            for k, v in c.ucsc_links.iteritems():
                name_sorted[v['link_name']] = k
            %>
            % for link in sorted(name_sorted, key=lambda v: v.lower()):
                <li><a target="_blank" href="${c.ucsc_data['base_url']}?position=chr${c.ucsc_data['chr']}:${c.ucsc_data['start']}-${c.ucsc_data['end']}&db=${c.ucsc_data['ucsc_db_id']}&hgt.customText=${c.ucsc_links[name_sorted[link]]['url']}" id="AButton">${c.ucsc_links[name_sorted[link]]['group_name']} ${c.ucsc_links[name_sorted[link]]['link_name']} on UCSC Genome Browser</a></li>
            % endfor
        % endif
        </ul>
    </li>
</%def>


<%def name="choose_dataset_graph()">

    <div id="choose_dataset" class="modal">

        <div class="wb_modal_title">
            Choose Dataset by clicking on links below
        </div>

        <div id="form">
            <div class="innerDiv">
                <div class="scrollWrapper">
                    <table id="chooseDatasetTable">
                        <thead>
                            <tr>
                                <th class="th1">Name</th>
                                <th>Title</th>
                                <th>Sample/Cell Types</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for dataset in c.datasets:
                                <%
                                    organism = c.datasets[dataset]['organism']
                                    datasetID = dataset
                                    name = c.datasets[dataset]['handle']
                                    title = c.datasets[dataset]['title']
                                    cells_samples_assayed = c.datasets[dataset]['cells_samples_assayed']
                                    contact = c.datasets[dataset]['name']
                                    url_link = "&datasetID=" if c.url.find('?') != -1 else "?datasetID="

                                    # strip out any datasetID values in the url
                                    import re
                                    expression='\&datasetID=[0-9]+'
                                    clean_url = re.sub(expression,'',c.url)

                                    expression='\?datasetID=[0-9]+\&'
                                    clean_url = re.sub(expression,'?',clean_url)
                                %>

                                % if organism == c.species or c.species is None:
                                <tr>
                                    <td><a href="${clean_url}${url_link}${datasetID}">${name}</a></td>
                                    <td>${title}</td>
                                    <td>${cells_samples_assayed}</td>
                                </tr>
                                % endif

                            % endfor
                        </tbody>
                    </table>
                </div>

                <div class="clear" > </div>

            </div>
            <div class="clear" > </div>
        </div>
        <div class="clear" > </div>
    </div>
</%def>

<%def name="displayGeneDetail()" >
           <div id="displayGeneDetail" class="showDetail searchDiv hidden" >
                <div class="innerDiv">
                    <%
                        # may need to replace spaces with comma for links to NCBI
                        entrez_id = c.data[c.ensemblID]['EntrezID']


                        if (int(c.human_db) == c.db_id):
                            ensembl_link = "http://www.ensembl.org/Homo_sapiens/Gene/Summary?g="+c.ensemblID
                        else:
                            ensembl_link = "http://www.ensembl.org/Mus_musculus/Gene/Summary?g="+c.ensemblID

                        aliases = c.data[c.ensemblID]['Synonyms']

                    %>

                    <div class='hidden entrezID'>${c.data[c.ensemblID]['EntrezID']}</div>
                    <div class='hidden ensemblID'>${c.ensemblID}</div>
                    <div class='hidden db_id'>${c.db_id}</div>
                    <div id='official_symbol' class='hidden'>${c.symbol}</div>

                    <div class='title showEntrez'>${c.symbol}</div>
                    <div class='description'><div class='description'>${c.data[c.ensemblID]['description'].replace('<br />','')}</div></div>

                    <!-- <a href='${h.url('/expressions/result?graphType=box&gene='+str(c.ensemblID)+'&db_id='+str(c.db_id))}' class='linkButtons' id='viewLargerImage'>VIEW EXPRESSION > </a>
                    % if c.user != "":
                    <a href='${h.url('/expressions/multi_dataset_result?graphType=sca&gene='+str(c.ensemblID)+'&db_id='+str(c.db_id))}' class="linkButtons" id="multiview">MULTIVIEW > </a>
                    % endif
-->



                    <div class='showDescription showLabel'>Entrez Gene ID:</div><div class='showDescriptionValue'><a target='_blank' href='http://www.ncbi.nlm.nih.gov/gene/${entrez_id.replace(' ',',')}' class='showDescriptionValue showEntrez'>${entrez_id}</a></div>
                    <div class='showDescription showLabel'>Ensembl ID: </div><div class='showDescriptionValue'><a target='_blank' href='${ensembl_link}' class='showDescriptionValue showEnsembl underline'>${c.ensemblID}</a></div>
                    <div class='showDescription showLabel'> Aliases: </div><div class='showDescriptionValue'><a target='_blank' href='http://www.ncbi.nlm.nih.gov/gene/${entrez_id.replace(' ',',')}' class='showDescriptionValue showEntrez'>${aliases}</a></div>
                    <div class='showDescription showLabel '>  Diseases via OMIM:</div><div class='showDescriptionValue'><a target='_blank' href='http://www.ncbi.nlm.nih.gov/gene?Db=omim&DbFrom=gene&Cmd=Link&LinkName=gene_omim&LinkReadableName=OMIM&IdsFromResult=${entrez_id.replace(' ',',')}' class='showDescriptionValue showDiseases underline '> Click here for details</a></div>
                    <div class='showDescription showLabel '>  UCSC Browser:</div> <div class='showDescriptionValue'><a target='_blank' class='showDescriptionValue underline' href="${c.ucsc_data['base_url']}?position=chr${c.ucsc_data['chr']}:${c.ucsc_data['start']}-${c.ucsc_data['end']}&db=${c.ucsc_data['ucsc_db_id']}" id="otheh_link">Public UCSC</a></div>
                    <div class='showDescription showLabel '>  Pubmed Links </div><div class='showDescriptionValue'><a target='_blank' href='http://www.ncbi.nlm.nih.gov/gene?Db=pubmed&DbFrom=gene&Cmd=Link&LinkName=gene_pubmed&LinkReadableName=PubMed&IdsFromResult=${entrez_id.replace(' ',',')}' class='showDescriptionValue showPubMed underline '> Click here for details</a></div>

                    <div class="clear"></div>
                <div class='title'>${c.site_name} Data Methods</div>
                <div class="description">This document includes the normalisation methods, mappings and database imports like Kegg.</div>
                <div class='showDescription showLabel '>  Document Link </div><div class='showDescriptionValue'><a target='_blank' href='/${c.site_name}_data_methods.pdf' class='showDescriptionValue '>Data Methods PDF</a></div>

            </div>

        </div>
        <div class=clear></div>
</%def>



<%def name="display_gene_expression_graph_values(view_data)" >

        <table>
            %try:
                % if view_data.graph_type != 'scatter':

                    % if view_data.sort_by == 'Sample Type':
                    <tr><th>Identifier</th><th>Average</th><th>Standard Deviation</th><th>Minimum Value</th><th>Maximum Value</th><th>Median</th><th>Q1</th><th>Q3</th><th>Extra Information</th></tr>
                        % for item in view_data.sample_type_display_order:
                            % for count in view_data.plot_data[item]['values']:
                                <% row_data = view_data.plot_data[item]['values'][count] %>
                                <tr><td>${row_data['level_above']} ${item}</td><td>${row_data['average']}</td><td>${row_data['sd']}</td><td>${row_data['min']}</td><td>${row_data['max']}</td><td>${row_data['median']}</td><td>${row_data['Q1']}</td><td>${row_data['Q3']}</td><td>${row_data['extra_info']}</td></tr>
                            % endfor

                        % endfor

                    % elif view_data.sort_by == 'LineGraphGroup':

            <%
xaxis_map_dict = {}
for row_count in c.view_data.xaxis_labels['full']:
    row = c.view_data.xaxis_labels['full'][row_count]
    xaxis = row['xaxis_position']
    name = row['name']
    level = row['level']
    if level == 1:
       xaxis_map_dict[xaxis] = name
            %>

                    <tr><th>Identifier</th><th>Time</th><th>Average</th><th>Standard Deviation</th><th>Minimum Value</th><th>Maximum Value</th><th>Median</th><th>Q1</th><th>Q3</th><th>Extra Information</th></tr>

                        % for item in view_data.plot_data:
                            % for count in view_data.plot_data[item]['values']:
                                <% row_data = view_data.plot_data[item]['values'][count] %>
                                <% name = xaxis_map_dict[row_data['xaxis']] %>
                                <tr><td>${item}</td><td>${name}</td><td>${row_data['average']}</td><td>${row_data['sd']}</td><td>${row_data['min']}</td><td>${row_data['max']}</td><td>${row_data['median']}</td><td>${row_data['Q1']}</td><td>${row_data['Q3']}</td><td>${row_data['extra_info']}</td></tr>
                            % endfor
                        % endfor

                    % else:
                    <tr><th>Identifier</th><th>Average</th><th>Standard Deviation</th><th>Minimum Value</th><th>Maximum Value</th><th>Median</th><th>Q1</th><th>Q3</th><th>Extra Information</th></tr>
                        % for item in view_data.plot_data:
                            % for count in view_data.plot_data[item]['values']:
                                <% row_data = view_data.plot_data[item]['values'][count] %>
                                <tr><td>${row_data['level_above']} ${item}</td><td>${row_data['average']}</td><td>${row_data['sd']}</td><td>${row_data['min']}</td><td>${row_data['max']}</td><td>${row_data['median']}</td><td>${row_data['Q1']}</td><td>${row_data['Q3']}</td><td>${row_data['extra_info']}</td></tr>
                            % endfor
                        % endfor
                    % endif

                % endif
                % if view_data.graph_type == 'scatter':
                <tr><th>Probe and Sample ID</th><th>Expression Value</th><th>Standard Deviation</th></tr>
                    % for probe in view_data.probe_list:
                        % for row_data in view_data.plot_data[probe]:
                        <%
                            x_axis = row_data[0]
                            expression_value = row_data[1]
                            sample_id = row_data[2]
                            sd = row_data[3]
                            base_id=probe.replace(' ','_')+"_"+str(c.ds_id)+"_"+str(x_axis)
                        %>
                        <tr><td id="${base_id}_sample_id">${probe} - ${sample_id}</td><td id="${base_id}_expression_value">${expression_value}</td><td id="${base_id}_sd">${sd}</td></tr>
                        % endfor
                    % endfor


                % endif
            %except:

            %endtry
        </table>

</%def>



<%def name="large_icon(main_div_class,logo_class,header,description,hover_text,src='#')" >
<% class_header=header.replace(' ','_') %>

<div class="large_icon ${main_div_class}  ${class_header} hover_text" data_hover_text="${hover_text}">
    <a href="${src}"><span class="clickable_div ${class_header}"></span></a>
    <div class="header">${header}</div>
    <div class="logo ${logo_class}"></div>
    <div class="description">${description}</div>
</div>
</%def>

<%def name="content_menu_iii(action)">
        <a href="${h.url('/projects/iiiformatics')}">
            <div class="contact_menu ${'selected' if action == 'iiiformatics' else ''}">
                <div class="contact_menu_title">3IIIformatics</div>
            </div>
        </a>
        <a href="${h.url('/projects/iii_wellcome')}">
            <div class="contact_menu ${'selected' if action == 'iii_wellcome' else ''}">
                <div class="contact_menu_title">Wellcome Trust Centre for Molecular Parasitology</div>
            </div>
        </a>
        <a href="${h.url('/projects/iii_arthritis')}">
            <div class="contact_menu ${'selected' if action == 'iii_arthritis' else ''}">
                <div class="contact_menu_title">Arthritis Pathogenesis Centre of Excellence</div>
            </div>
        </a>
        <a href="${h.url('/projects/iii_immunobiology')}">
            <div class="contact_menu ${'selected' if action == 'iii_immunobiology' else ''}">
                <div class="contact_menu_title">Immunobiology</div>
            </div>
        </a>
</%def>


<%def name="content_menu(action)">
        <a class="about_us" href="${h.url('/contents/about_us')}">
            <div class="contact_menu ${'selected' if action == 'about_us' else ''}">
                <div class="contact_menu_title">About Us</div>
                <div class="clear"></div>
            </div>
        </a>
        <a class="faq" href="${h.url('/contents/faq')}">
            <div class="contact_menu ${'selected' if action == 'faq' else ''}">
                <div class="contact_menu_title">Help & FAQ</div>
                <div class="clear"></div>
            </div>
        </a>
        <a class="our_data" href="${h.url('/contents/our_data')}">
            <div class="contact_menu ${'selected' if action == 'our_data' else ''}">
                <div class="contact_menu_title">Our Data</div>
                <div class="clear"></div>
            </div>
        </a>
        <a class="our_publications" href="${h.url('/contents/our_publications')}">
            <div class="contact_menu ${'selected' if action == 'our_publications' else ''}">
                <div class="contact_menu_title">Our Publications</div>
                <div class="clear"></div>
            </div>
        </a>
        <a class="disclaimer" href="${h.url('/contents/disclaimer')}">
            <div class="contact_menu ${'selected' if action == 'disclaimer' else ''}">
                <div class="contact_menu_title">Disclaimer</div>
                <div class="clear"></div>
            </div>
        </a>
        <a class="privacy_policy" href="${h.url('/contents/privacy_policy')}">
            <div class="contact_menu ${'selected' if action == 'privacy_policy' else ''}">
                <div class="contact_menu_title">Privacy Policy</div>
                <div class="clear"></div>
            </div>
        </a>
        <a class="contact_us" href="${h.url('/contents/contact_us')}">
            <div class="contact_menu ${'selected' if action == 'contact_us' else ''}">
                <div class="contact_menu_title">Contact Us</div>
                <div class="clear"></div>
            </div>
        </a>

</%def>

<%def name="citation_content()">

       <div class="content_box">
            <a id="citation"></a>
            <div class="header_2">
                How to Cite Us
            </div>
            <div class="text">
                <p>
Please ensure that you cite the original publications describing the datasets hosted by ${c.site_name}.
                </p>
                <p>
To cite Stemformatics, please use:<br/>
Wells CA et al Stemformatics: Visualisation and sharing of stem cell gene expression. Stem Cell Research, DOI http://dx.doi.org/10.1016/j.scr.2012.12.003

                </p>
                <p>
                    <ul>
                        <li><a target = "_blank" href="http://www.sciencedirect.com/science/article/pii/S1873506112001262">Stemformatics Publication (link)</a></li>
                        <li><a target = "_blank" href="${h.url('/stemformatics_publication.pdf')}">Download Stemformatics Publication (pdf)</a></li>

                    </ul>
                </p>
                <div class="clear"></div>

            </div>

        </div>

</%def>
<%def name="search_box(text)">
        <% text.input_id = text.input_id if hasattr(text,'input_id') else 'geneSearch' %>
        <% text.search_value = text.search_value if hasattr(text,'search_value') else '' %>
        <% text.search_button_id = text.search_button_id if hasattr(text,'search_button_id') else 'viewGenes' %>
        <% text.search_action = text.search_action if hasattr(text,'search_action') else '#' %>
        <% text.input_name = text.input_name if hasattr(text,'input_name') else 'filter' %>
        <% text.search_name = text.search_name if hasattr(text,'search_name') else 'SEARCH' %>
        <% text.other_inputs = text.other_inputs if hasattr(text,'other_inputs') else '' %>
            <div class="search_box">
                <div class="searchField">
                    <form id="${text.input_id}Form" name="search" method="GET" action="${text.search_action}">
                        <input id="${text.input_id}" name="${text.input_name}" class="${text.input_class}" type="text" value="${text.search_value}"/>
                    </form>
                </div>
                <a id="${text.search_button_id}"  class="searchButton"><span>${text.search_name}</span><img src="${h.url('/images/show_genes.png')}"/></a>
            </div>
</%def>


<%def name="enclosed_search_box(text,show_all_option)">

    <%
    try:
        extra_class = text.extra_class
    except:
        extra_class = ""
    %>

    <div class="enclosed_search_box ${extra_class}" >
        <div class="title">${text.title}</div>
        <div class="basic_help">${text.help}</div>
        <div class="clear"></div>
        ${self.search_box(text)}
        <div class="clear"></div>
        ${show_all_option()}
    </div>
</%def>

<%def name="pre_enclosed_search_box()">
    <%
    class tempData:
        pass
    text = tempData()
    text.title = "Gene Search for YuGene"
    text.help = "Enter Symbol or Ensembl IDs for more precise results. It will provide suggestions via an autocomplete after four characters."
    text.input_id = "geneSearch"
    text.search_button_id = "viewGenes"
    text.search_action ='#'
    text.search_value = ''
    text.input_class = 'yugene'
    text.extra_class = ''
    %>
</%def>

<%def name="tutorial_gene_search_single_gene_graphs()">
        <a href="${h.url('/contents/index#tutorial=gene_search')}" onclick="return audit_help_log ('gene_search', 'help_tutorial_landing'); ">
            <div class="display_box">
                <div class="left">
                    <div class="header">Accessing Graphs via Gene search</div>
                    <div class="description">
                        This tutorial will take you through the Gene search functionality and show you all the graphs available, including the Gene Expression Graph, Multiview and YuGene Interactive Graph.<br/><br/>At any time you can close the tutorial by clicking on the X in the top right hand corner. Please click to start.
                    </div>
                </div>
                <div class="snapshot big_arrow"></div>
            </div>
        </a>

</%def>

<%def name="tutorial_create_gene_list()">

            <a href="${h.url('/contents/index#tutorial=create_geneset')}" onclick="return audit_help_log ('create_geneset', 'help_tutorial_landing'); ">
                <div class="display_box">
                    <div class="left">
                        <div class="header">Create your own Gene List</div>
                        <div class="description">
    This link provides a tutorial to create your own Gene List. You will need to be registered to follow this tutorial, or you can use the Guest account.<br/><br/>At any time you can close the tutorial by clicking on the X in the top right hand corner. Please click to start.
                        </div>
                    </div>
                    <div class="snapshot big_arrow"></div>
                </div>
            </a>
</%def>

<%def name="tutorial_registration()">

            <a href="${h.url('/contents/index#tutorial=registration')}" onclick="return audit_help_log ('registration', 'help_tutorial_landing'); ">
                <div class="display_box">
                    <div class="left">
                        <div class="header">Free ${c.site_name} Registration</div>
                        <div class="description">
    This link provides a tutorial to show you how to register in ${c.site_name}. It's free and doesn't take long.<br/><br/>At any time you can close the tutorial by clicking on the X in the top right hand corner. Please click to start.
                        </div>
                    </div>
                    <div class="snapshot big_arrow"></div>
                </div>
            </a>
</%def>






<%def name="choose_datasets_table(datasets,url)">
                <table id="choose_dataset" class="fixed">
                    <thead>
                        <tr>
                            <th>Datasets</th>
                        </tr>
                    </thead>
                    <tbody>
                        %for ds_id in datasets:
                            %if not datasets[ds_id].has_key('has_data') or datasets[ds_id]['has_data'] == 'yes':
                                <%  organism = datasets[ds_id]['organism'] %>
                                <%
                                    show_row = True
                                    if hasattr(c, 'species'):
                                        if organism == c.species or c.species is None:
                                            show_row = True
                                        else:
                                            show_row = False
                                %>
                                %if show_row:
                                <tr>
                                    <td>
                                        <div class="multi_select_row">
                                            <a href="${url}${ds_id}">
                                                <div class="inner">
                                                    <div class="title">${datasets[ds_id]['title']}</div>
                                                    <div class="handle">${datasets[ds_id]['handle']}</div>
                                                    <div class="cells">${datasets[ds_id]['cells_samples_assayed']}</div>
                                                </div>
                                                <div class="organism">${datasets[ds_id]['organism']}</div>
                                                <div class="small_arrow"></div>
                                                <div class="clear"></div>
                                            </a>
                                        </div>
                                    </td>
                                </tr>
                                %endif
                            %endif
                        %endfor
                    </tbody>
                </table>
        </div>
</%def>


<%def name="print_plural(text)">
    <%
            postfix = 's'
            if len(text) > 2:
                vowels = 'aeiou'
                if text[-2:] in ('ch', 'sh'):
                    postfix = 'es'
                elif text[-1:] == 'y':
                    if (text[-2:-1] in vowels) or (text[0] in string.uppercase):
                        postfix = 's'
                    else:
                        postfix = 'ies'
                        text = text[:-1]
                elif text[-2:] == 'is':
                    postfix = 'es'
                    text = text[:-2]
                elif text[-1:] in ('s', 'z', 'x'):
                    postfix = 'es'


            plural_text = '%s%s' % (text, postfix)
    %>
    ${plural_text}
</%def>


<%def name="setup_dataset_search_box_variables()">
        <%
        text.help = "Keyword Search to filter available datasets: Filter on cell type, author name, publication title or dataset ID"
        text.input_id = "dataset_search"
        text.search_button_id = "view_datasets"
        text.search_action = "#"
        text.search_value = ""
        text.input_name = "filter"
        text.input_class = ""
       %>


</%def>


<%def name="content_menu_mcri(action)">
        <a href="${h.url('/projects/mcri')}">
            <div class="contact_menu ${'selected' if action == 'mcri' else ''}">
                <div class="contact_menu_title">Welcome</div>
            </div>
        </a>
        <a href="${h.url('/projects/mcri')}">
            <div class="contact_menu ${'selected' if action == 'iii_wellcome' else ''}">
                <div class="contact_menu_title">Data</div>
            </div>
        </a>
        <a href="${h.url('/projects/mcri')}">
            <div class="contact_menu ${'selected' if action == 'iii_arthritis' else ''}">
                <div class="contact_menu_title">Publications</div>
            </div>
        </a>
        <a href="${h.url('/projects/mcri')}">
            <div class="contact_menu ${'selected' if action == 'iii_arthritis' else ''}">
                <div class="contact_menu_title">New Methods</div>
            </div>
        </a>
</%def>

<%def name="content_menu_leukomics(action)">
        <a href="${h.url('/projects/leukomics')}">
            <div class="contact_menu ${'selected' if action == 'leukomics' else ''}">
                <div class="contact_menu_title">Welcome</div>
            </div>
        </a>
        <a href="${h.url('/projects/leukomics_data')}">
            <div class="contact_menu ${'selected' if action == 'leukomics_data' else ''}">
                <div class="contact_menu_title">Data</div>
            </div>
        </a>
        <!--
        <a href="${h.url('/projects/leukomics_publications')}">
            <div class="contact_menu ${'selected' if action == 'leukomics_publications' else ''}">
                <div class="contact_menu_title">Publications</div>
            </div>
        </a> -->
</%def>
