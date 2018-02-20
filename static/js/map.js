// Rendering Google Maps //

function initMap() {
    let sf = {lat: 37.7995971, lng: -122.327749};
    let map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: sf,
        scrollwheel: true,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
    });
    console.log('Hi I initiated the map')

    let infoWindow = new google.maps.InfoWindow({
      width: 150
    })
    console.log('I made an info window~')

    // doesn't ever make this get request
    $.get('/dispensaries.json', function(disp_json) {
        console.log('I am GETting the dispensaries information for map!');
        console.log(disp_json);
        if (disp_json.count === 0) {
            alert('No dispenaries near you offer this strain, sorry!')
        } else {
            let marker, disp, html;

            for (let key in disp_json.dispensaries) {
                disp = disp_json.dispensaries[key];

                marker = new google.maps.Marker({
                  position: new google.maps.LatLng(disp.lat, disp.lng),
                  map: map,
                  title: disp.name,
                });

                html = (
                    '<div class="window-content">' +
                          '<p><b>Dispensary: </b>' + disp.name + '</p>' +
                          '<p><b>Address: </b>' + disp.address + '</p>' +
                          '<a href="https://www.google.com/maps?saddr=My+Location&daddr='+disp.lat+','+disp.lng+'" target="_blank">' +
                          '<p><b>Take Me There!</b></p></a>' +
                    '</div>');

                bindInfoWindow(marker, map, infoWindow, html);
            } //end for loop
        } //end else
    }); //end ajax

    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'mouseover', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
        });
    }
}

google.maps.event.addDomListener(window, 'load', initMap);