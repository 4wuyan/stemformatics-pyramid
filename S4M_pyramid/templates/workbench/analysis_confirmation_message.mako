<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link href="${h.url('/css/workbench/analysis_confirmation_message.css')}" type="text/css" rel="stylesheet">
</%def>

    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">
            <div id="confirmText">
                <div id="confirmText_inner_div">
                    <div id=message>${c.title}</div>
                    <div id=prompt>
                        ${c.message}
                        % if c.job.analysis == 0:
                            <br>
                            <br>
                            Rows with expression value as None will be filtered out from Heatmap.
                        % endif
                        <br>
                        % if c.job.gene_set_name is not None:
                            <br>
                            Gene List: ${c.job.gene_set_name}
                        % endif

                        % if c.job.gene is not None:
                            <br>
                            Gene: ${c.job.gene}
                        % endif

                        % if c.job.probe is not None:
                            <br>
                            Probe ID: ${c.job.probe}
                        % endif

                        % if c.job.comparison_type is not None and c.job.comparison_type != "":
                            <br>
                            Comparison Type: ${c.job.comparison_type}
                        % endif

                        <br>
                        Analysis: ${c.analysis[c.job.analysis]['name']}
                        <br>

                        % if hasattr(c.job, 'handle'):
                        Dataset: ${c.job.handle}
                        % endif

                    </div>

                    <div id="links">
                        <a href="${h.url('/workbench/index')}"> Other Analyses <img class="confirm_arrow" src="${h.url('/images/workbench/confirm_arrow.png')}"></a>  <a href="${h.url('/workbench/jobs_index')}"> View Job Result <img class="confirm_arrow" src="${h.url('/images/workbench/confirm_arrow.png')}"></a>

                        % if c.job.analysis == 0:
                        <a href="${h.url('/workbench/hierarchical_cluster_wizard')}">Run another Hierarchical Cluster Analysis <img class="confirm_arrow" src="${h.url('/images/workbench/confirm_arrow.png')}"></a>
                        % endif

                        % if c.job.analysis == 1:
                        <a href="${h.url('/workbench/comparative_marker_selection_wizard')}">Run another Comparative Marker Selection Analysis <img class="confirm_arrow" src="${h.url('/images/workbench/confirm_arrow.png')}"></a>
                        % endif

                        % if c.job.analysis == 2:
                        <a href="${h.url('/workbench/gene_neighbour_wizard')}">Run another Gene Neighbourhood Analysis <img class="confirm_arrow" src="${h.url('/images/workbench/confirm_arrow.png')}"></a>
                        % endif

                        % if c.job.analysis == 4:
                        <a href="${h.url('/workbench/gene_set_annotation_wizard')}">Run another Gene List Annotation <img class="confirm_arrow" src="${h.url('/images/workbench/confirm_arrow.png')}"></a>
                        % endif

                        % if c.job.analysis == 7:
                        <a href="${h.url('/workbench/user_defined_expression_profile')}">Run another User Defined Expression Profile<img class="confirm_arrow" src="${h.url('/images/workbench/confirm_arrow.png')}"></a>
                        % endif
                         <div class="clear"></div>
                    </div>
                </div>
            </div>
            <div class="clear"></div>
        </div>

    </div>
    <div class="hidden" id="show_help_flag">NO</div>
