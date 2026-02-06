# Quickstart Guide: Gemini AI Agent with OpenAI Agents SDK for Phase III Todo AI Chatbot

## Overview
This guide provides a quick setup and usage guide for the Gemini AI Agent with OpenAI Agents SDK for Phase III Todo AI Chatbot feature.

## Prerequisites
- Python 3.11+
- pip package manager
- Access to Google's Gemini API (GEMINI_API_KEY)
- Docker and docker-compose (optional, for containerized deployment)

## Setup

### 1. Environment Configuration
Create a `.env` file in the backend directory with the following variables:
```bash
GEMINI_API_KEY=your_google_gemini_api_key_here
BETTER_AUTH_SECRET=your_jwt_secret_here
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 2. Install Dependencies
In the backend directory:
```bash
pip install -r requirements.txt
```

### 3. Database Setup
Ensure your PostgreSQL database is running and accessible via the DATABASE_URL in your environment.

## Usage

### 1. Starting the Service
Start the backend service:
```bash
cd backend
python -m src.main
```

Or with Docker:
```bash
docker-compose up
```

### 2. Interacting with the AI Agent
Send a POST request to the chat endpoint:
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {your_jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### 3. Supported Commands
The AI agent understands natural language commands for:
- Adding tasks: "Add a task to...", "Create a task for..."
- Listing tasks: "Show my tasks", "List tasks", "What do I have to do?"
- Updating tasks: "Update task...", "Change task status..."
- Deleting tasks: "Delete task...", "Remove task..."
- Completing tasks: "Complete task...", "Mark task as done..."

## Troubleshooting

### Common Issues
1. **Invalid API Key**: Ensure your GEMINI_API_KEY is valid and has the necessary permissions.
2. **JWT Token Issues**: Verify that your JWT token is valid and matches the user_id in the request.
3. **Database Connection**: Check that your DATABASE_URL is correct and the database is accessible.

### Logs
Check the service logs for detailed error information:
```bash
# If running with Docker
docker-compose logs backend

# If running directly
# Check the output of the Python process
```

## Development
For development, you can run the service in debug mode:
```bash
cd backend
python -m src.main --debug
```

This will provide more detailed logging for troubleshooting purposes.