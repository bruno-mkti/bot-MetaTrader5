fetch("http://localhost:5000/price/EURUSD")
  .then(response => response.json())
  .then(data => console.log(data));
