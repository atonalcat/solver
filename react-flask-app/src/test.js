console.log("hello")
fetch("http://127.0.0.1:5000/time").then(pepe => pepe.json()).then(data => console.log(data.time))
const request = new XMLHttpRequest();

request.addEventListener('readystatechange', () => {
    if(request.readyState === 4){
        console.log(request.responseText);
    }
});

request.open('GET', 'https://jsonplaceholder.typicode.com/todos/');
request.send();