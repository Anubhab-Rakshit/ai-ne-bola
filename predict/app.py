from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model_filename = os.path.join(os.getcwd(),'ebolahackathon\knn_model.pkl')

try:
    with open(model_filename, 'rb') as f:
        knn_model = pickle.load(f)
    print(f"Model loaded successfully from {model_filename}")
except Exception as e:
    print(f"Error loading model: {e}")

# Define the home route to display the form
@app.route('/')
def home():
    return render_template('index.html')

# Define the prediction route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the latitude and longitude from the form
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])

        # Predict the death rate using the model
        prediction = knn_model.predict(np.array([[longitude, latitude]]))

        # Return the prediction as part of the rendered template
        return render_template('index.html', death_rate=prediction[0], longitude=longitude, latitude=latitude)

    except Exception as e:
        return render_template('index.html', error=str(e))

# Define the main entry point to run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
