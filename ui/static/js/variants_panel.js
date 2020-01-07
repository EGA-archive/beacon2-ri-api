function openVariant(evt, variantName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("variant");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" selected", ""); 
    }
    document.getElementById(variantName).style.display = "block";
    evt.currentTarget.className += " selected";
}