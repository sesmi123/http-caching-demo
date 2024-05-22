const baseUrl = "http://localhost:5000";

function fetchData(endpoint, headers={}) {
  fetch(baseUrl + endpoint, { headers: headers })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").textContent = JSON.stringify(
        data,
        null,
        2
      );
    })
    .catch((error) => console.error("Error:", error));
}

function fetchData_custom(endpoint, caching = "no-cache") {
  fetch(baseUrl + endpoint, { cache: caching })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").textContent = JSON.stringify(
        data,
        null,
        2
      );
    })
    .catch((error) => console.error("Error:", error));
}
