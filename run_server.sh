#!/bin/bash

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Run the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
