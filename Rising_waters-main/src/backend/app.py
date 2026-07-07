# Minimal wrapper that imports the main app logic from the repository root
# The original `app.py` remains at project root for compatibility.
# This file lets the project follow a `src/` layout expected by many templates.

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import the root app (existing app.py)
from app import app as flask_app

if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
