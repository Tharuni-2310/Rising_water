# Run Flask backend using venv python
cd $PSScriptRoot\..\
.venv\Scripts\Activate.ps1
c:/skillwallet/.venv/Scripts/python.exe -m flask --app app run --host 0.0.0.0 --port 5000
