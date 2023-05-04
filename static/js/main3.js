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

            // reset carousel indicators
            document.querySelector('.carousel-indicators').innerHTML = ""
            document.querySelector('.carousel-indicators').insertAdjacentHTML("afterbegin",
                `<button type="button" data-bs-target="#my-carousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Region"></button>
                `);

            // reset carousel contents
            document.querySelector('.carousel-inner').innerHTML = ""
            document.querySelector('.carousel-inner').insertAdjacentHTML("afterbegin",
                `<div class="carousel-item active">
                    <div class="region">
                        <label for="region-choice">Please choose a US Forest Service Region:</label>
                            <select name="region-choice" id="region-choice">
                                <option value="" disabled selected>Regions</option>
                        </select>
                        <div class="map region"style="overflow: visible;">
                            <h2>Region Map</h2>
                            <div id="region-map" style="width:100%; height: 100%; min-width: 300px; min-height: 500px;"></div>
                        </div>
                    </div>
                </div>`);

            // Populate region choices
            for (const region of regions) {
                document.querySelector('#region-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${region['id']}'>${region['name']}</option>`)
            }

            // Create map
            const map = new mapboxgl.Map({
                container: 'region-map', // container ID
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

                    map.addLayer({
                        'id': `${region.name}-label`,
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
                            'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                        }
                    });
                    
                    // map.setFilter(`${region.name}-label`, ['==', ['get', 'REGION'], region.id]);
                    
                }
                
                
                // Add zoom and rotation controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
                
                console.log('done with region map')
            });
        })
});

document.querySelector('#region-choice').addEventListener('input', (evt) => {
    const region = `?region=${evt.target.value}`
    fetch(`/region${region}`)
        .then((response) => response.json())
        .then((data) => {
            const forests = data['forests'];

            // add carousel indicators
            document.querySelector('.carousel-indicators').insertAdjacentHTML("beforeend",
                `<button type="button" data-bs-target="#my-carousel" data-bs-slide-to="1" aria-label="Forest"></button>

                `);

            // add carousel contents
            document.querySelector('.carousel-inner').insertAdjacentHTML("beforeend",
                `<div class="carousel-item">
                    <div class="forest">
                        <label for="forest-choice">Please choose a Forest:</label>
                            <select name="forest-choice" id="forest-choice">
                                <option value="" disabled selected>National Forests</option>
                            </select>    
                            <div class="map forest">
                                <h2>Forest Map</h2>
                                <div id="forest-map"></div>
                        </div>  
                    </div>
                </div>
            `);

            // Populate Forest Choices
            document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                '<option value="" disabled selected>Choose a National Forest</option>')
            for (const forest of forests) {
                const name = forest['name']
                const id = forest['id']
                const isEmpty = forest['isEmpty']
                if (isEmpty === true){
                    document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                    `<option value = '${id}' disabled>${name}</option>`)
                } else {
                    document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                    `<option value = '${id}'>${name}</option>`)
                }
            }

            // Create map
            const map = new mapboxgl.Map({
                container: 'forest-map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                // TODO: change to center of region
                center: data['startingLngLat'], // starting position [lng, lat] (geographic center of US, 39°50′N 98°35′W, according to https://en.wikipedia.org/wiki/Geographic_center_of_the_United_States)
                zoom: 6 // starting zoom
                });
            
            // Load map
            map.on('load', () => {
                map.addSource(
                    'forests', {
                        'type': 'geojson',
                        'data': `/forests.geojson${region}`
                    });

                // add fill color to forests
                for (const forest of forests) {
                    console.log(forest.id)
                    const newColor = generateColor()
                    console.log(newColor)
                    map.addLayer({
                        'id': `${forest.name}-layer`,
                        'type': 'fill',
                        'source': 'forests',
                        'paint': {
                            'fill-color': newColor,
                            'fill-opacity': 0.5,
                            'fill-outline-color': newColor
                        },
                        'filter': ["==", forest.name, ["get", "FORESTNAME"]]
                    })
                    
                    map.addLayer({
                        'id': `${forest.name}-label`,
                        'type': 'symbol',
                        'source': 'forests',
                        'layout': {
                            'text-field': [
                                'format',
                                ['upcase', ['get', 'FORESTNAME']],
                                { 'font-scale': 0.8 },
                                '\n',
                                {},
                                ['downcase', ['get', 'FORESTNUMBER']],
                                { 'font-scale': 0.6 }
                            ],
                            'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                        }
                    });

                    
                }

                // Add navigation controls
                map.addControl(new mapboxgl.NavigationControl());
                
                console.log('done with forest map')
                
            });

        })
});