
function showStuff(id, btn) {
    if (document.getElementById(id).style.display != 'none') {
        document.getElementById(id).style.display = 'none';
    }
    
    // hide the link
    //btn.style.display = 'none';

    // Stop Js from reloading page
    return false;
}