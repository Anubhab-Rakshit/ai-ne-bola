# **AI Ne Bola** 🌟

AI Ne Bola is a comprehensive project that predicts the number of death cases, case fatality ratio (CFR), and other related metrics for various scenarios using machine learning models. It also provides detailed 3D visualizations and interactive web interfaces for users to explore the predictions.

---

## **Project Overview**

### **Live Links**  
- **Home Page:** [https://ai-ne-bola.netlify.app/](https://ai-ne-bola.netlify.app/)  
  This website offers a detailed view of the project and its purpose.  
- **Prediction Backend:** [https://ai-ne-bola-pvt.onrender.com/](https://ai-ne-bola-pvt.onrender.com/)  
  This backend predicts death cases and CFR using external parameters like temperature and humidity.

---

## **Repository Structure**

### 📁 `Website_Files`  
Contains the files used to host the homepage: **[https://ai-ne-bola.netlify.app/](https://ai-ne-bola.netlify.app/)**.  
Explore the project overview and interact with the user-friendly interface here.

---

### 📁 `backend_predict`  
Houses the backend files used for predictions.  
- **Deployed at:** [https://ai-ne-bola-pvt.onrender.com/](https://ai-ne-bola-pvt.onrender.com/)  
- Predicts:
  - **Number of Death Cases**
  - **Case Fatality Ratio (CFR)**  
  - Considers **external parameters** like temperature and humidity for accurate predictions.

---

### 📁 `graph_plots`  
Contains Python scripts for generating **3D visualizations** of death cases and the number of cases based on longitude and latitude.  
- Key Features:
  - **Interactive 3D plots** for better visualization.
  - Visual insights into the spread and impact of cases.

---

### 📁 `predict`  
This directory includes:  
- **Machine Learning Models**:
  - K-Nearest Neighbors (KNN) model.
- **Prediction Analysis**:
  - Plots for **Predicted Cases vs. Actual Cases**.
  - Mean Square Error (MSE) to evaluate model accuracy (**very low** in our case).  
- **Example Implementation**:
  - Sampled longitude and latitude for verifying predictions.

---
## 🤖 AI NE BOLA - Ebola Chatbot  

We have developed a **custom-trained chatbot** using the **Gemini API**, designed specifically to provide **accurate and reliable information about Ebola and its related topics**. This chatbot has been fine-tuned to ensure that it stays **focused solely on Ebola-related queries**, offering:  

- ✅ **General Information** about Ebola (causes, symptoms, transmission, and prevention)  
- ✅ **Predictive Analysis** based on available data  
- ✅ **Guidelines from WHO & CDC** for Ebola prevention and control  
- ✅ **Myths vs. Facts** to combat misinformation  

This chatbot is integrated seamlessly into our platform, allowing users to interact and get **real-time answers** to their questions about Ebola.  


### 🚀 How It Works  
1. The chatbot processes user queries using **Gemini’s NLP model**, ensuring context-aware responses.  
2. It retrieves and structures responses **based on our training data** and **verified health resources**.  
3. It is **restricted to Ebola-related topics** to maintain accuracy and relevance.  

---

### 📄 `predicted_test_data.csv`  
This file contains the data predicted using our model . It contains the test points along with paremeters number of death cases, CFR and total cases.  
- Format: **CSV**  
- Includes essential data points like longitude, latitude, and other parameters.

---

### 📄 `train_data_predicted(1).csv`  
This file contains the data predicted using our model when it is run on the training points provided.
It shows the MSE , Absolute Error for showing prediction variations.
- Format: **CSV**  

---

### 📄 `main.py`
This file is the building block of our model , all our mathematical assumptions like temperature dependency , prediction of unreported regions are done here.
So the whole prediction process has been done in this file.

---

## **How to Use**

### **1. View the Homepage**
- Visit [https://ai-ne-bola.netlify.app/](https://ai-ne-bola.netlify.app/) to explore the project.

### **2. Use the Prediction API**
- Access the backend service at [https://ai-ne-bola-pvt.onrender.com/](https://ai-ne-bola-pvt.onrender.com/).

### **3. Generate Graphs**
- Navigate to the `graph_plots` directory and run the Python scripts for interactive 3D visualizations.

### **4. Evaluate Predictions**
- Analyze the models in the `predict` directory to understand prediction accuracy and insights.

---

## **Technologies Used**

- **Frontend:** HTML, CSS, JavaScript , Flask (Python)
- **Backend:** Node.js, Express.js
- **Data Visualization:** Python (Matplotlib, Plotly)
- **Machine Learning:** Scikit-learn
- **Hosting:** 
  - [Netlify](https://www.netlify.com/) for the homepage.
  - [Render](https://render.com/) for backend services.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute:  
1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature-name`.  
3. Commit your changes: `git commit -m "Description of changes"`.  
4. Push to the branch: `git push origin feature-name`.  
5. Open a pull request.

---

## **Acknowledgements**  
- Thanks to the teams behind [Netlify](https://www.netlify.com/) and [Render](https://render.com/) for hosting services.
- Libraries and tools like **Scikit-learn**, **Matplotlib**, **Numpy** and **Plotly** for powering machine learning and visualization.

---

Feel free to add any additional details or sections that suit your project!
