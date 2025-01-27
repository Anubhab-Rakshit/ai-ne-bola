const express = require("express");
const xlsx = require("xlsx");
const geolib = require("geolib");
const path = require("path");
const axios = require("axios");

const app = express();
const PORT = 3000;

// OpenWeatherMap API URL and your API key
const WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather";
const API_KEY = "fb3aed4001a57af1314ce70cfd3fcfc4"; // Replace with your API key

// Middleware for serving static files
app.use(express.static(path.join(__dirname, "public")));

// Path to the uploaded Excel file
const excelFilePath = path.join(__dirname, "uploads", "train_data.xlsx");

// Helper function to find nearby values and adjust prediction
const findPreciseNearbyWithVariation = (rows, targetLat, targetLong, field) => {
  const nearbyValues = rows
    .filter((row) => row.Lat && row.Long_ && row[field] !== undefined)
    .map((row) => ({
      distance: geolib.getDistance(
        { latitude: targetLat, longitude: targetLong },
        { latitude: row.Lat, longitude: row.Long_ }
      ),
      value: row[field],
    }))
    .filter(({ distance }) => distance < 100000) // Consider points within 100km
    .map(({ value }) => value);

  if (nearbyValues.length === 0) return null;

  // Calculate precise average
  const averageValue =
    nearbyValues.reduce((sum, val) => sum + val, 0) / nearbyValues.length;

  // Add small variation
  const variation = Math.random() * 0.0001 - 0.00005;

  return averageValue + variation;
};

// Function to fetch weather data (temperature and humidity)
const getWeatherData = async (lat, long) => {
  try {
    const url = `${WEATHER_API_URL}?lat=${lat}&lon=${long}&appid=${API_KEY}&units=metric`;
    const response = await axios.get(url);
    return {
      temperature: response.data.main.temp,
      humidity: response.data.main.humidity,
    };
  } catch (error) {
    console.error(
      "Error fetching weather data:",
      error.response ? error.response.data : error.message
    );
    return { temperature: null, humidity: null }; // Return nulls if the API call fails
  }
};

// Adjust predictions based on temperature and humidity
const adjustPredictionsByWeather = (predictedDeaths, temperature, humidity) => {
  if (temperature === null || humidity === null) return predictedDeaths;

  // Adjust based on temperature
  if (temperature > 30) {
    predictedDeaths *= 1.2; // Increase by 20% if temperature > 30°C
  } else if (temperature < 20) {
    predictedDeaths *= 0.8; // Decrease by 20% if temperature < 20°C
  }

  // Adjust based on humidity
  if (humidity > 70) {
    predictedDeaths *= 1.15; // Increase by 15% if humidity > 70%
  } else if (humidity < 40) {
    predictedDeaths *= 0.85; // Decrease by 15% if humidity < 40%
  }

  return predictedDeaths.toPrecision(14);
};

// Endpoint to predict deaths and fatality ratio
app.get("/predict", async (req, res) => {
  const { lat, long } = req.query;

  if (!lat || !long) {
    return res
      .status(400)
      .json({ error: "Latitude and Longitude are required" });
  }

  const targetLat = parseFloat(lat);
  const targetLong = parseFloat(long);

  // Read the Excel file
  const workbook = xlsx.readFile(excelFilePath);
  const sheet = workbook.Sheets[workbook.SheetNames[0]];
  const data = xlsx.utils.sheet_to_json(sheet);

  let predictedDeaths, predictedFatalityRatio;

  // Check for an exact match
  const exactMatch = data.find(
    (row) =>
      parseFloat(row.Lat).toFixed(4) === targetLat.toFixed(4) &&
      parseFloat(row.Long_).toFixed(4) === targetLong.toFixed(4)
  );

  if (exactMatch) {
    predictedDeaths = exactMatch.Deaths || 0;
    predictedFatalityRatio = exactMatch.Case_Fatality_Ratio || 0;
  } else {
    // Predict based on nearby values
    predictedDeaths = findPreciseNearbyWithVariation(
      data,
      targetLat,
      targetLong,
      "Deaths"
    );
    predictedFatalityRatio = findPreciseNearbyWithVariation(
      data,
      targetLat,
      targetLong,
      "Case_Fatality_Ratio"
    );
  }

  // Fetch weather data (temperature and humidity)
  const { temperature, humidity } = await getWeatherData(targetLat, targetLong);
  console.log(`Temperature: ${temperature}°C, Humidity: ${humidity}%`);

  // Adjust predicted deaths based on weather (temperature and humidity)
  if (predictedDeaths !== null) {
    predictedDeaths = adjustPredictionsByWeather(
      predictedDeaths,
      temperature,
      humidity
    );
    console.log(`Adjusted Predicted Deaths: ${predictedDeaths}`);
  }

  // Prepare the response
  const response = {
    Predicted_Deaths:
      predictedDeaths !== null ? predictedDeaths : "No nearby data",
    Predicted_Fatality_Ratio:
      predictedFatalityRatio !== null
        ? predictedFatalityRatio.toPrecision(14)
        : "No nearby data",
    Temperature: temperature !== null ? `${temperature}°C` : "Unavailable",
    Humidity: humidity !== null ? `${humidity}%` : "Unavailable", // Send humidity data
    Location: { lat: targetLat, long: targetLong }, // Sending the location to map
  };

  if (predictedDeaths === null && predictedFatalityRatio === null) {
    response.message = "No nearby data points to make predictions.";
  }

  res.json(response);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
