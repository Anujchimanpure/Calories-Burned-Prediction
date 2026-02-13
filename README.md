# 🔥 Calories Burned Prediction using Machine Learning

A Machine Learning project that predicts the number of calories burned based on physiological and exercise-related parameters such as age, gender, height, weight, duration, heart rate, and body temperature.

---

## Project Overview

This project applies Supervised Machine Learning (Regression) techniques to estimate calories burned by an individual during physical activity.  

The model is trained using real-world exercise and calorie datasets and deployed through an interactive user interface.

---

## Objectives

- Predict calories burned using ML algorithms
- Perform Exploratory Data Analysis (EDA)
- Visualize feature relationships
- Build an interactive GUI/Web App
- Evaluate model performance

---

## Machine Learning Approach

- **Problem Type:** Regression  
- **Algorithm Used:** Linear Regression (sklearn)  
- **Evaluation Metrics:**  
  - R² Score  
  - MAE  
  - RMSE  

---

## Dataset Information

The project uses two datasets:

1. **exercise.csv** → Input features  
   - User_ID  
   - Gender  
   - Age  
   - Height  
   - Weight  
   - Duration  
   - Heart_Rate  
   - Body_Temp  

2. **calories.csv** → Target variable  
   - User_ID  
   - Calories  

Both datasets are merged using **User_ID**.

---

## Technologies Used

- Python 
- Jupyter Lab 
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit / Tkinter (for GUI)

---

## Features

✔ Data Preprocessing  
✔ Feature Encoding  
✔ Data Visualization (EDA)  
✔ Regression Model Training  
✔ Model Evaluation  
✔ Calories Prediction  
✔ Interactive GUI/Web Interface  
