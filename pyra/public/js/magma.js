
/*
 * Take an array of dictionaries (hashes) and a list of keys
 * and construct an array of arrays in which the elements of each
 * sub-array correspond to the dictionary elements retrieived using
 * the keys.   This makes it possible to arrange data from a collection
 * of dictionaries (such as returned by selection.py) into a form
 * that can be easily digested by DataTables.
 *
 * Example:
 *
 *    myHashes = [ { "x": 10, "y",: 20, "z": 30 },
 *                 { "x": 6,  "y",: -1, "z": 207 },
 *                 { "x": 1001, "y",: 0,  "z": 3 } ]
 *
 *    cols = ["x", "z"]
 *
 *    columnize(myHashes, cols) returns
 *               [ [ 10, 30], [6, 207], [1001], 3] ]
 *
 */
function columnize(dl, cl) {
    var result = [];

    for (var i=0; i < dl.length; i++) {
	var row = [];
	for (var c=0; c < cl.length; c++) {
	    row.push(dl[i][cl[c]]);
	}
	result.push(row);
    }
    return result;
}


function metadataOptions(d) {
    var result = [];
 
    for (var i=0; i < d.length; i++) {
	result.push('<option>'+d[i][0]+'</option>');
    }

    return result.join('\n');
}

// Arguments: number to round, number of decimal places
function rounder(rnum, rlength) {
    return Math.round(rnum*Math.pow(10,rlength))/Math.pow(10,rlength);
}

// Returns an array (list) of keys (properties / attributes) in an object.
function getKeys(obj) {
    var keys = [];
    for(var key in obj){
	keys.push(key);
    }
    return keys;
}

// Stub function to call when there's just nothing else there.
function unimplemented () { 
    alert("Imagine, if you will, a function that does just this");
}




    
