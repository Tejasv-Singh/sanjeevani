import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# API URL (assuming running locally)
API_URL = "http://127.0.0.1:8000/assess_credit"

st.set_page_config(page_title="Sanjeevani AI", layout="wide")

# --- Sidebar: Language & Input ---
st.sidebar.image("https://img.icons8.com/color/96/000000/sprout.png", width=50)
st.sidebar.title("Sanjeevani AI")
language = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])

st.sidebar.header("User Data Input")

# Default values for easy testing
input_data = {
    "annual_income": st.sidebar.number_input("Annual Income (₹)", 10000, 1000000, 180000),
    "existing_debt": st.sidebar.number_input("Existing Debt (₹)", 0, 500000, 15000),
    "payment_history_score": st.sidebar.slider("Payment History (0-10)", 0, 10, 8),
    "mobile_payment_volume": st.sidebar.number_input("Avg UPI Vol (₹/mo)", 0, 50000, 4500),
    "transaction_regularity": st.sidebar.slider("Digital Consistency (0-1)", 0.0, 1.0, 0.8),
    "crop_yield_index": st.sidebar.slider("Crop Yield Index", 0.0, 2.0, 1.1),
    "renewable_energy_usage": st.sidebar.selectbox("Uses Solar/Renewable?", [0, 1], index=1),
    "waste_management_score": st.sidebar.slider("Waste Mgmt Score (1-5)", 1, 5, 4),
    "water_efficiency_score": st.sidebar.slider("Water Efficiency (1-10)", 1, 10, 7),
}

# --- Main Dashboard ---
st.title("🌿 Sanjeevani: Sustainable Credit Scoring")
st.markdown("Financial inclusion powered by Alternative Data & ESG Metrics.")

if st.button("Analyze Creditworthiness"):
    with st.spinner("Agents are processing satellite, financial, and ESG data..."):
        try:
            response = requests.post(API_URL, json=input_data)
            result = response.json()
            
            if result['status'] == "success":
                analysis = result['analysis']
                recs = result['recommendations']
                
                col1, col2, col3 = st.columns(3)
                
                # Gauge: Credit Score
                with col1:
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = analysis['credit_score'],
                        title = {'text': "Credit Score"},
                        gauge = {'axis': {'range': [300, 900]},
                                 'bar': {'color': "#2E8B57"}}
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Gauge: SDG Score
                with col2:
                    fig_sdg = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = analysis['sdg_score'],
                        title = {'text': "SDG Sustainability Score"},
                        gauge = {'axis': {'range': [0, 100]},
                                 'bar': {'color': "#4682B4"}}
                    ))
                    st.plotly_chart(fig_sdg, use_container_width=True)
                
                # Risk Factors
                with col3:
                    st.subheader("🔍 Risk Explainability")
                    for factor in analysis['risk_factors']:
                        feat = factor['feature']
                        imp = factor['impact']
                        color = "red" if imp < 0 else "green"
                        st.markdown(f"- **{feat}**: :{color}[{imp:.2f} impact]")

                # Recommendations
                st.divider()
                st.subheader("📋 Recommended Financial Products")
                for rec in recs:
                    st.success(rec)
                    
            else:
                st.error("Error in analysis")
                
        except Exception as e:
            st.error(f"Could not connect to Backend. Ensure FastAPI is running. Error: {e}")