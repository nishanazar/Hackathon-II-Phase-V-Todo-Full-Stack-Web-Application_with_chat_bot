from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
import json
from enum import Enum

class TaskEventType(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    COMPLETED = "completed"
    RECURRING_CREATED = "recurring_created"


class TaskEventBase(SQLModel):
    task_id: UUID
    event_type: TaskEventType
    payload: Optional[str] = Field(default=None)  # Store payload as JSON string
    processed: bool = Field(default=False)

    @property
    def parsed_payload(self) -> Optional[Dict[str, Any]]:
        """Parse the payload JSON string into a dictionary."""
        if self.payload:
            try:
                return json.loads(self.payload)
            except json.JSONDecodeError:
                return None
        return None

    @parsed_payload.setter
    def parsed_payload(self, value: Optional[Dict[str, Any]]):
        """Set the payload property by converting a dict to JSON string."""
        self.payload = json.dumps(value) if value else None


class TaskEvent(TaskEventBase, table=True):
    """
    Task Event model representing events published to Kafka topics for task creation, 
    updates, completion, and recurring task generation.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskEventCreate(TaskEventBase):
    """
    Request model for creating new task events.
    """
    pass


class TaskEventRead(TaskEventBase):
    """
    Response model for task event operations.
    """
    id: UUID
    timestamp: datetime