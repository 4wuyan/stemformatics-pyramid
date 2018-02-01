<%inherit file="../default.html"/>
<%namespace name="Base" file="../base.mako"/>

<%def name="includes()">
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/gene_set_manage_bulk_import.css')}" >
    <script type="text/javascript" src="${h.url('/js/workbench/gene_set_manage_bulk_import.js')}"></script>
</%def>




    <div id="wb_background" class="wb_background_divs">
        <div id="wb_background_inner_div">


            <div class="wb_question_groups_selected">
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                % if c.gene_set_id is None:
                                    Add/paste Gene List
                                % else:
                                    Add genes to ${c.gene_set_name}
                                % endif
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">
                                <p>
                                    Enter a gene list in the genes text box by copy/paste, or entering manually.
                                </p>
                                <p>
                                    We accept gene symbols, Ensembl and Entrez IDs, aliases and probes.
                                </p>
                                <p>
                                    "Total" is the total number of separate inputs.
                                    <br/>
                                    "Ambiguous" is the number of inputs that map to two or more Ensembl identifiers.
                                    <br/>
                                    "No match" signifies that the input did not match an Ensembl identifier.
                                    <br/>
                                    "Match" is the number of inputs that matched to an Ensembl identifier.
                                    <br/>
                                    "Ensembl Identifiers" is the number of unique Ensembl identifiers that will be in a Gene list if saved.
                                </p>
                                <p>
                                    Use the "Validate" button to check your gene inputs. When all are "OK", they will be selected and you may "Save" the list to save all the genes that are checked.
                                </p>
                                <p>
                                    You can select "Select all genes for ambiguous items" and then click on "Validate" to select every gene that was associated with the ambiguous items.
                                </p>
                                <p>
                                    Click on the Ambiguous, No match or Match plus signs to show a detailed list of inputs.
                                </p>
                                <p>
                                    Note: Click on "Ambiguous" genes to resolve gene ambiguity. These genes will be converted to Ensembl IDs.
                                </p>
                            </div>
                        </div>

                    </div>
                    <div class="clear"></div>
                </div>
            </div>

            <div id="form" class="gene_set_bulk">
                <div class="innerDiv">

                    <div class="title">Bulk Import Manager</div>
                    ${c.error_message}
                    <form action="${h.url('/workbench/gene_set_bulk_import_manager')}" method="post" id="form_gene_set_items">

                        <input type="hidden" name="gene_set_id" value="${c.gene_set_id}"/>
                        <% value_ambiguous = 1 if c.select_all_ambiguous else 0 %>
                        <input type="hidden" name="select_all_ambiguous" id="select_all_ambiguous" value="${value_ambiguous}"/>

                        <input type="hidden" id="gene_set_name" name="gene_set_name" value=""/>
                        <input type="hidden" name="description" id="description" />

                        <div id="col_left">
                            <dl class="gene_sets">
                                <dt>
                                    Paste / Edit List of Genes
                                </dt>
                                <dd>
                                    <textarea name="revalidateText" id="revalidateText">${c.gene_set_raw}</textarea>
                                </dd>
                            </dl>
                        </div>

                        <div id="col_right">

                            <div id="search-options">
                                <dl class="col1">
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
                                            probes_chr_checked = ''

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

                                            if c.search_type == 'probes_using_chromosomal_locations':
                                                probes_chr_checked = 'checked'
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
                                        <div class="clear"></div>
                                        <input type="radio" name="search_type" value="probes_using_chromosomal_locations" ${probes_chr_checked}/><label>Probe (chromosomal locations)</label>

                                    </dd>
                                </dl>
                                <dl class="col2">
                                    <dt>Species:</dt>
                                    <dd>
                                        <%
                                            try:
                                                c.db_id = int(c.db_id)
                                            except:
                                                c.db_id = None

                                        %>
                                        <%
                                            if c.db_id == c.human_db or c.db_id is None:
                                                human_checked = 'checked'
                                                mouse_checked = ''
                                            else:
                                                human_checked = ''
                                                mouse_checked = 'checked'
                                        %>
                                        <input type="radio" name="db_id" value="${c.human_db}"  ${human_checked} /><label>Human</label>
                                        <div class="clear"></div>
                                        <input type="radio" name="db_id" value="${c.mouse_db}" ${mouse_checked} /><label>Mouse</label>
                                    </dd>
                                    <dt>
                                        Select all ambiguous
                                    </dt>
                                    <dd>
                                        <input id="select_all_ambiguous_checkbox" type="checkbox"

                                        % if c.select_all_ambiguous:
                                            checked
                                        %endif

                                        /><label> Select all ambiguous genes</label>
                                    </dd>
                                </dl>
                            </div>

                            <%
                                overall_total = 0
                                raw_ok_total = 0

                                ambiguous_dict = {}
                                not_found_dict = {}
                                ok_dict = {}
                                for item in c.gene_set_processed:

                                    overall_total +=1

                                    status = c.gene_set_processed[item]['status']
                                    original = c.gene_set_processed[item]['original']
                                    symbol = c.gene_set_processed[item]['symbol']
                                    ensemblID = c.gene_set_processed[item]['ensemblID']
                                    checked = "checked" if status == "OK" else ""

                                    temp_dict = {'status': status, 'original': original, 'symbol':symbol,'ensemblID': ensemblID,'checked':checked}

                                    if c.gene_set_processed[item]['status'] == 'Ambiguous':
                                        ambiguous_dict[original] = temp_dict
                                    elif c.gene_set_processed[item]['status'] == 'Not found':
                                        not_found_dict[original] = temp_dict
                                    else:
                                        raw_ok_total += 1
                                        if ensemblID not in ok_dict:
                                            ok_dict[ensemblID] = temp_dict
                                        else:
                                            ok_dict[ensemblID]['original'] = ok_dict[ensemblID]['original'] + " " + original
                            %>

                            <div class="clear"></div>

                            <div id="buttons_top">
                                <input type="submit" name="validate" id="revalidate" value="Validate"></input>
                                % if not c.hide_save:
                                    <input type="submit" name="saveGeneSet" id="saveGeneSet" value="Save" />
                                % endif

                                <div class="clear"></div>
                            </div>

                            <h1>Summary</h1>

                            <table id="summary">
                                <thead>
                                    <tr>
                                        <th>Total</th>
                                        <th>Ambiguous</th>
                                        <th>No match</th>
                                        <th>Match</th>
                                        <th>Ensembl Identifiers</th>
                                    </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td>${overall_total}</td>
                                    <td>${len(ambiguous_dict)}</td>
                                    <td>${len(not_found_dict)}</td>
                                    <td>${raw_ok_total}</td>
                                    <td>${len(ok_dict)}</td>
                                </tr>
                                </tbody>
                            </table>

                            % if len(ambiguous_dict) != 0:
                                <h2 id="ambiguous_header">Ambiguous <img class="expand" src="/images/workbench/plus.png"></h2>
<div class="generic_orange_button"><a href="#" id="export_ambiguous" class="linkButtons">EXPORT AMBIGUOUS &gt;</a></div>
                                <table id="ambiguous_table">
                                    <thead>

                                        <tr>
                                            <th id="select">Select</th>
                                            <th id="original">Original</th>
                                            <th id="symbol">Symbol</th>
                                            <th id="status">Choose Gene</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        % for item in ambiguous_dict:
                                            <%
                                                status = ambiguous_dict[item]['status']
                                                original = ambiguous_dict[item]['original']
                                                symbol = ambiguous_dict[item]['symbol']
                                                ensemblID = ambiguous_dict[item]['ensemblID']
                                                print_symbol = ""
                                                for final_symbol in symbol:
                                                    print_symbol = print_symbol + " " + final_symbol
                                            %>
                                            <tr>
                                                <td>
                                                </td>
                                                <td class="original">${original}</td>
                                                <td>${print_symbol}</td>
                                                <td><a class="popup" href="${h.url('/workbench/uniquely_identify_gene?original=')}${original.replace('+','plus')}&db_id=${c.db_id}">${status}</a></td>
                                            </tr>
                                        % endfor
                                    </tbody>
                                </table>
                            % endif

                            % if len(not_found_dict) != 0:
                                <h2 id="not_found_header">Not Match <img class="expand" src="/images/workbench/plus.png" /></h2>
                                <div class="generic_orange_button"><a href="#" id="export_not_found" class="linkButtons">EXPORT NON MATCHES &gt;</a></div>
                                <table  id="not_found_table">
                                    <thead>
                                        <tr>
                                            <th id="original">Original</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        % for item in not_found_dict:
                                            <%
                                                status = not_found_dict[item]['status']
                                                original = not_found_dict[item]['original']
                                                symbol = not_found_dict[item]['symbol']
                                                ensemblID = not_found_dict[item]['ensemblID']
                                            %>
                                            <tr>
                                                <td class="original">${original}</td>
                                            </tr>
                                        % endfor
                                    </tbody>
                                </table>
                            % endif

                            % if len(ok_dict) != 0:
                                <h2 id="ok_header">Match <img class="expand" src="/images/workbench/plus.png"></h2>
                                <div class="generic_orange_button"><a href="#" id="export_ok">EXPORT MATCHES &gt;</a></div>
                                <table id="ok_table">
                                    <thead>
                                        <tr>
                                            <th id="select">Select</th>
                                            <th id="original">Original</th>
                                            <th id="symbol">Symbol</th>
                                            <th>Ensembl ID</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        % for item in ok_dict:
                                            <%
                                                status = ok_dict[item]['status']
                                                original = ok_dict[item]['original']
                                                symbol = ok_dict[item]['symbol']
                                                ensemblID = ok_dict[item]['ensemblID']
                                            %>
                                            <tr>
                                                <td>
                                                    <input type="checkbox" name="${ensemblID}" checked />
                                                </td>
                                                <td class="original">${original}</td>
                                                <td>${symbol}</td>
                                                <td>${ensemblID}</td>
                                            </tr>
                                        % endfor
                                    </tbody>
                                </table>
                            % endif

                        </div><!-- /col_right -->

                        <div id="details_modal" class="modal simplemodal-data">
                            <div id="wb_modal_title" class="wb_modal_title">
                                Enter New Gene List Details
                            </div>
                            <div id="wb_modal_content" class="wb_modal_content">
                                <div class="save-error"></div>
                                <dl>
                                    <dt>Gene List Name:</dt>
                                    <dd>
                                        <input type="text" id="modal_gene_set_name" value="${c.gene_set_name}" />
                                    </dd>
                                    <dt>Gene List Description:</dt>
                                    <dd>
                                        <textarea id="modal_description">${c.description}</textarea>
                                    </dd>
                                    <dt>
                                        <button id="finalGeneSetSave">Save Gene List</button>
                                    </dt> <dd> </dd>
                                </dl>
                                <div class="clear"></div>
                            </div>
                            <div class="clear"></div>
                        </div>

                    </form>
                    <div class="clear"></div>

                </div><!-- /innerDiv -->
                <div class="clear"></div>

            </div><!-- /form -->

        </div><!-- /wb_background_inner_div -->
    </div><!-- /wb_background -->
