from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime

# Import fix for Hugging Face deployment - ensuring correct module path
from models import Task, TaskCreate, TaskUpdate, TaskResponse, PriorityEnum, RecurringIntervalEnum  # This is the correct import
from services.task_service import (
    create_task as service_create_task,
    get_tasks as service_get_tasks,
    get_task as service_get_task,
    update_task as service_update_task,
    delete_task as service_delete_task,
    complete_task_and_create_next_occurrence as service_complete_task_with_recurring
)
from services.search_service import search_tasks as service_search_tasks

from sqlmodel import Session, select
from auth import get_current_user, verify_user_id_match
from db import get_db
from exceptions import TaskNotFoundException, UserMismatchException, ValidationErrorException
from uuid import UUID

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task: TaskCreate
):
    """
    Create a new task for the authenticated user.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Validate title length
    if len(task.title) < 1 or len(task.title) > 200:
        raise ValidationErrorException("Title must be between 1 and 200 characters")

    # Validate description length if provided
    if task.description and len(task.description) > 1000:
        raise ValidationErrorException("Description must be less than 1000 characters")

    # Use the service to create the task
    db_task = service_create_task(db, task, user_id)

    return db_task

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    status_filter: str = "all",  # all, pending, completed
    priority_filter: Optional[str] = None,  # low, medium, high
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    tags_filter: Optional[str] = None,  # comma-separated tags
    sort_by: str = "created_at",  # created_at, due_date, priority
    sort_order: str = "asc"  # asc, desc
):
    """
    Retrieve tasks for the authenticated user with optional filtering and sorting.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Use the service to get tasks with filtering and sorting
    tasks = service_get_tasks(
        db, 
        user_id, 
        status_filter, 
        priority_filter, 
        due_date_from, 
        due_date_to, 
        tags_filter, 
        sort_by, 
        sort_order
    )
    
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str
):
    """
    Get a specific task by ID.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    # Use the service to get the task
    task = service_get_task(db, uuid_task_id, user_id)

    if not task:
        raise TaskNotFoundException(task_id)

    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str,
    task: TaskUpdate
):
    """
    Update a specific task completely.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    # Use the service to update the task
    updated_task = service_update_task(db, uuid_task_id, task, user_id)

    if not updated_task:
        raise TaskNotFoundException(task_id)

    return updated_task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_partial(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str,
    task: TaskUpdate
):
    """
    Partially update a specific task.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    # Use the service to update the task
    updated_task = service_update_task(db, uuid_task_id, task, user_id)

    if not updated_task:
        raise TaskNotFoundException(task_id)

    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str
):
    """
    Delete a specific task.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    # Use the service to delete the task
    success = service_delete_task(db, uuid_task_id, user_id)

    if not success:
        raise TaskNotFoundException(task_id)

    return


@router.post("/{task_id}/complete-with-recurring", response_model=TaskResponse)
def complete_task_with_recurring_logic(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str
):
    """
    Mark a task as complete and if it's recurring, create the next occurrence.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    # Use the service to complete the task and create next occurrence if needed
    new_task = service_complete_task_with_recurring(db, uuid_task_id, user_id)

    if not new_task:
        raise TaskNotFoundException(task_id)

    return new_task


@router.get("/search/", response_model=List[TaskResponse])
def search_tasks(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    search_query: Optional[str] = None,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    tags_filter: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "asc"
):
    """
    Search tasks with multiple criteria including text search, filters, and sorting.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Use the service to search tasks
    tasks = service_search_tasks(
        db,
        user_id,
        search_query,
        status_filter,
        priority_filter,
        due_date_from,
        due_date_to,
        tags_filter,
        sort_by,
        sort_order
    )
    
    return tasks