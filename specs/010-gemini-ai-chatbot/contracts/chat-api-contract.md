# API Contract: Chat Endpoint for Gemini AI Agent

## Overview
This document defines the API contract for the chat endpoint that integrates the Gemini AI Agent with OpenAI Agents SDK.

## Endpoints

### POST /api/{user_id}/chat
Processes user input through the AI agent and returns a response.

#### Request
- **Method**: POST
- **Path**: `/api/{user_id}/chat`
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Path Parameters**:
  - `user_id` (string, required): The ID of the authenticated user
- **Body** (application/json):
  ```json
  {
    "message": "User's message to the AI agent",
    "session_id": "Optional session ID to continue a conversation"
  }
  ```

#### Response
- **Success Response** (200 OK):
  ```json
  {
    "response": "AI agent's response to the user",
    "session_id": "ID of the chat session",
    "task_created": {
      "id": "ID of any task created by the agent",
      "title": "Title of the created task",
      "status": "Current status of the task"
    },
    "tool_calls": [
      {
        "name": "Name of the MCP tool called",
        "arguments": "Arguments passed to the tool"
      }
    ]
  }
  ```
- **Unauthorized Response** (401 Unauthorized):
  ```json
  {
    "error": "Invalid or missing JWT token"
  }
  ```
- **Forbidden Response** (403 Forbidden):
  ```json
  {
    "error": "Access denied: Cannot access another user's endpoint"
  }
  ```
- **Server Error Response** (500 Internal Server Error):
  ```json
  {
    "error": "Internal server error during AI processing"
  }
  ```

#### Business Logic
1. Validate JWT token and ensure user_id matches the token's subject
2. Initialize or retrieve the chat session for the user
3. Pass the user's message to the AI agent
4. The AI agent processes the message and may call MCP tools
5. Return the agent's response along with any created tasks or tool calls

### GET /api/{user_id}/chat/sessions
Retrieves a list of chat sessions for the user.

#### Request
- **Method**: GET
- **Path**: `/api/{user_id}/chat/sessions`
- **Headers**:
  - `Authorization: Bearer {jwt_token}`

#### Response
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "Session ID",
      "title": "Session title",
      "created_at": "Timestamp",
      "updated_at": "Timestamp"
    }
  ]
  ```

### GET /api/{user_id}/chat/sessions/{session_id}/messages
Retrieves messages from a specific chat session.

#### Request
- **Method**: GET
- **Path**: `/api/{user_id}/chat/sessions/{session_id}/messages`
- **Headers**:
  - `Authorization: Bearer {jwt_token}`

#### Response
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "Message ID",
      "role": "user|assistant",
      "content": "Message content",
      "created_at": "Timestamp"
    }
  ]
  ```