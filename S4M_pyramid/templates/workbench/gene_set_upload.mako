<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>
<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_upload.css')}" >
</%def>





    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">

            ${Base.wb_breadcrumbs()}

            <div class="wb_question_groups_selected">

                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">



                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                Upload new Gene List
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>Upload a gene list from file. Most "simple" (i.e. delimited) formats will work.  This will not work with an Excel spreadsheet.</p>
                                <p>We accept gene symbols, Ensembl and Entrez IDs, aliases and probes.</p>
                            </div>

                        </div>

                    </div>
                    <div class="clear"></div>
                </div>

            </div>
            <div id=form>
                <div class="innerDiv">
                    <div class="title">Please upload a file</div>
                    <form enctype="multipart/form-data" action="${h.url('/workbench/gene_set_upload')}" method="post">
                      <dl class="gene_sets">
                        <dt>${c.error_message}</dt>
                        <dt>Name of new gene list:</dt>
                        <dd><input type="text" name="gene_set_name"></dd>
                        <dt>Species:</dt>
                        <dd>
                            <input type="radio" name="db_id" value="${c.human_db}" checked /><label>Human</label>
                            <div class="clear"></div>
                            <input type="radio" name="db_id" value="${c.mouse_db}" /><label>Mouse</label>
                        </dd>
                        <dt>Search Type:</dt>
                                <dd>
                                    <%

                                        all_checked = ''
                                        ensembl_checked = ''
                                        symbol_checked = ''
                                        fts_checked = ''
                                        probe_checked = ''
                                        alias_checked = ''
                                        entrez_checked = ''
                                        refseq_checked = ''

                                        if c.search_type == 'all':
                                            all_checked = 'checked'

                                        if c.search_type == 'ensembl_id':
                                            ensembl_checked = 'checked'

                                        if c.search_type == 'symbol':
                                            symbol_checked = 'checked'

                                        if c.search_type == 'alias':
                                            alias_checked = 'checked'

                                        if c.search_type == 'entrez':
                                            entrez_checked = 'checked'

                                        if c.search_type == 'probe':
                                            probe_checked = 'checked'

                                        if c.search_type == 'refseq':
                                            refseq_checked = 'checked'
                                    %>


                                    <input type="radio" name="search_type" value="all" ${all_checked} /><label>All</label>
                                    <div class="clear"></div>
                                    <input type="radio" name="search_type" value="ensembl_id"  ${ensembl_checked} /><label>Ensembl Gene ID</label>
                                    <div class="clear"></div>
                                    <input type="radio" name="search_type" value="symbol" ${symbol_checked}/><label>Gene Symbol</label>
                                    <div class="clear"></div>
                                    <input type="radio" name="search_type" value="alias" ${alias_checked}/><label>Aliases</label>
                                    <div class="clear"></div>
                                    <input type="radio" name="search_type" value="entrez" ${entrez_checked}/><label>Entrez</label>
                                    <div class="clear"></div>
                                    <input type="radio" name="search_type" value="refseq" ${refseq_checked}/><label>Refseq</label>
                                    <div class="clear"></div>
                                    <input type="radio" name="search_type" value="probe" ${probe_checked}/><label>Probe</label>
                                </dd>
                        <dt>Upload File:</dt>
                        <dd><input type="file" name="gene_set_file" /></dd>
                        <input type="hidden" name="posted" value="1">
                      </dl>
                      <input type="submit" name="authform" value="Upload" />
                      <div class="clear"></div>
                    </form>
                </div>
            </div>
        </div>
    </div>
