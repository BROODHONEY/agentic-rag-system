# Activate virtual environment and start the backend server
.\.venv\Scripts\Activate.ps1
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
