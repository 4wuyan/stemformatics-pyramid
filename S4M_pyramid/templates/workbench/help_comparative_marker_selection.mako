<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_index.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_index.js')}"></script>
</%def>

    <div id="help_flag_message" class="hidden">Click the grey help bar to hide. Click again to expand.</div>
    <div id="help_flag_top_position" class="hidden">230px</div>
    
    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            
            ${Base.wb_breadcrumbs()}  
                
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Comparative Marker Selection Analysis Help
                            </div>
                        </div>
                        <div class="wb_help_bar_showing wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Hide help information <img class="help" src="/images/workbench/minus.png" "="">
                            </div>
                        </div>
                        <div class="wb_help_showing wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>This analysis shows you which of your genes of interest are most differentially expressed in distinct phenotypes within a study.</p>
                                
                                <p>It uses the analysis provided by <a target="_blank" href="http://www.broadinstitute.org/cancer/software/genepattern/">GenePattern</a> from MIT. Three separate Gene Pattern modules are used, one to do the analysis, one to extract the information and one to create an image.</p>
                                <p>To see more detail about the underlying analysis that is provided by Gene Pattern, please <a target="_blank" href="http://gepetto.qfab.org:8080/gp/module/doc/urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00044:7">click here</a>.</p>
                                <p>To see more detail about the extraction module provided by Gene Pattern, please <a target="_blank" href="http://gepetto.qfab.org:8080/gp/module/doc/urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00046:3">click here</a>.</p>
                                <p>To see more detail about the image creation provided by Gene Pattern, please <a target="_blank" href="http://gepetto.qfab.org:8080/gp/module/doc/urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00032:6">click here</a>.</p>
                                <p>The default settings for the ${c.site_name} Gene Pattern Comparative Marker Selection analysis are shown below.</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>    
            <div class="tables">
                <table>
                    <tr>
                        <th>Field name</th>
                        <th>Description</th>
                        <th>${c.site_name} Default</th>
                        <th>Reason for Default</th>
                    </tr>
                    <tr>
                        <td>test direction</td>
                        <td>The test to perform</td>
                        <td>2 Sided</td>
                        <td>Assumes that the population of probes being tested between
two samples have equivalent means and variance, such that probes
considered to be significantly different may be smaller or larger in
one population compared to the other.  This may be adjusted to a
one-tailed test at the  GenePattern server, where only genes larger in
one population are ranked significantly different.</td>
                    </tr>
                    <tr>
                        <td>test statistic</td>
                        <td>The statistic to use</td>
                        <td>T-Test</td>
                        <td>A widely used test between two groups of samples which tests
the mean differences of each probe between two unpaired samples, and
does not assume that there should be a minimum standard deviation
(STD). This may be adjusted at the GenePattern server to test a
median-based difference and/or specification of a minimum STD. A
paired t-test can be chosen at the GenePattern server.</td>
                    </tr>
                    <tr>
                        <td>min std</td>
                        <td>Minimum standard deviation if used in the test statistic</td>
                        <td>N/A</td>
                        <td>Not used in the T-Test</td>
                    </tr>
                    <tr>
                        <td>number of permutations</td>
                        <td>Number of permutations to disclose</td>
                        <td>1000</td>
                        <td>ComparativeMarkerSelection computes p-values
assuming the test statistic scores follow Student's t-distribution. A
permutation test is used to estimate the significance (p-value) of the
test statistic score, and is useful when each sample class contains at
least 10 members. As several of the stemformatics datasets meet this
criteria, the default permutation = 1000. A more indepth analysis of
larger stemformatics datasets may benefit from more permutations,
whereas those datasets with fewer than 10 members in each class do not
benefit from permutation. This value can be adjusted to 0 at the
GenePattern server.</td>
                    </tr>
                    <tr>
                        <td>complete</td>
                        <td>Perform all possible permutations</td>
                        <td>no</td>
                        <td>This is an alternate to specifying the number of permutations
(see above) but is not used as a default setting in the stemformatics
tests.</td>
                    </tr>
                    <tr>
                        <td>balanced</td>
                        <td>Perform balanced permutations </td>
                        <td>no</td>
                        <td>${c.site_name} does not assume equal numbers of samples in
each class, which would be required for a balanced t-test.</td>
                    </tr>
                    <tr>
                        <td>random seed</td>
                        <td>Seed of the reandom number generator to produce permutations</td>
                        <td>Undisclosed</td>
                        <td>This was chosen arbitrarily</td>
                    </tr>
                    <tr>
                        <td>smooth p values</td>
                        <td>Use smooth p values</td>
                        <td>yes</td>
                        <td>This constrains the p-values between 1 and 0.</td>
                    </tr>
                    <tr>
                        <td>phenotype test</td>
                        <td>Tests to perform when data has more than two classes</td>
                        <td>all pairs</td>
                        <td>This was chosen to allow all combinations of comparisons to be calculated at the same time.</td>
                    </tr>
                    
                    
                    <!-- 
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    -->
                </table>
                <!-- <img src="${h.url('/images/workbench/gn-1.png')}" style="width:100%;border: 1px solid #5a5a5a;" /> -->
            </div>
        
            <div class="clear" > </div>
        </div>
    </div>
