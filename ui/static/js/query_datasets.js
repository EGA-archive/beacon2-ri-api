function select(target) {
    checkboxes = document.getElementsByName('datasetIds');
    if (target == 'all') {
        for(var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = true;
        }
    }
    else if (target == 'none') {
        for(var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
    }
}