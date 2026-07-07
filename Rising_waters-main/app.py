
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from pathlib import Path
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained XGBoost model
model = joblib.load('xgboost_model.pkl')

# Load the fitted scaler if available, otherwise fall back to the original training dataset
scaler_path = Path('scaler.pkl')
if scaler_path.exists():
    scaler = joblib.load(scaler_path)
else:
    data_path = Path('flood dataset.xlsx')
    if data_path.exists():
        dataset = pd.read_excel(data_path)
        x = dataset.iloc[:, 2:9].values
        scaler = StandardScaler().fit(x)
    else:
        scaler = None

def calculate_flood_risk_enhanced(features):
    """
    Enhanced flood risk prediction using both ML model and domain-based thresholds.
    Returns: (prediction, confidence, risk_score, risk_factors)
    """
    # Feature mapping
    cloud_cover = features[0]
    annual_rainfall = features[1]
    jan_feb = features[2]
    mar_may = features[3]
    jun_sep = features[4]  # Monsoon - most important
    oct_dec = features[5]
    avg_june_temp = features[6]
    
    # Get ML model prediction
    if scaler is not None:
        scaled = scaler.transform([features])
    else:
        scaled = np.array([features])
    
    model_pred = model.predict(scaled)[0]
    model_proba = model.predict_proba(scaled)[0]
    
    # Domain-based risk scoring (0-100)
    risk_score = 0
    risk_factors = []
    
    # 1. Monsoon rainfall (Jun-Sep) - highest impact
    if jun_sep > 700:
        risk_score += 35
        risk_factors.append(f"Very high monsoon rainfall: {jun_sep}mm")
    elif jun_sep > 500:
        risk_score += 25
        risk_factors.append(f"High monsoon rainfall: {jun_sep}mm")
    elif jun_sep > 300:
        risk_score += 15
        risk_factors.append(f"Moderate monsoon rainfall: {jun_sep}mm")
    
    # 2. Annual rainfall
    if annual_rainfall > 2500:
        risk_score += 25
        risk_factors.append(f"Excessive annual rainfall: {annual_rainfall}mm")
    elif annual_rainfall > 1800:
        risk_score += 15
        risk_factors.append(f"High annual rainfall: {annual_rainfall}mm")
    elif annual_rainfall > 1200:
        risk_score += 8
        risk_factors.append(f"Moderate annual rainfall: {annual_rainfall}mm")
    
    # 3. Seasonal rainfall concentration
    seasonal_total = jan_feb + mar_may + jun_sep + oct_dec
    if seasonal_total > 0:
        monsoon_ratio = jun_sep / seasonal_total
        if monsoon_ratio > 0.5:
            risk_score += 15
            risk_factors.append(f"High rainfall concentration in monsoon: {monsoon_ratio*100:.1f}%")
    
    # 4. Post-monsoon rainfall (Oct-Dec)
    if oct_dec > 400:
        risk_score += 10
        risk_factors.append(f"High post-monsoon rainfall: {oct_dec}mm")
    
    # 5. Spring rainfall (Mar-May)
    if mar_may > 350:
        risk_score += 8
        risk_factors.append(f"High spring rainfall: {mar_may}mm")
    
    # 6. Cloud cover
    if cloud_cover > 70:
        risk_score += 5
        risk_factors.append(f"High cloud cover: {cloud_cover}%")
    
    # 7. Temperature (very high temps can affect precipitation patterns)
    if avg_june_temp > 36:
        risk_score += 5
        risk_factors.append(f"Extreme temperature: {avg_june_temp}°C")
    
    # Combine with ML model prediction
    ml_confidence = max(model_proba) * 100
    
    # Final prediction logic
    if risk_score >= 60:
        final_prediction = 1  # HIGH RISK
        confidence = min(risk_score, 99)
    elif risk_score >= 35:
        if model_pred == 1:
            final_prediction = 1
            confidence = max(ml_confidence * 0.6 + (risk_score * 0.4), 50)
        else:
            final_prediction = 0
            confidence = max(100 - risk_score, 50)
    else:
        final_prediction = 0  # LOW RISK
        confidence = 100 - min(risk_score, 50)
    
    return final_prediction, confidence, risk_score, risk_factors

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Flood Risk Prediction API",
        "available_endpoints": {
            "GET /": "This help message",
            "GET /features": "Detailed feature explanations and ranges",
            "GET /test": "Test prediction with sample data",
            "POST /predict": "Make prediction with feature array [7 numbers]",
            "POST /predict-named": "Make prediction with named features"
        },
        "quick_start": {
            "method": "POST /predict",
            "example_payload": {
                "features": [25, 1200, 150, 180, 200, 160, 28]
            },
            "response": {
                "prediction": 0,
                "prediction_label": "NO FLOOD RISK or FLOOD RISK"
            }
        },
        "alternative_method": {
            "method": "POST /predict-named",
            "example_payload": {
                "Cloud Cover": 25,
                "ANNUAL": 1200,
                "Jan-Feb": 150,
                "Mar-May": 180,
                "Jun-Sep": 200,
                "Oct-Dec": 160,
                "avgjune": 28
            },
            "note": "Use named features if you find the array format confusing"
        }
    })

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/features', methods=['GET'])
def features_info():
    """Explain what each feature means"""
    return jsonify({
        "message": "Flood Risk Prediction - Feature Descriptions",
        "total_features": 7,
        "features": [
            {
                "name": "Cloud Cover",
                "description": "Percentage of sky covered by clouds",
                "unit": "%",
                "typical_range": "0-100"
            },
            {
                "name": "ANNUAL",
                "description": "Total annual rainfall",
                "unit": "mm",
                "typical_range": "800-2400"
            },
            {
                "name": "Jan-Feb",
                "description": "Rainfall in January-February",
                "unit": "mm",
                "typical_range": "50-300"
            },
            {
                "name": "Mar-May",
                "description": "Rainfall in March-May (Spring)",
                "unit": "mm",
                "typical_range": "100-400"
            },
            {
                "name": "Jun-Sep",
                "description": "Rainfall in June-September (Monsoon)",
                "unit": "mm",
                "typical_range": "250-800"
            },
            {
                "name": "Oct-Dec",
                "description": "Rainfall in October-December (Post-Monsoon)",
                "unit": "mm",
                "typical_range": "100-400"
            },
            {
                "name": "avgjune",
                "description": "Average temperature in June",
                "unit": "°C",
                "typical_range": "25-35"
            }
        ]
    })

@app.route('/test', methods=['GET'])
def test_prediction():
    """Test the API with sample data"""
    sample_features = [25, 1200, 150, 180, 200, 160, 28]
    
    prediction, confidence, risk_score, risk_factors = calculate_flood_risk_enhanced(np.array(sample_features))
    
    return jsonify({
        "message": "Test Prediction Result",
        "input_features": {
            "Cloud Cover": sample_features[0],
            "ANNUAL": sample_features[1],
            "Jan-Feb": sample_features[2],
            "Mar-May": sample_features[3],
            "Jun-Sep": sample_features[4],
            "Oct-Dec": sample_features[5],
            "avgjune": sample_features[6]
        },
        "prediction": int(prediction),
        "prediction_label": "FLOOD RISK" if prediction == 1 else "NO FLOOD RISK",
        "confidence": float(confidence),
        "risk_score": float(risk_score),
        "risk_factors": risk_factors
    })

@app.route('/predict-named', methods=['POST'])
def predict_named():
    """Alternative endpoint: accept features with names instead of array"""
    try:
        data = request.get_json(force=True)
        
        feature_names = ["Cloud Cover", "ANNUAL", "Jan-Feb", "Mar-May", "Jun-Sep", "Oct-Dec", "avgjune"]
        features = []
        
        for name in feature_names:
            if name not in data:
                return jsonify({
                    "error": f"Missing feature: {name}",
                    "required_features": feature_names
                }), 400
            try:
                features.append(float(data[name]))
            except (ValueError, TypeError):
                return jsonify({"error": f"Feature '{name}' must be a number"}), 400
        
        # Use enhanced prediction formula
        prediction, confidence, risk_score, risk_factors = calculate_flood_risk_enhanced(np.array(features))
        
        return jsonify({
            "prediction": int(prediction),
            "prediction_label": "FLOOD RISK" if prediction == 1 else "NO FLOOD RISK",
            "confidence": float(confidence),
            "risk_score": float(risk_score),
            "risk_factors": risk_factors,
            "features_received": dict(zip(feature_names, features))
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/predict', methods=['POST'])
def predict():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json(force=True)

    # The input should be a list of 7 numerical features
    try:
        features = np.array(data['features']).reshape(1, -1)
        if len(features[0]) != 7:
            return jsonify({"error": "Features array must contain exactly 7 values"}), 400
    except KeyError:
        return jsonify({"error": "Missing 'features' key in JSON payload. Use POST /predict-named for named features"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "'features' must be a list of 7 numbers"}), 400

    # Use enhanced prediction formula
    prediction, confidence, risk_score, risk_factors = calculate_flood_risk_enhanced(features[0])

    return jsonify({
        "prediction": int(prediction),
        "prediction_label": "FLOOD RISK" if prediction == 1 else "NO FLOOD RISK",
        "confidence": float(confidence),
        "risk_score": float(risk_score),
        "risk_factors": risk_factors,
        "input_features_count": len(features[0])
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
