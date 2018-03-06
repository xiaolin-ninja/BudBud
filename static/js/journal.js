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
      <textarea class='form-control' rows='4' id='story'\
       placeholder='Share with us your adventure!' name='story'\
       required></textarea> </div> </div> </div>")
    ) //close append new strain
}); //close addStory
}});  // GET else, GET request
} // else
}}) //close main else, close main event listener

function updateJournal(result) {
  console.log(result);
  $('#strainFormsGroup').empty();
  $('#findStrain').val('');
  count = 1;
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
        'story': $('#story').val(),
  };
  $.post("/journal/update", newStrainData, updateJournal);
// To-do: alert error if user inputs random strain
  };
})

$('#finishUpdates').click(function(evt){
  evt.preventDefault();
  location.reload();
})

$('.removeStrain').click(function() {
  entry = $(this).data('entry')
  console.log(entry)

  $.post("/journal/remove_strain.json", {
    'entry' : entry,
  }, function(result) {
    console.log(result);
    location.reload();

  })
})

$('.removeJournal').click(function(evt) {
  evt.preventDefault();
  let journal= $(this).data('journal')
  $.post("/journal/remove", {
    'journal' : journal,
  }, function(result) {
    console.log(result);
    location.reload();
  })
})

// Generate photo for carousel background
let images = ['./static/img/carousel_bg/1.jpg',
'./static/img/carousel_bg/2.jpg','./static/img/carousel_bg/3.jpg','./static/img/carousel_bg/4.jpg','./static/img/carousel_bg/5.jpg',
'./static/img/carousel_bg/6.jpg','./static/img/carousel_bg/7.jpg','./static/img/carousel_bg/8.jpg',
'./static/img/carousel_bg/13.jpg', './static/img/carousel_bg/11.jpg',
'./static/img/carousel_bg/12.jpg', './static/img/carousel_bg/10.jpg',
'./static/img/carousel_bg/9.jpg']

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