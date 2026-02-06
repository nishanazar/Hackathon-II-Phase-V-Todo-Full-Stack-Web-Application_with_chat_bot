---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "latest"
app_file: main.py
pinned: false
---

# Backend Todo API

This is the backend service for the Todo application, built with FastAPI and SQLModel. It provides a secure, user-isolated task management API with JWT authentication and an integrated AI chatbot powered by Google's Gemini model.

## Features

- JWT-based authentication and authorization
- User-isolated task management (users can only access their own tasks)
- Full CRUD operations for tasks
- Task filtering by status (all, pending, completed)
- Input validation for task titles and descriptions
- Comprehensive error handling
- AI-powered chatbot for natural language task management
- Conversation history persistence
- MCP tools integration for standardized task operations

## API Endpoints

All endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <JWT_TOKEN>`

The user_id in the path must match the user_id in the JWT token for authorization.

### Task Management

- `GET /api/{user_id}/tasks` - List all tasks for the authenticated user with optional filtering
- `POST /api/{user_id}/tasks` - Create a new task for the authenticated user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task by ID
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task completely
- `PATCH /api/{user_id}/tasks/{id}` - Partially update a specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task

### Health Check

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Validation Rules

- Title: 1-200 characters (inclusive)
- Description: ≤1000 characters if provided
- user_id in path must match user_id in JWT token
- Task operations only allowed on tasks belonging to authenticated user

## Setup and Development

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Poetry (for dependency management)
- Docker and docker-compose (optional, for containerized deployment)
- Google's Gemini API access (GEMINI_API_KEY)

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
4. Set up environment variables in both frontend and backend directories:
   ```bash
   # Backend
   cp .env.example .env
   # Edit .env to include your values

   # Frontend
   cp .env.example .env.local
   # Edit .env.local to include your values
   ```
5. Ensure your PostgreSQL database is running and accessible via the DATABASE_URL in your environment

### Environment Variables

#### Backend
- `GEMINI_API_KEY`: Your Google Gemini API key for AI agent functionality
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing/verification
- `DATABASE_URL`: Database connection string (PostgreSQL)

#### Frontend
- `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for authentication service (e.g., http://localhost:3000)
- `NEXT_PUBLIC_API_URL`: URL for backend API (e.g., http://localhost:8000)

### Running the Application

#### Development Mode
Backend:
```bash
cd backend
python -m src.main
```

Frontend:
```bash
cd frontend
npm run dev
```

#### Containerized Deployment
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

## Testing

### Backend Testing

Run the backend tests using pytest:

```bash
cd backend
pytest tests/ -v
```

### Frontend Testing

Run the frontend tests:

```bash
cd frontend
npm test
```

### End-to-End Testing

To test the complete flow:
1. Start both frontend and backend services
2. Navigate to the ChatKit UI in your browser
3. Authenticate with your credentials
4. Test the following commands:
   - "Add a task to buy groceries" (add task)
   - "List my tasks" (list tasks)
   - "Complete the task to buy groceries" (complete task)
   - "Update the task 'buy groceries' to 'buy organic groceries'" (update task)
   - "Delete the task 'buy groceries'" (delete task)
5. Test conversation persistence by restarting the server and verifying history loads
6. Test user isolation by having multiple users interact with the system simultaneously

## Docker

To run the application with Docker:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

## Architecture

- **Frontend**: Next.js 16+ App Router with ChatKit UI component
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL (Neon) for storing tasks and user data
- **Authentication**: Better Auth with JWT tokens for stateless authentication
- **AI Agent**: Google's Gemini model via OpenAI-compatible endpoint
- **MCP Tools**: Model Context Protocol tools for standardized task operations
- **PyJWT**: JWT token handling
- **Pydantic**: Data validation and settings management

## Security

- JWT tokens are verified using the `BETTER_AUTH_SECRET`
- All endpoints verify that the user_id in the JWT matches the user_id in the path
- Database queries are filtered by the authenticated user's ID to prevent cross-user access
- User isolation is enforced via JWT + DB filtering to ensure users can only access their own data
- Conversation history is secured and isolated per user