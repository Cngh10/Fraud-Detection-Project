import streamlit as st
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .fraud-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    .fraud-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .fraud-card:hover {
        transform: translateY(-5px);
    }
    
    .input-section {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .prediction-result {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .prediction-safe {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }
    
    h1, h2, h3 {
        color: white;
        font-weight: 600;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Load the saved model
@st.cache_resource
def load_model():
    with open('final_xgboost_model.joblib', 'rb') as file:
        return joblib.load(file)

model = load_model()

# Header with animation
st.markdown("""
<div class="fraud-header">
    <h1>🛡️ FraudGuard AI</h1>
    <p style="color: white; font-size: 1.2rem; margin-top: 0;">Advanced Machine Learning for Real-time Fraud Detection</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for additional info
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: white;">📊 Model Information</h3>
        <p style="color: white; font-size: 0.9rem;">XGBoost Classifier trained on historical transaction data</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;">
        <h3 style="color: white;">🔍 Features Used</h3>
        <ul style="color: white; font-size: 0.9rem;">
            <li>Transaction Amount</li>
            <li>Balance Changes</li>
            <li>Transaction Type</li>
            <li>Frequency Metrics</li>
            <li>Temporal Patterns</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="input-section">
        <h2 style="color: #333; margin-bottom: 1.5rem;">📝 Transaction Details</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for inputs
    col1_1, col1_2 = st.columns(2)
    
    with col1_1:
        step = st.number_input("⏰ Step (Time Unit)", min_value=0, value=0, help="Time step of the transaction")
        amount = st.number_input("💰 Amount", min_value=0.0, value=1000.0, help="Transaction amount in local currency")
        oldbalanceOrg = st.number_input("🏦 Old Balance (Origin)", min_value=0.0, value=10000.0, help="Initial balance before transaction")
        newbalanceOrg = st.number_input("🏦 New Balance (Origin)", min_value=0.0, value=9000.0, help="New balance after transaction")
        oldbalanceDest = st.number_input("🏦 Old Balance (Destination)", min_value=0.0, value=0.0, help="Initial balance of recipient")
        
    with col1_2:
        newbalanceDest = st.number_input("🏦 New Balance (Destination)", min_value=0.0, value=1000.0, help="New balance of recipient")
        transactionFlag = st.selectbox("🚩 Transaction Flag", [0, 1], help="Flag for certain transaction types")
        nameOrig_freq = st.number_input("👤 Origin Frequency", min_value=0, value=1, help="Frequency of origin account")
        nameDest_freq = st.number_input("👤 Destination Frequency", min_value=0, value=1, help="Frequency of destination account")
        
        # Transaction type selection with better styling
        type_options = ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT", "CASH_IN"]
        selected_type = st.selectbox("💳 Transaction Type", type_options, help="Type of transaction")

with col2:
    st.markdown("""
    <div class="fraud-card">
        <h3 style="color: #333; text-align: center;">📈 Transaction Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate and display transaction metrics
    balance_change_org = newbalanceOrg - oldbalanceOrg
    balance_change_dest = newbalanceDest - oldbalanceDest
    
    st.metric("💸 Amount", f"${amount:,.2f}")
    st.metric("📊 Origin Balance Change", f"${balance_change_org:,.2f}")
    st.metric("📊 Destination Balance Change", f"${balance_change_dest:,.2f}")
    st.metric("🔄 Transaction Type", selected_type)

# Prediction button with animation
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button("🔮 Predict Fraud Risk", use_container_width=True)

# Prediction logic
if predict_button:
    # Show loading animation
    with st.spinner("🤖 Analyzing transaction patterns..."):
        time.sleep(1)  # Simulate processing time
    
    # Prepare input data
    type_encoded = {option: 1 if option == selected_type else 0 for option in type_options}
    
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
    
    for option, value in type_encoded.items():
        input_df[f'type_{option}'] = value
    
    numeric_cols = ['amount', 'oldbalanceOrg', 'newbalanceOrg', 'oldbalanceDest', 'newbalanceDest',
                    'transactionFlag', 'nameOrig_freq', 'nameDest_freq']
    input_df[numeric_cols] = input_df[numeric_cols].astype(float)
    
    scaler = StandardScaler()
    input_df[numeric_cols] = scaler.fit_transform(input_df[numeric_cols])
    
    expected_columns = model.get_booster().feature_names
    input_df = input_df.reindex(columns=expected_columns, fill_value=0)
    
    try:
        # Make prediction
        prediction_proba = model.predict_proba(input_df)
        fraud_probability = prediction_proba[0][1]
        non_fraud_probability = prediction_proba[0][0]
        prediction = 1 if fraud_probability >= 0.5 else 0
        
        # Display results with modern styling
        if prediction == 1:
            st.markdown(f"""
            <div class="prediction-result">
                <h2>🚨 FRAUD DETECTED!</h2>
                <p style="font-size: 1.5rem; margin: 1rem 0;">This transaction shows suspicious patterns</p>
                <div style="background: rgba(255, 255, 255, 0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <p><strong>Fraud Probability:</strong> {fraud_probability:.1%}</p>
                    <p><strong>Safe Probability:</strong> {non_fraud_probability:.1%}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="prediction-safe">
                <h2>✅ TRANSACTION SAFE</h2>
                <p style="font-size: 1.5rem; margin: 1rem 0;">This transaction appears legitimate</p>
                <div style="background: rgba(255, 255, 255, 0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <p><strong>Safe Probability:</strong> {non_fraud_probability:.1%}</p>
                    <p><strong>Fraud Probability:</strong> {fraud_probability:.1%}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Create animated gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=fraud_probability * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Fraud Risk Level"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional insights
        st.markdown("""
        <div class="fraud-card">
            <h3 style="color: #333; text-align: center;">🔍 Risk Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_insight1, col_insight2, col_insight3 = st.columns(3)
        
        with col_insight1:
            st.metric("💰 Amount Risk", "High" if amount > 10000 else "Low")
        with col_insight2:
            st.metric("⏰ Time Risk", "Medium" if step > 100 else "Low")
        with col_insight3:
            st.metric("🔄 Type Risk", "High" if selected_type in ["TRANSFER", "CASH_OUT"] else "Low")
            
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; background: rgba(255, 255, 255, 0.1); border-radius: 15px;">
    <p style="color: white; font-size: 0.9rem;">🛡️ FraudGuard AI - Powered by XGBoost Machine Learning</p>
    <p style="color: white; font-size: 0.8rem;">Built with Streamlit • Real-time Fraud Detection</p>
</div>
""", unsafe_allow_html=True)
