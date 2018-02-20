
autocompleteTimeout = 5000;


function check_browser_version(browser_version,minimum_version){
    if (parseInt(browser_version) < minimum_version && (document.URL.indexOf('browser_compatibility') == -1)){
        window.location=BASE_PATH+'contents/browser_compatibility';
    }
}


function check_browser(){
    // from here: http://stackoverflow.com/questions/2400935/browser-detection-in-javascript
    navigator.sayswho= (function(){
        var ua= navigator.userAgent, tem,
        M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
        if(/trident/i.test(M[1])){
            tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
            return 'IE '+(tem[1] || '');
        }
        if(M[1]=== 'Chrome'){
            tem= ua.match(/\b(OPR|Edge)\/(\d+)/);
            if(tem!= null) return tem.slice(1).join(' ').replace('OPR', 'Opera');
        }
        M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
        if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
        full_browser_name = M.join(' ');
        browser_name = M[0];
        browser_version = M[1];
        return [browser_name,browser_version];
    })();

    result = navigator.sayswho;

    browser_name = result[0];
    browser_version = result[1];

    if (browser_name == 'Chrome'){
        minimum_version = 39;
        check_browser_version(browser_version,minimum_version);
    }

    if (browser_name == 'Firefox'){
        minimum_version = 34;
        check_browser_version(browser_version,minimum_version);
    }

    if (browser_name == 'Safari'){
        minimum_version = 7;
        check_browser_version(browser_version,minimum_version);
    }

    if (browser_name == 'MSIE'){
        minimum_version = 11;
        check_browser_version(browser_version,minimum_version);
    }

}





function project_grandiose_click_header(){
    $('div.pg_header').click(function(){
        window.location = BASE_PATH + 'project_grandiose';
    });
}

function filterGeneSymbol(geneSymbol,delimiter){

    var tempSymbol = geneSymbol.split(' ');
    var showSymbol = tempSymbol[0];

    for (var i =1;i<tempSymbol.length;++i){

        var thisSymbol = tempSymbol[i];

        if (thisSymbol.search(/LOC[0-9]{1,10}?/)) {
            showSymbol =showSymbol +delimiter+ thisSymbol;
        }
    }

    return showSymbol;

}



function filterGeneDescription(geneSymbol,geneDescription){

    delimiter = '&lt;br /&gt;';

    var tempSymbol = geneSymbol.split(' ');
    var tempDescription = geneDescription.split(delimiter);
    var showDescription = tempDescription[0];

    for (var i =1;i<tempSymbol.length;++i){

        var thisSymbol = tempSymbol[i];
        if (thisSymbol.search(/LOC[0-9]{1,10}?/)) {
            showDescription =showDescription +'<br />'+ tempDescription[i];
        }
    }

    return showDescription;
}

// http://greenethumb.com/article/1429/user-friendly-image-saving-from-the-canvas/
function CanvasSaver(url) {

    this.url = url;

    this.savePNG = function(cnvs, fname) {
        if(!cnvs || !url) return;
        fname = fname || 'picture';

        var data = cnvs.toDataURL("image/png");
        data = data.substr(data.indexOf(',') + 1).toString();

        var dataInput = document.createElement("input") ;
        dataInput.setAttribute("name", 'imgdata') ;
        dataInput.setAttribute("value", data);
        dataInput.setAttribute("type", "hidden");

        var nameInput = document.createElement("input") ;
        nameInput.setAttribute("name", 'name') ;
        nameInput.setAttribute("value", fname + '.png');

        var myForm = document.createElement("form");
        myForm.method = 'post';
        myForm.action = url;
        myForm.appendChild(dataInput);
        myForm.appendChild(nameInput);

        document.body.appendChild(myForm) ;
        myForm.submit() ;
        document.body.removeChild(myForm) ;
    };

}

function export_image_button_click(){
    // handlers for graph image export
    var cs = new CanvasSaver('/main/save_image')

    $('.exportImageButton').unbind("click");
    $('.exportImageButton').click(function(e){


        graph_id = $(this).attr('data-id');

        var ecanvas = $(graph_id + " canvas.flot-base").get(0);

        fname = 'save_img';
        cs.savePNG(ecanvas, fname);


        //var img_src = $(Canvas2Image.saveAsPNG(ecanvas, true)).attr("src");
        //window.open(img_src, "Graph Image", "location=no,menubar=no,toolbar=no,titlebar=no");
        return false;
    });

    $('.exportLegendButton').unbind("click");
    $('.exportLegendButton').click(function(e){
        graph_id = $(this).attr('data-id');
        var ecanvas = $(graph_id + " canvas").get(0);
        fname = 'save_img';
        cs.savePNG(ecanvas, fname);

        return false;
    });
}

function help_icon_in_page_help(){
    $('div.help_icon').hover(function(){
        $("div.help_icon ul").addClass('main_help_menu').removeClass('hidden');

    });
    var ref_id = "help";
    var ref_type = "help_in_page";
    $helpButton = $('div.help_icon a.page_guide');
    $('div.help_icon a').click(function(){
        $("div.help_icon ul.main_help_menu").removeClass('main_help_menu').addClass('hidden');
    });
    $('div.help_icon').on('click.PageGuide','a.page_guide',function(event){
        if (helpsystem.pageHelp.isOn) {
            helpsystem.pageHelp.turnOff();
            $helpButton.removeClass('active');
        } else {
            helpsystem.pageHelp.turnOn();
            $helpButton.addClass('active');
            audit_help_log(ref_id,ref_type);
        }

        return false;
    });

}
function dropdown_buttons(){

    // dropdown code for buttons
    $("body").on('click', 'a.button.dropdown', function(e) {
        e.preventDefault();
        var $button = $(this);
        var $menu = $button.parent().children("ul");
        $button.addClass("down");
        $menu.toggle();
        $('ul.submenu').bind('mouseup', function(e) {
            $("ul.submenu").hide();
            $button.removeClass("down");
            $('ul.submenu').unbind('mouseup');
        });
    });
    $('ul.buttonMenus ul.submenu').on( "mouseleave", function() {
        $(this).hide();
    });



}

function contextHelpClick(){
    $helpButton = $('a.helpPopup,a.helpbtnPopup,#helpMenu');
    $helpButton.unbind("click");
    var ref_id = "help";
    var ref_type = "help_in_page";
    $helpButton.click(function(event){
        if (helpsystem.pageHelp.isOn) {
            helpsystem.pageHelp.turnOff();
            $helpButton.removeClass('active');
        } else {
            helpsystem.pageHelp.turnOn();
            $helpButton.addClass('active');
            audit_help_log(ref_id,ref_type);
        }
        return false;
    });
}

function audit_help_log (ref_id,ref_type) {
    var url = window.location.href.split('//') ; //this splits url into two parts http: and www.stemformatics.org/controller/action
    if (!url[1].split(BASE_PATH)[1] || !url[1].split(BASE_PATH)[2]) {
      var controller = "";
      var action = "";
    }
    else {
      // splits www.stemformatics.org/controller/action on every '/' and gets the controller name
      var controller = url[1].split(BASE_PATH)[1];
      // splits www.stemformatics.org/controller/action on every '/' and gets the action name
      var action = url[1].split(BASE_PATH)[2].split('?')[0];
    }

    $.ajax({
      url: BASE_PATH + 'main/audit_help_log',
      data: {ref_id: ref_id, ref_type: ref_type, controller: controller, action: action}
    });
}

//////////////////////////
// URL PARSER
// parseUri 1.2.2
// (c) Steven Levithan <stevenlevithan.com>
// MIT License
function parseUri (str) {
    var o   = parseUri.options,
        m   = o.parser[o.strictMode ? "strict" : "loose"].exec(str),
        uri = {},
        i   = 14;

    while (i--) uri[o.key[i]] = m[i] || "";

    uri[o.q.name] = {};
    uri[o.key[12]].replace(o.q.parser, function ($0, $1, $2) {
        if ($1) uri[o.q.name][$1] = $2;
    });

    return uri;
};
parseUri.options = {
    strictMode: false,
    key: ["source","protocol","authority","userInfo","user","password","host","port","relative","path","directory","file","query","anchor"],
    q:   {
        name:   "queryKey",
        parser: /(?:^|&)([^&=]*)=?([^&]*)/g
    },
    parser: {
        strict: /^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)/,
        loose:  /^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/
    }
};

function URL(url) {

    url = url.replace('#','');
    temp_result = url.split("?");
    this.base_url = temp_result[0];
    get_data = temp_result[1];

    get_data_array = get_data.split('&');

    get_dict = {};
    for (var pos in get_data_array){
        temp_result = get_data_array[pos].split('=');
        get_dict[temp_result[0]] = temp_result[1];
    }
    this.get_data = get_dict;

}

URL.prototype.get_url = function(){
    temp_array = [];
    for (key in this.get_data){
        value = this.get_data[key];
        if (value != ""){
            temp_string = key+'='+value;
            temp_array.push(temp_string);
        }
    }
    var temp_url = temp_array.join('&');

    url = this.base_url + "?" + temp_url;
    return url;
}

CURRENT_URL = parseUri(window.location);
////////////////////////////////

////////////////////////////////
// Viewport - jQuery selectors for finding elements in viewport
// Copyright (c) 2008-2009 Mika Tuupola
// Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
// Project home: http://www.appelsiini.net/projects/viewport




(function($){$.belowthefold=function(element,settings){var fold=$(window).height()+$(window).scrollTop();return fold<=$(element).offset().top-settings.threshold;};$.abovethetop=function(element,settings){var top=$(window).scrollTop();return top>=$(element).offset().top+$(element).height()-settings.threshold;};$.rightofscreen=function(element,settings){var fold=$(window).width()+$(window).scrollLeft();return fold<=$(element).offset().left-settings.threshold;};$.leftofscreen=function(element,settings){var left=$(window).scrollLeft();return left>=$(element).offset().left+$(element).width()-settings.threshold;};$.inviewport=function(element,settings){return!$.rightofscreen(element,settings)&&!$.leftofscreen(element,settings)&&!$.belowthefold(element,settings)&&!$.abovethetop(element,settings);};$.extend($.expr[':'],{"below-the-fold":function(a,i,m){return $.belowthefold(a,{threshold:0});},"above-the-top":function(a,i,m){return $.abovethetop(a,{threshold:0});},"left-of-screen":function(a,i,m){return $.leftofscreen(a,{threshold:0});},"right-of-screen":function(a,i,m){return $.rightofscreen(a,{threshold:0});},"in-viewport":function(a,i,m){return $.inviewport(a,{threshold:0});}});})(jQuery);
////////////////////////////////
// could put this into it's own javascript for readability
$(function () {

    $('div.showText').mouseover(function(){
        $(this).children().addClass('hoverState').children().addClass('hoverState');

    }).mouseout(function(){
        $(this).children().removeClass('hoverState').children().removeClass('hoverState');
    });

    /* setup all the links to confirm that you are going to another site */
    $('a[target=_blank]').click(function(){
            var answer = confirm("The link you clicked is opening up another window/tab. Is that OK?");

            if (!answer) {
                return false;
            }
        });

    project_grandiose_click_header();
    $('body').on('click','a.in_page_tutorial_link',function (){
        tutorial_name= $(this).attr('data-tutorial');
        helpsystem.tutorial.start(tutorial_name);
        return false;
    });

    /* remove the recaptcha what's this from the confirmation */
    if ($('#recaptcha_whatsthis_btn')) {
        $('#recaptcha_whatsthis_btn').unbind('click');
    }


    $('#ucsc_select').change(function(){
        var url = $(this).val();
        if (url!=0){
            newwindow = window.open(url, "_blank", "resizable=yes, scrollbars=yes, width=1024, height=900, top=10, left=10");
        }
    });


    $('div.search_box a.searchButton').hover(
        function () {
            $(this).children("img").attr("src", BASE_PATH+'images/show_genes_rollover.png');
        },
        function () {
            $(this).children("img").attr("src", BASE_PATH+'images/show_genes.png');
        }
    );



    $('body').on('click','div.wb_help_bar',function(){


        $(this).children().html("Hide help information <img class=\"help\" src=\""+BASE_PATH+"images/workbench/minus.png\"\">");

        $(this).removeClass('wb_help_bar').addClass('wb_help_bar_showing');
        $(this).next('.wb_help').addClass('wb_help_showing').removeClass('wb_help');

    });

    $('body').on('click','div.wb_help_bar_showing',function(){

        $(this).children().html("Show help information <img class=\"help\" src=\""+BASE_PATH+"images/workbench/plus.png\"\">");

        $(this).removeClass('wb_help_bar_showing').addClass('wb_help_bar');
        $(this).next('.wb_help_showing').addClass('wb_help').removeClass('wb_help_showing');

    });


    /* lazy - set all the extra pngs here */

    $('div.wb_help_bar div.wb_help_bar_inner_div').html("Show help information <img class=\"help\" src=\""+BASE_PATH+"images/workbench/plus.png\"\">");


    /*
     *  Options for each workbench mako template for the flags
     *

        <div class="hidden" id="show_help_flag">NO</div>
        <div class="hidden" id="help_flag_message">Password is 15 characters with at least one space</div>
        <div class="hidden" id="help_flag_top_position">300px</div>
        <div class="hidden" id="help_flag_left_position">482px</div>
     *
     *
     * */


    var showFlag = $('#show_help_flag').html();

    if (showFlag == 'NO'){
        $('div.flag').remove();
    } else {

        var newFlagMessage = $('#help_flag_message').html();

        if (newFlagMessage != null) {
            $('div.flag div.flag_inner_div').html(newFlagMessage);
        }

        var newFlagTopPosition = $('#help_flag_top_position').html();

        if (newFlagTopPosition != null) {
            $('div.flag').css('top',newFlagTopPosition);
        }


        var newFlagLeftPosition = $('#help_flag_left_position').html();

        if (newFlagLeftPosition != null) {
            $('div.flag').css('left',newFlagLeftPosition);
        }


      }
     $('a.wb_open_help').click(function(){

        $('div.wb_help_bar_inner_div').click();

     });


    simple_tooltip('div.large_icon','tooltip');
    simple_tooltip('a.logo','tooltip');

    help_icon_in_page_help();
    dropdown_buttons();

});


function simple_tooltip(target_items, name){
 $(target_items).each(function(i){


        $(this).mouseover(function(){
                my_tooltip = create_tooltip($(this))
                my_tooltip.css({ display:"none"}).fadeIn(40);
        }).mousemove(function(kmouse){
                my_tooltip.css({left:kmouse.pageX+15, top:kmouse.pageY-15});
        }).mouseout(function(){
                my_tooltip.fadeOut(40);
                my_tooltip.remove();
        });
    });
}

function create_tooltip(this_object){
        $('#generic_tooltip').remove();
        $("body").append("<div id='generic_tooltip'><p>"+this_object.attr('data_hover_text')+"</p></div>");
        var my_tooltip = $("#generic_tooltip");
        return my_tooltip;
}

function innate_db_link_clicks(){

    $('a.innate_db').click(function(){
        // have to set the type when passing to innatedb
        innate_db_type = $(this).attr('data_type');

        var answer = confirm("This will take you to the InnateDB website. Any analyses will need to be saved at this website. Is that OK?");

        if (!answer) {
            return false;
        }


        $('form.innate_db_form input[name="listType"]').val(innate_db_type);
        $('form.innate_db_form').submit();
    });
}


function setup_feature_search_autocomplete(details){

    /*
    var details = new Object();
    details.id = "#featureSearch";
    details.data_url = BASE_PATH + 'genes/get_feature_search_autocomplete?feature_type=all&db_id=';
    details.target_url = BASE_PATH + 'genes/feature_search?feature_search_term=';
    details.append_to = ".searchBox";
    */
    // NOTE: I had the following two statements joined together but got an error when minifying. So I kept them separate.
    var feature_search_autocomplete = $(details.id);

    if (feature_search_autocomplete.length > 0) {
        feature_search_autocomplete.autocomplete({
            source: details.data_url,
            minLength: 4, // because the names are very small eg. STAT1
            timeout: autocompleteTimeout,
            appendTo: details.append_to,
            select: function(event, ui) {
                var feature = ui.item.feature_id;
                window.location =  details.target_url + encodeURIComponent(feature);
            }
        });
        // This should be separated as per the comment above. DOesn't work when minifying using Portal/setup_js_minify.sh
        feature_search_autocomplete.data("ui-autocomplete")._renderItem = function( ul,item ){
            html = $("<li></li>").append("<a> <div class='symbol'>" + item.symbol + "</div><div class='species'>"+item.species+"</div><div class='aliases'>"+item.aliases+"</div><div class='description'>"+item.description+"</div><div class='clear'></div></a>").appendTo(ul);
            return html;
        };
    }

}

/*
    How to use the ajax_search class in a mako template

    <script>
        base_url = BASE_PATH+"msc_signature/rohart_msc_test";
        filter_dict = {'rohart_msc_test':true};
        set_view_datasets(base_url,filter_dict);
    </script>


    in mako template:
        <%def name="show_all_option()"> </%def>
        ${Base.pre_enclosed_search_box()}
        ${Base.setup_dataset_search_box_variables()}
        ${Base.enclosed_search_box(text,self.show_all_option)}

    example see msc_signature/rohart_msc_test.mako

*/

var  ajax_search;

ajax_search = function(init_options)
{
    var base_url,
        data,
        data_type,
        html,
        table_id,
        ajax_url;

    this.get_base_url = function(){
        return base_url;
    } // end set_data


    this.set_data = function(new_data){
        data = new_data;
        return true;
    } // end set_data

    this.get_data = function(){
        return data;
    } // end get_data

    this.get_ajax_url = function(){
        return ajax_url;
    } // end get_data

    this.get_html = function(){
        return html;
    } // end get_data



    // T#2372 we don't need search anymore, it's in data.filter
    // T#2372 need to make this dataset specific
    // T#2372 relying on a data.filter - will need a new action to make this easier to move. need filter,genes and order (not used yet) options
    // T#2372 could make genes the same as the current autocomplete, list of associated arrays
    this.build_html_from_data_for_datasets = function(json_data,search){
        data = jQuery.parseJSON(json_data);
        datasets = data.datasets;
        filter = data.filter; // original search query
        html =
           '<div class="basic_help">Select a dataset</div>' +

           '<div class="multi_select">' +
               '<div class="export">'+
                   '<ul class="buttonMenus">'+
                        '<li id="exportMenu">'+
                            '<a class="button dropdown">'+
                                '<span><span class="icon go"></span>Export</span><span class="arrow down"></span>'+
                            '</a>'+
                            '<ul class="submenu">'+
                                '<li><a href="'+base_url+'?filter='+filter+'&export=true" id="exportTableCSVButton">Export Data</a></li>'+
                            '</ul>'+
                        '</li>'+
                    '</ul>'+
                '</div>'+


               '<table id="'+table_id+'" class="fixed">'+
                    '<thead>'+
                        '<tr>'+
                            '<th>Datasets</th>'+
                        '</tr>'+
                    '</thead>'+
                    '<tbody>';

        count = 0;
        for (ds_id in datasets){
            count++;
            row = datasets[ds_id];
            name = row.name;
            cells_samples_assayed = row.cells_samples_assayed;
            organism = row.organism;
            title = row.title;
            html = html +
                            '<tr>'+
                                '<td>'+
                                    '<div class="multi_select_row">'+
                                        '<a id="choose_dataset_'+ds_id+'" href="'+base_url+'?ds_id='+ds_id+'&filter='+filter+'">'+
                                            '<div class="inner">'+
                                                '<div class="title">'+title+'</div>'+
                                                '<div class="handle">'+name+'</div>'+
                                                '<div class="cells">'+cells_samples_assayed+'</div>'+
                                            '</div>'+
                                            '<div class="organism">'+organism+'</div>'+
                                            '<div class="small_arrow"></div>'+
                                            '<div class="clear"></div>'+
                                        '</a>'+
                                    '</div>'+
                                '</td>'+
                               '</tr>';

        }


                html = html +
                    '</tbody>'+
                '</table>'+
        '</div>';

        return html;

    }

    // THis is for the genes
    this.build_html_from_data_for_genes = function(json_data,search){
        data = jQuery.parseJSON(json_data);
        genes = data.genes;
        filter = data.filter; // original search query
        html =
           '<div class="basic_help">Select a gene</div>' +

           '<div class="multi_select">' +
               '<div class="export">'+
                   '<ul class="buttonMenus">'+
                        '<li id="exportMenu">'+
                            '<a class="button dropdown">'+
                                '<span><span class="icon go"></span>Export</span><span class="arrow down"></span>'+
                            '</a>'+
                            '<ul class="submenu">'+
                                '<li><a href="'+base_url+'?filter='+filter+'&export=true" id="exportTableCSVButton">Export Data</a></li>'+
                            '</ul>'+
                        '</li>'+
                    '</ul>'+
                '</div>'+


               '<table id="'+table_id+'" class="fixed">'+
                    '<thead>'+
                        '<tr>'+
                            '<th>Genes</th>'+
                        '</tr>'+
                    '</thead>'+
                    '<tbody>';

        count = 0;
        for (number in genes){
            count++;
            row = genes[number];
            aliases = row.aliases;
            species = row.species;
            ensembl_id = row.ensembl_id;
            db_id = row.db_id;
            description = row.description;
            symbol = row.symbol;
/*
<div class="multi_select_row">
                    <a href="/genes/search?gene=mincle&amp;ensembl_id=ENSG00000166523">
                        <div class="inner">
                            <div class="title"><span class="ensembl_id">ENSG00000166523</span> CLEC4E </div>
                            <div class="handle">CLECSF9 MINCLE</div>
                            <div class="cells">C-type lectin domain family 4, member E </div>
                        </div>
                        <div class="organism">Homo sapiens</div>
                        <div class="small_arrow"></div>
                        <div class="clear"></div>
                    </a>
                </div>

 */
           html = html +
                            '<tr>'+
                                '<td>'+
                                    '<div class="multi_select_row">'+
                                        '<a id="choose_gene_'+ensembl_id+'" href="'+base_url+'?ensembl_id='+ensembl_id+'&filter='+filter+'">'+
                                            '<div class="inner">'+
                                                '<div class="title"><span class="ensembl_id">'+ensembl_id+'</span>'+symbol+'</div>'+
                                                '<div class="handle">'+aliases+'</div>'+
                                                '<div class="cells">'+description+'</div>'+
                                            '</div>'+
                                            '<div class="organism">'+species+'</div>'+
                                            '<div class="small_arrow"></div>'+
                                            '<div class="clear"></div>'+
                                        '</a>'+
                                    '</div>'+
                                '</td>'+
                               '</tr>';

        }


                html = html +
                    '</tbody>'+
                '</table>'+
        '</div>';

        return html;

    }



    this.show_html = function(html,data_type){

        $('#wb_modal_title').html('Showing all '+count+' '+data_type+' for "'+filter+'"');
        $('#wb_modal_content').html(html);
        $('#wb_modal_content div.multi_select').show();

        $('#modal_div').modal({
            minHeight: 400,
            minWidth: 800,
            onShow:function (dialog){
                $("#"+table_id).dataTable({
                    "bPaginate": false,
                    "bLengthChange": false,
                    "bFilter": true,
                    "bSort": false,
                    "bInfo": false,
                    "bAutoWidth": false,
                    "oLanguage": {"sSearch": "Filter: "}
                })
            }

        });

    }

    this.get_data_from_ajax = function(filter_dict){
        var build_html_from_data_for_datasets = this.build_html_from_data_for_datasets;
        var build_html_from_data_for_genes = this.build_html_from_data_for_genes;
        var show_html = this.show_html;
        var data_type = this.data_type;
        url = ajax_url + '?';

        filters = new Array();
        for (key in filter_dict){
            value = filter_dict[key];
            url_part = key+'='+value;
            filters.push(url_part);
        }
        url = url + filters.join('&');

        var request = $.ajax({
            type: "POST",
            data: data,
            url: url
        });

        request.done(function(data) {
            // T#2372 would have a data_type if statement here
            // T#2372 if data_type == datasets or data_type == genes
            if (data_type == 'datasets'){
                html = build_html_from_data_for_datasets(data,filter);
                show_html(html,data_type);
            }
            if (data_type == 'genes'){
                build_html_from_data_for_genes(data,filter);
                show_html(html,data_type);
            }
        });

        request.fail(function( jqXHR, textStatus ) {
          alert( "Request failed: " + textStatus );
        });

    } // get_data_from_ajax

    // constructor to run right at the start
    this.init = function(init_options){
        html = init_options.html;
        ajax_url = init_options.ajax_url;
        data = init_options.data;
        data_type = init_options.data_type;
        base_url = init_options.base_url;

        // T#2372 would have a data_type here

    } // end init

    // constructor to run right at the start
    this.init(init_options);

    return this;
}  // end of ajax_search

/*  set_view_datasets can be called from any mako template that has a datasets
    example is from workbench/rohart_msc_landing_page.mako
    $(document).ready(function() {
        base_url = BASE_PATH+"msc_signature/rohart_msc_test";
        filter_dict = {'rohart_msc_test':true};
        set_view_datasets(base_url,filter_dict);
    });
*/

function set_view_datasets(base_url,filter_dict){

        search_button_id = "#view_datasets";
        input_text_field_id = "#dataset_search";
        data_type = "datasets";
        set_search_and_choose(base_url,filter_dict,search_button_id,input_text_field_id,data_type);

}


/*  set_search_and_choose can be called from any mako template
    $(document).ready(function() {
        base_url = base_path+"msc_signature/rohart_msc_test";
        filter_dict = {'rohart_msc_test':true};
        search_button_id = "#view_datasets";
        input_text_field_id = "#dataset_search";
        data_type = "datasets"; // or genes
        set_search_and_choose(base_url,filter_dict,search_button_id,input_txt_field_id,data_type);
    });
*/

function set_search_and_choose(base_url,filter_dict,search_button_id,input_text_field_id,data_type){

        // only do this if the element is there
        if ( search_button_id.length ) {

            // data_type eg. genes or datasets
            ajax_url =BASE_PATH + data_type + "/search_and_choose_"+data_type+"_ajax"

            var options = {
                base_url: base_url,
                data_type: data_type,
                ajax_url: ajax_url
            }

            var this_ajax_search = ajax_search(options);
            ajax_url = this_ajax_search.get_ajax_url();

            input_text_field = $(input_text_field_id);
            search_button = $(search_button_id);
            // this is for when the press enter
            input_text_field.keypress(function(e){
                if(e.which == 13){
                    e.preventDefault();
                    filter = input_text_field.val().replace("<script>","").replace("</script>","");
                    filter_dict['filter'] = filter;
                    this_ajax_search.get_data_from_ajax(filter_dict);
                }
            });

            // this is for when they click the button
            search_button.click(function(e){
                e.preventDefault();
                filter = input_text_field.val().replace("<script>","").replace("</script>","");
                filter_dict['filter'] = filter;
                this_ajax_search.get_data_from_ajax(filter_dict);
            });
        }
}




/*
    data_table is to create a modal table for showing graph data
    it will have a filter and you can pass in the columns you want to show
    data will be using d3 format - which is an array of objects

    Usage:
        options = {
            title: "Hello",
            data:data,
            target_id: "#table",
            columns_to_show_in_order: ['chip_id','Replicate Group ID'],
            table_class: "show_data_table"
        }
        var new_show_table = data_table(options);

*/
data_table = function(init_options)
{
    var title,
        ds_id,
        data,
        min_height,
        min_width,
        click_target_id,
        column_names,
        columns_to_show_in_order,
        div_class;

    this.setup_click_target_id = function(){
        target = $(click_target_id);
        var show_data_table = this.show_data_table;
        target.click(function(){
            show_data_table();
        });
    } // setup_click_target_id


    this.show_data_table = function(){
        // make this modal
        // add in a dataTable call

        html =
           '<div class="'+div_class+'">'+
               '<table id="'+id_for_table+'" class="fixed">'+
                    '<thead>'+
                        '<tr>';

        for (key in columns_to_show_in_order){
            value = column_names[key];
            html = html + '<th>'+value.replace(/_/g,' ')+'</th>';
        }


        html = html +
                        '</tr>'+
                    '</thead>'+
                    '<tbody>';

        count = 0;
        for (row_num in data){
            count++;
            row = data[row_num];
            html = html +
                           '<tr>';

            for (key in columns_to_show_in_order){
                column_name = columns_to_show_in_order[key];
                value = row[column_name];

                if (is_float(value)){
                    value = round_to_two_decimal_places(value);
                }

                html = html + '<td>'+value+'</td>';
            }


            html = html +
                           '</tr>';

        }


        html = html +
                    '</tbody>'+
                '</table>'+
        '</div>';




        $('#wb_modal_title').html(title);
        $('#wb_modal_content').html(html);
        $('#modal_div').modal({
            minHeight: min_height,
            minWidth: min_width,
            onShow:function (dialog){
                $("#"+id_for_table).dataTable({
                    "bPaginate": false,
                    "bLengthChange": false,
                    "bFilter": true,
                    "bSort": true,
                    "bInfo": false,
                    "oLanguage": {"sSearch": "Filter: "},
                    "aaSorting": [[ 1, "asc" ]],
                    "bAutoWidth": false
                })
            }
        });

    } // set_data

    // constructor to run right at the start
    this.init = function(init_options){
        title = init_options.title;
        click_target_id = init_options.click_target_id;
        min_width = init_options.min_width;
        min_height = init_options.min_height;
        ds_id = init_options.ds_id;
        column_names = init_options.column_names;
        data = init_options.data;
        columns_to_show_in_order = init_options.columns_to_show_in_order;
        div_class = init_options.div_class;
        id_for_table = ds_id+div_class;
        table_id = "new_choose_dataset";
        this.setup_click_target_id();
    } // end init

    // constructor to run right at the start
    this.init(init_options);

    return this;
}


function round_to_two_decimal_places(num){
    new_num = Math.round(num * 100) / 100;
    return new_num;
}

function is_float(value) {

    var er = /^-?[.0-9]+$/;

    return er.test(value);
}

function check_user_logged_in_for_sharing(){
        // check that the user is logged in and if so, display a warning and exit
        var full_name = $("#full_name").html();
        var uid = $("#uid").html();
        if (uid == "0" || full_name =="Guest Account"){

            $('#wb_modal_title').html('Share this graph');
            $('#wb_modal_content').html('You must be logged in to share in '+SITE_NAME+'.');

            $('#modal_div').modal({
                minHeight: 80
            });
            return false;
        }
        return true;
}
