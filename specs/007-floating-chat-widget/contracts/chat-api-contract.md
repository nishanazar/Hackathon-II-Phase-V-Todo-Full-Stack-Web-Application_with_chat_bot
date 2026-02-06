# API Contract: Chat Endpoint

## Overview
This document defines the API contract for the chat endpoint that the floating chat widget will communicate with.

## Endpoint
`POST /api/{user_id}/chat`

## Purpose
Handles chat messages sent from the floating chat widget and returns appropriate responses from the AI service.

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
  "timestamp": "ISO 8601 datetime string (optional)",
  "metadata": {
    "source": "string (e.g., 'floating_widget', optional)"
  }
}
```

**Body Fields:**
- `message` (string, required): The text content of the user's message
- `timestamp` (string, optional): ISO 8601 formatted timestamp of when the message was sent
- `metadata` (object, optional): Additional metadata about the message
  - `source` (string, optional): Identifier for the source of the message

## Response

### Success Response (200 OK)
```json
{
  "id": "string",
  "response": "string",
  "timestamp": "ISO 8601 datetime string",
  "status": "success",
  "metadata": {
    "processing_time_ms": "number (optional)"
  }
}
```

**Response Fields:**
- `id` (string): Unique identifier for the response
- `response` (string): The AI-generated response to the user's message
- `timestamp` (string): ISO 8601 formatted timestamp of when the response was generated
- `status` (string): Status of the response ("success")
- `metadata` (object, optional): Additional metadata about the response
  - `processing_time_ms` (number, optional): Time taken to process the request in milliseconds

### Error Responses

#### 400 Bad Request
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "string",
    "details": "object (optional)"
  }
}
```

#### 401 Unauthorized
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing authentication token"
  }
}
```

#### 403 Forbidden
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied. User ID mismatch."
  }
}
```

#### 404 Not Found
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "The specified user does not exist"
  }
}
```

#### 429 Rate Limited
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Please try again later."
  }
}
```

#### 500 Internal Server Error
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred"
  }
}
```

## Authentication
This endpoint requires a valid JWT token in the Authorization header. The token must be verified against the Better Auth system, and the user ID in the token must match the `user_id` in the path parameter.

## Validation Rules
- The `user_id` in the path must match the authenticated user's ID from the JWT
- The `message` field in the request body must not be empty
- The request must include a valid Authorization header with a JWT token
- Rate limiting should be applied per user to prevent abuse

## Example Request
```
POST /api/12345/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Hello, how can you help me?",
  "timestamp": "2023-07-25T10:30:00Z"
}
```

## Example Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "resp_67890",
  "response": "Hello! I'm here to assist you. How can I help today?",
  "timestamp": "2023-07-25T10:30:05Z",
  "status": "success",
  "metadata": {
    "processing_time_ms": 120
  }
}
```