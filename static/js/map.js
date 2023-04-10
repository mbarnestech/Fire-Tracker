// enforce better formatting
'use strict';

// function fetchTrailPoints{
//   fetch('/go_to_map')
//     .then((response)=>response.json())
//     .then((data)=>{
//       // TODO
//     });
// }

function initMap() {
  let uluru = {lat: -25.344, lng: 131.036};
  let map = new google.maps.Map(
      document.getElementById('map'), {zoom: 4, center: uluru}
  );
  let marker = new google.maps.Marker({position: uluru, map: map});
}