
/*  This is for the alternate index mako */
$(document).ready(function() {

    $('#workbench div.search').mouseover(function(){
        $(this).addClass('hoverState').children().addClass('hoverState');
    }).mouseout(function(){
        $(this).removeClass('hoverState').children().removeClass('hoverState');
    });  

    $('#workbench div.search').click(function(){
        window.location = $(this).children('a').attr('href');
    });

    $('div.wb_main_menu').live('click',function(){
        
        var old_main_menu_selected = $('div.wb_main_menu_selected');
        var old_question_groups_selected = $('div.wb_question_groups_selected');
        
        
        old_main_menu_selected.removeClass('wb_main_menu_selected').addClass('wb_main_menu');
        old_question_groups_selected.removeClass('wb_question_groups_selected').addClass('wb_question_groups');
        
        var object = $(this);
        
        object.removeClass('wb_main_menu').addClass('wb_main_menu_selected');    

        object.parent().removeClass('wb_question_groups').addClass('wb_question_groups_selected');
        
        $('div.flag_inner_div').html('Clicking on purple link takes you to the next step');
        
        var idealPosition = $('#' + object.parent().attr('id') + ' div.wb_sub_menu_inner_div');
        
        var idealOffset = idealPosition.offset();
        var idealTop = idealOffset.top;
        var chromeTop = idealTop - 72; /*  this is for google chrome and firefox */
        $('div.flag').css('top',chromeTop + 'px'); 
        
    });
    

    $('div.wb_main_menu_selected').live('click',function(){
        var old_main_menu_selected = $('div.wb_main_menu_selected');
        var old_question_groups_selected = $('div.wb_question_groups_selected');
        
        
        old_main_menu_selected.removeClass('wb_main_menu_selected').addClass('wb_main_menu');
        old_question_groups_selected.removeClass('wb_question_groups_selected').addClass('wb_question_groups');
        $('div.flag_inner_div').html('Click the bar to expand to see the options underneath.');
        
        var idealPosition = $(this);
        var idealOffset = idealPosition.offset();
        var idealTop = idealOffset.top;
        var chromeTop = idealTop - 72; /*  this is for google chrome and firefox */
        $('div.flag').css('top',chromeTop + 'px'); 
    });
    
    $('div.wb_sub_menu').click(function(){
        var href = $(this).find('a').attr('href');
        window.location = BASE_PATH + href;
    });

    $('div.flag_inner_div').html('Click the bar to expand to see the options underneath.');
    $('div.flag').show().css('top','258px');
    
    
    var show = $('#show').html();
    
    if (show != ''){
        var element = '#' + show + ' div.wb_main_menu';
        $(element).click();
    }
    
    $('div.wb_help_showing').live('click',function(){
        
        var object = $(this);
        var target_url = object.prev().prev().find('a').attr('href');
        
        target_url = BASE_PATH + target_url;
        window.location = target_url;
    });
    
    
    
});

    
