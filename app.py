import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the saved model
with open('/Users/chandanmahato/Downloads/BIA/Fraud_detection_project/API/xgb_fraud_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Title of the app
st.title("Fraud Detection Model")

# Input fields for features (adjust based on your dataset columns)
st.header("Enter Transaction Details")
step = st.number_input("Step", min_value=0, value=0)
amount = st.number_input("Amount", min_value=0.0, value=0.0)
oldbalanceOrg = st.number_input("Old Balance (Origin)", min_value=0.0, value=0.0)
newbalanceOrg = st.number_input("New Balance (Origin)", min_value=0.0, value=0.0)
oldbalanceDest = st.number_input("Old Balance (Destination)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Destination)", min_value=0.0, value=0.0)
transactionFlag = st.selectbox("Transaction Flag (1 for certain types, 0 otherwise)", [0, 1])
nameOrig_freq = st.number_input("Name Origin Frequency", min_value=0, value=0)
nameDest_freq = st.number_input("Name Destination Frequency", min_value=0, value=0)

# One-hot encoded type columns with generic labels
type_options = ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT", "CASH_IN"]
selected_type = st.selectbox("Select Transaction Type", type_options)
type_encoded = {option: 1 if option == selected_type else 0 for option in type_options}

# Prepare input data with dynamic columns
input_data = {
    'step': step,
    'amount': amount,
    'oldbalanceOrg': oldbalanceOrg,
    'newbalanceOrg': newbalanceOrg,
    'oldbalanceDest': oldbalanceDest,
    'newbalanceDest': newbalanceDest,
    'transactionFlag': transactionFlag,
    'nameOrig_freq': nameOrig_freq,
    'nameDest_freq': nameDest_freq
}
input_df = pd.DataFrame([input_data])

# Add type-encoded columns dynamically
for option, value in type_encoded.items():
    input_df[f'type_{option}'] = value

# Ensure numeric columns and scaling
numeric_cols = ['amount', 'oldbalanceOrg', 'newbalanceOrg', 'oldbalanceDest', 'newbalanceDest',
                'transactionFlag', 'nameOrig_freq', 'nameDest_freq']
input_df[numeric_cols] = input_df[numeric_cols].astype(float)

# Scale the input data
scaler = StandardScaler()
input_df[numeric_cols] = scaler.fit_transform(input_df[numeric_cols])

# Align input_df with expected columns from the model dynamically
expected_columns = model.get_booster().feature_names
input_df = input_df.reindex(columns=expected_columns, fill_value=0)

# Make prediction
if st.button("Predict"):
    try:
        # Get prediction probability
        prediction_proba = model.predict_proba(input_df)
        fraud_probability = prediction_proba[0][1]  # Probability of fraud (class 1)
        non_fraud_probability = prediction_proba[0][0]  # Probability of non-fraud (class 0)
        prediction = 1 if fraud_probability >= 0.5 else 0  # Fixed threshold at 0.5

        st.write(f"Fraud Probability: {fraud_probability:.2f}")
        st.write(f"Non-Fraud Probability: {non_fraud_probability:.2f}")

        if prediction == 1:
            st.error("This transaction is predicted as FRAUD!")
        else:
            st.success("This transaction is predicted as NOT FRAUD!")
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")

# Add a note about the model
st.write("**Note:** This model was trained using XGBoost.")