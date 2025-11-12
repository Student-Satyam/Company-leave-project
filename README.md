💼 Employee Attrition Prediction App

An interactive Streamlit web application that predicts whether an employee is likely to leave the company based on demographic, job-related, and performance factors.

This app uses a trained XGBoost model (xgb_model.pkl) to assess attrition risk.

🚀 Features

🧠 Predicts employee attrition likelihood

⚙️ Powered by a trained XGBoost model

🧾 Collects both numeric and categorical employee attributes

📊 Displays probability-based results (chance of leaving or staying)

💡 Intuitive form-based interface built with Streamlit

🧠 Model Details

Algorithm: XGBoost (Classification)

Target Variable: Attrition (Yes / No)

Input Features:

Demographics: Age, Gender, Marital Status

Compensation: Monthly Income, Percent Salary Hike, Stock Options

Work Details: Department, Job Role, Total Working Years, Years at Company

Engagement: Training Times, Work-Life Balance, OverTime, etc.

Model File:

xgb_model.pkl → Trained classifier
