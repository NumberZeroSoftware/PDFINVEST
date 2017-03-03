// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 02/03/2017


$("#textStringHTML").hide();
// If we are showing the html TextString
var showingHtmlTextstring = false;

function updateTextString(){
	var textString = $("#textString");
	var textStringHTML = $("#textStringHTML");
	// Update the crude html if we are showing the rendered html
	if (!showingHtmlTextstring) {
		var edited_content = textString.html(); 
		textString.html(edited_content);
		textStringHTML.val(edited_content);
	}
	// Update the rendered html if we are showing the crude html
	else {
		textString.html(textStringHTML.val());
	}
}

// Autosave
$("#textString").blur(function(){updateTextString();});

// Change view
$('#showOther').on('click', function(){
	updateTextString();
	var textString = $("#textString");
	var textStringHTML = $("#textStringHTML");
	if (!showingHtmlTextstring) {
		textString.hide();
		textStringHTML.show();
		$('#showOther').text('Show Text');
	}
	else {
		textString.show();
		textStringHTML.hide();
		$('#showOther').text('Show HTML');
	}
	showingHtmlTextstring = !showingHtmlTextstring;
});