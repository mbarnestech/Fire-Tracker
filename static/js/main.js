// enforce better formatting
'use strict';

document.addEventListener("DOMContentLoaded", () => {
    fetch("/initialize")
        .then((response) => response.json())
        .then((data) => {
            const trails = data['trails'];
            const regions = data['regions'];
            const regionCoords = data['regionCoords']
            const forests = data['forests'];
            const districts = data['districts'];
            mapboxgl.accessToken = `${data.mapKey}`;

            // Populate region choices
            for (const region of regions) {
                document.querySelector('#region-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${region['name']}'>${region['name']}</option>`)
            }

            // Populate forest choices
            for (const forest of forests) {
                const name = forest['name']
                const isEmpty = forest['isEmpty']
                if (isEmpty === true){
                document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}' disabled>${name}</option>`)} else {
                document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}'>${name}</option>`)}
            }

            // Populate district choices
            for (const district of districts) {
                const name = district['name']
                const isEmpty = district['isEmpty']
                if (isEmpty === true){
                document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}' disabled>${name}</option>`)} else {
                document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}'>${name}</option>`)}
            }
            // Populate trail choices
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
                console.log(map.getSource('regions'))

                map.addLayer({
                    'id': 'regions-layer',
                    'type': 'fill',
                    'source': 'regions',
                    // 'source-layer': 'Forest_Service_Regional_Boundaries__Feature_Layer_',
                    'paint': {
                        'fill-color': 'rgba(255, 0, 0, 0.4)'
                    }
                });
                console.log(map.getLayer('regions-layer'))

                map.addLayer({
                    'id': 'region-borders',
                    'type': 'line',
                    'source': 'regions',
                    'layout': {},
                    'paint': {
                    'line-color': '#627BC1',
                    'line-width': 2
                    }
                });

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
                console.log(map.getLayer('region-borders'))
                
                
                // Add zoom and rotation controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
            });
            console.log('donezo.')
        })
  });


//   both 'input' and 'change' events seem to listen equally well for selection
document.querySelector('#region-choice').addEventListener('input', (evt) => {
const region = `?region=${evt.target.value}`
fetch(`/region${region}`)
    .then((response) => response.json())
    .then((data) => {
        const trails = data['trails'];
        const forests = data['forests'];
        const districts = data['districts'];

        // Update Forests
        document.querySelector('#forest-choice').innerHTML = ''
        document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
            '<option value="" disabled selected>Choose a National Forest</option>')
        for (const forest of forests) {
            const name = forest['name']
            const isEmpty = forest['isEmpty']
            if (isEmpty === true){
            document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
            `<option value = '${name}' disabled>${name}</option>`)} else {
            document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
            `<option value = '${name}'>${name}</option>`)}
        }
        
        // Update Districts
        document.querySelector('#district-choice').innerHTML = ''
        document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
            '<option value="" disabled selected>Choose a Ranger District</option>')
        for (const district of districts) {
            const name = district['name']
            const isEmpty = district['isEmpty']
            if (isEmpty === true){
            document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
            `<option value = '${name}' disabled>${name}</option>`)} else {
            document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
            `<option value = '${name}'>${name}</option>`)}
        }

        // Update trails
        document.querySelector('#trail-choice').innerHTML = ''
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

    })
});


document.querySelector('#forest-choice').addEventListener('input', (evt) => {
const forest = `?forest=${evt.target.value}`
fetch(`/forest${forest}`)
    .then((response) => response.json())
    .then((data) => {
        const trails = data['trails'];
        const districts = data['districts'];

        // Update Districts
        document.querySelector('#district-choice').innerHTML = ''
        document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
            '<option value="" disabled selected>Choose a Ranger District</option>')
        for (const district of districts) {
            const name = district['name']
            const isEmpty = district['isEmpty']
            if (isEmpty === true){
            document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
            `<option value = '${name}' disabled>${name}</option>`)} else {
            document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
            `<option value = '${name}'>${name}</option>`)}
        }

        // Update trails
        document.querySelector('#trail-choice').innerHTML = ''
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
    })
});


document.querySelector('#district-choice').addEventListener('input', (evt) => {
const district = `?district=${evt.target.value}`
fetch(`/district${district}`)
    .then((response) => response.json())
    .then((data) => {
        const trails = data['trails'];

        // Update trails
        document.querySelector('#trail-choice').innerHTML = ''
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

    })
});

// {% if fires %}
//     <h1> Fires within {{ miles }} of {{ trail_name }}:</h1> 
//     <ul>{% for fire in fires %}
//         <li>{{ fire.fire_name }}</li>
//         <li><a href='{{ fire.fire_url }}'/> Link to inciweb information on {{ fire.fire_name }}</a></li>
//         {% endfor %}
//     </ul>
//     {% else %}
//         <p>There are no fires within {{ miles }} of {{ trail_name }}.</p>
//     {% endif %}