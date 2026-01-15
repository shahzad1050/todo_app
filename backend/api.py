# Vercel-compatible entry point for FastAPI backend
from mangum import Mangum
from .main import app

# Create the Mangum adapter for serverless compatibility
handler = Mangum(app, lifespan="off")

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)