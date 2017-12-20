$(document).ready(function() {
    // do stuff when DOM is ready
    
    // **************** All the tab functions **************************
    $("#accordion").accordion({
        change: function(event, ui) { $("#geneSearch").focus();  }
        });
    
    // Set the focus up on gene search straight away
    $("#geneSearch").focus();   
    
    
    // **************** All the auto complete functions **************************
    
    var geneData = "STAT1 RCC1 ACF64 ACF1 REELIN".split(" ");
    $("#geneSearch").autocomplete({
			source: geneData,
            minLength: 2, // because the names are very small eg. STAT1
            select: function(event, ui) {  
                        getGeneDetails(); // each time selected, get the gene details
                    }
            
		});
    
    var cellMouseData = "NIH/3T3 COS CHO C6 MCF-7 PC12".split(" ");
    var cellHumanData = "FS K562 HEK-293 H1299 Saos-2 S180 BCP-1".split(" ");
    $("#cellSearch").autocomplete({
			source: cellHumanData,
            minLength: 2
            
		});    
        
    
    var sampleData = "hONS PD MSC MDM-LPS Sz".split(" ");
    $("#sampleSearch").autocomplete({
			source: sampleData,
            minLength: 2
            
		});      
    
    
    function getGeneDetails (){
        // What we want to do is get back the gene description after the enter button has been pressed
        $('#displayGeneDetails').show();
        $.ajax({
            url: '/genes/get_details',
            type: 'post',
            data: {geneSearch: $('#geneSearch').val()},
            success: function(data) {
                var returnDetails = JSON.parse(data);
                $('#displayGeneDetails').html(
                    returnDetails["description"] 
                    + "<div class='showAliases'> Aliases: " + returnDetails["aliases"]+ "</div>"
                    + "<div class='showAltSplicing'> Evidence of Alt Splicing: " + returnDetails["alt_splicing"]+ "</div>"
                    + "<div class='showCage'> Evidence of Cage data: " + returnDetails["cage_data"]+ "</div>"
                    + "<div class='showDiseases'> Diseases: " + returnDetails["diseases"] + "</div>").show() ;
                
                // resize for the changes just made
                $('#accordion').accordion('option','autoHeight', true);
            }
        });
    }    
    
});    
