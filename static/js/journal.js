// Strain event listener
let count = 1;

$('#addStrain').click(function() {
  if (!$('#findStrain').val()) {
    alert('Please enter a strain')
  } else {
  console.log("I'm inside the event listener");
  console.log('journal',$('#journal').val(), $('#findStrain').val())
  if (count > 1) {
    alert('Please add one strain at a time.')
  } else {
    $('#strainFormsGroup').show();
    $('#strainFormsGroup').append("\
    <div class='newStrain' id='newStrain"+count+"'>\
    <div class='form-group'>\
      <label for='rating' class='col-sm-4 col-push-4\
      control-label'>Dankness:</label>\
      <div class='col-sm-2'>\
        <select type='rating' class='form-control' name='rating' required>\
          <option value='1'>1</option>\
          <option value='2'>2</option>\
          <option value='3'>3</option>\
          <option value='4'>4</option>\
          <option value='5'>5</option>\
        </select>\
      </div>\
    </div>\
     <div class='form-group'>\
        <label for='notes' class='col-sm-4 col-push-4 control-label'>\
          Notes:</label> <div class='col-sm-6'>\
        <textarea class='form-control' rows='2' id='notes'\
        name='notes' placeholder='Optional, talk to your future self.'><textarea> </div> </div>\
        <div class='checkbox'>\
        <label> <input type='checkbox' id='addStory'>\
        Do you have a story to tell?</label>\
    </div>\
    </div>")
    count ++;

$('#addStory').click(function() {
    $('#strainFormsGroup').append(
      $('#newStrain1').append("\
        <br>\
      <div class='form-group'>\
        <label for='dosage' class='col-sm-4 col-push-4 control-label'>\
          Dosage:</label> <div class='col-sm-5'>\
        <input type='dosage' class='form-control' name='dosage' id='dosage'\
        placeholder='in milligrams(mg)'> </div> </div>\
      <div class='form-group'>\
      <div class='col-sm-10 col-sm-offset-1'>\
      <textarea class='form-control' rows='4' id='story'\
       placeholder='Share with us your adventure!' name='story'></textarea>\
       </div> </div> </div>")
    ) //close append new strain
});} //close else
}}) //close main else, close main event

function updateJournal(result) {
  $('#strainFormsGroup').hide();
}

$('#submitUpdate').click(function(evt) {
  evt.preventDefault();
  if ($('#strainFormsGroup').is(":hidden")) {
    alert('Please enter a strain and click the check icon.')
  } else {
  let newStrainData = {
        'journal': $('#journal').val(),
        'strain': $('#strain').val(),
        'user_rating': $('#rating').val(),
        'note': $('#note').val(),
        'dosage': $('#dosage').val(),
        'story': $('#story').val(),
  };
  $.post("/journal/update", newStrainData, updateJournal);
}
})