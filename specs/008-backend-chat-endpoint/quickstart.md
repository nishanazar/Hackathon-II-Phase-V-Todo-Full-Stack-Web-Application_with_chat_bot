# Quickstart Guide: Backend Chat Endpoint

## Prerequisites

Before implementing the backend chat endpoint, ensure your development environment has:

- Python 3.11+ installed
- FastAPI and SQLModel dependencies installed
- Database connection configured (Neon PostgreSQL)
- Better Auth JWT authentication configured

## Installation

1. Ensure the following dependencies are in your `requirements.txt`:

```txt
fastapi==0.104.1
sqlmodel==0.0.8
pydantic==2.5.0
better-auth==0.0.1-beta.13
```

2. Verify installation by checking your environment:

```bash
pip list | grep -E "(fastapi|sqlmodel|pydantic|better-auth)"
```

## Basic Implementation

### 1. Create the Chat Request/Response Models

Create a new file at `backend/schemas/chat.py`:

```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict] = []
```

### 2. Create the Chat Endpoint

Create a new file at `backend/routes/chat.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
from auth import get_current_user
from models import User, Conversation, Message
from schemas.chat import ChatRequest, ChatResponse
from db import get_db
from datetime import datetime

router = APIRouter()

@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def handle_chat(
    user_id: str,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied. User ID mismatch.")
    
    # Validate the message is not empty
    if not chat_request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Get or create conversation
    conversation_id = chat_request.conversation_id
    
    if conversation_id is None:
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        conversation_id = conversation.id
    else:
        # Verify conversation exists and belongs to user
        conversation = db.get(Conversation, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied. Conversation does not belong to user.")
    
    # Save user message
    user_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    db.commit()
    
    # Process the chat message and return a response
    # This is where you'd integrate with OpenAI's API or your own AI service
    # For now, we'll return a simple echo response
    response_text = f"Echo: {chat_request.message}"
    
    # Save assistant response
    assistant_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,  # This might be an AI user ID in the future
        role="assistant",
        content=response_text
    )
    db.add(assistant_message)
    db.commit()
    
    # Update conversation timestamp
    conversation.updated_at = datetime.now()
    db.add(conversation)
    db.commit()
    
    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        tool_calls=[]
    )
```

### 3. Update Main Application

Update `backend/main.py` to include the chat router:

```python
from fastapi import FastAPI
from routes import tasks, chat  # Import the new chat route

app = FastAPI(title="Todo API", version="1.0.0")

# Include the task routes
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

# Include the chat routes
app.include_router(chat.router, tags=["chat"])
```

### 4. Update Models (if needed)

If the Conversation and Message models don't exist yet, create them in `backend/models.py`:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

## Testing

1. Start your backend server:

```bash
cd backend
uvicorn main:app --reload
```

2. Test the endpoint with curl:

```bash
# Test with a new conversation
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{"message": "Hello, how are you?"}'

# Test with an existing conversation
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{"message": "Tell me more about yourself", "conversation_id": 1}'
```

3. Verify that messages are stored in the database:

```sql
SELECT * FROM messages WHERE conversation_id = 1 ORDER BY created_at DESC LIMIT 5;
```

## Troubleshooting

### 401 Unauthorized
- Verify that your JWT token is valid and not expired
- Check that the BETTER_AUTH_SECRET environment variable is set correctly

### 403 Forbidden
- Ensure the user_id in the URL path matches the user_id in the JWT token
- Verify that the conversation belongs to the authenticated user

### 404 Not Found
- Check that the conversation_id exists in the database if provided
- Verify that the endpoint path is correct

### Database Connection Issues
- Ensure your database connection string is properly configured
- Verify that the Neon PostgreSQL database is accessible
- Check that the required tables (conversations, messages) exist