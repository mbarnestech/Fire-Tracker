// enforce better formatting
'use strict';


document.querySelector('#fire-form').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const newFormInputs = {
        miles: document.querySelector('#fire-distance').value,
    };

    fetch('/fire_check', {
        method: 'POST',
        body: JSON.stringify(newFormInputs),
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response)=>response.json())
      .then((data)=>{
        console.log(data);
        document.querySelector('#nearby-fires').innerHTML = '';
        document.querySelector('#nearby-fires').insertAdjacentHTML('afterbegin', `<h2>Testing</h2>`);
      });
  });
  
document.querySelector('#fire-form').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
        miles: document.querySelector('#fire-distance').value,
    };

    fetch('/fire_check', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response)=>response.json())
      .then((data)=>{
        console.log(data);
        document.querySelector('#nearby-fires').innerHTML = '';
        document.querySelector('#nearby-fires').insertAdjacentHTML('afterbegin', `<h2>Testing</h2>`);
      });
  });