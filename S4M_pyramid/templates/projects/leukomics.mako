<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
</%def>

<%
    landing_page_name = "LEUKomics"
%>
<style>
.abstract { width: 600px; }
</style>
<div class="content iiiformatics">
    <div class="content_left_column">
        ${Base.content_menu_leukomics(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column ">
        <div class="box display">
            <div id="introduction" class="content_box">
                <a id="introduction"></a>
                <div class="header_1">
                LEUKomics
                </div>
                <div class="text">
                <p>
As we learn more about the molecular changes that drive cancer, so our power to combat it grows. Researchers of many cancer types aspire to build our understanding of these drivers and use this knowledge to create targeted therapies. High-throughput technologies, which are becoming ever more powerful, have the potential to lead us to a truer picture of the molecular features of cancer cells.
                </p>
                <p>
CML researchers led the way in the search for targeted cancer therapies through discovery of the BCR-ABL1 tyrosine kinase inhibitors, leading to huge improvements in patient care. However, challenges still remain in CML. At ${landing_page_name} we believe that the groundbreaking CML research happening across the world could be enhanced by use of a growing collection of high throughput data. Our goal is to bring these datasets together and create a tool to facilitate in depth analysis of the wealth of information that resides within them.
                </p>
                <img class="abstract" src="/images/leukomics/leukomics_graphical_abstract.png"></img>
                <p>
The ${landing_page_name} datasets detail gene expression in sample types relating to key areas of modern CML research. These include:
<ol>
<li>Clinical parameters – such as response to treatment and aggressiveness of disease </li>
<li>Stem cells – from CML patients and healthy individuals </li>
<li>Disease stage – chronic, accelerated and blast phases </li>
<li>Drug treatments – response to drugs such as tyrosine kinase inhibitors </li>
<li>Mouse models – stem and progenitor cells from mouse models of CML </li>
</ol>
                </p>
                <p>
We are continuously updating to include more datasets, but if there is one in particular you would like to see here let us know. If you would like to host a dataset privately for comparison with the publicly available data you may do so through the dataset request page.
                </p>
                <p>
                <ul>
                    <li>
                        <a target = "_blank" href="${h.url('/datasets/search?filter=leukomics')}">View Datasets associated with ${landing_page_name}</a>
                    </li>
                    <li>
                        <a target = "_blank" href="${h.url('/main/suggest_dataset')}">Suggest Datasets for ${landing_page_name}</a>
                    </li>
                </ul>
                </p>
                <p>
                <div class="partner_labs">Links to Partner Labs</div>
                <ul>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/tessaholyoake/">
                        Tessa Holyoake
                        </a></br>
                        <span>Email : Tessa.Holyoake@glasgow.ac.uk </span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/davidvetrie/">
                        David Vetrie
                        </a></br>
                        <span>Email : David.Vetrie@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/heatherjorgensen/">
                            Heather Jorgenson
                        </a></br>
                        <span>Email : Heather.Jorgensen@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/xuhuang/">
                            Xu Huang
                        </a></br>
                        <span>Email : Xu.Huang@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/vignirhelgason/">
                            Vignir Helgason
                        </a></br>
                        <span>Email : Vignir.Helgason@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/alisonmichie/">
                            Alison Michie
                        </a></br>
                        <span>Email : Alison.Michie@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/helenwheadon/">
                            Helen Wheadon
                        </a></br>
                        <span>Email : Helen.Wheadon@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/karenkeeshan/">
                            Karen Keeshan
                        </a></br>
                        <span>Email : Karen.Keeshan@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/chrishalsey/">
                            Chris Halsey
                        </a></br>
                        <span>Email : Chris.Halsey@glasgow.ac.uk</span>
                    </li>
                    <li>
                        <a target="_blank" href="http://www.gla.ac.uk/researchinstitutes/cancersciences/staff/mhairicopland/">
                            Mhairi Copland
                        </a></br>
                        <div.aggregate span>Email : Mhairi.Copland@glasgow.ac.uk</span>
                    </li>
                </ul>
                </p>

                <p>
                Paul O'Gorman Leukaemia Research Centre:
                <ul>
                    <li>
                        <a target = "_blank" href="http://www.gla.ac.uk/about/supportus/medicalfund/paulogormanleukaemiaresearchcentre/">University of Glasgow Page</a>
                    </li>
                    <li>
                        <a target = "_blank" href="https://www.facebook.com/POGLRC/">Facebook Page</a>
                    </li>
                    <li>
                        <a target = "_blank" href="https://twitter.com/pog_lrc">Twitter</a>
                    </li>
                </ul>
                </p>
                <p>
                Our funders include:
                <ul>
                  <li>
                      <a target = "_blank" href="https://bloodwise.org.uk">Bloodwise</a>
                      <p>
                      <a target = "_blank" href="https://bloodwise.org.uk">
                      <img width="300" src="/images/leukomics/bloodwise_logo.jpg"></img>
                      </a>
                      </p>
                  </li>
                  <li>
                      <a target = "_blank" href="https://scottishcancerfoundation.org.uk">Scottish Cancer Foundation</a>
                      <p>
                      <a target = "_blank" href="https://scottishcancerfoundation.org.uk">
                      <img width="300" src="/images/leukomics/scottishcancerfoundation_logo.png"></img>
                      </a>
                      </p>
                      <br/>
                      <br/>
                  </li>
                  <li>
                      <a>JEM Research Foundation philanthropic funding</a>
                      <p>
                      <img width="300" src="/images/logos/STE_JEM.png"></img>
                      </a>
                      </p>
                  </li>
                </ul>
                </p>

                </div>
            </div>
        </div>
    </div>
</div>
