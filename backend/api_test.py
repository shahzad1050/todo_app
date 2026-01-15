# Simple Vercel-compatible entry point for testing
import os
from mangum import Mangum

# Import the test app
from .main_test import app

# Disable lifespan handling for serverless environments
if os.getenv("VERCEL_ENV"):  # Vercel environment
    handler = Mangum(app, lifespan="off")
else:  # Local development
    handler = Mangum(app)