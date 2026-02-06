import os
import sys
from pathlib import Path

# Change to the backend directory to ensure proper imports
backend_dir = Path(__file__).parent / "backend"
os.chdir(backend_dir)

# Now import and run the app
from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)