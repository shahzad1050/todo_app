# Vercel-compatible entry point for FastAPI backend
import os
from mangum import Mangum
from .main import app

# Disable lifespan handling for serverless environments to avoid initialization issues
if os.getenv("VERCEL_ENV"):  # Vercel environment
    handler = Mangum(app, lifespan="off")
else:  # Local development
    handler = Mangum(app)

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)