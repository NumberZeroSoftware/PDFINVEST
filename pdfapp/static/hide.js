// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 02/12/2017


// Show something with a button
// The value of the button is the name of the button + Show or Hide
// id : name of the thing to hode or show
// btn : button that got clickt to do that
function showStuff(id, btn) {
    var displayStyle = document.getElementById(id).style.display;
    if (displayStyle != 'none') {
        setCookie(id+"cssStyleDisplay", displayStyle, 1);
        document.getElementById(id).style.display = 'none';
        btn.value = "Show " + btn.name;
    }
    else {
        document.getElementById(id).style.display = getCookie(id+"cssStyleDisplay");
        btn.value = "Hide " + btn.name;
    }
    return false;
}