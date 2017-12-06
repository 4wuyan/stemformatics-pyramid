
var helpsystem = (function($, guiders, marked, CURRENT_URL) {
    
    $.cookie.json = true;
    
    var PAGE_GUIDE = "page_guide",
        TUTORIAL_HASH_TAG = "tutorial=",
        JSON_PATH = "/help/json",
        guideDefaults,
        activeGuide,
        tutorial,
        pageHelp;

    guiders._htmlSkeleton = [
        "<div class='guider'>",
        "    <div class='guiders_content'>",
        "        <div class='guiders_close'></div>",
        "        <h1 class='guiders_title'></h1>",
        "        <div class='guiders_description'></div>",
        "        <div class='guiders_buttons_container'></div>",
        "    </div>",
        "    <div class='guiders_arrow'></div>",
        "</div>"
    ].join("");
    
    guideDefaults = {
        title: "",
        description: "",
        width: 500,
        position: 11,
        autoFocus: true,
        xButton: true,
        overlay: true,
        highlight: true,
        showNext: true,
        showPrev: true,
        isHashable: false,
        intro: false,
        break: false,
        final: false,
        css: {},
        scripts: {}
    }
    
    activeGuide = null;
    
    function setHash(guide) { window.location.hash = "tutorial=" + guide.group; }
    function removeHash() { window.location.hash = ""; }
    function getTutFromHash() {
        var hashIndex = window.location.hash.indexOf(TUTORIAL_HASH_TAG);
        return (hashIndex !== -1) ? window.location.hash.substr(hashIndex + TUTORIAL_HASH_TAG.length) : null ;
    }
    
    function getTutCookie() {
        var cookie = $.cookie('activeTutorial');
        if (cookie && cookie.group in tutorial.guides) {
            if (cookie.break) {
                return guideByID(cookie.id).nextGuide();
            } else {
                return firstGuideFor(cookie.group);
            }
        } else {
            return null;
        }
    }
    function removeTutCookie() { $.removeCookie('activeTutorial', { path: '/' }); }
    function setTutCookie(guide) {
        var expDate = new Date();
        expDate.setTime(expDate.getTime() + (5 * 60 * 1000));
        $.cookie('activeTutorial', {group: guide.group, id: guide.id, break: guide.break}, { path: '/', expires: expDate });
    }
    
    function hasTutorial() { return !$.isEmptyObject(tutorial.guides); }
    function hasHelp() { return !$.isEmptyObject(pageHelp.guides); }
    
    function guideByID(id) { return guiders._guiderById(id); }
    function firstGuideFor(tutorialID) { return tutorial.guides[tutorialID][0]; }
    
    tutorial = {
        guides: {},
        current: null,
        initialized: false,
        repositionTimer: null,
        
        initialize: function(guide) {
            if (guide) { // initialize with given guide
                this.current = guide;
            } else if (tutorialID = getTutFromHash()) { // no guide given so try to initialize from cookie then hash
                this.current = firstGuideFor(tutorialID);
            } else if (guide = getTutCookie()) {
                this.current = guide;
            } else {
                removeHash();
                return false;
            }
            setTutCookie(this.current);
            setHash(this.current);
            this.initialized = true;
            return true;
        },
        start: function(thing) {
            var guide = ($.type(thing) == "string") ? firstGuideFor(thing) : thing;
            if (!guide) throw "Tutorial doesn't exist on this page.";
            if (!this.initialized) this.initialize(guide);
            guiders.show(guide.id);
            clearInterval(this.repositionTimer);
            this.repositionTimer = setInterval(function() {
                if (!$(guiders._guiderById(guiders._currentGuiderID).elem).is(":in-viewport")) {
                    guiders.reposition();
                }
            }, 80);
            $.event.trigger({type: "tutorialStarted.HelpSystem"});
        },
        resume: function() {
            this.start(this.current);
            $.event.trigger({type: "tutorialResumed.HelpSystem"});
        },
        stop: function() {
            guiders.hideAll();
            removeHash();
            removeTutCookie();
            this.current = null;
            clearInterval(this.repositionTimer);
            $.event.trigger({type: "tutorialStopped.HelpSystem"});
        },
        next: function() {
            if (activeGuide && $.inArray(activeGuide, tutorial.guides[activeGuide.group]) === tutorial.guides[activeGuide.group].length-1) {
                window.location.href = "http://" + CURRENT_URL.authority + activeGuide.nextPage + "#tutorial=" + activeGuide.group;
            } else {
                guiders.next();
            }
        },
        prev: function() {
            guiders.prev();
        },
        onShow: function(guide) {
            this.current = guide;
            setTutCookie(guide);
            if (guide.highlight) guide.addElemBackground();
            if (guide.customOnShow) guide.customOnShow();
            if (guide.final) this.deactivate();
        },
        onHide: function(guide) {
            if (guide.highlight) guide.removeElemBackground();
            if (guide.customOnHide) guide.customOnHide();
        },
        onClose: function(guide) {
            this.stop();
        },
        isActive: function() {
            return (this.current != null);
        },
        deactivate: function() {
            removeTutCookie();
        }
    };
    
    pageHelp = {
        guides: [],
        isOn: false,
        turnOn: function () {
            tutorial.stop();
            this.isOn = true;
            $.each(this.guides, function(index, guide) {
                if (guide.attachedElem) {
                    guide.highlight = false;
                    guide.overlay = false;
                    guide.attachedElem.on("mouseenter.PageGuide", function(event) { guiders.show(guide.id); });
                    guide.attachedElem.on("mouseleave.PageGuide", function(event) { guiders.hideAll(); });
                    guide.attachedElem.addClass("active");
                    guide.elem.find("div.guiders_buttons_container").hide();
                    guide.elem.find("div.guiders_close").hide();
                }
            });
            $(".guider.pageGuide .guiders_buttons_container").hide();
        },
        turnOff: function () {
            guiders.hideAll();
            this.isOn = false;
            $.each(this.guides, function(index, guide) {
                if (guide.attachedElem) {
                    guide.highlight = "#" + guide.attachedElem.attr('id');
                    guide.overlay = true;
                    guide.attachedElem.off(".PageGuide");
                    guide.attachedElem.removeClass("active");
                    guide.elem.find("div.guiders_buttons_container").show();
                    guide.elem.find("div.guiders_close").show();
                }
            });
            $(".guider.pageGuide .guiders_buttons_container").show();
        }
    }
    
    function createGuide(guideData, step, group, noOfGuides) {
        guideData = $.extend({}, guideDefaults, guideData)
        guideData.id = group+"_"+(step);
        guideData.step = step;
        guideData.group = group;
        guideData.isPageGuide = (group == PAGE_GUIDE);
        guideData.highlight = (guideData.highlight === true) ? guideData.attachTo : null;
        guideData.overlay = (guideData.highlight != null);
        guideData.buttons = [];
        
        // Parse markdown
        if (guideData.description instanceof Array) {
            guideData.description = marked(guideData.description.join('\n'));
        } else {
            guideData.description = marked(guideData.description);
        }
        
        // Setup Flow
        if (step !== 0) {
            guideData.prev = group+"_"+(step-1);
            if (guideData.showPrev) {
                guideData.buttons.push({
                    name: "Previous",
                    onclick: tutorial.prev
                });
            }
        }
        if (step !== noOfGuides-1) {
            guideData.next = group+"_"+(step+1);
            if (guideData.showNext && !guideData.break) {
                guideData.buttons.push({
                    name: "Next",
                    onclick: tutorial.next
                });
            }
        } else if (guideData.nextPage && guideData.showNext) {
            guideData.buttons.push({
                name: "Next Page",
                onclick: tutorial.next
            });
        }
        guideData.nextGuide = function() { return guiders._guiders[guideData.next]; }
        guideData.prevGuide = function() { return guiders._guiders[guideData.prev]; }
        
        // Setup Handlers
        guideData.onShow = function(guide) {
            activeGuide = guide;
            if (tutorial.isActive()) tutorial.onShow(guide);
        };
        guideData.onHide = function(guide) {
            activeGuide = null;
            if (tutorial.isActive()) tutorial.onHide(guide);
        };
        guideData.onClose = function(guide) {
            if (tutorial.isActive()) tutorial.onClose(guide);
        };
        
        // Now create the actual guide
        var guide = guiders.createGuider(guideData)._guiderById(guideData.id);
        
        // Setup custom script functions
        $.each(guideData.scripts, function(event, script) {
            switch(event) {
                case 'onShow':
                    guide.customOnShow = new Function(script); break;
                case 'onHide':
                    guide.customOnHide = new Function(script); break;
            }
        });
        if (guideData.shouldSkip != null) {
            guide.shouldSkip = new Function(guideData.shouldSkip);
        }
        
        // Setup classes and attached element
        guide.elem.addClass(group);
        if (guide.attachTo) {
            guide.attachedElem = $(guideData.attachTo);
            guide.attachedElem.addClass(group+"-attached");
        } else {
            guide.attachedElem = null;
        }
        
        // Add class if guide is intro
        if (guideData.intro) guide.elem.addClass('intro');
        
        // Remove title margin if no title set
        var $guideTitle = guide.elem.find('.guiders_title');
        if ($guideTitle.html() == "") {
            $guideTitle.css('margin-bottom', '0px');
        }
        
        // Setup transparent background fix functions
        guide.addElemBackground = function () {
            if (guide.attachedElem) {
                guide.bgcolor = guide.attachedElem.css('background-color');
                if (guide.bgcolor == undefined || guide.bgcolor == 'transparent' || guide.bgcolor == 'rgba(0, 0, 0, 0)') {
                    guide.attachedElem.css('background-color', 'white');
                }
            }
        }
        guide.removeElemBackground = function () {
            if (guide.attachedElem) {
                guide.attachedElem.css('background-color', guide.bgcolor);
            }
        }
        
        // Add classed to buttons
        guide.elem.find(".guiders_button:contains('Previous')").addClass("previous");
        guide.elem.find(".guiders_button:contains('Next')").addClass("next");
        
        // Appy custom css
        $.each(guideData.css, function(selector, css) {
            if (selector == "root") {
                guide.elem.css(css);
            } else {
                guide.elem.find(selector).css(css);
            }
        });
        
        return guide;
    }
    
    function jsonFileURL() { // Builds the url to access the page's help data
        var query = "?";
        if (CURRENT_URL.path == "/") {
            query += "path=contents_index";
        } else {
            var path = CURRENT_URL.path.split("/").slice(1, 3).join("/");
            query += CURRENT_URL.query + "&path=" + path;
        }
        return JSON_PATH + query;
    }
    
    function getHelpJSON (jsonFileURL) {
        var jsonData = null;
//        $.ajax({
//            url: jsonFileURL,
//            dataType: 'json',
//            async: false,
//            success: function(guideData) {
//                jsonData = guideData;
//            },
//            error: function(jqXHR, textStatus, errorThrown) {
//                if (jqXHR.status === 0){
//                } else if (jqXHR.status === 404){
//                } else if (jqXHR.status === 500){
//                } else if (textStatus === 'parsererror'){
//                    throw "JSON Parse Error";
//                } else if (textStatus === 'timeout'){
//                } else {
//                }
//            }
//        });
        jsonData = jQuery.parseJSON($('#tutorials_for_page').html());
        return jsonData;
    }
    
    function buildHelp(jsonData) {
        var tutorials = jsonData["tutorials"],
            pageGuides = jsonData["page_guide"],
            noOfGuides;
        
        if (tutorials !== null) {
            $.each(tutorials, function(group, tutorialData) {
                noOfGuides = tutorialData.length;
                tutorial.guides[group] = [];
                $.each(tutorialData, function(index, guideData) {
                    guide = createGuide(guideData, index, group, noOfGuides);
                    tutorial.guides[group].push(guide);
                });
            });
        }
        if (pageGuides !== null) {
            noOfGuides = pageGuides.length;
            tutorial.guides[PAGE_GUIDE] = [];
            $.each(pageGuides, function(index, guideData) {
                guide = createGuide(guideData, index, PAGE_GUIDE, noOfGuides);
                pageHelp.guides.push(guide);
                tutorial.guides[PAGE_GUIDE].push(guide);
            });
        }
    }
    
    // $(window).unload(function() {
    //     if (tutorial.isActive()) {
    //         //tutorial.current.id = (activeGuide.continues) ? activeGuide.next : activeGuide.group+"_0";
    //         setTutCookie(tutorial.current);
    //     }
    // });

    function run() {
        var jsonData = getHelpJSON(jsonFileURL());
        
        if (!$.isEmptyObject(jsonData)) {
            buildHelp(jsonData);
            if (tutorial.initialize()) {
                tutorial.resume();
            }
        }
    }
    
    return {
        tutorial: tutorial,
        pageHelp: pageHelp,
        activeGuide: activeGuide,
        
        hasTutorial: hasTutorial,
        hasHelp: hasHelp,
        
        run: run
    }
    
}(jQuery, guiders, marked, CURRENT_URL));


$(function () { helpsystem.run(); });
