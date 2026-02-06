# API Contract: Chat Endpoint

## Overview
This document defines the API contract for the chat endpoint that handles user messages and manages conversation state in the database.

## Endpoint
`POST /api/{user_id}/chat`

## Purpose
Handles chat messages from the frontend, manages conversation state in the database, and returns AI responses. Implements stateless design with all persistence in the database.

## Request

### Path Parameters
- `user_id` (string, required): The ID of the authenticated user. Must match the user ID in the JWT token.

### Headers
- `Authorization` (string, required): Bearer token containing the JWT for authentication
- `Content-Type` (string, required): `application/json`

### Body
```json
{
  "message": "string",
  "conversation_id": "integer (optional)"
}
```

**Body Fields:**
- `message` (string, required): The text content of the user's message
- `conversation_id` (integer, optional): The ID of an existing conversation to continue. If not provided, a new conversation will be created.

## Response

### Success Response (200 OK)
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array"
}
```

**Response Fields:**
- `conversation_id` (integer): The ID of the conversation (newly created or existing)
- `response` (string): The AI-generated response to the user's message
- `tool_calls` (array): Empty array for now, reserved for future AI agent integration

### Error Responses

#### 400 Bad Request
```json
{
  "detail": "string"
}
```
Example: "Message cannot be empty"

#### 401 Unauthorized
```json
{
  "detail": "string"
}
```
Example: "Not authenticated"

#### 403 Forbidden
```json
{
  "detail": "string"
}
```
Examples: 
- "Access denied. User ID mismatch."
- "Access denied. Conversation does not belong to user."

#### 404 Not Found
```json
{
  "detail": "string"
}
```
Example: "Conversation not found"

#### 500 Internal Server Error
```json
{
  "detail": "string"
}
```
Example: "Internal server error"

## Authentication
This endpoint requires a valid JWT token in the Authorization header. The token must be verified against the Better Auth system, and the user ID in the token must match the `user_id` in the path parameter.

## Validation Rules
- The `user_id` in the path must match the authenticated user's ID from the JWT
- The `message` field in the request body must not be empty
- The `conversation_id` must exist in the database if provided
- The conversation must belong to the authenticated user

## Database Operations
- If no `conversation_id` is provided: Creates a new Conversation record
- Loads conversation history from Message table if `conversation_id` is provided
- Stores user message in Message table with role "user"
- Stores assistant response in Message table with role "assistant"
- Updates conversation's `updated_at` timestamp

## Example Request
```
POST /api/user123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Hello, how can you help me?",
  "conversation_id": 1
}
```

## Example Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": 1,
  "response": "Echo: Hello, how can you help me?",
  "tool_calls": []
}
```

## Statelessness Requirements
- No in-memory state storage
- All conversation data persisted in database
- Endpoint can be restarted without losing conversation context
- Each request contains all necessary information to reconstruct conversation state