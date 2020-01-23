// samplesPanel
(function(){ // scoping

    samplesPanel = $("#samplesPanel");
    sampleButtons = $(".resultCard", samplesPanel); 
    resultSections = $(".resultVariants", samplesPanel);
    // console.log(sampleButtons);
    // console.log(resultSections);


    samplesPanel.on('click', '.resultCard', function(){

            var me = $(this);

            sampleButtons.removeClass('selected');
            me.addClass('selected');

            resultSections.removeClass('selected');
            var idx = sampleButtons.index(me);
            // console.log(idx)
            resultSections.eq(idx).addClass('selected');

    });


})(); // end scoping


// adapted variantsPanel
(function(){ // scoping

    variantsPanel = $(".per-variant");
    variantButtons = $(".variantButton", variantsPanel); 
    variantSections = $(".content.variant", variantsPanel);
    // console.log(variantButtons);
    // console.log(variantSections);


    variantsPanel.on('click', '.variantButton', function(){

            var me = $(this);
            // console.log(me)
            var targetParent = $(me.parents()[3]);
            // console.log(targetParent);
            var targetResultNum = targetParent.attr('class').split(/\s+/)[ 1 ];
            // console.log(targetResultNum);


            $.each(variantButtons, function(i, val) {
                // console.log(i)
                // console.log(val)
                var current = $(val)
                // console.log(current)
                var valParent = $(current.parents()[3]);
                var valResultNum = valParent.attr('class').split(/\s+/)[ 1 ];
                if (valResultNum == targetResultNum) {
                    current.removeClass('selected');
                }
            });
            // variantButtons.removeClass('selected');
            me.addClass('selected');

            $.each(variantSections, function(i, val) {
                var current = $(val)
                var valParent = $(current.parents()[2]);
                var valResultNum = valParent.attr('class').split(/\s+/)[ 1 ];
                if (valResultNum == targetResultNum) {
                    current.removeClass('selected');
                }
            });
            // variantSections.removeClass('selected');
            var idx = variantButtons.index(me);
            variantSections.eq(idx).addClass('selected');

    });


})(); // end scoping