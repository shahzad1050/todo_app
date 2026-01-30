import uvicorn
from .main import app

if __name__ == "__main__":
    print("Starting AI-Powered Todo Chatbot server...")
    print("Visit http://127.0.0.1:8000/docs to access the API documentation")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)