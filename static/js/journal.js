// Strain event listener
let count = 1;
var entry;

$('#addStrain').click(function() {
  let user_input = $('#findStrain').val();
  if (!user_input) {
    alert('Please enter a strain')
  } else {
    if (count > 1) {
    alert('Please add one strain at a time.')
    } else {
    console.log(`I am checking if ${user_input} is in the database`);
    $.get('/check_strain', {'strain': user_input}, function(result){
      console.log(result);
      if (result=="") {
        alert('Strain not found in database.')
      } else {
    $('#strainFormsGroup').show();
    $('#strainFormsGroup').append("\
    <div class='newStrain' id='newStrain"+count+"'>\
    <div class='form-group'>\
      <label for='rating' class='col-sm-4 col-push-4\
      control-label'>Dankness:</label>\
      <div class='col-sm-2'>\
        <select type='rating' class='form-control' name='rating' id='rating'\
        required>\
          <option value='1'>1</option>\
          <option value='2'>2</option>\
          <option value='3'>3</option>\
          <option value='4'>4</option>\
          <option value='5'>5</option>\
          <option value='6'>6</option>\
          <option value='7'>7</option>\
          <option value='8'>8</option>\
          <option value='9'>9</option>\
          <option value='10'>10</option>\
        </select>\
      </div>\
    </div>\
     <div class='form-group'>\
        <label for='notes' class='col-sm-4 col-push-4 control-label'>\
          Notes:</label> <div class='col-sm-6'>\
        <textarea class='form-control' rows='2' id='notes'\
        name='notes' placeholder='Optional, talk to your future self.'></textarea> </div> </div>\
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
      <textarea class='form-control story' name='story' rows='4'\
      placeholder='Share with us your adventure!'\
       required></textarea> </div> </div> </div>")
    ) //close append new strain
}); //close addStory
}});  // GET else, GET request
} // else
}}) //close main else, close main event listener

// display new journal entry without refresh callback //
function updateJournal(result) {
  console.log(result);
  $('#strainFormsGroup').empty();
  $('#findStrain').val('');
  count = 1;
  $(`#journal_body${result['journal']}`).append("\
    <div class='row' id='entry"+ result['log_id']+"' style='margin:0;'><div\
    class='col-xs-4'style='padding:\
    0px, margin:0px'>\
              <a href='https://www.leafly.com/{{\
            entry.strain.leafly_url }}' target='_blank'>" + result['strain'] +
            "</a></div><div class='col-xs-3'>rating:" + result['rating'] +
            "</div><div class='col-xs-4' style='width:110px'>" +
            result['notes'] + "</div><div class='col-xs-1' style='padding: 0px,\
            margin: 0px'>" + "<a><span class='removeStrain glyphicon\
            glyphicon-remove' data-entry=" + result['log_id']
            + "></span></a></div></div>")
}

$('#submitUpdate').click(function(evt) {
  evt.preventDefault();
  if ($('#strainFormsGroup').is(":hidden")) {
    alert('Please click the "add" button.')
  } else {
  let newStrainData = {
        'journal': $('#journal').val(),
        'strain': $('#findStrain').val(),
        'user_rating': $('#rating').val(),
        'notes': $('#notes').val(),
        'dosage': $('#dosage').val(),
        'story': $('.story').val(),
  };
  console.log('Story:',newStrainData['story'])
  $.post("/journal/update", newStrainData, updateJournal);
// To-do: alert error if user inputs random strain
  };
})

$('#finishUpdates').click(function(evt){
  evt.preventDefault();
  location.reload();
})

$('.removeStrain').click(function() {
  console.log('I am removing a strain')
  entry = $(this).data('entry');
  $(`#entry${entry}`).remove();

  $.post("/journal/remove_strain.json", {
    'entry' : entry,
  }, function(result) {
    console.log(result);
  });
})


$('.removeJournal').click(function(evt) {
  evt.preventDefault();
  let journal= $(this).data('journal')
  $(`#${journal}`).remove();

  $.post("/journal/remove", {
    'journal' : journal,
  }, function(result) {
    console.log(result);
  })
})

// Generate photo for carousel background
let images = ['./static/img/carousel_bg/1.jpg',
'./static/img/carousel_bg/2.jpg','./static/img/carousel_bg/3.jpg','./static/img/carousel_bg/4.jpg','./static/img/carousel_bg/5.jpg',
'./static/img/carousel_bg/6.jpg','./static/img/carousel_bg/7.jpg','./static/img/carousel_bg/8.jpg','./static/img/carousel_bg/11.jpg',
'./static/img/carousel_bg/10.jpg', './static/img/carousel_bg/9.jpg']

let i = 0;
let j = randomize();

function randomize() {
  return Math.floor(Math.random() * images.length);
}

function randomPic() {
  j = randomize();
  if (i === j) {
    randomPic();
  } else {
    $(element).attr('src', images[j]);
    i = j;
    console.log('random image generator working');
  }};

for (element of $('.carousel-bg')) {
  randomPic();
};