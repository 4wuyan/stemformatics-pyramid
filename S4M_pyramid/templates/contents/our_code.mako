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
Our code is Open Source.

            </div>
            <div class="text">
                <p>${c.site_name} is an Open Source web-based pocket dictionary for stem cell biologists. You can learn more about the technical background of ${c.site_name} here.  </p>
                 <p>If you would like to contribute as a collaborator or as a student intern, please contact us by gitter chat <a style="font-size:16px;"  href="https://gitter.im/stemformatics/Lobby">(link)</a> or by email via the Contact Us page <a style="font-size:16px;" href="/contents/contact_us">(link)</a>.</p>
            </div>
        </div>
        <div class="content_box">
            <div class="content_links">
                <a href="#gsoc">Google Summer of Code / Student Projects ></a>
                <a href="#system_architecture">System Architecture ></a>
                <a href="#repos">Repositories ></a>
                <a href="#open_source">Open Source Dependencies ></a>
                <a href="#providers">Infrastructure Providers ></a>
                <div class="clear"></div>
            </div>
        </div>
        <div class="content_box">
            <a id="gsoc"></a>
            <div class="header_2">
                Google Summer of Code 2018 (GSoC) / Student Projects
            </div>
            <div class="text">
                <p>
                </p>
For any students interested in the Google Summer of Code or a student internship, please check out our project ideas page <a style="font-size:16px;" href="https://docs.google.com/document/d/1zcuCTUMqbR7QFrUaGmxYGD_iKt8XCK6a35RtN6GGUC0/edit#heading=h.6egttnvbi2gu">(link)</a>.
                </p>
                <p>
If we are accepted as a mentor organisation, we will be open to start discussing these projects with students in mid February 2018. This is when Google will announce which mentor organisations will be participating.
                </p>
                <p>
For the full Google Summer of Code 2018 timeline, <a style="font-size:16px;" href="https://summerofcode.withgoogle.com/how-it-works/#timeline">please see here</a>.
                </p>
                <p>
                   If you would like to start contributing, or if you have any questions, please ask us here - <a style="font-size:16px;"  href="https://gitter.im/stemformatics/Lobby">https://gitter.im/stemformatics/Lobby</a>
                </p>
            </div>
        </div>
        <div class="content_box">
            <a id="system_architecture"></a>
            <div class="header_2">
                System Architecture
            </div>
            <div class="text">
                <p>
</p>
<p>
${c.site_name} requires multiple servers to run. We process raw data at our High Performance Compute (HPC) servers and send the processed data to the ${c.site_name} website. In the future, we will share our public datasets via the Data Portal.
</p>
<p>
Here is a simplified diagram of our future ecosystem, where the ${c.site_name} website (denoted by S) is a launching pad for other web based tools such as <a href="http://www.innatedb.com">InnateDB</a>:

                    <img style="margin-top: 20px; width:500px;height:300px;" src="/images/contents/flow_of_data_stemformatics_ecosystem.png"/>
                </p>
                <br/> <br/>
                <p>
Our system architecture is based on simplicity and reliability. We use Apache for a reverse proxy and Pylons as the middleware. The fact that we are a web-based pocket dictionary means we also focus on speed. This is why we run a Redis in-memory cache.
                </p>
                <p>
                    <img style="margin-top: 20px; height:350px;" src="/images/contents/architecture_overview.png"/>
                </p>
                <div class="clear"></div>

            </div>

        </div>

        <div class="content_box">
            <a id="repos"></a>
            <div class="header_2">
                Repositories
            </div>
            <div class="text">
                <p>
                ${c.site_name} is an Open Source project that has a number of public repositories. Here are the most important ones:

                </p>
                <p>
                    <ul>
                        <li><a href="https://bitbucket.org/stemformatics/stemformatics">${c.site_name} Main Website</a></li>
                        <li><a href="https://bitbucket.org/stemformatics/stemformatics_tools">${c.site_name} Microarray Pipelines</a></li>
                        <li><a href="https://bitbucket.org/uqokorn/s4m_base/wiki/Home">${c.site_name} NGS Pipelines</a></li>
                        <li><a href="https://bitbucket.org/stemformatics/data-portal">${c.site_name} Data Portal (Beta)</a></li>
                        <li><a href="https://bitbucket.org/stemformatics/pathway_viewer">Omicxview Website - Metabolomics Viewer (Beta)</a></li>
                    </ul>
                </p>
                <p>We aim to write readible, maintainable code that is fit for purpose.  We work in PHP, Python, Javascript, Bash, R and Perl. </p>
                <div class="clear"></div>

            </div>

        </div>

        <div class="content_box">
            <a id="open_source"></a>
            <div class="header_2">
                Open Source Dependencies
            </div>
            <div class="text">
                <p>

                </p>

                    ${c.site_name} is built on top of numerous Open Source projects. For example, in the ${c.site_name}  Web server we have:
                <p>
                </p>

                    <ul>
                        <li><a href="https://www.centos.org/">CentOS Linux operating system</a></li>
                        <li><a href="https://httpd.apache.org/">Apache Http Server Project for reverse proxy</a></li>
                        <li><a href="https://pylonsproject.org/about-pylons-framework.html">Pylons (Pyramid pre-cursor) for Python middleware web framework</a></li>
                        <li><a href="https://www.postgresql.org/">PostgreSQL database</a></li>
                        <li><a href="https://redis.io/">Redis for key value in memory cache</a></li>
                        <li><a href="https://jquery.com/">JQuery for javascript framework</a></li>
                        <li><a href="https://d3js.org/">D3 JS for visualisation in SVG</a></li>
                        <li><a href="http://biojs.io/">BioJS for D3JS component visualisation</a></li>
                    </ul>
                </p>
                <div class="clear"></div>

            </div>

        </div>
        <div class="content_box">
            <a id="providers"></a>
            <div class="header_2">
                Infrastructure Providers
            </div>
            <div class="text">
                <p>

                </p>

                    ${c.site_name} runs with the help of many different infrastructure provides:
                <p>
                </p>

                    <ul>
                        <li><a href="https://nectar.org.au/">NeCTAR</a> for academic cloud infrastructure</li>
                        <li><a href="https://www.qriscloud.org.au/about-qriscloud">QRISCloud</a> for providing Queensland based NeCTAR compute, storage and services</li>
                        <li><a href="https://blogs.unimelb.edu.au/researchplatforms/cloud/">Research Platform Services</a> for providing Victoria based NeCTAR compute, storage and services</li>
                        <li><a href="http://www.intersect.org.au/time/cloud/nectar">Intersect</a> for providing New South Wales based NeCTAR compute, storage and services</li>
                    </ul>
                </p>
                <div class="clear"></div>

            </div>

        </div>

    </div>
</div>


