// Modal for displaying individual strain info on Strains page //

// Get the <span> element that closes the modal
let span = document.getElementsByClassName('close')[0];

$('.openmodal').click(function(evt) {
    evt.preventDefault();
    console.log("I'm inside the event listener")
    let strain = $(this).data('strain');

    $.get('/map.json', {'strain': strain}, function(json) {
        console.log('I am inside the modal');
        document.getElementsByClassName('modal-title')[0].innerHTML = json.name;
        document.getElementsByClassName('modal-body')[0].innerHTML = json.pos +
            "<br><br><div class='description' align='left'>" + json.desc + "</div>" +
            "<p align='right'><i>source: Leafly.com</i></p>";
        document.getElementsByClassName('modal-map')[0].innerHTML =
            "<h5>Where can I find it?</h5><div id='map'></div>"
        initMap(json);
        modal.style.display = "block";
    })
})

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
    document.getElementsByClassName('modal-title')[0].innerHTML = "Please Wait...";
    document.getElementsByClassName('modal-body')[0].innerHTML = "Loading page";
    document.getElementsByClassName('modal-map')[0].innerHTML = ":)";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.getElementsByClassName('modal-title')[0].innerHTML = "Please Wait...";
        document.getElementsByClassName('modal-body')[0].innerHTML = "Loading page";
        document.getElementsByClassName('modal-map')[0].innerHTML = ":)";
    }
}