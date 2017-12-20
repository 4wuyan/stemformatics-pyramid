


$(document).ready(function() {
    
    helpSystem.run();
    
    $('#help-menu').bind("mouseover.helpMenu", helpEnterHandler);
    $('#help-menu').bind("mouseout.helpMenu", helpLeaveHandler);
    
});

function helpEnterHandler() {
    $('#help-menu').width(130).height(190);
    $('#help-menu').css("background-color", "rgba(0, 0, 0, 0.8)");
    $("#help-menu:hover ul").show();
}

function helpLeaveHandler() {
    $("#help-menu:hover ul").hide();
    $('#help-menu').width(60).height(60);
    $('#help-menu').css("background-color", "rgba(104, 34, 139, 0.8)");
}

function onShowHandler(guideID) {
    place.set(guideID);
    if (place.group() != "guide") {
        tutorial.set(place.group());
    }
    turnHelpOn();
    place.currentGuide = guiders._guiderById(guideID);
    //setupNextGuide(place.currentGuide.nextGuide());
}

function setupNextGuide(guide) {
    if (guide && guide.showOn) {
        var guideEvent = guide.showOn.event+"."+guide.id+"Event";
        $(guide.showOn.element).bind(guideEvent, function() {
            $(guide.showOn.element).unbind(guideEvent);
            guiders.hideAll();
            guiders.show(guide.id);
        });
    };
}

function onHideHandler() {
    place.currentGuide = null;
}

function onCloseHandler() {
    stopGuides();
}

function onHoverInHandler(guideID) {
    if (pageHelp.isActive()) {
        guiders.show(guideID);
    }
}

function onHoverOutHandler() {
    guiders.hideAll();
}

function startGuides() {
    guiders.hideAll();
    turnHelpOn();
    if (tutorial.isActive()) {
        guiders.show(place.get());
    }
}

function stopGuides() {
    guiders.hideAll();
    tutorial.stop();
    turnHelpOff();
}

function restartGuides() {
    place.reset();
    if (isHelpOn()) {
        startGuides();
    }
}

function isHelpControlsActive() {
    return $('#help-menu li.action').first().css("display") == "none";
}

function isHelpOn() {
    return $('#help-stop').css("display") == "none";
}

function turnHelpOn() {
    $('#help-menu').unbind("mouseout.helpMenu", helpLeaveHandler);
    help.setActive();
    $('#help-start').hide();
    $('#help-stop').show();
}

function turnHelpOff() {
    $('#help-menu').bind("mouseout.helpMenu", helpLeaveHandler);
    help.setInactive();
    $('#help-stop').hide();
    $('#help-start').show();
}

function activateHelpControls() {
    $('#help-menu li.no-help').hide();
    $('#help-menu li.action').show();
    $('#help-start').bind('click', startGuides);
    $('#help-stop').bind('click', stopGuides);
    $('#help-restart').bind('click', restartGuides);
}

function disableHelpControls() {
    $('#help-menu li.action').hide();
    $('#help-menu li.no-help').show();
    $('#help-start').unbind('click', startGuides);
    $('#help-stop').unbind('click', stopGuides);
    $('#help-restart').unbind('click', restartGuides);
}

function nextPage(url) {
    window.location.href = "http://" + CURRENT_URL.authority + url;
}