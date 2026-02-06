import os
from main import app

# For Hugging Face Spaces, we need to expose the FastAPI app directly
# The app is already defined in main.py

# If running on Hugging Face Spaces, the app will be served through their infrastructure
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 7860)),  # Hugging Face typically uses port 7860
        log_level="info"
    )