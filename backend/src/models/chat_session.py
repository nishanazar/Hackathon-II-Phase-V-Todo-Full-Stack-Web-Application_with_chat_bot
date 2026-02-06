from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class ChatSessionBase(SQLModel):
    title: str = Field(default="New Chat Session")
    user_id: str = Field()  # Changed to string to match the existing auth system


class ChatSession(ChatSessionBase, table=True):
    """
    Conversational context between user and AI agent
    """
    __tablename__ = "chat_session"  # Explicitly set table name

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["ChatMessage"] = Relationship(back_populates="chat_session", cascade_delete=True)


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionRead(ChatSessionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ChatSessionUpdate(SQLModel):
    title: Optional[str] = None