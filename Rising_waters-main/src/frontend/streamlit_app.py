# Wrapper to run Streamlit app from src/frontend while reusing root streamlit_app.py
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importing the main streamlit app logic
from streamlit_app import *
