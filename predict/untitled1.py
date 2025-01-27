import pandas as pd
import numpy as np
import joblib
from matplotlib import pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error,mean_absolute_error
import pickle
import matplotlib 
import os

matplotlib.rcParams["figure.figsize"] = (20,10)

data_path=os.path.join(os.getcwd(),r"ebolahackathon\train_data.xlsx")
data = pd.read_excel(data_path)
data = data.dropna()

from scipy.spatial.distance import cdist

# Function for Inverse Distance Weighting (IDW)
def idw_predict(random_coords, data, power=2):
    # Calculate the Euclidean distance between the random coordinates and all points in the dataset
    distances = cdist(random_coords, data[['Lat', 'Long_']])
    
    # Avoid division by zero by setting a minimum distance threshold
    distances = np.maximum(distances, 1e-5)
    
    # Compute the weights (1 / distance^power)
    weights = 1 / distances**power
    
    # Calculate the weighted sum of the death rates
    weighted_sum = np.sum(weights * data['Deaths'].values)
    weight_sum = np.sum(weights)
    
    # Return the predicted death rate
    return weighted_sum / weight_sum

# Predict death rate for a random coordinate using IDW
random_coords = np.array([[42.5063,1.5218]])  # Example random coordinates
predicted_death_rate = idw_predict(random_coords, data)

# Display the predicted death rate
print(f"Predicted Death Rate for random coordinates {random_coords[0]} using IDW: {predicted_death_rate}")



# Load dataset and drop missing values

# Feature columns (latitude, longitude) and target column (death rate)
X = data[['Lat', 'Long_']]  # Features: Latitude and Longitude
y = data['Case_Fatality_Ratio']  # Target: Case Fatality Ratio (death rate)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Predict the death rate for the test set
y_pred = rf_model.predict(X_test)

# Calculate accuracy metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Print accuracy results
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Root Mean Squared Error (RMSE): {rmse}")


import matplotlib.pyplot as plt

# Plotting actual vs predicted death rates
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Predicted')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Actual')
plt.title("Actual vs Predicted Death Rates")
plt.xlabel("Test Cases")
plt.ylabel("Fatality")

# Adding a legend
plt.legend()

# Display the plot
plt.show()
