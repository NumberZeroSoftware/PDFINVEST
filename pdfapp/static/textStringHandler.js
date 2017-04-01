// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 29/03/2017


$("#textStringHTML").hide();
$("#textStringHTML").val($("#id_textstring-html_text_string").val());
$("#textString").html($("#id_textstring-html_text_string").val());

function loadTextstring() {
	var textStringForm = $("#id_textstring-html_text_string");
	$("#textStringHTML").val(textStringForm.val());
	$("#textString").html(textStringForm.val());
}

// If we are showing the html TextString
var showingHtmlTextstring = false;
loadTextstring();

// Update the textString in the correct places
function updateTextString(){
	var textString = $("#textString");
	var textStringHTML = $("#textStringHTML");
	var textStringForm = $("#id_textstring-html_text_string");
	// Update the crude html if we are showing the rendered html
	if (!showingHtmlTextstring) {
		var edited_content = textString.html(); 
		textString.html(edited_content);
		textStringHTML.val(edited_content);
		textStringForm.val(edited_content);

	}
	// Update the rendered html if we are showing the crude html
	else {
		textString.html(textStringHTML.val());
		textStringForm.val(textStringHTML.val());
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
		$('#showOther').text('Mostrar Texto');
	}
	else {
		textString.show();
		textStringHTML.hide();
		$('#showOther').text('Mostrar HTML');
	}
	showingHtmlTextstring = !showingHtmlTextstring;
});
