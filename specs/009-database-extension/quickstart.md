# Quickstart Guide: MCP Server & Tools Implementation

## Overview
This guide provides a quick introduction to setting up and using the MCP (Model Context Protocol) server for Phase III of the Todo AI Chatbot.

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Existing project setup with FastAPI, SQLModel, and Neon PostgreSQL
- Valid JWT authentication configured

## Setup

### 1. Install Dependencies
Add the MCP SDK to your project dependencies:

```bash
poetry add mcp-sdk-python
# or
pip install mcp-sdk-python
```

### 2. Environment Variables
Ensure the following environment variables are set:
```bash
DATABASE_URL=your_neon_db_url
BETTER_AUTH_SECRET=your_jwt_secret
```

### 3. Database Models
Make sure the following models are defined in your backend:

- `Conversation` model with fields: id, user_id, created_at, updated_at
- `Message` model with fields: id, user_id, conversation_id, role, content, created_at
- Proper indexes on user_id and conversation_id for performance

## Implementation Steps

### 1. Create MCP Server
Create `backend/mcp_server.py` with the basic server setup:

```python
from mcp.server import Server
from sqlmodel import Session, select
from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.database import engine

# Initialize the MCP server
mcp_server = Server("todo-chat-mcp")

# Define your 5 tools using decorators
@mcp_server.tool("create_conversation")
def create_conversation(user_id: str) -> dict:
    """Create a new conversation."""
    with Session(engine) as session:
        # Implementation here
        pass

# Add other tools similarly...
```

### 2. Define the 5 MCP Tools
Implement the following tools with proper SQLModel database operations:

1. `create_conversation` - Creates a new conversation record
2. `add_message` - Adds a message to an existing conversation
3. `get_conversation_history` - Retrieves all messages in a conversation
4. `list_user_conversations` - Lists all conversations for a user
5. `update_message` - Updates the content of an existing message

### 3. Add JWT Authentication
Ensure each tool validates the JWT token and verifies that the user_id in the token matches the user_id in the request parameters.

### 4. Mount the Server in FastAPI
In your main FastAPI app (`backend/main.py`):

```python
from fastapi import FastAPI
from backend.mcp_server import mcp_server

app = FastAPI()

# Mount the MCP server at /mcp
app.mount("/mcp", mcp_server)
```

## Running the Server
Start your FastAPI application as usual. The MCP server will be available at `/mcp`.

## Testing
Use the existing pytest setup to create tests for your MCP tools:

```python
def test_create_conversation():
    # Test implementation
    pass
```

## Best Practices
- Always validate JWT tokens before executing any database operations
- Filter all database queries by user_id to ensure proper user isolation
- Use SQLModel sessions properly to avoid connection leaks
- Handle errors appropriately and return standard MCP error responses
- Log tool executions for debugging and monitoring purposes