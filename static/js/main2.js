// enforce better formatting
'use strict';

// random color generator from https://www.tutorialstonight.com/random-color-generator-javascript
function generateColor() {
    let color = '#';
    let digits = '0123456789ABCDEF';
    for (let i = 0; i < 6; i++) {
      // generate a random number between 0 and 15
      let randomDigit = Math.floor(Math.random() * 16);
      // append the random number to the color string
      color += digits[randomDigit];
    }
    return `${color}`
}

document.addEventListener("DOMContentLoaded", () => {
    fetch("/initialize")
        .then((response) => response.json())
        .then((data) => {
            const regions = data['regions'];
            mapboxgl.accessToken = `${data.mapKey}`;

            // Create map
            const map = new mapboxgl.Map({
                container: 'map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                center: [-98.5833, 39.8333], // starting position [lng, lat] (geographic center of US, 39°50′N 98°35′W, according to https://en.wikipedia.org/wiki/Geographic_center_of_the_United_States)
                zoom: 4 // starting zoom
                });
            
            // Load map
            map.on('load', () => {
                map.addSource(
                    'regions', {
                        'type': 'geojson',
                        'data': '/regions.geojson'
                    });

                // add fill color to regions
                for (const region of regions) {
                    const newColor = generateColor()
                    map.addLayer({
                        'id': `${region.name}-layer`,
                        'type': 'fill',
                        'source': 'regions',
                        // 'source-layer': 'Forest_Service_Regional_Boundaries__Feature_Layer_',
                        'paint': {
                            'fill-color': newColor,
                            'fill-opacity': 0.5,
                            'fill-outline-color': newColor
                        },
                        'filter': ["==", region.name, ["get", "REGIONNAME"]]
                    });
                }

                // add labels to regions
                map.addLayer({
                    'id': 'region-names',
                    'type': 'symbol',
                    'source': 'regions',
                    'layout': {
                        'text-field': [
                            'format',
                            ['upcase', ['get', 'REGIONNAME']],
                            { 'font-scale': 0.8 },
                            '\n',
                            {},
                            ['downcase', ['get', 'REGION']],
                            { 'font-scale': 0.6 }
                        ],
                        'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold']
                    }
                });                
                
                // Add zoom and rotation controls to the map.
                map.addControl(new mapboxgl.NavigationControl());

            });

            map.on('click', (evt) => {
                console.log(`A click event has occurred at ${evt.lngLat}`)
                // const clickedRegion = `?region=${"REGION"}`
            } )
        })
  });