// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 12/03/2017

$(document).ready(function() {
    $('#id_program-validity_year').material_select();
    $('#id_program-department').material_select();
    $('#id_program-division').material_select();
    $('#id_program-validity_trimester').material_select();
    $('#id_program-coordination').material_select();
    $('#id_program-division').change(function(){$('#id_program-department').material_select();});
    $('#id_program-code').material_select();
  });