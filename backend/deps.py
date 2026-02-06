from sqlmodel import Session
from db import get_db
from auth import get_current_user, verify_user_id_match
from typing import Generator, Callable, Any
from fastapi import Depends, HTTPException, status
from src.services.task_service import TaskService
from src.services.recurring_service import RecurringService
from src.services.reminder_service import ReminderService
from src.dapr.dapr_client import dapr_service
from src.dapr.pubsub import task_events_pubsub


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """
    Dependency to get the TaskService instance
    """
    return TaskService(db=db)


def get_recurring_service() -> RecurringService:
    """
    Dependency to get the RecurringService instance
    """
    return RecurringService()


def get_reminder_service() -> ReminderService:
    """
    Dependency to get the ReminderService instance
    """
    return ReminderService(dapr_service=dapr_service)


def get_dapr_service():
    """
    Dependency to get the Dapr service instance
    """
    return dapr_service


def get_task_events_pubsub():
    """
    Dependency to get the task events pubsub instance
    """
    return task_events_pubsub