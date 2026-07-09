Rising Waters — Flood Prediction App
A flood risk prediction project built with a Flask backend, an XGBoost model, and a Streamlit frontend.

Project Overview
This repository includes:

app.py — Flask API server that loads the trained xgboost_model.pkl model and predicts flood risk using both ML and domain-based rule scoring.
streamlit_app.py — Streamlit frontend for entering weather features and viewing predictions.
requirements.txt — Python dependencies required to run the project.
Risin.ipynb — Jupyter notebook used for model training and analysis.
xgboost_model.pkl — Pre-trained XGBoost model used by the backend.
Features
Flood risk prediction using named weather features
Enhanced risk scoring with monsoon and seasonal rainfall logic
Model confidence and risk factors returned with each prediction
Streamlit UI with a Flipkart-inspired design
Detailed feature help and batch prediction support
Folder / File Structure
app.py — Flask API and prediction logic
streamlit_app.py — Streamlit user interface
requirements.txt — Python packages to install
README.md — Project documentation
Risin.ipynb — Notebook for training and exploration
xgboost_model.pkl — Saved trained model
.gitignore — Files to ignore in Git
Entity Relationship Diagram (ERD)
The following diagram shows the conceptual entities and relationships for this project:


Prerequisites
Python 3.11+ installed
Windows PowerShell (commands shown below)
Project virtual environment available at .venv
Setup
Open PowerShell in C:\skillwallet and run:

cd C:\skillwallet
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
If you do not have the virtual environment, create one first:

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Running the Project
1. Start the Flask backend
In Terminal 1:

cd C:\skillwallet
.venv\Scripts\Activate.ps1
python app.py
or optionally:

.venv\Scripts\python.exe -m flask --app app run --host 0.0.0.0 --port 5000
The backend should be available at:

http://127.0.0.1:5000
http://localhost:5000
2. Start the Streamlit frontend
In Terminal 2:

cd C:\skillwallet
.venv\Scripts\Activate.ps1
python -m streamlit run streamlit_app.py --server.port=8501
Then open:

http://localhost:8501
Project layout (template-style)
This repository follows a simple template layout:

.
├─ .github/workflows/   # CI workflow stubs
├─ models/              # Trained model artifacts
├─ scripts/             # Convenience scripts to run the app
├─ src/
│  ├─ backend/          # Backend entrypoint wrapper
  │  └─ frontend/         # Frontend entrypoint wrapper
├─ tests/               # Basic tests
├─ app.py               # Flask app (root for compatibility)
├─ streamlit_app.py     # Streamlit UI (root for compatibility)
├─ requirements.txt
└─ README.md
How to Use
Run the Flask backend first.
Run the Streamlit frontend.
Open the Streamlit URL in a browser.
Use the Prediction page to enter feature values.
Available API Endpoints
The backend exposes these endpoints:

GET / — API home and quick start information
GET /features — Feature descriptions and ranges
GET /test — Sample prediction using default feature values
POST /predict — Predict using an array of 7 numeric features
POST /predict-named — Predict using named feature keys
Example named payload
{
  "Cloud Cover": 30,
  "ANNUAL": 1500,
  "Jan-Feb": 120,
  "Mar-May": 200,
  "Jun-Sep": 600,
  "Oct-Dec": 300,
  "avgjune": 32
}
Example array payload
{
  "features": [30, 1500, 120, 200, 600, 300, 32]
}
Notes
The project currently uses xgboost_model.pkl as the trained model.
If a scaler.pkl file is present, it will be used for feature scaling.
If flood dataset.xlsx is available, the app can fit a fallback scaler from it.
Use two terminal windows: one for Flask and one for Streamlit.
Troubleshooting
If Cannot connect to API appears on the Streamlit page, confirm that Flask is running on port 5000.
If model predictions are not changing, ensure valid weather values are entered.
Use Ctrl+C in each terminal to stop the servers.
License
This project is provided as-is for educational and demonstration purposes.
