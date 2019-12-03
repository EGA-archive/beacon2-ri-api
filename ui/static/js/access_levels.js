(function(){ // scoping

    var fieldsParam = $( "#fields-param" ),
	datasetsParam = $( "#datasets-param" );

    var reloadParams = function(){
	var url_params =
	    '?'+ fieldsParam.attr('data-param') +'=' + ((fieldsParam.prop('checked'))?'true':'false') +
	    '&'+ datasetsParam.attr('data-param') +'=' + ((datasetsParam.prop('checked'))?'true':'false');
	var loc = '//' + location.host + location.pathname;
	window.location.href = loc + url_params;
    }

    fieldsParam.on('change', reloadParams);
    datasetsParam.on('change', reloadParams);

})();
