// Rendering Google Maps //

function initMap(data) {
    let sf = {lat: 37.7995971, lng: -122.327749};
    let map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: sf,
        scrollwheel: true,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: [
  {
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#ebe3cd"
      }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#523735"
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#f5f1e6"
      }
    ]
  },
  {
    "featureType": "administrative",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#c9b2a6"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#dcd2be"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#ae9e90"
      }
    ]
  },
  {
    "featureType": "landscape.natural",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#93817c"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#a5b076"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#447530"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f5f1e6"
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#fdfcf8"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f8c967"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#e9bc62"
      }
    ]
  },
  {
    "featureType": "road.highway.controlled_access",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e98d58"
      }
    ]
  },
  {
    "featureType": "road.highway.controlled_access",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#db8555"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#806b63"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#8f7d77"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#ebe3cd"
      }
    ]
  },
  {
    "featureType": "transit.station",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#b9d3c2"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#92998d"
      }
    ]
  }
],
    });
    console.log('Hi I initiated the map')

    let infoWindow = new google.maps.InfoWindow({
      width: 150
    })
    console.log('I made the info window~')

    console.log('I am querying the dispensaries database.');
    if (data.count === 0) {
        let x = document.getElementById("map");
        x.style.display = "none";
        document.getElementsByClassName('modal-map')[0].innerHTML = "No dispenaries near you offer this strain, sorry!";
    } else {
        let marker, disp, html;

        for (let key in data.dispensaries) {
            disp = data.dispensaries[key];

            marker = new google.maps.Marker({
              position: new google.maps.LatLng(disp.lat, disp.lng),
              map: map,
              title: disp.name,
              icon: '/static/img/bud-icon.png',
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
    }; //end else
     //end ajax

    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'mouseover', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
        });
    }
}

let modal = document.getElementsByClassName('modal')[0];
google.maps.event.addDomListener(modal, 'load', initMap);