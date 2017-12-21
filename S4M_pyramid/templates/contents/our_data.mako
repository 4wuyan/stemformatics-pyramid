<%inherit file="../default.html"/>\
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
</%def>


<div class="content">
    <div class="content_left_column">
        ${Base.content_menu(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column">
        <div class="content_box">
            <div class="header_1">
All of the data on this site has been handpicked, checked for experimental reproducibility and design quality, and normalized in-house.

            </div>
            <div class="text">
                <p>
                We share all of our published datasets with ArrayExpress and all links to publications are provided through PubMed. Our backend analyses use a mixture of our own code and GenePattern from the Broad Institute.
                </p>
                <p>
                    You can find documentation on all of our data processing, QC and analysis on this page.
                </p>
            </div>
        </div>
        <div class="content_box">
            <div class="content_links">
                <a href="#data">Data Methods  ></a>
                <a href="#formats">Formats and Standards ></a>
                <div class="clear"></div>
            </div>
        </div>
        <div class="content_box">
            <a id="data"></a>
            <div class="header_2">
                Data Methods
            </div>
            <div class="text">
                <p>
                    This is the documentation that explains how data is imported into ${c.site_name}. It includes the normalisation methods, mappings and database imports like Kegg.
                </p>
                <p>
                    <ul>
                        <li><a target = "_blank" href="${h.url('/'+str(c.site_name)+'_data_methods.pdf')}">${c.site_name} Data Methods (pdf)</a></li>

                    </ul>
                </p>
                <div class="clear"></div>

            </div>

        </div>
        <div class="content_box">
            <a id="formats"></a>
            <div class="header_2">
                Formats and Standards
            </div>
            <div class="text">
                <p>
                    These are some of the formats and standards we have based ${c.site_name} on.
                </p>
                <p>
                    <ul>
                    	<li><a target = "_blank" href="http://obi-ontology.org/page/Main_Page">The Ontology for Biomedical Investigations project</a></li>

                    </ul>
                </p>
                <div class="clear"></div>

            </div>

        </div>
    </div>
</div>


