function fetchData(){
      fetch('/testData')
        .then((response)=>response.json())
        .then((data)=>{
            mapboxgl.accessToken = `${data.mapKey}`;
            const map = new mapboxgl.Map({
            container: 'map', // container ID
            // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
            style: 'mapbox://styles/mapbox/streets-v12', // style URL
            center: [`${data.thLng}`, `${data.thLat}`], // starting position [lng, lat]
            zoom: 9 // starting zoom
            });
        });
    }

fetchData()
