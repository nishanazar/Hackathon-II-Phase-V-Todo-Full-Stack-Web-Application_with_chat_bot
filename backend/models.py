from sqlmodel import SQLModel, Field, Relationship
from pydantic import Field as PydanticField
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import field_serializer

# Task model (existing Phase II model - unchanged)
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    """
    Task model representing a task entity with user ownership and CRUD operations.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Removed foreign_key constraint for simplicity
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class TaskCreate(TaskBase):
    """
    Request model for creating new tasks.
    """
    pass

class TaskUpdate(SQLModel):
    """
    Request model for updating existing tasks.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)

class TaskResponse(TaskBase):
    """
    Response model for task operations.
    """
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at')
    def serialize_created_at(self, value: datetime) -> str:
        """Serialize created_at datetime to ISO format string."""
        return value.isoformat()

    @field_serializer('updated_at')
    def serialize_updated_at(self, value: datetime) -> str:
        """Serialize updated_at datetime to ISO format string."""
        return value.isoformat()


# Conversation model (new for Phase III)
class ConversationBase(SQLModel):
    user_id: str = Field(index=True)

class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a conversation thread between a user and the AI assistant.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)

class ConversationCreate(ConversationBase):
    """
    Request model for creating new conversations.
    """
    pass

class ConversationRead(ConversationBase):
    """
    Response model for conversation operations.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime


# Message model (new for Phase III)
class MessageBase(SQLModel):
    user_id: str = Field(index=True)
    conversation_id: UUID = Field(index=True)  # Will be set as foreign key
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str = Field()

class Message(MessageBase, table=True):
    """
    Message model representing a message within a conversation between user and AI assistant.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True)  # Foreign key to conversations table
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    """
    Request model for creating new messages.
    """
    pass

class MessageRead(MessageBase):
    """
    Response model for message operations.
    """
    id: UUID
    created_at: datetime