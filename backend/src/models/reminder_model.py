from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4


class ReminderBase(SQLModel):
    task_id: UUID
    scheduled_time: datetime
    user_id: str
    sent: bool = Field(default=False)


class Reminder(ReminderBase, table=True):
    """
    Reminder model representing scheduled notifications for upcoming task due dates 
    managed through Dapr Jobs API.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    sent_time: Optional[datetime] = Field(default=None)


class ReminderCreate(ReminderBase):
    """
    Request model for creating new reminders.
    """
    pass


class ReminderRead(ReminderBase):
    """
    Response model for reminder operations.
    """
    id: UUID
    sent_time: Optional[datetime]


class ReminderUpdate(SQLModel):
    """
    Request model for updating existing reminders.
    """
    sent: Optional[bool] = Field(default=None)
    sent_time: Optional[datetime] = Field(default=None)