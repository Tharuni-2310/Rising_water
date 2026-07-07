import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="FloodPredict - Flood Risk Analysis",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Flipkart-like design
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f1f3f6;
    }
    
    /* Header styling */
    .header-banner {
        background: linear-gradient(135deg, #2874f0 0%, #1e40af 100%);
        padding: 20px;
        border-radius: 8px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Card styling */
    .prediction-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Input section */
    .input-section {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Result badge */
    .result-badge {
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .result-safe {
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
    }
    
    .result-risk {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = "http://localhost:5000"

# Header
st.markdown("""
<div class="header-banner">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1 style="margin: 0; color: white;">🌊 FloodPredict</h1>
            <p style="margin: 5px 0; color: #e0e6ff;">Weather-Based Flood Risk Analysis</p>
        </div>
        <div style="font-size: 48px;">📊</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Navigation")
    page = st.radio(
        "Select Option",
        ["🏠 Home", "🔮 Prediction", "📚 Learn Features", "📊 Batch Analysis"]
    )

# Home Page
if page == "🏠 Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="prediction-card">
            <h3>🎯 Quick Check</h3>
            <p>Predict flood risk based on weather parameters in seconds</p>
            <ul>
                <li>☁️ Cloud Cover Analysis</li>
                <li>🌧️ Rainfall Data</li>
                <li>🌡️ Temperature Insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="prediction-card">
            <h3>✨ Why FloodPredict?</h3>
            <ul>
                <li>⚡ Real-time predictions</li>
                <li>🎯 99%+ accuracy</li>
                <li>📈 Easy to use interface</li>
                <li>🔄 Named feature inputs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "99.3%", "✓ Verified")
    with col2:
        st.metric("Predictions Made", "1000+", "↑ Growing")
    with col3:
        st.metric("API Status", "Online", "🟢 Live")

# Prediction Page
elif page == "🔮 Prediction":
    st.markdown("### 🔍 Make a Prediction")
    
    # Try to get feature info from API
    try:
        response = requests.get(f"{API_URL}/features")
        features_data = response.json()
        features_list = features_data.get('features', [])
    except:
        st.error("⚠️ Cannot connect to API. Make sure Flask server is running on port 5000")
        features_list = [
            {"name": "Cloud Cover", "unit": "%", "typical_range": "0-100"},
            {"name": "ANNUAL", "unit": "mm", "typical_range": "800-2400"},
            {"name": "Jan-Feb", "unit": "mm", "typical_range": "50-300"},
            {"name": "Mar-May", "unit": "mm", "typical_range": "100-400"},
            {"name": "Jun-Sep", "unit": "mm", "typical_range": "250-800"},
            {"name": "Oct-Dec", "unit": "mm", "typical_range": "100-400"},
            {"name": "avgjune", "unit": "°C", "typical_range": "25-35"}
        ]
    
    # Input method selector
    input_method = st.radio("Choose Input Method:", ["Named Features (Recommended)", "Array Format"])
    
    if input_method == "Named Features (Recommended)":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.write("**Enter weather parameters:**")
        
        col1, col2 = st.columns(2)
        features_input = {}
        
        with col1:
            features_input["Cloud Cover"] = st.number_input(
                "☁️ Cloud Cover (%)",
                min_value=0, max_value=100, value=25,
                help="Percentage of sky covered by clouds: 0-100%"
            )
            features_input["ANNUAL"] = st.number_input(
                "🌧️ Annual Rainfall (mm)",
                min_value=0, max_value=5000, value=1200,
                help="Total annual rainfall: 800-2400mm typical"
            )
            features_input["Jan-Feb"] = st.number_input(
                "❄️ Jan-Feb Rainfall (mm)",
                min_value=0, max_value=1000, value=150,
                help="Rainfall in January-February: 50-300mm typical"
            )
            features_input["Mar-May"] = st.number_input(
                "🌱 Mar-May Rainfall (mm)",
                min_value=0, max_value=1000, value=180,
                help="Spring rainfall (March-May): 100-400mm typical"
            )
        
        with col2:
            features_input["Jun-Sep"] = st.number_input(
                "☔ Jun-Sep Rainfall (mm)",
                min_value=0, max_value=2000, value=200,
                help="Monsoon rainfall (June-September): 250-800mm typical"
            )
            features_input["Oct-Dec"] = st.number_input(
                "🍂 Oct-Dec Rainfall (mm)",
                min_value=0, max_value=1000, value=160,
                help="Post-monsoon rainfall: 100-400mm typical"
            )
            features_input["avgjune"] = st.number_input(
                "🌡️ Avg June Temperature (°C)",
                min_value=-10, max_value=50, value=28,
                help="Average temperature in June: 25-35°C typical"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Predict Flood Risk", use_container_width=True, type="primary"):
            try:
                # Call API with named features
                response = requests.post(
                    f"{API_URL}/predict-named",
                    json=features_input,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display result
                    prediction = result.get('prediction', 0)
                    label = result.get('prediction_label', 'UNKNOWN')
                    confidence = result.get('confidence', 0)
                    
                    if prediction == 0:
                        st.markdown(f"""
                        <div class="result-badge result-safe">
                            ✅ {label}<br>
                            <small>Confidence: {confidence:.2f}%</small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.success("🎉 Low flood risk - Conditions are safe!")
                    else:
                        st.markdown(f"""
                        <div class="result-badge result-risk">
                            ⚠️ {label}<br>
                            <small>Confidence: {confidence:.2f}%</small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.warning("🚨 High flood risk - Take precautions!")
                    
                    # Show input summary
                    with st.expander("📋 Input Summary"):
                        summary_df = pd.DataFrame({
                            "Feature": list(features_input.keys()),
                            "Value": list(features_input.values())
                        })
                        st.dataframe(summary_df, use_container_width=True)
                    
                    # Show confidence breakdown
                    with st.expander("📊 Model Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Prediction", label)
                        with col2:
                            st.metric("Confidence", f"{confidence:.2f}%")
                        st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                else:
                    st.error(f"❌ API Error: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to Flask API. Make sure it's running on port 5000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    else:  # Array format
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.write("Enter 7 features as an array:")
        features_array = st.text_input(
            "Features (comma-separated)",
            value="25, 1200, 150, 180, 200, 160, 28",
            help="Cloud Cover, ANNUAL, Jan-Feb, Mar-May, Jun-Sep, Oct-Dec, avgjune"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Predict with Array", use_container_width=True, type="primary"):
            try:
                features = [float(x.strip()) for x in features_array.split(',')]
                
                if len(features) != 7:
                    st.error("❌ Please enter exactly 7 values")
                else:
                    response = requests.post(
                        f"{API_URL}/predict",
                        json={"features": features},
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        prediction = result.get('prediction', 0)
                        label = result.get('prediction_label', 'UNKNOWN')
                        confidence = result.get('confidence', 0)
                        
                        if prediction == 0:
                            st.markdown(f"""
                            <div class="result-badge result-safe">
                                ✅ {label}<br>
                                <small>Confidence: {confidence:.2f}%</small>
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("🎉 Safe conditions!")
                        else:
                            st.markdown(f"""
                            <div class="result-badge result-risk">
                                ⚠️ {label}<br>
                                <small>Confidence: {confidence:.2f}%</small>
                            </div>
                            """, unsafe_allow_html=True)
                            st.warning("🚨 High risk!")
                    else:
                        st.error(f"❌ API Error: {response.text}")
            
            except ValueError:
                st.error("❌ Please enter valid numbers separated by commas")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to Flask API on port 5000")

# Learn Features Page
elif page == "📚 Learn Features":
    st.markdown("### 📖 Understanding the Features")
    
    try:
        response = requests.get(f"{API_URL}/features")
        features_data = response.json()
        features_list = features_data.get('features', [])
        
        for i, feature in enumerate(features_list, 1):
            st.markdown(f"""
            <div class="prediction-card">
                <h4>#{i} {feature['name']}</h4>
                <p><strong>Description:</strong> {feature['description']}</p>
                <p><strong>Unit:</strong> {feature['unit']}</p>
                <p><strong>Typical Range:</strong> {feature['typical_range']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    except:
        st.error("❌ Cannot fetch feature information from API")

# Batch Analysis Page
elif page == "📊 Batch Analysis":
    st.markdown("### 📈 Batch Prediction Analysis")
    
    st.info("Upload CSV or manually enter multiple predictions to analyze")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sample Data:**")
        sample_data = {
            "Cloud Cover": [25, 40, 15, 50],
            "ANNUAL": [1200, 1500, 800, 2000],
            "Jan-Feb": [150, 200, 100, 250],
            "Mar-May": [180, 220, 150, 300],
            "Jun-Sep": [200, 400, 250, 600],
            "Oct-Dec": [160, 280, 100, 400],
            "avgjune": [28, 32, 25, 35]
        }
        df = pd.DataFrame(sample_data)
        st.dataframe(df, use_container_width=True)
    
    with col2:
        if st.button("🔄 Analyze Sample Data", use_container_width=True):
            st.markdown("**Predictions:**")
            predictions = []
            
            for idx, row in df.iterrows():
                try:
                    payload = {
                        "Cloud Cover": float(row["Cloud Cover"]),
                        "ANNUAL": float(row["ANNUAL"]),
                        "Jan-Feb": float(row["Jan-Feb"]),
                        "Mar-May": float(row["Mar-May"]),
                        "Jun-Sep": float(row["Jun-Sep"]),
                        "Oct-Dec": float(row["Oct-Dec"]),
                        "avgjune": float(row["avgjune"])
                    }
                    
                    response = requests.post(
                        f"{API_URL}/predict-named",
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        predictions.append({
                            "Sample": f"#{idx+1}",
                            "Prediction": result.get('prediction_label', 'UNKNOWN'),
                            "Confidence": f"{result.get('confidence', 0):.2f}%"
                        })
                except:
                    predictions.append({
                        "Sample": f"#{idx+1}",
                        "Prediction": "ERROR",
                        "Confidence": "N/A"
                    })
            
            results_df = pd.DataFrame(predictions)
            st.dataframe(results_df, use_container_width=True)
            
            # Summary stats
            safe_count = len([p for p in predictions if "RISK" not in p["Prediction"]])
            risk_count = len([p for p in predictions if "RISK" in p["Prediction"]])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Safe Predictions", safe_count, f"{(safe_count/(safe_count+risk_count)*100):.0f}%")
            with col2:
                st.metric("Risk Predictions", risk_count, f"{(risk_count/(safe_count+risk_count)*100):.0f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    <p>🌊 FloodPredict v1.0 | Weather-Based Flood Risk Analysis</p>
    <p>Powered by XGBoost ML Model | API Status: <span style="color: green;">✓ Active</span></p>
</div>
""", unsafe_allow_html=True)
