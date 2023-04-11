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
            zoom: 9 // starting zoom
            });
            
            // Fire marker test
            if (data.fires.length > 0){
                const marker1 = new mapboxgl.Marker()
                    .setLngLat([`${data.fires[0][1]}`, `${data.fires[0][2]}`])
                    .addTo(map)};

            // create list of coordinates the map can use
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
