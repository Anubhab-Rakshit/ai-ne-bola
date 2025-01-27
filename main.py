from flask import Flask, request, jsonify
import pandas as pd
import geopy.distance
import os
import random
import requests

app = Flask(__name__)
PORT = 3000


WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "fb3aed4001a57af1314ce70cfd3fcfc4"  

# Path to the uploaded Excel file
excel_file_path = os.path.join(os.getcwd(),r"predictioner1\backend\uploads\train_data.xlsx")

def find_precise_nearby_with_variation(rows, target_lat, target_long, field):
    nearby_values = []
    
    for _, row in rows.iterrows():
        if pd.notnull(row['Lat']) and pd.notnull(row['Long_']) and pd.notnull(row[field]):
            distance = geopy.distance.distance((target_lat, target_long), (row['Lat'], row['Long_'])).meters
            if distance < 100000:  # Consider points within 100km
                nearby_values.append(row[field])
    
    if not nearby_values:
        return None
    
    average_value = sum(nearby_values) / len(nearby_values)
    variation = random.uniform(-0.00005, 0.00005)
    
    return average_value + variation

def get_weather_data(lat, long):
    try:
        url = f"{WEATHER_API_URL}?lat={lat}&lon={long}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"]
        }
    except Exception as e:
        print("Error fetching weather data:", str(e))
        return {"temperature": None, "humidity": None}

def adjust_predictions_by_weather(predicted_deaths, temperature, humidity):
    if temperature is None or humidity is None:
        return predicted_deaths

    if temperature > 30:
        predicted_deaths *= 1.2  
    elif temperature < 20:
        predicted_deaths *= 0.8  

    if humidity > 70:
        predicted_deaths *= 1.15  
    elif humidity < 40:
        predicted_deaths *= 0.85  

    return round(predicted_deaths, 5)

@app.route("/predict", methods=["GET"])
def predict():
    lat = request.args.get("lat")
    long = request.args.get("long")

    if not lat or not long:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    target_lat = float(lat)
    target_long = float(long)

    df = pd.read_excel(excel_file_path)

    predicted_deaths = None
    predicted_fatality_ratio = None

    exact_match = df[(df['Lat'].round(4) == round(target_lat, 4)) & (df['Long_'].round(4) == round(target_long, 4))]
    
    if not exact_match.empty:
        predicted_deaths = exact_match.iloc[0]['Deaths'] if 'Deaths' in exact_match.columns else 0
        predicted_fatality_ratio = exact_match.iloc[0]['Case_Fatality_Ratio'] if 'Case_Fatality_Ratio' in exact_match.columns else 0
    else:
        predicted_deaths = find_precise_nearby_with_variation(df, target_lat, target_long, "Deaths")
        predicted_fatality_ratio = find_precise_nearby_with_variation(df, target_lat, target_long, "Case_Fatality_Ratio")
    
    weather_data = get_weather_data(target_lat, target_long)
    temperature = weather_data["temperature"]
    humidity = weather_data["humidity"]
    
    
    if predicted_deaths is not None:
        predicted_deaths = adjust_predictions_by_weather(predicted_deaths, temperature, humidity)
        print(f"Adjusted Predicted Deaths: {predicted_deaths}")
    
    response = {
        "Predicted_Deaths": predicted_deaths if predicted_deaths is not None else "No nearby data",
        "Predicted_Fatality_Ratio": round(predicted_fatality_ratio, 5) if predicted_fatality_ratio is not None else "No nearby data",
        "Temperature": f"{temperature} degree C" if temperature is not None else "Unavailable",
        "Humidity": f"{humidity}%" if humidity is not None else "Unavailable",
    }

    if predicted_deaths is None and predicted_fatality_ratio is None:
        response["message"] = "No nearby data points to make predictions."
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
