#!/usr/bin/env python3
"""
Entry point for running the FastAPI server.
"""
import os
import uvicorn
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    # Run the API server
    logger.info(f"Starting Clinic Finder API server on port {port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
