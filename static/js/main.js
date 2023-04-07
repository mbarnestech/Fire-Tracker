// enforce better formatting
'use strict';

document.querySelector('#trail-form').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
        trailChoice: document.querySelector('#trail-choice').value,
        miles: document.querySelector('#fire-distance').value,
    };

    fetch('/choose_trail', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response)=>response.json())
      .then((data)=>{
        console.log(data);
//         document.querySelector('nearby-fires').insertAdjacentHTML('afterbegin',
//         `<h1> Fires near {{ session['trail_name'] }}:</h1> 
// ${if }

// <ul>{% for fire in fires %}
//     <li>{{ fire.fire_name }}</li>
//     <li><a href='{{ fire.fire_url }}'/> Link to inciweb information on {{ fire.fire_name }}</a></li>
//     {% endfor %}
// </ul>
// {% else %}
// <p>There are no fires near {{ session['trail_name']}}.</p>
// {% endif %}`)
      });
  });