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
            // const trails = data['trails'];
            const regions = data['regions'];
            // const forests = data['forests'];
            // const districts = data['districts'];
            mapboxgl.accessToken = `${data.mapKey}`;

            // Populate region choices
            for (const region of regions) {
                document.querySelector('#region-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${region['id']}'>${region['name']}</option>`)
            }

            // Reset Dropdowns
            document.querySelector('#forest-choice').innerHTML = ''
            document.querySelector('#district-choice').innerHTML = ''
            document.querySelector('#trail-choice').innerHTML = ''

            // make sure trail info is hidden
            document.getElementById('trail-info').style.visibility = "hidden";

            // Create map
            const map = new mapboxgl.Map({
                container: 'region-map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                center: [-98.5833, 39.8333], // starting position [lng, lat] (geographic center of US, 39°50′N 98°35′W, according to https://en.wikipedia.org/wiki/Geographic_center_of_the_United_States)
                zoom: 3 // starting zoom
                });
            
            // resize map on render
            map.on('render', () => {
                map.resize();});

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
                
                
                // Add zoom, rotation, and full-screen controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
                // map.addControl(new mapboxgl.FullscreenControl({container: document.querySelector('body')}));
                console.log('done with region map')
            });
        })
  });


// //   both 'input' and 'change' events seem to listen equally well for selection
document.querySelector('#region-choice').addEventListener('input', (evt) => {
    const region = `?region=${evt.target.value}`
    fetch(`/region${region}`)
        .then((response) => response.json())
        .then((data) => {
            // const trails = data['trails'];
            const forests = data['forests'];
            // const districts = data['districts'];

            // Reset Maps
            document.querySelector("#forest-map").innerHTML = ''
            document.querySelector("#district-map").innerHTML = ''
            document.querySelector("#trail-map").innerHTML = ''
            document.querySelector("#trail-and-fire-map").innerHTML = ''

            // Reset Dropdowns
            document.querySelector('#forest-choice').innerHTML = ''
            document.querySelector('#district-choice').innerHTML = ''
            document.querySelector('#trail-choice').innerHTML = ''

            // make sure trail info is hidden
            document.getElementById('trail-info').style.visibility = "hidden";

            // Update Forests
            document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                '<option value="" disabled selected>Choose a National Forest</option>')
            for (const forest of forests) {
                const name = forest['name']
                const id = forest['id']
                const isEmpty = forest['isEmpty']
                if (isEmpty === true){
                document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${id}' disabled>${name}</option>`)} else {
                document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${id}'>${name}</option>`)}
            }

            // Create map
            const map = new mapboxgl.Map({
                container: 'forest-map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                center: data['startingLngLat'], // starting position [lng, lat] (geographic center of US, 39°50′N 98°35′W, according to https://en.wikipedia.org/wiki/Geographic_center_of_the_United_States)
                zoom: 5 // starting zoom
                });
            
            // resize map on render
            map.on('render', () => {
                map.resize();});
            
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

                // Add zoom, rotation, and full-screen controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
                // map.addControl(new mapboxgl.FullscreenControl({container: document.querySelector('body')}));
                console.log('done with forest map')
                
            });

        })
});


document.querySelector('#forest-choice').addEventListener('input', (evt) => {
    const forest = `?forest=${evt.target.value}`
    console.log(`forest=${forest}`)
    fetch(`/forest${forest}`)
        .then((response) => response.json())
        .then((data) => {
            // const trails = data['trails'];
            const districts = data['districts'];

            // Reset Maps
            document.querySelector("#district-map").innerHTML = ''
            document.querySelector("#trail-map").innerHTML = ''
            document.querySelector("#trail-and-fire-map").innerHTML = ''

            // Reset Dropdowns
            document.querySelector('#district-choice').innerHTML = ''
            document.querySelector('#trail-choice').innerHTML = ''

            // make sure trail info is hidden
            document.getElementById('trail-info').style.visibility = "hidden";

            // Update Districts
            document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
                '<option value="" disabled selected>Choose a Ranger District</option>')
            for (const district of districts) {
                const name = district['name']
                const id = district['id']
                const isEmpty = district['isEmpty']
                if (isEmpty === true){
                document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${id}' disabled>${name}</option>`)} else {
                document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${id}'>${name}</option>`)}
            }

            // Create map
            const map = new mapboxgl.Map({
                container: 'district-map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                center: data['startingLngLat'], // starting position [lng, lat] (geographic center of US, 39°50′N 98°35′W, according to https://en.wikipedia.org/wiki/Geographic_center_of_the_United_States)
                zoom: 7.5 // starting zoom
                });
            
            // resize map on render
            map.on('render', () => {
                map.resize();});

            // Load map
            map.on('load', () => {
                map.addSource(
                    'districts', {
                        'type': 'geojson',
                        'data': `/districts.geojson${forest}`
                    });

                // add fill color to districts
                for (const district of districts) {
                    console.log(district.id)
                    const newColor = generateColor()
                    console.log(newColor)
                    map.addLayer({
                        'id': `${district.name}-layer`,
                        'type': 'fill',
                        'source': 'districts',
                        'paint': {
                            'fill-color': newColor,
                            'fill-opacity': 0.5,
                            'fill-outline-color': newColor
                        },
                        'filter': ["==", district.id, ["get", "DISTRICTORGCODE"]]
                    })
                    
                    map.addLayer({
                        'id': `${district.name}-label`,
                        'type': 'symbol',
                        'source': 'districts',
                        'layout': {
                            'text-field': [
                                'format',
                                ['upcase', ['get', 'DISTRICTNAME']],
                                { 'font-scale': 0.8 },
                                '\n',
                                {},
                                ['downcase', ['get', 'DISTRICTNUMBER']],
                                { 'font-scale': 0.6 }
                            ],
                            'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                        }
                    });

                    map.setFilter(`${district.name}-label`, ['==', ['get', 'DISTRICTORGCODE'], district.id]);
                    
                }

                // Add zoom, rotation, and full-screen controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
                // map.addControl(new mapboxgl.FullscreenControl({container: document.querySelector('body')}));
                console.log('done with district map')
                
            });
        })
});


document.querySelector('#district-choice').addEventListener('input', (evt) => {
    const district = `?district=${evt.target.value}`
    fetch(`/district${district}`)
        .then((response) => response.json())
        .then((data) => {
            const trails = data['trails'];
            console.log(trails)

            // Reset Maps
            document.querySelector("#trail-map").innerHTML = ''
            document.querySelector("#trail-and-fire-map").innerHTML = ''

            // Reset Dropdowns
            document.querySelector('#trail-choice').innerHTML = ''

            // make sure trail info is hidden
            document.getElementById('trail-info').style.visibility = "hidden";

            // Update trails
            document.querySelector('#trail-choice').insertAdjacentHTML("beforeend", 
                '<option value="" disabled selected>Choose a Trail</option>')
            for (const trail of trails) {
                const name = `${trail['no']}: ${trail['name']}`
                const id = trail['id']
                const isEmpty = trail['isEmpty']
                if (isEmpty === true){
                document.querySelector('#trail-choice').insertAdjacentHTML("beforeend", 
                `<option value = '' disabled>${name}</option>`)} else {
                document.querySelector('#trail-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${id}'>${name}</option>`)}
            }

            // Create map
            const map = new mapboxgl.Map({
                container: 'trail-map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                center: data['startingLngLat'], // starting position [lng, lat] (geographic center of US, 39°50′N 98°35′W, according to https://en.wikipedia.org/wiki/Geographic_center_of_the_United_States)
                zoom: 8 // starting zoom
                });
            
            // resize map on render
            map.on('render', () => {
                map.resize();});

            // Load map
            map.on('load', () => {
                map.addSource(
                    'trails', {
                        'type': 'geojson',
                        'data': `/trails.geojson${district}`
                    });

                // add fill color to trails
                for (const trail of trails) {
                    console.log(trail.id)
                    const newColor = generateColor()
                    console.log(newColor)
                    map.addLayer({
                        'id': `${trail.name}-line`,
                        'type': 'line',
                        'source': 'trails',
                        'layout': {
                            'line-join': 'round',
                            'line-cap': 'round'
                        },
                        'paint': {
                            'line-color': newColor,
                            'line-width': 8
                        }
                    })
                    
                    map.setFilter(`${trail.name}-line`, ['==', ['get', 'TRAIL_CN'], trail.id]);

                    map.addLayer({
                        'id': `${trail.name}-label`,
                        'type': 'symbol',
                        'source': 'trails',
                        'layout': {
                            'text-field': [
                                'format',
                                ['upcase', ['get', 'TRAIL_NAME']],
                                { 'font-scale': 0.8 },
                                '\n',
                                {},
                                ['downcase', ['get', 'TRAIL_NO']],
                                { 'font-scale': 0.6 }
                            ],
                            'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                        }
                    });

                    map.setFilter(`${trail.name}-label`, ['==', ['get', 'TRAIL_CN'], trail.id]);


                    // map.setFilter(`${trail.name}-label`, ['==', ['get', 'TRAIL_CN'], trail.id]);
                    
                }

                // Add zoom, rotation, and full-screen controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
                // map.addControl(new mapboxgl.FullscreenControl({container: document.querySelector('body')}));
                console.log('done with trail map')
                
            });

        })
});

document.querySelector('#trail-choice').addEventListener('input', () => {
    const trail = `?trail=${document.getElementById('trail-choice').value}`
    const distance = `${document.getElementById('fire-distance').value}`
    fetch(`/trail${trail}&distance=${distance}`)
        .then((response) => response.json())
        .then((data) => {
            const fires = data.fires
            const trail_name = data.trail_name
            const trailhead = data.trailhead
            const aqi = data.aqi

            // Reset Map
            document.querySelector("#trail-and-fire-map").innerHTML = ''

            // reset fire & weather information
            document.querySelector('#fire-info').innerHTML = ""
            document.querySelector('#aqi-info').innerHTML = ""
            document.querySelector('#weather-today').innerHTML = ""
            document.querySelector('#forecast-info').innerHTML = ""
            document.querySelector('#historic-weather-info').innerHTML = ""

            // make sure trail info is visible
            document.getElementById('trail-info').style.visibility = "visible";
            
            // provide fire info outside of map
            if (fires.length === 0){
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<h6> There are currently no fires within 25 miles of ${trail_name}. </h6>`)
            } else if (fires.length === 1){
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<h6> There is currently one fire within 25 miles of ${trail_name}: </h6>
                    <h6><a href=${fires[0].url} target="popup" 
                    onclick="window.open('${fires[0].url}','popup','width=600,height=600'); return false;">${fires[0].name}</a></h6>
                    `)
            } else {
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<h6> There are currently ${fires.length} fires within 25 miles of ${trail_name}:</h6>
                    <ul>`)
                for (const fire of fires){
                    document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<li><a href=${fire.url} target="popup" 
                    onclick="window.open('${fire.url}','popup','width=600,height=600'); return false;">${fire.name}</a></li>`)
                }
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `</ul`)
            }

            // add AQI data
            document.querySelector('#aqi-info').insertAdjacentHTML("beforeend", 
                    `<p> The AQI at ${trail_name} is currently ${aqi} on a scale of 1 (good) to 5 (very poor).</p>`)


            // add today's weather
            const today = document.getElementById('trip-date').value
            fetch(`/weather${trail}&date=${today}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data)
                    if ('current' in data) {
                        console.log(data.current)
                        document.querySelector('#weather-today').insertAdjacentHTML("beforeend", 
                        `<p> Today, the weather will be: ${data.current.description}.</p>`)
                    } 
            });

            /* ---------- CREATE MAP ---------- */

            // create new map centering on beginning of trail
            const map = new mapboxgl.Map({
                container: 'trail-and-fire-map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                center: trailhead, // starting position [lng, lat]
                // there is a map.fitBounds() feature but I haven't figured out yet how to use it to set original map
                zoom: 10 // starting zoom
            });

            // resize map on render
            map.on('render', () => {
                map.resize();});
            
            /* ---------- CREATE POINT FEATURES ---------- */

            // Create list of features
            const geoJsonFeatures = []
            // Add fire features only if fires were found in range
            if (data.fires.length > 0){
                // loop through those fires
                for (const fire of data.fires){
                    // create one feature for each fire, changing description and coordinate with each
                    geoJsonFeatures.push(
                        {
                            'type': 'Feature',
                            'properties': {
                            'description': `<p>${fire.name}</p>`,
                            // 'iconSize': [30, 30],
                            'icon': 'fire-station' // maki icon stylized for this map
                            },
                            'geometry': {
                            'type': 'Point',
                            'coordinates': [`${fire.longitude}`, `${fire.latitude}`]
                            }
                        }
                    )
                }
            };
            // create a Trailhead feature at first long/lat trail point
            geoJsonFeatures.push(
                {
                    'type': 'Feature',
                    'properties': {
                    'description': `<p>Trailhead of ${trail_name}</p>`,
                    // 'iconSize': [30, 30],
                    'icon': 'parking' // maki icon stylized for this map
                    },
                    'geometry': {
                    'type': 'Point',
                    'coordinates': trailhead
                    }
                }
            )
            

            // include the above list of features when loading map
            map.on('load', () => {
                map.addSource('places', {
                    'type': 'geojson',
                    'data': {
                        'type': 'FeatureCollection',
                        'features': geoJsonFeatures
                    }
                });

                // Add a layer showing the places.
                map.addLayer({
                    'id': 'places',
                    'type': 'symbol',
                    'source': 'places',
                    'layout': {
                    'icon-image': ['get', 'icon'],
                    'icon-allow-overlap': true
                    }
                });

                // When a click event occurs on a feature in the places layer, open a popup at the
                // location of the feature, with description HTML from its properties.
                map.on('click', 'places', (e) => {
                    // Copy coordinates array.
                    const coordinates = e.features[0].geometry.coordinates.slice();
                    const description = e.features[0].properties.description;
                    
                    // Ensure that if the map is zoomed out such that multiple
                    // copies of the feature are visible, the popup appears
                    // over the copy being pointed to.
                    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                    coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                    }
                    
                    new mapboxgl.Popup()
                    .setLngLat(coordinates)
                    .setHTML(description)
                    .addTo(map);
                    });
                    
                // Change the cursor to a pointer when the mouse is over the places layer.
                map.on('mouseenter', 'places', () => {
                    map.getCanvas().style.cursor = 'pointer';
                    });
                
                // Change it back to a pointer when it leaves.
                map.on('mouseleave', 'places', () => {
                    map.getCanvas().style.cursor = '';
                    });

                // Add zoom, rotation, and full-screen controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
                // map.addControl(new mapboxgl.FullscreenControl({container: document.querySelector('body')}));
            });

            // /* ---------- CREATE TRAIL FEATURE ---------- */

            // // create connected line of all trailpoint coordinates
            // map.on('load', () => {
            //     console.log("OH HI I'M LOADING")
            //     // adding the coordinates for the line to use
            //     map.addSource('route', {
            //         'type': 'geojson',
            //         'data': `/trail.geojson${trail}`
            //     });
            //     // adding the line itself
            //     console.log(trail_name)
            //     const newColor = generateColor()
            //     console.log(newColor)
            //     map.addLayer({
            //         'id': 'trail-route',
            //         'type': 'line',
            //         'source': 'route',
            //         'layout': {
            //             'line-join': 'round',
            //             'line-cap': 'round'
            //         },
            //         'paint': {
            //             'line-color': newColor,
            //             'line-width': 10
            //         },
            //     });
                // console.log(map.getLayer('trail-route'))
                // });

      
        });
});




document.querySelector('#trip-date').addEventListener('input', (evt) => {
    const date = `${evt.target.value}`
    const trail = `${document.getElementById('trail-choice').value}`
    console.log(`date=${date}, trail=${trail}`)
    fetch(`/weather?date=${date}&trail=${trail}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)

            // reset forecast & historic weather information

            document.querySelector('#forecast-info').innerHTML = ""
            document.querySelector('#historic-weather-info').innerHTML = ""

            if ('current' in data) {
                console.log(data.current)
                document.querySelector('#forecast-info').insertAdjacentHTML("beforeend", 
                `<p> On ${date}, the weather will be: ${data.current.description}.</p>`)
            } 
            if ('historic' in data) {
                console.log(data.historic)
                if (data.historic.description.length == 2){
                    document.querySelector('#historic-weather-info').insertAdjacentHTML("beforeend", 
                    `<p> Over the last five years, the weather on ${date.slice(5,)} has been: ${data.historic.description[0]} and ${data.historic.description[1]}.</p`)
                } else if (data.historic.description.length == 3){
                    document.querySelector('#historic-weather-info').insertAdjacentHTML("beforeend", 
                    `<p> Over the last five years, the weather on ${date.slice(5,)} has been: ${data.historic.description[0]}, ${data.historic.description[1]}, and ${data.historic.description[2]}.</p`)
                } else {
                    document.querySelector('#historic-weather-info').insertAdjacentHTML("beforeend", 
                    `<p> Over the last five years, the weather on ${date.slice(5,)} has been: ${data.historic.description}.</p`)
                }
            }

        });
});

document.querySelector('#fire-distance').addEventListener('change', () => {
    const trail = `?trail=${document.getElementById('trail-choice').value}`
    const distance = `${document.getElementById('fire-distance').value}`
    fetch(`/trail${trail}&distance=${distance}`)
        .then((response) => response.json())
        .then((data) => {
            const fires = data.fires
            const trail_name = data.trail_name
            const trailhead = data.trailhead

            // reset fire information
            document.querySelector('#fire-info').innerHTML = ""

            // make sure trail info is visible
            document.getElementById('trail-info').style.visibility = "visible";
            
            // provide fire info outside of map
            if (fires.length === 0){
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<h6> There are currently no fires within ${distance} miles of ${trail_name}. </h6>`)
            } else if (fires.length === 1){
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<h6> There is currently one fire within ${distance} miles of ${trail_name}: </h6>
                    <h6><a href=${fires[0].url} target="popup" 
                    onclick="window.open('${fires[0].url}','popup','width=600,height=600'); return false;">${fires[0].name}</a></h6>
                    `)
            } else {
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<h6> There are currently ${fires.length} fires within ${distance} miles of ${trail_name}:</h6>
                    <ul>`)
                for (const fire of fires){
                    document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `<li><a href=${fire.url} target="popup" 
                    onclick="window.open('${fire.url}','popup','width=600,height=600'); return false;">${fire.name}</a></li>`)
                }
                document.querySelector('#fire-info').insertAdjacentHTML("beforeend", 
                    `</ul`)
            }

            // Reset Map
            document.querySelector("#trail-and-fire-map").innerHTML = ''


            /* ---------- CREATE MAP ---------- */

            // create new map centering on beginning of trail
            const map = new mapboxgl.Map({
                container: 'trail-and-fire-map', // container ID
                style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
                center: trailhead, // starting position [lng, lat]
                // there is a map.fitBounds() feature but I haven't figured out yet how to use it to set original map
                zoom: 10 // starting zoom
            });

            // resize map on render
            map.on('render', () => {
                map.resize();});
            
            /* ---------- CREATE POINT FEATURES ---------- */

            // Create list of features
            const geoJsonFeatures = []
            // Add fire features only if fires were found in range
            if (data.fires.length > 0){
                // loop through those fires
                for (const fire of data.fires){
                    // create one feature for each fire, changing description and coordinate with each
                    geoJsonFeatures.push(
                        {
                            'type': 'Feature',
                            'properties': {
                            'description': `<p>${fire.name}</p>`,
                            // 'iconSize': [30, 30],
                            'icon': 'fire-station' // maki icon stylized for this map
                            },
                            'geometry': {
                            'type': 'Point',
                            'coordinates': [`${fire.longitude}`, `${fire.latitude}`]
                            }
                        }
                    )
                }
            };
            // create a Trailhead feature at first long/lat trail point
            geoJsonFeatures.push(
                {
                    'type': 'Feature',
                    'properties': {
                    'description': `<p>Trailhead of ${trail_name}</p>`,
                    // 'iconSize': [30, 30],
                    'icon': 'parking' // maki icon stylized for this map
                    },
                    'geometry': {
                    'type': 'Point',
                    'coordinates': trailhead
                    }
                }
            )
            

            // include the above list of features when loading map
            map.on('load', () => {
                map.addSource('places', {
                    'type': 'geojson',
                    'data': {
                        'type': 'FeatureCollection',
                        'features': geoJsonFeatures
                    }
                });

                // Add a layer showing the places.
                map.addLayer({
                    'id': 'places',
                    'type': 'symbol',
                    'source': 'places',
                    'layout': {
                    'icon-image': ['get', 'icon'],
                    'icon-allow-overlap': true
                    }
                });

                // When a click event occurs on a feature in the places layer, open a popup at the
                // location of the feature, with description HTML from its properties.
                map.on('click', 'places', (e) => {
                    // Copy coordinates array.
                    const coordinates = e.features[0].geometry.coordinates.slice();
                    const description = e.features[0].properties.description;
                    
                    // Ensure that if the map is zoomed out such that multiple
                    // copies of the feature are visible, the popup appears
                    // over the copy being pointed to.
                    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                    coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                    }
                    
                    new mapboxgl.Popup()
                    .setLngLat(coordinates)
                    .setHTML(description)
                    .addTo(map);
                    });
                    
                // Change the cursor to a pointer when the mouse is over the places layer.
                map.on('mouseenter', 'places', () => {
                    map.getCanvas().style.cursor = 'pointer';
                    });
                
                // Change it back to a pointer when it leaves.
                map.on('mouseleave', 'places', () => {
                    map.getCanvas().style.cursor = '';
                    });

                // Add zoom, rotation, and full-screen controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
                // map.addControl(new mapboxgl.FullscreenControl({container: document.querySelector('body')}));
            });

            // /* ---------- CREATE TRAIL FEATURE ---------- */

            // // create connected line of all trailpoint coordinates
            // map.on('load', () => {
            //     console.log("OH HI I'M LOADING")
            //     // adding the coordinates for the line to use
            //     map.addSource('route', {
            //         'type': 'geojson',
            //         'data': `/trail.geojson${trail}`
            //     });
            //     // adding the line itself
            //     console.log(trail_name)
            //     const newColor = generateColor()
            //     console.log(newColor)
            //     map.addLayer({
            //         'id': 'trail-route',
            //         'type': 'line',
            //         'source': 'route',
            //         'layout': {
            //             'line-join': 'round',
            //             'line-cap': 'round'
            //         },
            //         'paint': {
            //             'line-color': newColor,
            //             'line-width': 10
            //         },
            //     });
                // console.log(map.getLayer('trail-route'))
                // });

      
        });
});

document.querySelector('img').addEventListener('click', () =>
    alert('This logo was generated by hotpot.ai.'))   