from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a minimal FastAPI app for testing
app = FastAPI(
    title="Todo Web Application API - Test",
    description="Minimal API for testing deployment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Web Application API - Test Version"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    from fastapi.responses import Response
    import base64
    # Return a minimal transparent favicon to avoid 404 errors
    transparent_favicon = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA"
        "B3RJTUUH5AgQDC421wKJLgAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBk"
        "LmUHAAAAFklEQVQ4y2P8//8/AzYwMjIyAAAc/Qv/rkZB4QAAAABJRU5ErkJggg=="
    )
    return Response(content=transparent_favicon, media_type="image/x-icon")