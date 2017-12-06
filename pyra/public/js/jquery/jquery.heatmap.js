/*
 * HEATMAP: HEatMaP pluging for jquery
 *
 * This module is written to work in tendem with the hamlet.py
 * controller, but it will work just as well with service that 
 * returns an object that can be used as in image.  (jpg, pnm, gif, etc.)
 *
 * Requires jquery-ui and imgAreaSelect (http://odyniec.net/projects/imgareaselect/)
 * modules.
 * 
 * Thanks to Mike Alsup for this nice article wherein I found the pattern
 * on which I modeled this plugin.
 * http://www.learningjquery.com/2007/10/a-plugin-development-pattern
 *
 * I also made heavy use of stackoverflow:Borger's pattern after finding the earlier
 * one was ill-suited to adding instance methods.
 *
 * Of course, the ultimate authority is the jquery plugin authoring guide.
 *
 * - - - - - - -
 *
 * Nick Seidenman <seidenman@wehi.edu.au>
 * Molecular Medicine Division
 * Walter and Eliza Hall Institute
 *
 * Copyright (c) 2011 Walter and Eliza Hall Institute of Medical Research
 *
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the <organization> nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. * LICENSE: BSD Licence
 * 
 */

(function ($) {
    
    var _methods = { 
	/* init (cfg)
	 *     initialize a heatmap instance.  If cfg is defined and is an object, modify this instance's
	 *     config with what's found in cfg.
	 */
	init: function (cfg) {

	    // Used to create an instance, for API-style calls.
	    if (this == window) { alert('here'); return new $.fn.heatmap(cfg || {}); }
	    
	    // Don't re-run this if already present.
	    if (this.item && this.item.data('heatmap')) { 
		//;;; _debug('returning myself ('+this.item.id+')'); 
		return this; 
	    }
	    
	    // Store the basics.
	    var $this = this;
	    $this.item = $(this);

	    _methods.config.apply(this, [ $.extend(true, { "width": parseInt($(this).width()), 
									  "height": parseInt($(this).height()) }, cfg) ]);
						
	    // Register the controlset with the element. (back-reference)
	    $this.item.data('heatmap', this);
	    
	    // Context -- includes profile & sample metedata, boundaries, coffee orders ...
	    $this.item.data('ctx', { });
	    
	    // a few other context variables.
	    var $divId = $(this).attr("id") + "-div";
	    var $htmltmp = $.fn.heatmap.defaults.html_template.val.replace(/divId/g, $divId);
	    
	    // If the HTML that will hold the image hasn'' been generaed yet,
	    // inject it now, replacing 'divId' with the actual value everywhere therein.
	    if (! $("#"+$divId+" div#hmDiv").id) {
		$(this).append($htmltmp);
		;;; _debug('bg-img: ' + $this.config.spinner_url.val);
		
        
	    } 
	    else {  // Already exists.  Not sure what to do, so for now, just log it.  NLS
		;;; alert("OK -- somehow got here.");
	    }
	    
        
        
	    // Load the initial image.
	    _load_heatmap.apply(this);
	    
	    // Set up event handlers
	    $("#hmDiv", this).livequery("mousemove", _mousemoveHandler);
	    $("#hmDiv", this).livequery("click", _clickHandler);

	    return this;
	},

	/* config({config_object})
	 *     set a heatmap objects configuration.  Configration items may be either those
	 *     found in $.fn.heatmap.defaults, below, or new items.   The first time this is
	 *     invoked, the instances config attribute is initialized with the defaults object,
	 *     and then the config_object parameter, if supplied, is applied to this copy.
	 *     subsequent calls will use the instances copy of the config_object.
	 *
	 *     If the item specified does not already exist in the instance's config,
	 *     a new item will be created and it's "val" attribute set to the value of the
	 *     new item, and its "reqparm" attribute will be set to false.  
	 *
	 *     If the cfg argument is the string "get", the instance's configuration is
	 *     is returned as a simple object  (i.e. { name: val }) with only the val attribs
	 *     returned and only for those items that are not marked as hidden.
	 *
	 *     (NLS:  Not sure why/if  I want this behaviour, but for now it seems safest since 
	 *     it prevents or, at least, limits the user from being able to introduce arbitrary 
	 *     crap into the request that is sent to the server.)
	 */
	config: function (cfg) {
	
	    ;;; _debug("this.config: " + this.config);
	    var new_cfg = $.extend(true, { }, 
				   (typeof this.config == 'undefined' || ! this.config) ? $.fn.heatmap.defaults : this.config );
	    
	    // We only want a copy of the existing config.
	    if (cfg == 'get') {
		var $stg = new Object();
		for (var a in new_cfg) {
		    if (! new_cfg[a].hidden) {   // Somethings are better left unsaid.
			$stg[a] = new_cfg[a].val;
		    }
		}

		return $stg; 
	    }

	    // We're actually gonna modify stuff.
	    for (var a in cfg) {
		if (typeof new_cfg[a] == 'undefined' || ! new_cfg[a]) { 
		    new_cfg[a] = { reqparm: false, val: '' }; 
		}
		new_cfg[a].val = cfg[a];
	    }

	    this.config = new_cfg;

	    return this;
	},
	
	defaults: function (cfg) {
	    delete this.config;
	    ;;; _debug('this.config: ' + this.config);
	    _methods.config.apply(this, [ $.extend(true, { "width": parseInt($(this).width()), 
									  "height": parseInt($(this).height()) }, cfg) ]);
	},

	/* selection (fn):  if fn is a function type, it will
	 *     be used as a callback when a selection event (jrcrop select or change)
	 *     occurs.  If it is null or undefined, selection is disabled and the
	 *     callback function is cleared from the configuration.
	 */
	selection: function (fn) {
	   ;;; _debug('** selection this: ' + this);
	    if (typeof fn == 'function') {
		;;; _debug('area: ' + $("#hmImg", this).attr("id"));
		this.config.onSelect.imgAreaObj = $("#hmImg", this).imgAreaSelect({instance: true});
		this.config.onSelect.imgAreaObj.setOptions($.extend(this.config.onSelect.ias_opts, 
								    {parent: this, enable: true }));
		this.config.onSelect.imgAreaObj.update();
		this.config.onSelect.val = fn;
		;;; _debug('selection enabled : callback fn set: ' + this.config.onSelect.imgAreaObj);
	    }
	    else if (typeof fn == 'undefined' || ! fn) {
		this.config.onSelect.val = null;
		if (this.config.onSelect['imgAreaObj']) {
		    $("#hmImg", this).imgAreaSelect({remove: true});
		    this.config.onSelect.imgAreaObj = null;
		}
		;;; _debug('selection disabled: callback fn cleared');
	    }
	    else {
		$.error( "function specified for heatmap selection isn't really a function!");
	    }

	   return this;
	},

	/* update(cfg)
	 *     Update a heatmap, posting the (possibly modified) params to the server to get
	 *     a new image and metadata set.  If cfg is defined and is an object it will
	 *     be applied to the instance's (visible) configuration before calling the server
	 */
	update: function(cfg) {
	
	    if (typeof cfg == 'object') {
		_methods.config.apply(this, [cfg]);
	    }
	  
	    //;;; _debug('updating ' + $(this).attr("id"));
	    //;;; _debug('this.config.profiles: ' + this.config.profiles.val);
	    //;;; _debug('this.config.samples: ' + this.config.samples.val);

	    _load_heatmap.apply(this);

	    return this;
	},

	/* echo(str)
	 *     This was the first method I wrote when developing this, my first plugin.  I used
	 *     it to figure out the dark art of passing params into closures (aka "the Abbyss")
	 *     which are known to pull arguments toward them so fast, light beer cannot escape.
	 *     (Stout or amber, however, passes happily and freely -- hint hint.)
	 */
	echo: function(str) { _debug('myInstMethod('+$(this).attr("id")+'): ' + str);  return this; },

	/* Clear error state.
	 *
	 */
	clear: function() {
	    ;;; _debug('error: ' + $(this).data('ctx').dataset);
	    $("#hmDiv", this).empty();
	    _loadedHandler.call(this, [loadStates.READY]);
	},
    };


    $.fn.heatmap = function(arg, parm) {
	
	// the triple-semicolon will cause this line to be omitted during 
	// (YUI) minimization
	// ;;; _debug(this);  
	var $args = arguments;
	
	// Special case.  (Until I figure out a way to do it "right".)
	if (arg == 'config' && parm == 'get') {
	    return _methods[arg].apply(this, Array.prototype.slice.call($args, 1));
	}

	// Iterate through all of "this"
	return this.each(function() {
	    if ( _methods[arg] ) {
		return _methods[arg].apply(this, Array.prototype.slice.call($args, 1));
	    }
	    else if (typeof arg == 'object' || ! arg ) { 
		_methods.init.apply(this, $args);
	    }
	    else {
		$.error( 'Method ' + arg + 'does not exist on jQuery.heatmap');
	    }
	});

    };
    

    // _load_heatmap:  Core function for (re)loading heatmap images and metadata.
    function _load_heatmap($$cfg) {
	// Build the http request settings object that we'll use in _load_heatmap().
	// This is done by harvesting the properties of this.config that have
	// the 'reqpqrm' attribute set to true.
	var $settings = { };
	for (var a in this.config) {
	    if (this.config[a].reqparm == true) { 
		$settings[a] = this.config[a].val;
	    }
	}

	var $$url = this.config.url.val;
	var $$spinner = this.config.spinner_url.val;

	// Apply custom configs.  (Untested as of 2011-07-28 NLS)
	if (typeof $$cfg == 'object') {
	    for (var a in $$cfg) {
		$settings[a] = $$cfg[a];
	    }
	    
	    if ($$cfg.url) $$url = $$cfg.url;
	    if ($$cfg.spinner_url) $$spinner = $$cfg.url;
	}

	// Distinguish "this" this from other (later) this's.
	var $this = this;

	// Store image context here.
	$(this).data('ctx', { heatmap_pos: { top: 0, left: 0 } });

	// Turn on the spinner background, if any.
	;;; _debug('url: ' + $$url + '    spinner: ' + $$spinner);
	//$("#hmDiv", $($this)).empty().append("<span id='statMsg' style='vertical-align: middle;'>Calculating ...</span>");
	$("#statMsg", $($this)).addClass("hm-calc-msg");
	$("#hmDiv", $($this)).css({ visibility: "visible","background-repeat": "no-repeat","background-position": "center", "background-image": "url('"+$$spinner+"')" });
	$("#hmImg", $($this)).css( {visibility: "hidden"} );

	// POST the request to the server.   What comes back will be a JSON string
	// that jquery will be good enough to parse into a javascript object for us.
	// We reference this in the first (hmo -- HeatMap Object) argument of the
	// callback function.
	this.config.onReady.state = loadStates.NOT_READY;
	$.post($$url, $settings, function(hmo, st, jx) {

	    ;;; _debug('status: '+st+'   image: ' + hmo.image + '   labels: ' + hmo.labels);

	    // Replace whatever img is in the hm subdiv with the one we just got
	    // from the server (heatmap.py).  If using heatmap.py, this will contain
	    // a src= attrib set to "/hamlet/retrieveImage/IMG_ID" where IMG_ID uniquely
	    // identifies the image and corresponding metadata for this heatmap.
	    $("#hmDiv", $($this)).html(hmo.image); // Rowland - removed append and replaced it due to ???  perhaps updated headers caused it to have an issue?

	    // Set a one-shot "imaged load complete" handler to do clean-up work.
	    $("#hmImg", $($this)).one("load",  { }, function () {
		$($this).data('ctx', $.extend($($this).data('ctx'), { "heatmap_pos": $(this).offset() }));
		_loadedHandler.apply($this, [loadStates.IMAGE_LOADED]);
		return true;
	    });
	    
	    // Update our status message to indicate we are now loading the metadata for this image.
	    //$("#statMsg", $($this)).removeClass('hm-calc-msg').addClass('hm-load-msg').text("Loading image and metadata...");
	    
	    // Now, go get the corresponding metadata.
	    $.post(hmo.labels, {}, 
		   function(d, s) {
		       if (s != 'success') {
			   ;;; _debug('oops!');
			   return false;
		       }
		       
		       if (d.orient == 'ver') {
			   d.pix_per_row = (d.heatmap_bbox[3] - d.heatmap_bbox[1]) / d.profile_metadata.length;
			   d.pix_per_col = (d.heatmap_bbox[2] - d.heatmap_bbox[0]) / d.sample_metadata.length;
		       }
		       else {
			   d.pix_per_row = (d.heatmap_bbox[3] - d.heatmap_bbox[1]) / d.sample_metadata.length;
			   d.pix_per_col = (d.heatmap_bbox[2] - d.heatmap_bbox[0]) / d.profile_metadata.length;
		       }
		       
		       d.src = $("#hmImg", $($this)).attr("src");
		       d.dataset = $settings.dataset;
		       ;;; _debug('d.axislabels: ' + d.axislabels);
		       ;;; _debug('this.config.axislabels: ' + $this.config.axislabels.val);

		       $($this).data('ctx', $.extend($($this).data("ctx"), d));
		       $this.config.axislabels.val = d.axislabels;

		       // Log that the metadata load has completed, taking action
		       // if any has been specified.
		       _loadedHandler.apply($this, [loadStates.METADATA_LOADED]);

		       // Clear the status message
		       $("#statMsg", $($this)).remove();

		       // Because the status message takes up space, we need to get rid of it before
		       // doing the following calculations:
		       var loose_ends  = { 
			   heatmap_pos: $("#hmImg").offset(),
		       };

		       $($this).data('ctx', $.extend($($this).data('ctx'), loose_ends));

		       return true;
		   });
	});

	return this;
    };

    /* ----------------------
     *   Utility Functions
     * ----------------------
     */

    // Return the mouse position corrected for DOM element offsets, lunar phase,
    // Planck Effect, etc.
    function _mouseAbs(e, $$ctx) {
	if (! $$ctx.heatmap_pos) return {"x": -1, "y": -1};

	//;;; _debug('e.pageX: ' + e.pageX + '   e.pageY: ' + e.pageY);
    
	return {"x": (e.pageX - $$ctx.heatmap_pos.left - $$ctx.heatmap_bbox[0]), 
		"y": (e.pageY - $$ctx.heatmap_pos.top - $$ctx.heatmap_bbox[1]) };
    }

    // Returns a list of an objects properties.
    function _getKeys(obj) {
	var keys = [];
	for(var key in obj){
	    keys.push(key);
	}
	return keys;
    };
    
    // Write debug messages to the console iff one exists.
    function _debug(str) {
	if (window.console && window.console.log) window.console.log(str);
    };


    // Map mouse position coordinates to indexes within the sample and profile
    // metadata arrays.
    function _getIndexes(mouse_pos, $$ctx) {
	
	if ($$ctx.orient == "ver") {
	    var smpl = $$ctx.sample_metadata.length - parseInt(mouse_pos.x / $$ctx.pix_per_col) - 1;
	    var prof = parseInt(mouse_pos.y / $$ctx.pix_per_row);
	}
	else {
	    var prof = parseInt(mouse_pos.x / $$ctx.pix_per_col);
	    var smpl = parseInt(mouse_pos.y / $$ctx.pix_per_row);
	}

	if (prof < 0 || prof >= $$ctx.profile_metadata.length) prof = null;
	if (smpl < 0 || smpl >= $$ctx.sample_metadata.length) smpl = null;
	//;;; _debug('m_x: ' + mouse_pos.x + '   m_y: ' + mouse_pos.y);
	return { 'profile' : prof, 'sample' : smpl };
    };


    /* -------------------------------
     *   E V E N T   H A N D L E R S
     * -------------------------------
     *
     * These will be called when the (obviously associated) event is triggered.
     * they serve as wrappers that will invoke user-specified event handlers
     * for the same, or similar (kinds of) events.  Most if not all of these are
     * installed using livequery and so follow that calling convention.
     
      -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

     * _mousemoveHandler(ev)
     *     triggered on mouse move.  If a user-specified callback exists,
     *     this will compute the indexes for the profile and sample metadata
     *     arrays and return the corresponding elements of those arrays corresponding
     *     to the current mouse position.  
     *
     *     The user call-back should expect up to four arguments:
     *         profile_metadata at mouse position
     *         sample_metadata at mouse position
     *         object with attributes "profile" and "sample", both integer indexes
     *         context object, contatining everything worth knowing about the heatmap
     *     
     *     In most cases it is sufficient for the callback to use just the first two
     *     or three arguments.  The context object should not be altered as this could
     *     negatively affect the heatmap instance.
     *
     */
    function _mousemoveHandler(ev) {

	var $this = $(ev.target).closest(".hm-container").parent();
	var $cfg = $this.data('heatmap').config;
	
	// Are both the image and its metadata loaded?  If not, just return.
	if ($cfg.onReady.state != loadStates.READY) return true;

	if (typeof $cfg.onMousemove.val == 'function') {
	    
	    var $$ctx = $this.data('ctx');
	    var mouse_pos = _mouseAbs(ev, $$ctx);
	    var ndxs = _getIndexes(mouse_pos, $$ctx);

	    //;;; _debug($this.attr("id") + '   x: ' + mouse_pos.x + '     y: ' + mouse_pos.y);
	    //;;; _debug ('    prof: ' + ndxs.profile + '     samp: ' + ndxs.sample);
	
	    return $cfg.onMousemove.val ( { "mouse": mouse_pos,
					    "profile": (ndxs.profile == null ? 'undefined' : $$ctx.profile_metadata[ndxs.profile]), 
					    "sample": (ndxs.sample == null ? 'undefined' : $$ctx.sample_metadata[ndxs.sample]), 
					    "indexes": ndxs, 
					    "context": $$ctx, 
					    "event": ev } );
	}

	return true;
    };
    
    /* _clickHandler(ev)
     *     triggered on mouse click.  If a user-specified callback exists,
     *     this will compute the indexes for the profile and sample metadata
     *     arrays and return the corresponding elements of those arrays
     *     corresponding to the position of the mouse where clicked.
     *
     *     The user call-back should expect up to four arguments:
     *         profile_metadata at mouse position
     *         sample_metadata at mouse position
     *         object with attributes "profile" and "sample", both integer indexes
     *         context object, contatining everything worth knowing about the heatmap
     *     
     *     In most cases it is sufficient for the callback to use just the first two
     *     or three arguments.  The context object should not be altered as this could
     *     negatively affect the heatmap instance.
     *
     */
    function _clickHandler(ev) {
	var $this = $(ev.target).closest(".hm-container").parent();
	var $cfg = $this.data('heatmap').config;

	if ($cfg.onReady.state != loadStates.READY) return true;

	// If there's an event handler registered for clicks, invoke it,
	// passing an object containing all the relevant info for the event.
	if (typeof $cfg.onClick.val == 'function') {
	    var $$ctx = $this.data('ctx');
	    var mouse_pos = _mouseAbs(ev, $$ctx);
	    var ndxs = _getIndexes(mouse_pos, $$ctx);

	    return $cfg.onClick.val ( { "profile": (ndxs.profile == null ? 'undefined' : $$ctx.profile_metadata[ndxs.profile]), 
					"sample": (ndxs.sample == null ? 'undefined' : $$ctx.sample_metadata[ndxs.sample]), 
					"indexes": ndxs, 
					"context": $$ctx, 
					"event": ev } );
	}
	return true;
    };
    

    /* _selectionHandler.  Internal method used as a callback for
     *     imgAreaSelect when selection is enabled.  This, in turn, will call
     *     the specified userland callback, indicated by this.config.onSelection.
     *
     *     The user call-back should expect up to four arguments:
     *         profile_metadata for this selection (an array of zero or more objects)
     *         sample_metadata for this selection (an array of zero or more objects)
     *         object with attributes "profiles" and "samples", both integer indexes
     *         context object, contatining everything worth knowing about the heatmap
     *     
     *     In most cases it is sufficient for the callback to use just the first two
     *     or three arguments.  The context object should not be altered as this could
     *     negatively affect the heatmap instance.
     *
     */
    function _selectionHandler(t, c) {
    
	var $this = $(t).closest('.hm-container').parent();
	var $cfg = $this.data('heatmap').config;

	if ($cfg.onReady.state != loadStates.READY) return true;

	var $ctx = $($this).data('ctx');

	var start_x = Math.min(c.x1, c.x2) - $ctx.heatmap_bbox[0];
	var end_x = Math.max(c.x1, c.x2) - $ctx.heatmap_bbox[0];
	
	var start_y = Math.min(c.y1, c.y2) - $ctx.heatmap_bbox[1];
	var end_y = Math.max(c.y1, c.y2) - $ctx.heatmap_bbox[1];
	
	var startCol =  parseInt(start_x / $ctx.pix_per_col);
	var endCol = parseInt(end_x / $ctx.pix_per_col + 1);
	
	var startRow = parseInt(start_y / $ctx.pix_per_row);
	var endRow = parseInt(end_y / $ctx.pix_per_row + 1);
	
	;;; var id = $($this).attr("id");
	//;;; _debug(id + ': ' + c.x1 + ' ' + c.x2 + ' ' + c.y1 + ' ' + c.y2 + ' ' + c.width + ' ' + c.height);
	//;;; _debug("startRow: " + startRow + "   endRow: " + endRow + "   startCol: " + startCol + "   endCol: " + endCol);
	
	//;;; _debug('onSelect: ' + typeof $cfg.onSelect.val);
	if (typeof $cfg.onSelect.val == 'function') {
	    var startProfile, endProfile, startSample, endSample;

	    if ($ctx.orient == 'ver') {
		startSample = Math.max(0, startCol);
		endSample = Math.max(0, endCol);
		startProfile = Math.max(0, startRow);
		endProfile = Math.max(0, endRow);
	    }
	    else {
		startSample = Math.max(0, startRow);
		endSample = Math.max(0, endRow);
		startProfile = Math.max(0, startCol);
		endProfile = Math.max(0, endCol);
	    }
	
	    var profiles = Array.prototype.slice.call($ctx.profile_metadata, startProfile, endProfile);
	    var samples = Array.prototype.slice.call($ctx.sample_metadata, startSample, endSample);

	    return $cfg.onSelect.val (profiles, samples, 
				      { start_profile: startProfile, end_profile: endProfile, 
					start_sample: startSample, end_sample: endSample }, $ctx);
	}
	return true;
    }


    /* _loadedHandler
     *     This is called when both the image and the corresponding metadata
     *     have been loaded and are ready for user interaction.  If present,
     *     it will invoke the config.OnReady user callback function.
     */
    function _loadedHandler (st) {
	this.config.onReady.state |= st;
	$("#hmDiv", $(this)).css("background-image", "");
	$("#hmImg", $(this)).css({ visibility: "visible" });
	
	if (this.config.onReady.state == loadStates.READY) {
	    if (this.config.resizable.val && this.config.dataset.val != 'banner') {
		$this = this;
		$("#hmImg", this).resizable({'ghost': true, 'stop': function(e) { 
		    //var $this = $(this).closest('.hm-container').parent();
		    _methods.config.apply($this,  [{ "width": parseInt($(this).width()), 
						     "height": parseInt($(this).height()) }]);			
		    
		    _load_heatmap.apply($this);
		} });
	    }

	    if (typeof this.config.onReady.val == 'function') {
		this.config.onReady.val.apply(this);
	    }
	}
	return true;
    }
	
    
    /* -----------------------------------------------
     *    D E F A U L T   C O N F I G U R A T I O N 
     * -----------------------------------------------
     * 
     * Keep default settings here.  Each setting indexes an object
     * that has two required attributes:
     *
     *   'reqparm' -- if true, indicates that this setting is used in the 
     *                http request sent to the server.
     *
     *    'val'    -- the (possibly empty or null) value for this attribute.
     *
     *    'hidden' -- do not copy this into any configuration that the user might see.
     *
     *    'callback'  -- item can incapsulate a user callback function
     *
     */
	    
    var loadStates = {  NOT_READY: 0, IMAGE_LOADED: 1, METADATA_LOADED: 2, READY: 3 };

    $.fn.heatmap.defaults = {
	// Parameters that will be passed in the HTTP POST request. (reqparm == true)
	dataset: { hidden: false,  reqparm: true, val: "testpattern"},
	width: { hidden: false, reqparm: true, val: ""},
	height: { hidden: false, reqparm: true, val: ""},
	aggrfn:  { hidden: false, reqparm: true, val: 'avg'},  // (avg|mod|max|min)
	colorize: { hidden: false, reqparm: true, val: 'local'},
	coloringmode: { hidden: false, reqparm: true, val: 'val'}, // (val|sat|both)
	bgcolor: { hidden: false, reqparm: true, val: "DAD8C8"},
	hicolor: { hidden: false, reqparm: true, val: "ff0000"},
	locolor: { hidden: false, reqparm: true, val: "0000ff"},
	nilcolor: { hidden: false, reqparm: true, val: "000000"},
	outlinecolor: { hidden: false, reqparm: true, val: ""},
	textcolor: { hidden: false, reqparm: true, val: "000000"},
	highlighttextcolor: { hidden: false, reqparm: true, val: 'ff2020'},
	axisfont: { hidden: false, reqparm: true, val: "helvR12"},
	highlighttextfont: { hidden: false, reqparm: true, val:  "helvB10"},
	axislabels: { hidden: false, reqparm: true, val: "mod"}, // (mod|max|min|avg|off)
	orient: { hidden: false, reqparm: true, val: "hor"},
	precision: { hidden: false, reqparm: true, val: 1},
	samples: { hidden: false, reqparm: true, val: ""},
	profiles: { hidden: false, reqparm: true, val: ""},
	samplemdcol: { hidden: false, reqparm: true, val: 0},
	profilemdcol: { hidden: false, reqparm: true, val: 0},
	samplesort: { hidden: false, reqparm: true, val: ""},  // (none|godel|hilo|choi)
	profilesort: { hidden: false, reqparm: true, val: ""},
	partition: { hidden: false, reqparm: true, val: ""},
	flatline: { hidden: false, reqparm: true, val: ""},
	cluster: { hidden: false, reqparm: true, val: ""},  //  (both|samp|prof|none)
	ref_profile: { hidden: false, reqparm: true, val: ""},
	ref_sample: { hidden: false, reqparm: true, val: ""},
	profile_dist: { hidden: false, reqparm: true, val: "c"},
	sample_dist: { hidden: false, reqparm: true, val: "c"},
	range_min: { hidden: false, reqparm: true, val: ""},
	range_max: { hidden: false, reqparm: true, val: ""},
	maxHighExprCount: { hidden: false, reqparm: true, val: ""},
	emphasis_mode: { hidden: false, reqparm: true, val: "zoom"},
	midpoint: { hidden: false, reqparm: true, val: "0.5"},
	rawdata: { hidden: false, reqparm: true, val: null},
	skipcols: { hidden: false, reqparm: true, val: null},
	skiprows: { hidden: false, reqparm: true, val: null},

	// DataTables support ...
	iDisplayStart: { hidden: true,  reqparm: true, val: 0},           // DataTables support ...
	iDisplayLength: { hidden: true,  reqparm: true, val: 1000000},    // DataTables support ...
	iSortCol_0: { hidden: true,  reqparm: true, val: 0},              // DataTables support ...
	
	// Parameters below are internal -- not passed to server.  (reqparm == false)
	url: { hidden: false,  reqparm: false, val: "/hamlet/image"},
	spinner_url: { hidden: false,  reqparm: false, val: "/images/mouse_wheel.gif"},
	
	resizable: { hidden: false,  reqparm: false, val: true },
	
	// User event handlers ...
	onMousemove: { hidden: false,  reqparm: false, val: null, callback: true },
	onSelect: { hidden: false,  reqparm: false, val: null, callback: true, 
		      imgAreaObj: null,
		      ias_opts: {  onSelectEnd: _selectionHandler, 
				     onSelectChange: _selectionHandler,
				     handles: true, 
				     show: true, hide: false,
				     x1: 0, y1: 0, x2: 0, y2: 0,
				     zIndex: 900,
				  } 
		    },
	onClick: { hidden: false, reqparm: false, val: null, callback: true },
	onReady: { hidden: false, reqparm: false, val: null, callback: true, state: loadStates.NOT_READY },

	html_template: { hidden: true,  reqparm: false, val: "\
<div id='divId' class='hm-container hm-noborder' style='width: inherit; height: inherit;'> \
 <div id='hmDiv' class='hm-noBorder hm-centeredContent'  style='width: inherit; height: inherit;'> \
  <img id='hmImg' src='' class='hm-noBorder' /> \
 </div> \
</div>"}
    };
    
    // Set up AJAX error handler.
    $.ajaxSetup({
	error: function(x,e){
	    if(x.status==0){
		alert('You are offline!!\n Please Check Your Network.');
	    }else if(x.status==404){
		alert('Requested URL not found.');
	    }else if(x.status==500){
		alert('Internel Server Error.');
	    }else if(x.status==504){
		alert('No data.');
	    }else if(x.status==505){
		alert('No such dataset.');
	    }else if(e=='parsererror'){
		alert('Error.\nParsing JSON Request failed.');
	    }else if(e=='timeout'){
		alert('Request Time out.');
	    }else {
		alert('Unknow Error: code='+x.status+'  response='+x.responseText);
	    }
	}
    });

    

}) (jQuery);

