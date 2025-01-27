import pandas as pd
import numpy as np
import os
import joblib
import matplotlib
from matplotlib import pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
import pickle
from sklearn.metrics import mean_squared_error, r2_score


 
matplotlib.rcParams["figure.figsize"] = (20,10)
file_path = os.path.join(os.getcwd(), r"ebolahackathon\train_data.xlsx")

df1 = pd.read_excel(file_path)


df1.columns = df1.columns.str.strip()

df1['Deaths'].unique()

df1['Deaths'].value_counts()

print(df1.isnull().sum())

df3 = df1.dropna()

df3.isnull().sum()

print(df3.shape)

df3.hist(bins=50, figsize=(15,15))
plt.show()

train_data = pd.DataFrame(df3)

X_train = train_data[['Lat', 'Long_']]
y_train = train_data['Deaths']

test_data_path = os.path.join(os.getcwd(), r"ebolahackathon\test_points.xlsx")
test_data = pd.read_excel(test_data_path)
print(test_data.head())

X_test = train_data[['Lat', 'Long_']]

knn = KNeighborsRegressor(n_neighbors=3)

knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

print("Predicted death rates for the validation data:")
for i, pred in enumerate(y_pred):
    print(f"Test data {i+1}: Predicted death rate = {pred}")

print(sklearn.__version__)

print(knn)
path_model=os.path.join(os.getcwd()+r"\ebolahackathon\knn_model.pkl")
model_filename = path_model
try:
    with open(model_filename, 'wb') as f:
        pickle.dump(knn, f)
    print(f"Model saved successfully as {model_filename}.")
except Exception as e:
    print(f"Error saving model: {e}")
