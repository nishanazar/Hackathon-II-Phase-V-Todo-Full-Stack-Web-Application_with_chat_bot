# Quickstart Guide: Full Integration & Testing for Phase III Todo AI Chatbot

## Overview
This guide provides a quick setup and testing guide for the Full Integration & Testing for Phase III Todo AI Chatbot feature.

## Prerequisites
- Python 3.11+
- Node.js 18+ and npm/yarn
- Docker and docker-compose (optional, for containerized deployment)
- Access to Google's Gemini API (GEMINI_API_KEY)
- Access to Neon PostgreSQL database

## Setup

### 1. Environment Configuration
Update your `.env` files in both frontend and backend directories with the required variables:
```bash
# Backend .env
GEMINI_API_KEY=your_google_gemini_api_key_here
BETTER_AUTH_SECRET=your_jwt_secret_here
DATABASE_URL=postgresql://user:password@localhost/dbname

# Frontend .env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Install Dependencies
In both frontend and backend directories:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 3. Database Setup
Ensure your PostgreSQL database is running and accessible via the DATABASE_URL in your environment.

## Testing

### 1. Running the Application
Start both frontend and backend services:
```bash
# Backend
cd backend
python -m src.main

# Frontend
cd frontend
npm run dev
```

Or with Docker:
```bash
docker-compose up
```

### 2. Testing the Complete Flow
1. Navigate to the ChatKit UI in your browser
2. Authenticate with your credentials
3. Test the following commands:
   - "Add a task to buy groceries" (add task)
   - "List my tasks" (list tasks)
   - "Complete the task to buy groceries" (complete task)
   - "Update the task 'buy groceries' to 'buy organic groceries'" (update task)
   - "Delete the task 'buy groceries'" (delete task)

### 3. Testing Conversation Persistence
1. Start a conversation with the AI agent
2. Restart the server
3. Resume the conversation to verify history persistence

### 4. Testing User Isolation
1. Login with User A
2. Create some tasks
3. Login with User B
4. Verify User B cannot see User A's tasks

## Testing Commands

### Single-Turn Commands
Test each of the 5 basic task operations:
- Add: "Add a task to walk the dog"
- List: "Show my tasks" or "What do I have to do?"
- Complete: "Complete the task to walk the dog"
- Update: "Update the task 'walk the dog' to 'walk the big dog'"
- Delete: "Delete the task 'walk the dog'"

### Multi-Turn & Chaining
Test chained commands like:
- "Add a task to buy milk and then list my tasks"
- "List my tasks and complete the first one"

### Error & Edge Case Testing
- Test with malformed commands
- Test with API temporarily unavailable
- Test with very long conversations
- Test with database connection issues

## Updating README
Ensure the main README.md file includes:
- Clear setup instructions
- Running instructions
- Testing procedures
- Troubleshooting tips