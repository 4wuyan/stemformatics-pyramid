<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
    <script type="text/javascript" src="${h.url('/js/landing_pages.js')}"></script>
    <script>
        $(document).ready(function() {
            base_url = BASE_PATH+"workbench/rohart_msc_graph";
            filter_dict = {'rohart_msc_test':true};
            set_view_datasets(base_url,filter_dict);
        });
    </script>
</%def>

<div class="content landing_page_analysis">
    <div class="baseMarginLeft" >
        <div class="hidden" id="show_help_flag">NO</div>

        <div class="landing_page_header analyses block">
            <div class="left_square">
                <div class="header">Rohart MSC Test</div>
                <div class="logo mdd_logo"></div>
            </div>
            <div class="description centered">
                <p>
                Use the Rohart MSC Test to see if a dataset contains samples behaving like mesenchymal stromal cells. <a href="/contents/contact_us">Contact us</a> for information on testing the MSC status of unpublished samples. You can view the publication <a href="/contents/our_publications#msc_paper">here.</a>
                To have ${c.site_name} run the Rohart MSC Test on your data, please click <a target="_blank" href="/main/suggest_dataset">here</a>.
              </p>
               <p>
                Use the search bar below using keywords (e.g. cell type or author name) to find relevant and available datasets.
               </p>
            </div>
        </div>

        <div class="clear"></div>

        <%def name="show_all_option()"> </%def>
        ${Base.pre_enclosed_search_box()}
        <% text.title = "Choose a dataset to score with the Rohart MSC test" %>
        ${Base.setup_dataset_search_box_variables()}
        ${Base.enclosed_search_box(text,self.show_all_option)}



        <div class="tutorials base_middle_width">
            <div class="title" >Tutorials</div>
            <a data-tutorial="Rohart_MSC_Test" class="in_page_tutorial_link" onclick="return audit_help_log ('Rohart_MSC_Test', 'help_tutorial_landing'); ">
                <div class="display_box">
                    <div class="left">
                        <div class="header">Direct access to Rohart MSC Test</div>
                        <div class="description">
    This link provides a tutorial to enter in a dataset to take you directly to the Rohart MSC Test page. It will show you some of the options available.<br/><br/>At any time you can close the tutorial by clicking on the X in the top right hand corner. Please click to start.
                        </div>
                    </div>
                    <div class="snapshot big_arrow"></div>
                </div>
            </a>

            <div class="clear"></div>
        </div>

    </div>
</div>
