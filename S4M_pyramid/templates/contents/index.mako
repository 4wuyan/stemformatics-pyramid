<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link href="${h.web_asset_url('/css/contents/index.css')}" type="text/css" rel="stylesheet">
    <script type="text/javascript" src="${h.web_asset_url('/js/contents/jquery.bxSlider.min.js')}"></script>
    <script type="text/javascript" src="${h.web_asset_url('/js/contents/index.js')}"></script>
</%def>
    <div id="main_slider_wrapper">
        <div id="main_slider">
            <div class="slide odd">
                <div class="content">
                    <h2>Welcome to ${c.site_name}</h2>
                    <p>This is a portal to a series of public experiments describing mouse and human
                        stem cells and how they differentiate to become mature cells, tissues and organs.</p>
                    <p>You'll find data from leading stem cell laboratories in a format that is easy to
                        search, easy to visualise and easy to export. Log in to run and
                        save your own analyses.</p>
                    <div><a class="slidebutton" href="${h.url('/genes/search#tutorial=gene_search')}">START EXPLORING</a></div>
                </div>
             </div>
            <div class="slide even">
                <div class="content">
                    <img class="screen" src="${h.web_asset_url('/images/leukomics/leukomics_graphical_abstract_front_page.png')}" />
                    <h2>LEUKomics</h2>
                    <p>Access the homepage of the blood cancer atlas LEUKomics. </p>
                    <div><a class="slidebutton" href="${h.url('/leukomics')}">LEUKOMICS</a></div>
                </div>
            </div>
             <div class="slide odd">
                <div class="content">
                    <img class="screen" src="${h.web_asset_url('/images/contents/slider/rohart_small.png')}" />
                    <h2>Rohart MSC Test</h2>
                    <p>Use the Rohart MSC Test to see if a dataset contains samples behaving like mesenchymal stromal cells. Contact us for information on testing the MSC status of unpublished samples.</p>
                    <div><a class="slidebutton" href="${h.url('/workbench/rohart_msc_test')}">SEE MORE</a></div>
                </div>
            </div>
            <div class="slide odd">
                <div class="content">
                    <img class="screen" src="${h.web_asset_url('/images/contents/slider/expbrowser-small.png')}" />
                    <h2>Datasets</h2>
                    <p>Choose from ${c.number_of_public_datasets} public studies with ${c.number_of_public_samples['Human']} human and ${c.number_of_public_samples['Mouse']} mouse samples. Filter by author,  cell type or keyword. Click on the icons for easy access to interesting datasets.</p>
                    <div><a class="slidebutton" href="${h.url('/datasets/search')}">FIND A DATASET</a></div>
                </div>
            </div>
            <div class="slide odd">
                <div class="content">
                    <img class="screen" src="${h.web_asset_url('/images/contents/slider/dr-andras-nagy-small.jpg')}" />
                    <h2>Project Grandiose</h2>
                    <p>Access the homepage of Project Grandiose that was released in Nature and Nature Communications in December 2014. </p>
                    <div><a class="slidebutton" href="${h.url('/project_grandiose')}">PROJECT GRANDIOSE</a></div>
                </div>
            </div>
        </div>
    </div>
    <div id="front_page_projects_line">
        <div class="project_name">
            LEUKomics
        </div> <!-- end project_name -->
        <div class="project_text">
            Recently launched:  LEUKomics online data portal
        </div> <!-- end of project_text -->
        <div class="slide"><a class="slidebutton" href="${h.url('/leukomics')}">TELL ME MORE</a></div>
        <div class="clear"></div>
    </div> <!-- End of projects_line -->
    <div class="big_links">
        <ul>
            <li>
                <a class="dataset" href="${h.url('/datasets/search')}">
                    <div>
                        <h2>Datasets</h2>
                        <p>Search from ${c.number_of_public_datasets} high quality public studies.</p>
                    </div>
                </a>
            </li>
            <li>
                <a class="general" href="http://www.stemcellsaustralia.edu.au/About-Stem-Cells.aspx">
                    <div>
                        <h2>Basic Info</h2>
                        <p>Want basic info about stem cells?</p>
                    </div>
                </a>
            </li>
            <li>
                <a class="helpvids" href="${h.url('/contents/help')}">
                    <div>
                        <h2>Help Tutorials</h2>
                        <p>Step by step instructions on how to use ${c.site_name}.</p>
                    </div>
                </a>
            </li>
        </ul>

    </div>
    <div class="info">
        <div class="left-col">
            <div class="section partners">
                <h2>PARTNERS</h2>
                <div>
                    <ul>
                        <li><a href="http://www.unimelb.edu.au/">University of Melbourne</a></li>
                        <li><a href="http://www.bioplatforms.com/">Bioplatforms Australia</a></li>
                        <li><a href="http://www.qcif.edu.au/">Queensland Cyber Infrastructure Foundation</a></li>
                        <li><a href="http://www.stemcellsaustralia.edu.au/">Stem Cells Australia</a></li>
                        <li><a href="https://nectar.org.au/">NeCTAR</a></li>
                        <li><a href="http://www.wehi.edu.au/">Walter and Eliza Hall Institute of Medical Research</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="middle-col">
            <div class="section news">
                <h2>RECENT NEWS</h2>
                <div>
                    <ul class="tweet_list">
                      % for tweet in c.tweets:
                        <li>
                            <div class="tweet_body">
                                ${tweet.html | n}
                            </div>
                            <div class="tweet_info">
                                <span class="tweet_time"><a href="${tweet.tweet_url}" title="view tweet on twitter">${tweet.relative_time}</a></span>
                                <span>·</span>
                                <a class="tweet_action tweet_reply" href="${tweet.reply_url}">reply</a>
                                <span>·</span>
                                <a class="tweet_action tweet_retweet" href="${tweet.retweet_url}">retweet</a>
                                <span>·</span>
                                <a class="tweet_action tweet_favorite" href="${tweet.favourite_url}">favorite</a>
                            </div>
                        </li>
                      % endfor
                    </ul>
                    <div class="more"><a href="http://twitter.com/${c.site_name}/">more news...</a></div>
                </div>
            </div>
            <div class="section assist">
                <div>
                    <a href="http://www.stemcellsaustralia.edu.au/"><img src="${h.url('/images/contents/ssaustlogo.png')}" alt="Stemcells Australia Icon"></a>
                    <p>${c.site_name} is the collaboration platform of <a href="http://www.stemcellsaustralia.edu.au/">Stem Cells Australia</a>.</p>
                </div>
            </div>
        </div>

        <div class="right-col">
            <div class="section grandiose">
                <h2>ANALYSES</h2>
                <div>
                    <p>Analyse and visualise stem cell gene lists. Compare with public gene lists and Kegg pathways.
                        Look for differential expression and co-expression and generate heatmaps to visualise expression patterns.</p>
                    <p>Check it out <a href="${h.url('/workbench/index')}">here...</a></p>
                </div>
            </div>
            <div class="section collabs">
                <h2>WHO ARE WE?</h2>
                <div>
                    <p>Check out our ‘About us’ page to find out more, which can be seen <a href="${h.url('/contents/about_us')}">here...</a></p>
                </div>
            </div>
            <div class="section feedback">
                <div>
                    <a href="mailto:${c.feedback_email}?Subject=${c.site_name}%20Feedback">
                        <img src="${h.url('/images/contents/feedbacklogo.png')}" alt="Feedback Icon">
                        <p>Your feedback is important to us, please let us know what you think.</p>
                        <div class="clear"></div>
                    </a>
                </div>
            </div>
        </div>
        <div class="clear"></div>
    </div>
