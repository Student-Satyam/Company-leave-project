import streamlit as st
import pandas as pd
import joblib

# Load trained XGBoost model
model = joblib.load("xgb_model.pkl")

st.set_page_config(page_title="Employee Attrition Prediction by Satyam", layout="wide")
st.title("💼 Employee Attrition Prediction")
st.markdown(
    "<h4 style='text-align: center;'>Fill in the employee details to predict Attrition</h4>",
    unsafe_allow_html=True
)

# Center layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form(key="employee_form"):
        # ----------- Numeric Inputs -----------
        age = st.slider("Age", 18, 60, 30)
        daily_rate = st.number_input("Daily Rate", 100, 2000, 800, step=50)
        hourly_rate = st.number_input("Hourly Rate", 10, 200, 60, step=5)
        monthly_income = st.number_input("Monthly Income", 1000, 20000, 5000, step=500)
        monthly_rate = st.number_input("Monthly Rate", 1000, 30000, 10000, step=1000)
        percent_hike = st.slider("Percent Salary Hike", 0, 30, 15)
        stock_option = st.selectbox("Stock Option Level", [0, 1, 2, 3])
        training_times = st.slider("Training Times Last Year", 0, 10, 3)
        work_life_balance = st.selectbox("Work Life Balance", [1, 2, 3, 4])
        total_working_years = st.slider("Total Working Years", 0, 40, 10)
        years_at_company = st.slider("Years At Company", 0, 40, 5)
        years_in_current_role = st.slider("Years In Current Role", 0, 20, 3)
        years_with_manager = st.slider("Years With Current Manager", 0, 20, 3)
        years_since_promo = st.slider("Years Since Last Promotion", 0, 15, 1)

        # ----------- Categorical Inputs -----------
        overtime = st.selectbox("OverTime", ["Yes", "No"])
        business_travel = st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
        department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
        education_field = st.selectbox("Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        job_role = st.selectbox("Job Role", [
            "Sales Executive", "Research Scientist", "Laboratory Technician", 
            "Manufacturing Director", "Human Resources", "Research Director", 
            "Manager", "Sales Representative"
        ])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])

        # ----------- Submit Button -----------
        submitted = st.form_submit_button("🔍 Predict Attrition")

if submitted:
    # ----------- Initialize feature dict with zeros -----------
    columns = [
        'Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EmployeeCount',
        'EmployeeNumber', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement', 'JobLevel',
        'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike',
        'PerformanceRating', 'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
        'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany',
        'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
        'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
        'Department_Research & Development', 'Department_Sales',
        'EducationField_Life Sciences', 'EducationField_Marketing', 'EducationField_Medical',
        'EducationField_Other', 'EducationField_Technical Degree', 'Gender_Male',
        'JobRole_Human Resources', 'JobRole_Laboratory Technician', 'JobRole_Manager',
        'JobRole_Manufacturing Director', 'JobRole_Research Director', 'JobRole_Research Scientist',
        'JobRole_Sales Executive', 'JobRole_Sales Representative', 'MaritalStatus_Married',
        'MaritalStatus_Single', 'OverTime_Yes'
    ]

    data = {col: 0 for col in columns}

    # ----------- Fill numeric inputs -----------
    data["Age"] = age
    data["DailyRate"] = daily_rate
    data["HourlyRate"] = hourly_rate
    data["MonthlyIncome"] = monthly_income
    data["MonthlyRate"] = monthly_rate
    data["PercentSalaryHike"] = percent_hike
    data["StockOptionLevel"] = stock_option
    data["TrainingTimesLastYear"] = training_times
    data["WorkLifeBalance"] = work_life_balance
    data["TotalWorkingYears"] = total_working_years
    data["YearsAtCompany"] = years_at_company
    data["YearsInCurrentRole"] = years_in_current_role
    data["YearsWithCurrManager"] = years_with_manager
    data["YearsSinceLastPromotion"] = years_since_promo

    # ----------- Fill categorical one-hot columns -----------
    if overtime == "Yes": data["OverTime_Yes"] = 1

    if business_travel == "Travel_Frequently": data["BusinessTravel_Travel_Frequently"] = 1
    elif business_travel == "Travel_Rarely": data["BusinessTravel_Travel_Rarely"] = 1

    if department == "Sales": data["Department_Sales"] = 1
    elif department == "Research & Development": data["Department_Research & Development"] = 1

    if education_field == "Life Sciences": data["EducationField_Life Sciences"] = 1
    elif education_field == "Medical": data["EducationField_Medical"] = 1
    elif education_field == "Marketing": data["EducationField_Marketing"] = 1
    elif education_field == "Technical Degree": data["EducationField_Technical Degree"] = 1
    else: data["EducationField_Other"] = 1

    if gender == "Male": data["Gender_Male"] = 1

    if job_role == "Sales Executive": data["JobRole_Sales Executive"] = 1
    elif job_role == "Research Scientist": data["JobRole_Research Scientist"] = 1
    elif job_role == "Laboratory Technician": data["JobRole_Laboratory Technician"] = 1
    elif job_role == "Manufacturing Director": data["JobRole_Manufacturing Director"] = 1
    elif job_role == "Human Resources": data["JobRole_Human Resources"] = 1
    elif job_role == "Research Director": data["JobRole_Research Director"] = 1
    elif job_role == "Manager": data["JobRole_Manager"] = 1
    elif job_role == "Sales Representative": data["JobRole_Sales Representative"] = 1

    if marital_status == "Single": data["MaritalStatus_Single"] = 1
    elif marital_status == "Married": data["MaritalStatus_Married"] = 1

    # ----------- Convert to DataFrame & predict -----------
    input_data = pd.DataFrame([data])
    pred = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    # ----------- Display result -----------
    if pred == 1:
        st.error(f"⚠️ Employee is likely to leave (Attrition Probability: {prob:.2f})")
    else:
        st.success(f"✅ Employee is likely to stay (Attrition Probability: {prob:.2f})")
