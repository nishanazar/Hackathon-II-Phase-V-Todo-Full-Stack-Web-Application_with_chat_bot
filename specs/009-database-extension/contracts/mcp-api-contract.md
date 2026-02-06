# MCP Server API Contract

## Overview
This document defines the API contract for the MCP (Model Context Protocol) server, which provides standardized tools for AI agents to interact with the system.

## Base Path
`/mcp`

## Supported Tools

### 1. create_conversation
Creates a new conversation record in the database.

**Parameters**:
- `user_id` (string, required): The ID of the user creating the conversation

**Returns**:
- `conversation_id` (string): The ID of the newly created conversation
- `created_at` (string): ISO 8601 timestamp of creation

**Errors**:
- `invalid_user_id`: If the user_id is malformed or unauthorized

### 2. add_message
Adds a message to an existing conversation.

**Parameters**:
- `conversation_id` (string, required): The ID of the conversation to add the message to
- `user_id` (string, required): The ID of the user adding the message
- `role` (string, required): Either "user" or "assistant"
- `content` (string, required): The content of the message

**Returns**:
- `message_id` (string): The ID of the newly created message
- `created_at` (string): ISO 8601 timestamp of creation

**Errors**:
- `conversation_not_found`: If the conversation doesn't exist or isn't accessible to the user
- `invalid_role`: If the role is neither "user" nor "assistant"
- `empty_content`: If the content is empty

### 3. get_conversation_history
Retrieves all messages in a conversation.

**Parameters**:
- `conversation_id` (string, required): The ID of the conversation to retrieve
- `user_id` (string, required): The ID of the user requesting the history

**Returns**:
- `messages` (array): Array of message objects with id, role, content, and created_at
- `conversation_info` (object): Object with id, user_id, created_at, and updated_at

**Errors**:
- `conversation_not_found`: If the conversation doesn't exist or isn't accessible to the user

### 4. list_user_conversations
Lists all conversations belonging to a user.

**Parameters**:
- `user_id` (string, required): The ID of the user whose conversations to list
- `limit` (integer, optional): Maximum number of conversations to return (default: 20)
- `offset` (integer, optional): Number of conversations to skip (default: 0)

**Returns**:
- `conversations` (array): Array of conversation objects with id, created_at, updated_at
- `total_count` (integer): Total number of conversations for the user

**Errors**:
- `invalid_user_id`: If the user_id is malformed

### 5. update_message
Updates the content of an existing message.

**Parameters**:
- `message_id` (string, required): The ID of the message to update
- `user_id` (string, required): The ID of the user requesting the update
- `content` (string, required): The new content for the message

**Returns**:
- `updated_at` (string): ISO 8601 timestamp of update

**Errors**:
- `message_not_found`: If the message doesn't exist or isn't accessible to the user
- `empty_content`: If the content is empty

## Authentication
All MCP tool calls must include a valid JWT token in the Authorization header. The server will validate that the user_id in the token matches the user_id in the request parameters to ensure proper authorization.

## Error Format
All errors follow the standard MCP error response format:
```json
{
  "error": {
    "code": "error_code",
    "message": "Human-readable error message"
  }
}
```

## Example Request/Response

### Example Request
```
POST /mcp
Authorization: Bearer <jwt_token>

{
  "method": "create_conversation",
  "params": {
    "user_id": "user_abc123"
  },
  "id": "req_123"
}
```

### Example Response
```
{
  "result": {
    "conversation_id": "conv_def456",
    "created_at": "2026-01-18T10:30:00Z"
  },
  "id": "req_123"
}
```