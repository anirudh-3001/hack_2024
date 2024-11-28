# loan_default_app.py
from PIL import Image
import pandas as pd
import numpy as np
import joblib
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load and preprocess data
df = pd.read_csv("dataset.csv")
df = df.drop(columns=['LoanID'])

# Label encoding for categorical variables
from sklearn.preprocessing import LabelEncoder

cols_to_label_encode = ['Education', 'EmploymentType', 'MaritalStatus', 'HasMortgage', 'HasDependents', 'LoanPurpose', 'HasCoSigner']
label_encoder = LabelEncoder()

for col in cols_to_label_encode:
    df[col] = label_encoder.fit_transform(df[col])

# Prepare data for training
X = df.drop(columns=['Default'])  # Features
y = df['Default']  # Target variable

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scaling data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training the model
logreg_model = LogisticRegression()
logreg_model.fit(X_train_scaled, y_train)

# Save the model
joblib.dump(logreg_model, 'logreg_model.pkl')

# Streamlit app for prediction
def predict_loan_default():
    st.header("Loan Default Prediction")
    image = Image.open('th.jpeg')
    st.image(image, caption='Loan Default Prediction', use_column_width=True)

    # Collect user inputs
    age = st.number_input("Enter your age", min_value=0, max_value=100, step=1)
    income = st.number_input("Enter your income", min_value=1, step=1000)
    loan_amount = st.number_input("Enter the loan amount", min_value=0, step=1000)
    credit_score = st.number_input("Enter your credit score", min_value=300, max_value=850, step=1)
    months_employed = st.number_input("Enter the number of months you are employed", min_value=0, step=1)

    loan_purpose = st.selectbox("Enter your loan purpose", ("Automobiles", "Business", "Education", "Home", "Others"))
    loan_purpose_dict = {"Automobiles": 0, "Business": 1, "Education": 2, "Home": 3, "Others": 4}
    loan_purpose_input = loan_purpose_dict[loan_purpose]
    
    # Set interest rate based on loan purpose
    if loan_purpose == "Automobiles":
        interest_rate = 8.8
    elif loan_purpose == "Business":
        interest_rate = 11.0
    elif loan_purpose == "Education":
        interest_rate = 5.5
    elif loan_purpose == "Home":
        interest_rate = 12.0
    else:
        interest_rate = 7.5

    loan_term = st.number_input("Enter the loan term (in months)", min_value=1, step=1)
    expenditure = st.number_input("Enter your monthly expenditure", min_value=0.0, step=0.1)

    education = st.selectbox("Enter your education", ("Bachelors", "High School", "Masters", "PhD"))
    education_dict = {"Bachelors": 0, "High School": 1, "Masters": 2, "PhD": 3}
    education_input = education_dict[education]

    employment_type = st.selectbox("Enter your employment type", ("Full Time", "Part Time", "Self Employed", "Unemployed"))
    employment_type_dict = {"Full Time": 0, "Part Time": 1, "Self Employed": 2, "Unemployed": 3}
    employment_type_input = employment_type_dict[employment_type]

    marital_status = st.selectbox("Enter your marital status", ("Married", "Single"))
    marital_status_dict = {"Married": 1, "Single": 2}
    marital_status_input = marital_status_dict[marital_status]

    mortgage = st.selectbox("Do you have a mortgage?", ("No", "Yes"))
    mortgage_input = 1 if mortgage == "Yes" else 0

    dependents = st.selectbox("Do you have dependents?", ("No", "Yes"))
    dependents_input = 1 if dependents == "Yes" else 0

    cosigner = st.selectbox("Do you have a cosigner?", ("No", "Yes"))
    cosigner_input = 1 if cosigner == "Yes" else 0

    expenditure = expenditure * 12

    if income != 0:
        dti_ratio = expenditure / income
    else:
        st.error("Income cannot be zero. Please enter a valid income.")
        return

    if st.button("Submit"):
        # Step 2: Collect User Input
        user_input = np.array([
            age,
            income,
            loan_amount,
            credit_score,
            months_employed,
            interest_rate,
            loan_term,
            dti_ratio,
            education_input,
            employment_type_input,
            marital_status_input,
            mortgage_input,
            dependents_input,
            loan_purpose_input,
            cosigner_input
        ]).reshape(1, -1)

        # Scale the user input
        user_input_scaled = scaler.transform(user_input)

        # Make prediction
        prediction = logreg_model.predict(user_input_scaled)

        # Display prediction result
        st.subheader("Prediction Result:")
        if prediction[0] == 1:
            st.write("Borrower cannot pay the loan")
        else:
            st.write("Loan can be approved, Thank you")

if __name__ == "__main__":
    predict_loan_default()
