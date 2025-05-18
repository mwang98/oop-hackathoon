"""
Main FastAPI application setup.
"""
import logging
from fastapi import FastAPI
from app.routers import providers

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("provider_finder")

app = FastAPI(
    title="Provider Finder API",
    description="API for finding and connecting with healthcare providers",
    version="1.0.0",
)

# Include routers
app.include_router(providers.router)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Provider Finder API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
