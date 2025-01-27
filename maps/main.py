from flask import Flask, render_template, jsonify
import pandas as pd
import folium
import os

# Initialize Flask app
app = Flask(__name__)

# Route to serve the map
@app.route("/")

def serve_map():
    # Load the Excel file
    data_path = os.path.join("data", "cases_data.xlsx")
    df = pd.read_excel(data_path)
    df_cleaned = df.dropna(subset=['Lat', 'Long_'])
    # Create a Folium map
    m = folium.Map(location=[20, 0], zoom_start=3, min_zoom=2, max_bounds=True , maxBounds= [[-80, -179],[90, 192]],maxBoundsViscosity= 1.0)

    # Function to determine marker color based on deaths
    def get_color(deaths):
        if deaths > 100:
            return "#FF4500"  # Red
        elif deaths > 50:
            return "#FF6347"  # Light Red
        elif deaths > 25:
            return "#FFA500"  # Orange
        elif deaths > 10:
            return "#FFD700"  # Yellow
        elif deaths > 0:
            return "#ADFF2F"  # Light Green
        else:
            return "#32CD32"  # Green

    # Add circle markers to the map
    for _, row in df_cleaned.iterrows():
        latitude = row.get("Lat", 0)
        longitude = row.get("Long_", 0)
        deaths = row.get("Deaths", 0)
        fatality_ratio = row.get("Case_Fatality_Ratio", "N/A")
        fatality_ratio = fatality_ratio if not pd.isna(fatality_ratio) else "N/A"
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=5,
            color=get_color(deaths),
            fill=True,
            fill_color=get_color(deaths),
            fill_opacity=0.7,
            tooltip=(
                f"<strong>Deaths:</strong> {deaths}<br>"
                f"<strong>Fatality Ratio:</strong> {fatality_ratio}"
            ),
        ).add_to(m)

    # Add a legend to the map
    legend_html = """
     <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 200px; height: 200px; 
                 background-color: white; z-index:9999; font-size:14px;
                 border:2px solid grey; padding: 10px;">
     <b>Deaths</b><br>
     <i style="background:#32CD32; width:20px; height:20px; display:inline-block;"></i> 0<br>
     <i style="background:#ADFF2F; width:20px; height:20px; display:inline-block;"></i> 1–10<br>
     <i style="background:#FFD700; width:20px; height:20px; display:inline-block;"></i> 11–25<br>
     <i style="background:#FFA500; width:20px; height:20px; display:inline-block;"></i> 26–50<br>
     <i style="background:#FF6347; width:20px; height:20px; display:inline-block;"></i> 51–100<br>
     <i style="background:#FF4500; width:20px; height:20px; display:inline-block;"></i> 101+<br>
     </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save the map as an HTML file
    map_path = os.path.join("templates", "index.html")
    m.save(map_path)
    if not os.path.exists(map_path):
        # Save the map as an HTML file if it doesn't exist
        m.save(map_path)

    return render_template("index.html")


# API endpoint to fetch case data (optional, for debugging or additional features)
@app.route("/cases", methods=["GET"])
def get_cases():
    try:
        data_path = os.path.join("data", "cases_data.xlsx")
        if not os.path.exists(data_path):
            return f"File not found at: {os.path.abspath(data_path)}"
        df = pd.read_excel(data_path)
        df_cleaned = df.dropna(subset=['Lat', 'Long_'])
        cleaned_data = df_cleaned[['Lat', 'Long_', 'Deaths', 'Case_Fatality_Ratio']].to_dict(orient='records')
        return jsonify(cleaned_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process the data."}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
