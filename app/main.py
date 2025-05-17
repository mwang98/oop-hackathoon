from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the FastAPI application
app = FastAPI(
    title="Clinic Finder API",
    description="API for finding and booking clinic appointments based on patient needs",
    version="1.0.0",
)

# Add CORS middleware for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.routers import clinics, appointments

# Include routers
app.include_router(clinics.router, prefix="/api/v1")
app.include_router(appointments.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Clinic Finder API"}
