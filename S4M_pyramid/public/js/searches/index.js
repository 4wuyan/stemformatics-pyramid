

/* update the search terms underneath the search boxes */
function updateSearchTerms(){
    var geneSearch = $("#geneSearch").val();
    var cellSearch = $("#cellSearch").val();
    var sampleSearch = $("#sampleSearch").val();
    
    if (geneSearch == "Type in your gene search"){ geneSearch = "N/A"; }
    if (cellSearch == "Type in your cell search"){ cellSearch = "N/A"; }
    if (sampleSearch == "Type in your sample search"){ sampleSearch = "N/A"; }
    
    var searchDescription = "Search terms  - Gene Search: " + geneSearch + 
    " Cell Search: " + cellSearch + 
    " Sample Search: " + sampleSearch + "<div id='oldSearch' class='hidden'>"+$("#geneSearch").val()+"</div>";
    
    //window.location.replace("/");
    
    $(".showSearchTerms").html(searchDescription).show(); 
    
    /*
    // get the number of samples currently available
    $.ajax({
        url: '/samples/get_summary_data',
        type: 'post',
        data: {geneSearch: $('#geneSearch').val()},
        success: function(data) {
            
            var returnDetails = jQuery.parseJSON(data);
            
            sampleSummary = "Number of Samples detected (should be gene centric): " + returnDetails["count"] + 
            " Summary: " + returnDetails["details"];
            
            $(".showSearchTerms").html(searchDescription).show();  
            
            
            $(".showSampleSummary").html(sampleSummary).show();  
            
        }
    });    
    */
}


/* get the gene details to display on the first tab */
function getGeneDetails (){
    // What we want to do is get back the gene description after the enter button has been pressed
    $('#displayGeneDetails').show();
    
    // destroy the autocomplete to stop it from kicking in with a fast typist
    $('#geneSearch').autocomplete( 'destroy' );
    
    // now get the details of the gene back
    $.ajax({
        url: BASE_PATH + 'genes/get_details',
        type: 'post',
        data: {geneSearch: $('#geneSearch').val()},
        success: function(data) {
            
            var returnDetails = jQuery.parseJSON(data);
            
            // clear the display gene details div
            $('#displayGeneDetails').html('').show();
            
            var newGeneDetails = '';
            
            // have to do a for each on the returned data
            for ( var gene in returnDetails ) {
                
                newGeneDetails = 
                "<div id='"+ returnDetails[gene]["EntrezID"] +"'>" + 
                    "<div id='ensemblID' class='hidden'>"+returnDetails[gene]["EnsemblID"] +"</div>"+
                    "<div id='official_symbol' class='hidden'>"+returnDetails[gene]["official_symbol"] +"</div>"+
                    "<div class='showDescription showSummary searchable'>" + returnDetails[gene]["official_symbol"] + " - " + returnDetails[gene]["official_name"] + " (hONS "+Math.floor(Math.random()*18)+"/18, MSC "+Math.floor(Math.random()*22)+"/22, MDM-LPS "+Math.floor(Math.random()*19)+"/19) (Click here for More)</div>" + 
                    "<div class='showDescription showEntrez searchable'>Entrez Gene ID: " + returnDetails[gene]["EntrezID"]+ "</div>" + 
                    "<div class='showDescription showEnsembl searchable'>Ensembl ID: " + returnDetails[gene]["EnsemblID"] + "</div>" +                 
                    "<div class='showDescription showEntrez searchable '> Aliases: " + returnDetails[gene]["aliases"]+ "</div>" + 
                    "<div class='showDescription showEntrez'> Pathways: <br>" + returnDetails[gene]["Pathways"].replace(/,/g,'<br>') + "</div>" + 
                    "<div class='showDescription showLocation'>Located at " 
                        + " Chromosome: " + returnDetails[gene]["Location"]["chromosome"] 
                        + " Direction: " + returnDetails[gene]["Location"]["direction"] 
                        + " Start: " + returnDetails[gene]["Location"]["start"] 
                        + " End: " + returnDetails[gene]["Location"]["end"] 
                        + " Orientation: " + returnDetails[gene]["Location"]["orientation"] 
                        + " Strand: " + returnDetails[gene]["Location"]["strand"] 
                        + " Chr: " + returnDetails[gene]["Location"] 
                    + "</div>" + 
                    "<div class='showDescription showAltSplicing'> Evidence of Alt Splicing: " + returnDetails[gene]["alt_splicing"]+ "</div>" + 
                    "<div class='showDescription showCageData'> Evidence of Cage data: " + returnDetails[gene]["cage_data"]+ "</div>" + 
                
                    "<div class='showDescription showEntrez'>Summary for Entrez Gene ID " + returnDetails[gene]["EntrezID"]+ " : " +returnDetails[gene]["description"]+ "</div>" + 
                    "<div class='showDescription showDiseases'> <a target='_blank' href='#'> Diseases:</a> " + returnDetails[gene]["diseases"].substring(0,200) + "</div>"  + 
                    "<div class='showDescription showPubMed'> <a target='_blank' href='#'> Pubmed Links</a> </div>"  + 
                "</div>";
                
                
              
                
                $('#displayGeneDetails').append(newGeneDetails);
            }
            
            $('.showDescription').hide();
            $('.showSummary').show();
            
            $('.showSummary').click(function(){
                $(this).siblings('.showDescription').toggle();
                $('.showSummary').show();   
            });
            
            $('.showDiseases').click(function(){
                window.open('http://www.ncbi.nlm.nih.gov/gene?Db=omim&DbFrom=gene&Cmd=Link&LinkName=gene_omim&LinkReadableName=OMIM&IdsFromResult='+$(this).parent().attr('id'));
            });
            
            
            $('.showPubMed').click(function(){
                window.open('http://www.ncbi.nlm.nih.gov/gene?Db=pubmed&DbFrom=gene&Cmd=Link&LinkName=gene_pubmed&LinkReadableName=PubMed&IdsFromResult='+$(this).parent().attr('id'));
            });
            
            
            $('.showEntrez').click(function(){
                window.open('http://www.ncbi.nlm.nih.gov/gene/'+$(this).parent().attr('id'));
            });
            
            $('.showEnsembl').click(function(){
                
                var ensemblID = $("#ensemblID").html();
                
                if (ensemblID.indexOf('ENSMUSG') == 0){
                    window.open('http://www.ensembl.org/Mus_musculus/Gene/Summary?g='+ensemblID);
                }
                else {
                    window.open('http://www.ensembl.org/Homo_sapiens/Gene/Summary?g='+ensemblID);
                }
                
                
            });
            
            /* Doesn't work 
             * $('.showLocation').click(function(){
                window.open('http://genome.ucsc.edu/cgi-bin/hgTracks?gene='+$("#official_symbol").html());
            }); */                  
            
            // have to reload the autocomplete after we destroyed it - not really the best way of doing this?
    
            $("#geneSearch").autocomplete({
                    source: BASE_PATH + 'genes/get_autocomplete',
                    minLength: 3, // because the names are very small eg. STAT1
                    appendTo: ".searchBox",
                    select: function(event, ui) {  
                                getGeneDetails(); // each time selected, get the gene details
                                updateSearchTerms(); // update the search terms under the search input                        
                            },
                });               
            
            

            
            //$('div.showSummary').draggable();
            
        }
    });
    
}



$(document).ready(function() {
    // do stuff when DOM is ready
    
    // **************** All the tab functions **************************
    $("#tabs").tabs({
        select: function (event,ui) {
            // go home to / if Home page is selected
            if (ui.index ==0) {
                window.location = BASE_PATH;
            }
        }
    });  
   
    // go to the next tab
    $(".nextTab").click( function (){
        // get current tab we are on
        var selected = $('#tabs').tabs('option', 'selected')
        
        // go to next tab
        $('#tabs').tabs("select",selected + 1);
        
    });
    
    // go to the previous tab
    $(".prevTab").click( function (){
        
        // get current tab we are on
        var selected = $('#tabs').tabs('option', 'selected')
        
        // go to next tab
        $('#tabs').tabs("select",selected - 1);
        
    });
    
    // go to the Results tab
    $(".showTab").click( function (){
        
        // go to next tab #4 is show results
        $('#tabs').tabs("select",2);
        
    });    
    
    // go to the Start tab
    $(".startTab").click( function (){
        
        // go to next tab #0 is show results
        $('#tabs').tabs("select",1);
        
    });    
    
    // everytime a new tab is shown, update the search results on the finish page
    $( "#tabs" ).bind( "tabsshow", function(event, ui) {
        $(".searchTerm").focus();
    });


    
    // **************** All the auto complete functions **************************
    
    geneData = "STAT1 RCC1".split(" ");
    $("#geneSearch").autocomplete({
			source: BASE_PATH + 'genes/get_autocomplete',
            minLength: 3, // because the names are very small eg. STAT1
            appendTo: ".searchBox",
            select: function(event, ui) {  
                        getGeneDetails(); // each time selected, get the gene details
                        updateSearchTerms(); // update the search terms under the search input                        
                    },
		});
    
    
    // **************** Cancel Form submit **************************
    
    
    // each time the show Gene clicked, get the gene details
    $('#viewGenes').click(function(){ 
        getGeneDetails();
        updateSearchTerms();
    });
    
    // each time the enter key pressed, get the gene details
    $('form').submit(function(){ 
        $("#geneSearch").autocomplete('close');
        
        // If the geneSearch is the same as the searched details, then go to next tab instead
        if ($("#geneSearch").val() ==  $('#oldSearch').html()){
            // get current tab we are on
            var selected = $('#tabs').tabs('option', 'selected')
            
            // go to next tab
            $('#tabs').tabs("select",selected + 1);            
        }
        
        getGeneDetails();
        updateSearchTerms();
        return false; 
    });
    
    
    /* *************** Initial actions ******************** */
    
    // choose Gene Selection first
    $('#tabs').tabs("select",1);
    
    // have to fix firefox issue with focus not highlighting all text
    // Set the focus up on gene search straight away
    $('#geneSearch').focus();
    
    // initiate search if gene has been passed as a get
    // eg. http://127.0.0.1:5000/searches/index?gene=stat1
    if ($("#initiateSearch").html() =="yes"){
        getGeneDetails(); // each time selected, get the gene details
        updateSearchTerms();
    }
    
 });
