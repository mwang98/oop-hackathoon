"""
Main FastAPI application setup.
"""
from fastapi import FastAPI
from app.routers import providers

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
    return {
        "message": "Provider Finder API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
