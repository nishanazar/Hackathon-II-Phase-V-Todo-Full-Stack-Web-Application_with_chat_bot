# API Endpoints Specification

## Overview
This document specifies all API endpoints available in the Todo AI Chatbot application.

## Authentication
All endpoints require a valid JWT token in the Authorization header, except for authentication endpoints.

## Endpoints

### Task Management Endpoints
- `GET /api/{user_id}/tasks` - Retrieve all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{task_id}` - Retrieve a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a specific task

### Chat Endpoint (New)
- `POST /api/{user_id}/chat` - Handle chat messages and manage conversation state
  - **Description**: Handles chat messages from the frontend, manages conversation state in the database, and returns AI responses. Implements stateless design with all persistence in the database.
  - **Request Body**:
    ```json
    {
      "message": "string",
      "conversation_id": "integer (optional)"
    }
    ```
  - **Response**:
    ```json
    {
      "conversation_id": "integer",
      "response": "string",
      "tool_calls": "array"
    }
    ```
  - **Headers Required**: 
    - `Authorization`: Bearer token containing the JWT for authentication
    - `Content-Type`: application/json
  - **Path Parameters**:
    - `user_id`: The ID of the authenticated user. Must match the user ID in the JWT token.
  - **Success Response**: 200 OK
  - **Error Responses**: 
    - 400 Bad Request: Message cannot be empty
    - 401 Unauthorized: Invalid or expired JWT token
    - 403 Forbidden: User ID mismatch or access denied
    - 404 Not Found: Conversation not found
    - 500 Internal Server Error: Internal server error

## Error Handling
All error responses follow the format:
```json
{
  "detail": "error message"
}
```

## Security
- All endpoints validate JWT tokens using BETTER_AUTH_SECRET
- User isolation is enforced by verifying that the user_id in the path matches the authenticated user
- Sensitive data is filtered based on user ownership