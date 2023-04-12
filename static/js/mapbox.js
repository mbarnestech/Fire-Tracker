function createMap(){
      fetch('/testData')
        .then((response)=>response.json())
        .then((data)=>{
            mapboxgl.accessToken = `${data.mapKey}`;
            // create new map centering on beginning of trail
            const map = new mapboxgl.Map({
            container: 'map', // container ID
            style: 'mapbox://styles/mapbox/outdoors-v12', // style URL
            center: [`${data.lngLatList[0][0]}`, `${data.lngLatList[0][1]}`], // starting position [lng, lat]
            // there is a map.fitBounds() feature but I haven't figured out yet how to use it to set original map
            zoom: 9 // starting zoom
            });
            
            // Create fire features
            geoJsonFeatures = []
            if (data.fires.length > 0){
                for (const fire of data.fires){
                    geoJsonFeatures.push(
                        {
                            'type': 'Feature',
                            'properties': {
                            'description': `<p>${fire[1]}</p>`,
                            // 'iconSize': [30, 30],
                            'icon': 'fire-station'
                            },
                            'geometry': {
                            'type': 'Point',
                            'coordinates': [`${fire[2]}`, `${fire[3]}`]
                            }
                        }
                    )
                }
            };
            geoJsonFeatures.push(
                {
                    'type': 'Feature',
                    'properties': {
                    'description': `<p>Trailhead</p>`,
                    // 'iconSize': [30, 30],
                    'icon': 'parking'
                    },
                    'geometry': {
                    'type': 'Point',
                    'coordinates': [`${data.lngLatList[0][0]}`, `${data.lngLatList[0][1]}`]
                    }
                }
            )

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
            });


            // create list of trail coordinates the map can use
            const coords = []
            for (const coord of data.lngLatList){
                coords.push(coord)
            }
            
            // create connected line of all trailpoint coordinates
            map.on('load', () => {
                map.addSource('route', {
                'type': 'geojson',
                'data': {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                'type': 'LineString',
                'coordinates': coords
                }
                }
                });
                map.addLayer({
                'id': 'route',
                'type': 'line',
                'source': 'route',
                'layout': {
                'line-join': 'round',
                'line-cap': 'round'
                },
                'paint': {
                'line-color': '#F00',
                'line-width': 1
                }
                });
                });
        
        });
}

createMap();
