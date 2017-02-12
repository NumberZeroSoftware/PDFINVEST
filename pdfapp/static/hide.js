// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 02/12/2017

function showStuff(id, btn) {
    var displayStyle = document.getElementById(id).style.display;
    if (displayStyle != 'none') {
        setCookie(id+"cssStyleDisplay", displayStyle, 1);
        document.getElementById(id).style.display = 'none';
        btn.value = "Show";
    }
    else {
        document.getElementById(id).style.display = getCookie(id+"cssStyleDisplay");
        btn.value = "Hide";
    }
    return false;
}