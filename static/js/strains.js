// Modal for displaying individual strain info on Strains page //
"use strict"

// Get the modal
let modal = document.getElementsByClassName('modal')[0];

// // Get the button that opens the modal
// let open = document.getElementById("openmodal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// // When the user clicks on the button, open the modal
// open.onclick = function() {
//     modal.style.display = "block";
// }

$('.openmodal').click(function(evt) {
    evt.preventDefault();
    let id = $(this).data('strain-id');
    map = 
    $.get(`/strains.json?id=${id}`, function(data) {
        document.getElementsByClassName('modal-header')[0].innerHTML = data.name
        document.getElementsByClassName('modal-body')[0].innerHTML =
            data.pos
            $.get(`/map?strain=${data.name}`, function() {
                document.getElementsByClassName('modal-map')[0].innerHTML =
                })
            // `<a href='/map?strain=${data.name}'>Find Dispensaries</a><br>`
        modal.style.display = "block";
    })
})

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}