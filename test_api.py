#!/usr/bin/env python3
"""
Test script to verify the API endpoints and troubleshoot the 422 error.
"""

import jwt
import requests
import json
from datetime import datetime, timedelta
from uuid import uuid4

# Configuration
BASE_URL = "http://127.0.0.1:8000"
SECRET = "Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk"  # Default from settings.py
USER_ID = str(uuid4())  # Generate a unique user ID

def create_test_token(user_id: str):
    """Create a test JWT token with the expected claims."""
    payload = {
        "user_id": user_id,
        "sub": user_id,
        "id": user_id,
        "userId": user_id,
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token

def test_task_creation():
    """Test creating a task with a valid token."""
    token = create_test_token(USER_ID)
    print(f"Generated test user ID: {USER_ID}")
    print(f"Generated test token: {token[:20]}...")  # Show only first 20 chars
    
    # Test task data
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "due_date": None,
        "priority": "medium",
        "tags": [],
        "recurring_interval": None
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}/api/{USER_ID}/tasks/"
    print(f"Making request to: {url}")
    print(f"Request data: {json.dumps(task_data, indent=2)}")
    
    try:
        response = requests.post(url, json=task_data, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 201:
            print("✓ Task created successfully!")
            return True
        else:
            print(f"✗ Failed to create task. Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    success = test_task_creation()
    
    if not success:
        print("\nTroubleshooting steps:")
        print("1. Ensure the backend server is running on http://127.0.0.1:8000")
        print("2. Verify that the BETTER_AUTH_SECRET matches between frontend and backend")
        print("3. Check that the user ID in the token matches the one in the URL path")
        print("4. Ensure all required fields are provided in the request body")
        print("5. Verify that field names match the expected snake_case format")