// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 12/03/2017

$(document).ready(function() {
    $('#id_program-validity_year').material_select();
    $('#id_program-validity_date_m').material_select();
    $('#id_program-validity_year').on('change', function() {
      handleYear( this );
    })
    $('#id_program-validity_date_m').on('change', function() {
      handleMonth( this );
    })
    $('#id_program-department').material_select();
    $('#id_program-division').material_select();
    $('#id_program-validity_trimester').material_select();
    $('#id_program-coordination').material_select();
    $('#id_program-division').change(function(){$('#id_program-department').material_select();});
    $('#id_program-code').material_select();

    if ( $('#id_program-validity_year').val() == "") {
    	$('#id_program-validity_date_m').val("");
    	$('#id_program-validity_date_m').attr('disabled','disabled');
    	$('#id_program-validity_date_m').material_select();
    	$('#id_program-validity_date_d').val("");
    	$('#id_program-validity_date_d').attr('disabled','disabled');
    }
    else {
    	$('#id_program-validity_date_m').removeAttr('disabled');
    	$('#id_program-validity_date_m').material_select();
    	if ($('#id_program-validity_date_m').val() == "") {
    		$('#id_program-validity_date_d').val("");
    		$('#id_program-validity_date_d').attr('disabled','disabled');
    	}
    	else {
    		$('#id_program-validity_date_d').removeAttr('disabled');
    	}
    }

  });


function handleYear(sel)
{
	if (sel.value == "") {
		$('#id_program-validity_date_m').val("");
		$('#id_program-validity_date_m').attr('disabled','disabled');
		$('#id_program-validity_date_m').material_select();
		$('#id_program-validity_date_d').val("");
		$('#id_program-validity_date_d').attr('disabled','disabled');
	}
	else {
		$('#id_program-validity_date_m').removeAttr('disabled');
		$('#id_program-validity_date_m').material_select();
	}
}

function handleMonth(sel)
{
	if (sel.value == "") {
		$('#id_program-validity_date_d').val("");
		$('#id_program-validity_date_d').attr('disabled','disabled');
	}
	else {
		$('#id_program-validity_date_d').removeAttr('disabled');
	}
}