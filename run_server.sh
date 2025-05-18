#!/bin/bash

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install required dependencies
pip install fastapi uvicorn[standard] pydantic

# Run the FastAPI server
cd /Users/mikewang/Documents/oop
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
