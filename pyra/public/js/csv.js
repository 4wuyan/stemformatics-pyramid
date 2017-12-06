// This will parse a delimited string into an array of
// arrays. The default delimiter is the comma, but this
// can be overriden in the second argument.
// From http://www.bennadel.com/blog/1504-Ask-Ben-Parsing-CSV-Strings-With-Javascript-Exec-Regular-Expression-Command.htm
//
// Modified 2011-09-13 by NLS to include a "limit" argument.  This will limit the
// number of input tokens and issue an alert if it looks like the limit will be exceeded.
// The returned array of arrays will then have no more than this number of elements.  The idea
// is not to choke the server (or the browser) with a huge chunk of input.  If a larger
// dataset is required, this should be uploaded via "file upload" (or permenent inclusion)
// to the dataset reposium.
//
function CSVToArray( strData, cfg ){
    

    // Check to see if the delimiter is defined. If not,
    // then default to comma.
    var config = $.extend({ strDelimiter: ',', limit: 1000}, cfg || { });
    
    // Create a regular expression to parse the CSV values.
    var objPattern = new RegExp(
	(
	    // Delimiters.
	    "(\\" + config.strDelimiter + "|\\r?\\n|\\r|^)" +
		
	    // Quoted fields.
	    "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
		
	    // Standard fields.
	    "([^\"\\" + config.strDelimiter + "\\r\\n]*))"
	),
	"gi"
    );
    
    
    // Create an array to hold our data. Give the array
    // a default empty first row.
    var arrData = [[]];
    
    // Create an array to hold our individual pattern
    // matching groups.
    var arrMatches = null;
    
    // Keept track of the number of elements we harvest.
    // This will not be allowed to exceed config.limit.
    var matchCount = 0;

    // Keep looping over the regular expression matches
    // until we can no longer find a match.
    while (arrMatches = objPattern.exec( strData )){
	
	// Get the delimiter that was found.
	var strMatchedDelimiter = arrMatches[ 1 ];
	
	// Check to see if the given delimiter has a length
	// (is not the start of string) and if it matches
	// field delimiter. If id does not, then we know
	// that this delimiter is a row delimiter.
	if (  strMatchedDelimiter.length && (strMatchedDelimiter != config.strDelimiter) ) {
	    // We're at the start of a row of data.

	    // Check to see if we've exceeded config.limit.  If so, alert and return 
	    // what we have so far.
	    if (matchCount > config.limit) {
		// Note, this may leave a "ragged" last row.
		alert("Number of matched elements exceeds limit of " + config.limit + ": result truncated.");
		break;
	    }

	    // Since we have reached a new row of data,
	    // add an empty row to our data array.
	    arrData.push( [] );
	}
	
	// Now that we have our delimiter out of the way,
	// let's check to see which kind of value we
	// captured (quoted or unquoted).
	if (arrMatches[ 2 ]){
	    
	    // We found a quoted value. When we capture
	    // this value, unescape any double quotes.
	    var strMatchedValue = arrMatches[ 2 ].replace(
		new RegExp( "\"\"", "g" ),
		"\""
	    );
	    
	} else {
	    
	    // We found a non-quoted value.
	    var strMatchedValue = arrMatches[ 3 ];
	    
	}
	
	
	// Now that we have our value string, let's add
	// it to the data array.
	arrData[ arrData.length - 1 ].push( strMatchedValue );
	
	++matchCount;
    }
    
    // Return the parsed data.
    return( arrData );
}

