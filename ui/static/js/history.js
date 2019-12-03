(function(){ // scoping

    // Check support for localStorage
    try { localStorage.setItem('somekey', 'somevalue'); localStorage.removeItem('somekey'); }
    catch (e) { return ; } // unsupported: exit


    var key = 'beacon-history';
    
    // localStorage handles only strings: Convert to Array with JSON
    var history_items = JSON.parse(localStorage.getItem(key)) || [];

    // console.log("History so far", history_items);

    // If we have a response, append to history
    var response = document.querySelector('#response-history');

    // var form = document.querySelector('form#query');
    // var main = document.querySelector('body#response main');
    // var footer = document.querySelector('body#response footer');
    var body   = document.querySelector('body'),
	form   = document.querySelector('body > form'),
	main   = document.querySelector('body > main'),
	footer = document.querySelector('body > footer');

    if (response){
	var thumbnail = response.cloneNode(true); // deep
	
	if(form && main && footer){
	    thumbnail.removeAttribute('id');
	    history_items.push([form.outerHTML,main.outerHTML,thumbnail.outerHTML,footer.outerHTML]);
	    // console.log("Appending to history");
	    localStorage.setItem(key, JSON.stringify(history_items));
	}
    }

    // If we do have some history to render
    var count = history_items.length;
    if ( count > 0 ){

	// console.log("Rendering history", count);
	var container = $('<aside><h1>History<span>'+count+'</span></h1></aside>');
	// console.log(container);

	while(count--){ // read count then decrement
	    var thumb_html = history_items[count][2]; // just the thumbnail
	    // Convert to JQuery and append
	    //$(thumb_html).appendTo(container)
	    var t = $(thumb_html);
	    t.attr('data-pos', count);
	    t.appendTo(container);
	}

	var clear_history = $('<span>Clear History</span>');
	clear_history.on('click', function(){
	    localStorage.removeItem(key);
	    $('aside').remove();
	});
	clear_history.appendTo(container);
	
	container.appendTo('body');


	// Reloading an item
	container.delegate("section h2 i", "click", function() {
	    var pos = $( this ).parents('section').attr('data-pos');
	    //console.log("position", pos);
	    var [form_html, main_html, thumb_html, footer_html] = history_items[pos];
	    body.setAttribute('id','response');
	    form.outerHTML = form_html;
	    main.outerHTML = main_html;
	    footer.outerHTML = footer_html;
	    //console.log("Repainting");
	    //console.log(history_items[pos]);

	    // outerHTML knocked the elements out
	    // need to re-find them
	    form   = document.querySelector('body > form');
	    main   = document.querySelector('body > main');
	    footer = document.querySelector('body > footer');

	    return false;
	});

    }

})();
