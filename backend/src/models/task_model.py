from sqlmodel import SQLModel, Field, Relationship
from pydantic import Field as PydanticField
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from pydantic import field_serializer
import json

# Enhanced Task model with due_date, priority, tags, and recurring_interval
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)
    priority: int = Field(default=3, ge=1, le=5)  # Priority from 1 (lowest) to 5 (highest)
    tags: Optional[str] = Field(default=None)  # Store tags as JSON string
    recurring_interval: Optional[str] = Field(default=None, 
        regex="^(daily|weekly|monthly|yearly)$")  # Recurrence interval

    @property
    def parsed_tags(self) -> List[str]:
        """Parse the tags JSON string into a list of tags."""
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return []
        return []

    @parsed_tags.setter
    def parsed_tags(self, value: List[str]):
        """Set the tags property by converting a list to JSON string."""
        self.tags = json.dumps(value) if value else None


class Task(TaskBase, table=True):
    """
    Enhanced Task model representing a task entity with user ownership and CRUD operations.
    Includes due_date, priority, tags, and recurring_interval fields.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Removed foreign_key constraint for simplicity
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self, **kwargs):
        # Handle tags conversion if provided as a list
        if 'parsed_tags' in kwargs:
            tags_list = kwargs.pop('parsed_tags')
            kwargs['tags'] = json.dumps(tags_list) if tags_list else None
        super().__init__(**kwargs)


class TaskCreate(TaskBase):
    """
    Request model for creating new tasks with enhanced fields.
    """
    pass


class TaskUpdate(SQLModel):
    """
    Request model for updating existing tasks with enhanced fields.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    tags: Optional[str] = Field(default=None)  # Store tags as JSON string
    recurring_interval: Optional[str] = Field(default=None, 
        regex="^(daily|weekly|monthly|yearly)$")  # Recurrence interval

    @property
    def parsed_tags(self) -> List[str]:
        """Parse the tags JSON string into a list of tags."""
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return []
        return []

    @parsed_tags.setter
    def parsed_tags(self, value: List[str]):
        """Set the tags property by converting a list to JSON string."""
        self.tags = json.dumps(value) if value else None


class TaskResponse(TaskBase):
    """
    Response model for task operations with enhanced fields.
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

    @field_serializer('due_date')
    def serialize_due_date(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize due_date datetime to ISO format string if it exists."""
        if value:
            return value.isoformat()
        return None