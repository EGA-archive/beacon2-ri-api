(function(){ // scoping

    // ----------------------------------------------
    // Cookie disclaimer
    // ----------------------------------------------
    var cookiePane = document.querySelector('#beacon-cookies'),
	cookieButton = null;
    if(cookiePane)
	cookieButton = cookiePane.querySelector('button');
    if(cookiePane && cookieButton)
	cookieButton.addEventListener('click', function(){
	    var expires = new Date(new Date().setFullYear(new Date().getFullYear() + 1)); // JS is so shitty
	    document.cookie = "beacon=consent;path=/;expires="+expires.toGMTString();
	    cookiePane.setAttribute("class", 'hide-me'); // set to 1s
	    setTimeout(function(){ cookiePane.remove(); }, 1100);
	    return false;
	});


    // Click/Toggle sidebar panel
    $( ".trigger" ).click(function() {
	$( this ).parent('div').toggleClass( "open" );
    });

    // ----------------------------------------------
    // Filters
    // ----------------------------------------------
    var filters = $( "#query-filters" );
    
    // Utilities
    if(typeof(String.prototype.trim)==="undefined"){String.prototype.trim=function(){return String(this).replace(/^\s+|\s+$/g,'');};}

    var make_autocomplete = function(el){
	el.autocomplete({
	    minLength: 0
	    , delay: 300
    	    , source: function (request, response) {

		var term = request.term;
		if(term.length >= 2){
		    var url = "/terms/" + term;
		    //console.log(url);
		    $.get(url, response);
		}
	    }
	    , focus: function() {
		// prevent value inserted on focus
		return false;
            }
	    // , _renderItem: function( ul, item ){
	    // 	return $( "<li>" )
	    // 	    .attr( "data-value", item.value )
	    // 	    .append( item.label )
	    // 	    .appendTo( ul );
	    // }
	    , select: function( event, ui ) {
		el.val(ui.item.value);
		// Delete spans from parent
		el.parent().find("span").remove();
		$( "<span>" ).html(ui.item.label).insertBefore(el);
		el.focus();
	    }
	});
    }

    filters.delegate( ".filter-add", "click", function() {

    	var button = $('<i/>');
	button
	    .addClass("filter-remove")
	    .addClass("fas")
	    .addClass("fa-minus-circle");

    	var input = $('<input/>', {
	    "type": "text",
	    "value": "",
	    "placeholder": "HP:0011007>=49 or PATO:0000383 or EFO:0009656",
	    "name": "filters" ,
	    "data-lpignore": "true"
	});

    	var section = $('<section/>');

	section.append(input);
	section.append(button);
    	filters.append(section);
	make_autocomplete(input);
	input.focus();

    });

    filters.delegate( ".filter-remove", "click", function() {
    	$( this ).parent('section').remove();
    });


    // Autocomplete for the already present one
    filters.find('input').each(function(){ make_autocomplete($(this)); });

    // ----------------------------------------------
    // Datasets
    // ----------------------------------------------
    var datasets = $( "#query-datasets" );
	var datasetsSelectors = datasets.find( "input:not([disabled])" ); // enough
    $("#datasets-header").delegate( "span", "click", function() {
	var content = $( this ).text();
	if( content == 'All' ){
		datasetsSelectors.prop('checked', true);
	}
	if( content == 'None' ){
	    datasetsSelectors.prop('checked', false);
	}
    });




    // ----------------------------------------------
    // Escape key to close the API popups
    // ----------------------------------------------
    $(document).keyup(function(e) {
	//console.log('Key Code', e.keyCode);
	if (e.keyCode == 27) { // escape
	    $('#beacon-response-trigger').prop('checked', false);
	    $('#beacon-request-trigger').prop('checked', false);
	}
    });

})();
