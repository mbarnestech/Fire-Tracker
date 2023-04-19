// enforce better formatting
'use strict';

document.addEventListener("DOMContentLoaded", () => {
    fetch("/initialize")
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            console.log(data['trails'][0])
            console.log(data['regions'][0])
            console.log(data['forests'][0])
            console.log(data['districts'][0])
        })
  });