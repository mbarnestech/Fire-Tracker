// enforce better formatting
'use strict';

document.addEventListener("DOMContentLoaded", () => {
    fetch("/initialize")
        .then((response) => response.json())
        .then((data) => {
            const trails = data['trails'];
            const regions = data['regions'];
            const forests = data['forests'];
            const districts = data['districts'];

            for (const region of regions) {
                document.querySelector('#region-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${region['name']}'>${region['name']}</option>`)
            }
            for (const forest of forests) {
                const name = forest['name']
                const isEmpty = forest['isEmpty']
                if (isEmpty === true){
                document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}' disabled>${name}</option>`)} else {
                document.querySelector('#forest-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}'>${name}</option>`)}
            }
            for (const district of districts) {
                const name = district['name']
                const isEmpty = district['isEmpty']
                if (isEmpty === true){
                document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}' disabled>${name}</option>`)} else {
                document.querySelector('#district-choice').insertAdjacentHTML("beforeend", 
                `<option value = '${name}'>${name}</option>`)}
            }
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

