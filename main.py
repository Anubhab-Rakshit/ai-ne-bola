import pandas as pd
import os
import random
import requests
from geopy.distance import distance
import math
import time

# Paths to the Excel files
train_data_path = os.path.join(os.getcwd(), "train_data.xlsx")
test_points_path = os.path.join(os.getcwd(), "test_points.xlsx")
output_file_path = os.path.join(os.getcwd(), "predicted_test_data.xlsx")

# OpenWeatherMap API URL and your API key
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "fb3aed4001a57af1314ce70cfd3fcfc4"  # Replace with your actual API key

def find_precise_nearby_with_variation(rows, target_lat, target_long, field):
    nearby_values = []
    
    for _, row in rows.iterrows():
        if pd.notnull(row['Lat']) and pd.notnull(row['Long_']) and pd.notnull(row[field]):
            dist = distance((target_lat, target_long), (row['Lat'], row['Long_'])).meters
            if dist < 10000000:  # Consider points within 100km
                nearby_values.append(row[field])
    
    if not nearby_values:
        return None
    
    average_value = sum(nearby_values) / len(nearby_values)
    variation = random.uniform(-0.00005, 0.00005)
    
    return average_value + variation

def adjust_predictions_by_weather(predicted_deaths, temperature, humidity):
    if temperature is None or humidity is None:
        return predicted_deaths

    if temperature > 30:
        predicted_deaths *= 1.2  # Increase by 20% if temperature > 30°C
    elif temperature < 20:
        predicted_deaths *= 0.8  # Decrease by 20% if temperature < 20°C

    if humidity > 70:
        predicted_deaths *= 1.15  # Increase by 15% if humidity > 70%
    elif humidity < 40:
        predicted_deaths *= 0.85  # Decrease by 15% if humidity < 40%

    return round(predicted_deaths, 5)

def calculate_total_cases(deaths, cfr):
    if cfr == 0 or cfr is None:
        return None
    return deaths / (cfr / 100)

def get_weather_data(lat, long):
    try:
        url = f"{WEATHER_API_URL}?lat={lat}&lon={long}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)  # Timeout of 10 seconds for the request
        data = response.json()

        # Extract temperature and humidity from the response
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        return {
            "temperature": temperature,
            "humidity": humidity
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"temperature": None, "humidity": None}

def is_valid_coordinate(lat, long):
    """Check if coordinates are valid (i.e., not NaN and finite)."""
    return not (math.isnan(lat) or math.isnan(long) or lat == 0.0 or long == 0.0)

def predict_and_save():
    # Load the data
    train_data = pd.read_excel(train_data_path)
    test_data = pd.read_excel(test_points_path)

    # Filter out invalid rows with NaN or invalid lat/long
    train_data = train_data[train_data.apply(lambda row: is_valid_coordinate(row['Lat'], row['Long_']), axis=1)]
    test_data = test_data[test_data.apply(lambda row: is_valid_coordinate(row['Lat'], row['Long_']), axis=1)]

    death_predictions = []
    cfr_predictions = []
    total_cases_predictions = []
    temperatures = []
    humidities = []

    # Track progress
    total_points = len(test_data)
    print(f"Starting predictions for {total_points} test points...")

    for idx, row in test_data.iterrows():
        target_lat = row["Lat"]
        target_long = row["Long_"]

        # Find prediction for deaths and fatality ratio
        predicted_deaths = None
        predicted_fatality_ratio = None
        
        exact_match = train_data[(train_data['Lat'].round(4) == round(target_lat, 4)) & 
                                 (train_data['Long_'].round(4) == round(target_long, 4))]
        
        if not exact_match.empty:
            predicted_deaths = exact_match.iloc[0]['Deaths'] if 'Deaths' in exact_match.columns else 0
            predicted_fatality_ratio = exact_match.iloc[0]['Case_Fatality_Ratio'] if 'Case_Fatality_Ratio' in exact_match.columns else 0
        else:
            predicted_deaths = find_precise_nearby_with_variation(train_data, target_lat, target_long, "Deaths")
            predicted_fatality_ratio = find_precise_nearby_with_variation(train_data, target_lat, target_long, "Case_Fatality_Ratio")
        
        # Get weather data for the location
        weather_data = get_weather_data(target_lat, target_long)
        temperature = weather_data["temperature"]
        humidity = weather_data["humidity"]
        
        # Adjust death predictions based on weather
        if predicted_deaths is not None:
            predicted_deaths = adjust_predictions_by_weather(predicted_deaths, temperature, humidity)
        
        # Calculate total cases
        total_cases = calculate_total_cases(predicted_deaths, predicted_fatality_ratio)

        # Append all data to lists
        death_predictions.append(predicted_deaths if predicted_deaths is not None else "No nearby data")
        cfr_predictions.append(round(predicted_fatality_ratio, 5) if predicted_fatality_ratio is not None else "No nearby data")
        total_cases_predictions.append(round(total_cases, 2) if total_cases is not None else "No nearby data")
        temperatures.append(f"{temperature:.2f}°C" if temperature is not None else "Unavailable")
        humidities.append(f"{humidity:.2f}%" if humidity is not None else "Unavailable")

        # Print progress for each test point
        if (idx + 1) % 10 == 0:  # Print progress every 10 rows
            print(f"Processed {idx + 1}/{total_points} test points...")

    # Add predictions and weather data to the test data
    test_data["Predicted_Deaths"] = death_predictions
    test_data["Predicted_Case_Fatality_Ratio"] = cfr_predictions
    test_data["Predicted_Total_Cases"] = total_cases_predictions
    test_data["Temperature"] = temperatures
    test_data["Humidity"] = humidities

    # Save the updated test data to a new Excel file
    test_data.to_excel(output_file_path, index=False)
    print(f"Predictions saved to {output_file_path}")

if __name__ == "__main__":
    start_time = time.time()
    predict_and_save()
    end_time = time.time()
    print(f"Script finished in {end_time - start_time:.2f} seconds.")
