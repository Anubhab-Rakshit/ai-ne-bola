// Initialize the Leaflet map globally (before form submission event)
const map = L.map("map", {
  center: [0, 0], // Default global center coordinates
  zoom: 2, // Default global zoom level
  minZoom: 3, // Minimum zoom level
  maxZoom: 10, // Maximum zoom level
  maxBounds: [
    // Restrict map panning to these bounds
    [-90, -180], // Southwest corner
    [90, 180], // Northeast corner
  ],
});

// Add OpenStreetMap tiles to the map globally
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Global variable to track the current marker (to update its position)
let currentMarker = null;

// Handle form submission for prediction
document
  .getElementById("predictForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page

    const lat = parseFloat(document.getElementById("lat").value);
    const long = parseFloat(document.getElementById("long").value);

    // Fetch prediction data from the server
    const response = await fetch(`/predict?lat=${lat}&long=${long}`);
    const data = await response.json();

    // Display prediction results
    const resultDiv = document.getElementById("predictionResult");
    resultDiv.innerHTML = `
      <h3>Prediction Result</h3>
      <p><strong>Predicted Deaths:</strong> ${data.Predicted_Deaths}</p>
      <p><strong>Predicted Fatality Ratio:</strong> ${data.Predicted_Fatality_Ratio}</p>
      <p><strong>Live Temperature:</strong> ${data.Temperature}°C</p>
      <p><strong>Live Humidity:</strong> ${data.Humidity}%</p>
    `;

    // Show the map section
    const mapSection = document.getElementById("mapSection");
    mapSection.style.display = "block";

    // Update map view with the new latitude and longitude
    map.setView([lat, long], 6); // Zoom to the new coordinates

    // If there's an existing marker, move it to the new position
    if (currentMarker) {
      currentMarker.setLatLng([lat, long]);
    } else {
      // If there's no existing marker, create a new one at the updated coordinates
      currentMarker = L.marker([lat, long]).addTo(map);
    }

    // Determine marker color based on predicted deaths
    let markerColor = "green"; // Default to green
    if (data.Predicted_Deaths > 100) {
      markerColor = "red";
    } else if (data.Predicted_Deaths > 50) {
      markerColor = "orange";
    } else if (data.Predicted_Deaths > 10) {
      markerColor = "yellow";
    }

    // Add a circle marker to indicate the prediction result
    const circleMarker = L.circle([lat, long], {
      color: markerColor,
      fillColor: markerColor,
      fillOpacity: 0.5,
      radius: 5000, // Radius in meters
    }).addTo(map);

    // Bind a popup to the circle marker with prediction details
    circleMarker
      .bindPopup(
        `
        <b>Location</b><br>
        Latitude: ${lat}<br>
        Longitude: ${long}<br><br>
        <b>Prediction Result</b><br>
        Predicted Deaths: ${data.Predicted_Deaths}<br>
        Fatality Ratio: ${data.Predicted_Fatality_Ratio}
      `
      )
      .openPopup();
  });

// Generate a random Ebola prevention tip
function generatePreventionTip() {
  const tips = [
    "Avoid direct contact with infected individuals and their body fluids.",
    "Wash hands frequently with soap and water.",
    "Wear protective gear if caring for someone who is infected.",
    "Do not handle or eat bushmeat (wild animals).",
    "Avoid areas with known Ebola outbreaks.",
    "Seek medical attention immediately if you experience symptoms.",
    "Follow public health guidelines and updates from authorities.",
  ];

  const randomTip = tips[Math.floor(Math.random() * tips.length)];
  document.getElementById("preventionTip").innerText = randomTip;
}
