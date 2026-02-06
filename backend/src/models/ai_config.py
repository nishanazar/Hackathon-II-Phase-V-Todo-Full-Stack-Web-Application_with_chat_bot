from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class AIConfigBase(SQLModel):
    model_name: str = Field(default="gemini-1.5-flash")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=1000)
    system_prompt: str = Field(
        default="You are a helpful task management assistant. ONLY respond to task-related queries "
                "(add, list, update, delete, complete). For unrelated queries, respond with: "
                "'Sorry, I only help with your tasks. Ask me to add, list, update, delete, complete, or get a task.'"
    )


class AIConfig(AIConfigBase, table=True):
    """
    Configuration for the AI agent
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AIConfigCreate(AIConfigBase):
    pass


class AIConfigRead(AIConfigBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class AIConfigUpdate(SQLModel):
    model_name: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None