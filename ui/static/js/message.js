(function(){ // scoping

    // Not super efficient, but we won't have many messages
    $('#messages li').each(function( index ) {
	var el = $( this )
	var hideMe = function(){ el.addClass('hidden'); };
	var timer = setTimeout(hideMe, 5000);
	el.on("mouveover", function() {
	    clearTimeout(timer);
	}).on("mouveout", function() {
	    timer = setTimeout(hideMe, 5000);
	});
    });


})();
