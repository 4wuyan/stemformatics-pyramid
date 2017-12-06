
$(document).ready(function() {
    
    $('div.contact_menu').click(function(){

        $('div.contact_menu.selected').removeClass('selected');
        this_object = $(this);
        this_object.addClass('selected');
        var hash = this_object.parent('a')[0]['hash'];
        $('div.box.display').removeClass('display').addClass('hidden');

        $(hash).parents('div.box').removeClass('hidden').addClass('display');
        return false;
    });   
});
