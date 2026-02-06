from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

# Import the new enhanced models
from src.models.task_model import TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import TaskService
from src.dapr.dapr_client import dapr_service
from auth import get_current_user, verify_user_id_match
from deps import get_task_service
from exceptions import TaskNotFoundException, ValidationErrorException
from uuid import UUID

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task: TaskCreate
):
    """
    Create a new task for the authenticated user with enhanced fields.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Validate title length
    if len(task.title) < 1 or len(task.title) > 200:
        raise ValidationErrorException("Title must be between 1 and 200 characters")

    # Validate description length if provided
    if task.description and len(task.description) > 1000:
        raise ValidationErrorException("Description must be less than 1000 characters")

    # Validate priority if provided
    if task.priority is not None and (task.priority < 1 or task.priority > 5):
        raise ValidationErrorException("Priority must be between 1 and 5")

    # Validate tags if provided
    if task.parsed_tags and len(task.parsed_tags) > 10:
        raise ValidationErrorException("Maximum 10 tags allowed per task")

    # Validate due date if provided
    if task.due_date and task.due_date < datetime.now():
        raise ValidationErrorException("Due date must be in the future")

    # Validate recurring interval if provided
    valid_intervals = ["daily", "weekly", "monthly", "yearly"]
    if task.recurring_interval and task.recurring_interval not in valid_intervals:
        raise ValidationErrorException(f"Recurring interval must be one of: {', '.join(valid_intervals)}")

    # Create the task using the service
    db_task = task_service.create_task(task, user_id)

    return db_task

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    *,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    status_filter: str = Query("all", description="Filter tasks by status: all, pending, completed"),
    priority: Optional[int] = Query(None, ge=1, le=5, description="Filter by priority level (1-5)"),
    due_after: Optional[datetime] = Query(None, description="Filter tasks due after this date"),
    due_before: Optional[datetime] = Query(None, description="Filter tasks due before this date"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)")
):
    """
    Retrieve tasks for the authenticated user with optional filtering.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Parse tags if provided
    tags_list = None
    if tags:
        tags_list = [tag.strip() for tag in tags.split(",")]

    # Get tasks with filters
    tasks = task_service.get_tasks(
        user_id=user_id,
        completed=True if status_filter == "completed" else False if status_filter == "pending" else None,
        priority=priority,
        due_after=due_after,
        due_before=due_before,
        tags=tags_list
    )

    return tasks


@router.get("/search", response_model=List[TaskResponse])
def search_tasks(
    *,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    q: str = Query(..., description="Search query string"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("asc", description="Sort order: asc or desc")
):
    """
    Search tasks for the authenticated user by title, description, or tags.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # In a real implementation, we would use the search service
    # For now, we'll use the existing task service to get all tasks and filter them
    all_tasks = task_service.get_tasks(user_id=user_id)

    # Simple search implementation - filter tasks that match the query
    search_results = [
        task for task in all_tasks
        if q.lower() in task.title.lower() or
        (task.description and q.lower() in task.description.lower()) or
        (task.tags and any(q.lower() in tag.lower() for tag in task.tags))
    ]

    # Apply sorting
    reverse_sort = sort_order.lower() == "desc"
    if sort_by == "title":
        search_results.sort(key=lambda x: x.title.lower(), reverse=reverse_sort)
    elif sort_by == "priority":
        search_results.sort(key=lambda x: x.priority, reverse=reverse_sort)
    elif sort_by == "due_date":
        search_results.sort(key=lambda x: x.due_date or datetime.min, reverse=reverse_sort)
    elif sort_by == "created_at":
        search_results.sort(key=lambda x: x.created_at, reverse=reverse_sort)
    elif sort_by == "updated_at":
        search_results.sort(key=lambda x: x.updated_at, reverse=reverse_sort)
    else:  # Default to created_at
        search_results.sort(key=lambda x: x.created_at, reverse=reverse_sort)

    # Apply pagination
    start_idx = offset
    end_idx = start_idx + limit
    paginated_results = search_results[start_idx:end_idx]

    return paginated_results

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    *,
    task_service: TaskService = Depends(get_task_service),
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

    task = task_service.get_task(uuid_task_id, user_id)

    if not task:
        raise TaskNotFoundException(task_id)

    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    *,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str,
    task: TaskUpdate
):
    """
    Update a specific task completely with enhanced fields.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    # Validate title length if provided
    if task.title is not None and (len(task.title) < 1 or len(task.title) > 200):
        raise ValidationErrorException("Title must be between 1 and 200 characters")

    # Validate description length if provided
    if task.description is not None and len(task.description) > 1000:
        raise ValidationErrorException("Description must be less than 1000 characters")

    # Validate priority if provided
    if task.priority is not None and (task.priority < 1 or task.priority > 5):
        raise ValidationErrorException("Priority must be between 1 and 5")

    # Validate tags if provided
    if task.parsed_tags and len(task.parsed_tags) > 10:
        raise ValidationErrorException("Maximum 10 tags allowed per task")

    # Validate due date if provided
    if task.due_date and task.due_date < datetime.now():
        raise ValidationErrorException("Due date must be in the future")

    # Validate recurring interval if provided
    valid_intervals = ["daily", "weekly", "monthly", "yearly"]
    if task.recurring_interval and task.recurring_interval not in valid_intervals:
        raise ValidationErrorException(f"Recurring interval must be one of: {', '.join(valid_intervals)}")

    # Update the task using the service
    updated_task = task_service.update_task(uuid_task_id, task, user_id)

    if not updated_task:
        raise TaskNotFoundException(task_id)

    return updated_task

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    *,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str
):
    """
    Mark a task as completed.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    completed_task = await task_service.complete_task(uuid_task_id, user_id)

    if not completed_task:
        raise TaskNotFoundException(task_id)

    return completed_task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_partial(
    *,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str,
    task: TaskUpdate
):
    """
    Partially update a specific task with enhanced fields.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    # Validate title length if provided
    if task.title is not None and (len(task.title) < 1 or len(task.title) > 200):
        raise ValidationErrorException("Title must be between 1 and 200 characters")

    # Validate description length if provided
    if task.description is not None and len(task.description) > 1000:
        raise ValidationErrorException("Description must be less than 1000 characters")

    # Validate priority if provided
    if task.priority is not None and (task.priority < 1 or task.priority > 5):
        raise ValidationErrorException("Priority must be between 1 and 5")

    # Validate tags if provided
    if task.parsed_tags and len(task.parsed_tags) > 10:
        raise ValidationErrorException("Maximum 10 tags allowed per task")

    # Validate due date if provided
    if task.due_date and task.due_date < datetime.now():
        raise ValidationErrorException("Due date must be in the future")

    # Validate recurring interval if provided
    valid_intervals = ["daily", "weekly", "monthly", "yearly"]
    if task.recurring_interval and task.recurring_interval not in valid_intervals:
        raise ValidationErrorException(f"Recurring interval must be one of: {', '.join(valid_intervals)}")

    # Update the task using the service
    updated_task = task_service.update_task(uuid_task_id, task, user_id)

    if not updated_task:
        raise TaskNotFoundException(task_id)

    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    *,
    task_service: TaskService = Depends(get_task_service),
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

    success = task_service.delete_task(uuid_task_id, user_id)

    if not success:
        raise TaskNotFoundException(task_id)

    return