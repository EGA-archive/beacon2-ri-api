(function(){ // scoping

    variantsPanel = $(".variantsPanel");
    variantButtons = $(".variantButton", variantsPanel); 
    variantSections = $(".content.variant", variantsPanel);
    // console.log(variantButtons);
    // console.log(variantSections);


    variantsPanel.on('click', '.variantButton', function(){

            var me = $(this);
            // console.log(me);

            variantButtons.removeClass('selected');
            me.addClass('selected');

            variantSections.removeClass('selected');
            var idx = variantButtons.index(me);
            // console.log(idx)
            variantSections.eq(idx).addClass('selected');

    });


})(); // end scoping

