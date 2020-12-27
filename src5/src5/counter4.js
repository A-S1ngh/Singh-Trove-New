let counter = 0;

document.addEventListener('DOMContentLoaded', function() {

});

function count(message) {
  console.log(message);
    counter++;

    if (counter % 10 === 0) {
        alert(`Count is now ${counter}`);
    }

    document.querySelector('h1').innerHTML = counter;
}
