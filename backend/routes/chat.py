from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from auth import get_current_user
from models import Task
from schemas.chat import ChatRequest, ChatResponse
from db import get_db
from datetime import datetime
from uuid import UUID
from src.agents.todo_agent import TodoMasterAI
from src.models.chat_session import ChatSessionCreate
from src.services.chat_session_service import create_chat_session, get_chat_session_by_id
from src.models.chat_message import ChatMessageCreate

# Initialize the AI agent only if API key is available
ai_agent = None
try:
    ai_agent = TodoMasterAI()
except ValueError as e:
    print(f"Warning: {e}. AI features will be disabled.")
    ai_agent = None

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
    user_id: str,
    chat_request: ChatRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify that the user_id in the path matches the authenticated user
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Access denied. User ID mismatch.")

    # Validate the message is not empty
    if not chat_request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Get or create chat session
    session_id = chat_request.conversation_id

    if session_id is None:
        # Create new chat session
        chat_session_data = ChatSessionCreate(
            user_id=user_id,
            title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
        )
        chat_session = create_chat_session(session=db, chat_session_create=chat_session_data)
        session_id = chat_session.id
    else:
        # Verify chat session exists and belongs to user
        chat_session = get_chat_session_by_id(session=db, chat_session_id=session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        if chat_session.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied. Chat session does not belong to user.")

    try:
        # Process the chat message with the AI agent
        result = await ai_agent.process_message(
            user_message=chat_request.message,
            user_id=user_id,
            session_id=session_id,
            db_session=db
        )

        # Extract response details
        response_text = result.get("response", "I couldn't process your request.")
        tool_calls = result.get("tool_calls", [])
        task_created = result.get("task_created")

        return ChatResponse(
            conversation_id=session_id,
            response=response_text,
            tool_calls=tool_calls,
            task_created=task_created
        )
    except Exception as e:
        # Handle any errors during AI processing
        error_message = f"Sorry, I encountered an error processing your request: {str(e)}"

        return ChatResponse(
            conversation_id=session_id,
            response=error_message,
            tool_calls=[],
            task_created=None
        )