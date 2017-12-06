$(document).ready(function() {
    
    editor = ace.edit("json-editor");
    editor.getSession().setMode("ace/mode/json");
    editor.getSession().setFoldStyle("manual");
    editor.getSession().setUseWrapMode(true);
    editor.setShowPrintMargin(false);
    editor.commands.addCommand({
        name: 'saveFile',
        bindKey: {
            win: 'Ctrl-S',
            mac: 'Command-S',
            sender: 'editor|cli'
        },
        exec: function(env, args, request) {
            $(".saveMenu a").click();
        }
    });
    
    function checkJSON (json) {
        try {
            JSON.parse(json);
        } catch(error) {
            if (error instanceof SyntaxError) {
                return false;
            } else {
                throw error;
            }
        }
        return true;
    }
    
    $(".saveCloseMenu a").on("click", function (event) {
        var alphanum = /^([a-zA-Z0-9_\/\-&\?]+)$/
        
        if (!alphanum.test($("#helpname").val())) {
            alert("Name cannot be empty and can only contain '/', '_', '-', '?', '&' and alphanumeric characters.");
            return false;
        }
        
        if (!$("#jsonfile").val()) {  // If no file
            var json = editor.getValue();
            if (json) {
                if (checkJSON(json)) {
                    $("#jsontext").val(json);
                } else {
                    alert("Incorrect JSON.");
                    return false;
                }
            } else { // No file or json 
                alert("Please add a file or enter some JSON.");
                return false;
            }
        }
        // Form now either has a file or has json so submit
        $("#save-json-form").submit();
        
        return false;
    });
    
    $(".saveMenu a").on("click", function (event) {
        $("#close").val("false");
        $(".saveCloseMenu a").click();
        return false;
    });
});