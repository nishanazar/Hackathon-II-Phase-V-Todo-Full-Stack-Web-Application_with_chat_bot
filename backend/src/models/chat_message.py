from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid


class ChatMessageBase(SQLModel):
    chat_session_id: uuid.UUID = Field()
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str
    task_id: Optional[uuid.UUID] = Field(default=None)


class ChatMessage(ChatMessageBase, table=True):
    """
    Individual message in a chat session
    """
    __tablename__ = "chat_message"  # Explicitly set table name

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    chat_session_id: uuid.UUID = Field(foreign_key="chat_session.id")  # Foreign key to chat_session table
    chat_session: "ChatSession" = Relationship(back_populates="messages")


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageRead(ChatMessageBase):
    id: uuid.UUID
    created_at: datetime


class ChatMessageUpdate(SQLModel):
    content: Optional[str] = None
    task_id: Optional[uuid.UUID] = None