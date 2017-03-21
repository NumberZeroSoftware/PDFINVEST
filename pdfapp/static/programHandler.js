// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 20/03/2017

var showingObjectives = false;

$(document).ready(function() {
    // Get Ready Materialize Selects
    $('#id_program-theory_hours').material_select();
    $('#id_program-practice_hours').material_select();
    $('#id_program-laboratory_hours').material_select();
    $('#id_program-validity_date_d').material_select();
    $('#id_program-credits').material_select();
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
            $('#id_program-validity_date_d').material_select();
        }
        else {
            $('#id_program-validity_date_d').removeAttr('disabled');
            $('#id_program-validity_date_d').material_select();
        }
    }


    if ($('#id_program-specific_objectives').val() == "") {
        $('#specific_objectives').hide();
        showingObjectives = false;
        $('#objectives').text('Agregar Objetivos Específicos');
    }
    else {
        showingObjectives = true;
        $('#objectives').text('Quitar Objetivos Específicos');
    }

    $('#objectives').on('click', function(){
        if (showingObjectives) {
            if (confirm("Está Apunto de Elimintar los Objetivos Específicos, ¿Está seguro?")) {
                $('#specific_objectives').hide();
                showingObjectives = false;
                $('#objectives').text('Agregar Objetivos Específicos');
                var aux = $('#id_program-objectives').val();
                if ($('#id_program-specific_objectives').val() != "") {
                    aux = aux + "\n"+ $('#id_program-specific_objectives').val(); 
                }          
                $('#id_program-objectives').val(aux);
                $('#id_program-specific_objectives').val("");
            }

        }
        else
        {
            if (confirm("Está Apunto de Agregar los Objetivos Específicos, ¿Está seguro?")) {
                $('#specific_objectives').show();
                showingObjectives = true;
                $('#objectives').text('Quitar Objetivos Específicos');
            }
        }
    });
  });


function handleYear(sel)
{
    if (sel.value == "") {
        $('#id_program-validity_date_m').val("");
        $('#id_program-validity_date_m').attr('disabled','disabled');
        $('#id_program-validity_date_m').material_select();
        $('#id_program-validity_date_d').val("");
        $('#id_program-validity_date_d').attr('disabled','disabled');
        $('#id_program-validity_date_d').material_select();
    }
    else {
        $('#id_program-validity_date_m').removeAttr('disabled');
        $('#id_program-validity_date_m').material_select();
        $('#id_program-validity_date_d').material_select();
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
        $('#id_program-validity_date_d').material_select();
    }
}