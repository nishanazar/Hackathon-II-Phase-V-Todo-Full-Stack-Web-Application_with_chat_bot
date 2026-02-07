"""
Startup script for the Todo AI Chatbot application.
This script ensures the database is properly initialized before starting the server.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Starting Todo AI Chatbot application setup...")
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    print(f"📁 Working in directory: {backend_dir}")
    
    # Step 1: Initialize the database
    print("\n🔍 Checking database...")
    try:
        # Import and run the initialization
        from initialize_db import initialize_database
        initialize_database()
        print("✅ Database initialization completed!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    
    # Step 2: Verify the database
    print("\n🔍 Verifying database...")
    try:
        from verify_db import verify_database
        if verify_database():
            print("✅ Database verification passed!")
        else:
            print("❌ Database verification failed!")
            return False
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False
    
    # Step 3: Start the server
    print("\n🚀 Starting the server...")
    try:
        # Run the server using uvicorn
        import uvicorn
        from main import app
        print("✅ Server started successfully! Access the app at http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 Application failed to start properly!")
        sys.exit(1)
    else:
        print("\n🎉 Application setup completed successfully!")