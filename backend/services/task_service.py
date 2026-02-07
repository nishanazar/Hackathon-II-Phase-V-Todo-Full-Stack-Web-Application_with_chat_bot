from sqlmodel import Session, select
from datetime import datetime, timedelta
from models import Task, TaskCreate, TaskUpdate, RecurringIntervalEnum
from uuid import UUID
from typing import List, Optional
import json
from .dapr_client import dapr_client
import asyncio


def create_task(db: Session, task: TaskCreate, user_id: str) -> Task:
    """Create a new task with the specified user_id."""
    # Convert tags list to JSON string for storage
    tags_json = json.dumps(task.tags) if task.tags is not None else '[]'

    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        due_date=task.due_date,
        priority=task.priority,
        tags=tags_json,
        recurring_interval=task.recurring_interval,
        user_id=user_id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Publish task created event asynchronously
    # Run in a background task to avoid event loop issues
    import threading
    def publish_event():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Handle tags appropriately - if it's already a list, use as-is, otherwise parse from JSON string
            tags_value = db_task.tags
            if isinstance(tags_value, list):
                processed_tags = tags_value
            else:
                try:
                    processed_tags = json.loads(tags_value) if tags_value else []
                except json.JSONDecodeError:
                    processed_tags = []

            loop.run_until_complete(
                dapr_client.publish_task_event("task.created", {
                    "taskId": str(db_task.id),
                    "userId": user_id,
                    "title": db_task.title,
                    "description": db_task.description,
                    "completed": db_task.completed,
                    "dueDate": db_task.due_date.isoformat() if db_task.due_date else None,
                    "priority": db_task.priority,
                    "tags": processed_tags,
                    "recurringInterval": db_task.recurring_interval
                })
            )
        finally:
            loop.close()

    # Run the event publishing in a separate thread
    event_thread = threading.Thread(target=publish_event, daemon=True)
    event_thread.start()
    
    return db_task


def get_tasks(
    db: Session, 
    user_id: str, 
    status_filter: str = "all",
    priority_filter: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    tags_filter: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "asc"
) -> List[Task]:
    """Retrieve tasks for a user with optional filtering and sorting."""
    query = select(Task).where(Task.user_id == user_id)

    # Add status filter if specified
    if status_filter == "pending":
        query = query.where(Task.completed == False)
    elif status_filter == "completed":
        query = query.where(Task.completed == True)

    # Add priority filter if specified
    if priority_filter:
        query = query.where(Task.priority == priority_filter)

    # Add due date range filter if specified
    if due_date_from:
        query = query.where(Task.due_date >= due_date_from)
    if due_date_to:
        query = query.where(Task.due_date <= due_date_to)

    # Add tags filter if specified
    if tags_filter:
        tag_list = tags_filter.split(',')
        for tag in tag_list:
            # For PostgreSQL JSON arrays, use the @> operator to check if tag exists in the array
            query = query.filter(Task.tags.op('@>')(f'["{tag.strip()}"]'))

    # Add sorting
    if sort_by == "due_date":
        if sort_order == "desc":
            query = query.order_by(Task.due_date.desc())
        else:
            query = query.order_by(Task.due_date.asc())
    elif sort_by == "priority":
        if sort_order == "desc":
            query = query.order_by(Task.priority.desc())
        else:
            query = query.order_by(Task.priority.asc())
    elif sort_by == "created_at":
        if sort_order == "desc":
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())

    tasks = db.exec(query).all()
    return tasks


def get_task(db: Session, task_id: UUID, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a user."""
    task = db.get(Task, task_id)
    
    if task and task.user_id == user_id:
        return task
    
    return None


def update_task(db: Session, task_id: UUID, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update a specific task completely."""
    db_task = db.get(Task, task_id)

    if not db_task or db_task.user_id != user_id:
        return None

    # Store original values for event
    original_values = {
        'title': db_task.title,
        'description': db_task.description,
        'completed': db_task.completed,
        'due_date': db_task.due_date,
        'priority': db_task.priority,
        'tags': db_task.tags,
        'recurring_interval': db_task.recurring_interval
    }

    # Update the task fields
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed
    if task_update.due_date is not None:
        db_task.due_date = task_update.due_date
    if task_update.priority is not None:
        db_task.priority = task_update.priority
    if task_update.tags is not None:
        # Convert tags list to JSON string for storage
        db_task.tags = json.dumps(task_update.tags)
    if task_update.recurring_interval is not None:
        db_task.recurring_interval = task_update.recurring_interval

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Publish task updated event asynchronously
    # Run in a background task to avoid event loop issues
    import threading
    def publish_updated_event():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Handle tags appropriately - if it's already a list, use as-is, otherwise parse from JSON string
            tags_value = db_task.tags
            if isinstance(tags_value, list):
                processed_tags = tags_value
            else:
                try:
                    processed_tags = json.loads(tags_value) if tags_value else []
                except json.JSONDecodeError:
                    processed_tags = []

            loop.run_until_complete(
                dapr_client.publish_task_event("task.updated", {
                    "taskId": str(db_task.id),
                    "userId": user_id,
                    "originalValues": original_values,
                    "updatedValues": {
                        "title": db_task.title,
                        "description": db_task.description,
                        "completed": db_task.completed,
                        "dueDate": db_task.due_date.isoformat() if db_task.due_date else None,
                        "priority": db_task.priority,
                        "tags": processed_tags,
                        "recurringInterval": db_task.recurring_interval
                    }
                })
            )
        finally:
            loop.close()

    # Run the event publishing in a separate thread
    event_thread = threading.Thread(target=publish_updated_event, daemon=True)
    event_thread.start()

    return db_task


def delete_task(db: Session, task_id: UUID, user_id: str) -> bool:
    """Delete a specific task."""
    task = db.get(Task, task_id)
    
    if task and task.user_id == user_id:
        db.delete(task)
        db.commit()
        return True
    
    return False


def complete_task_and_create_next_occurrence(db: Session, task_id: UUID, user_id: str) -> Optional[Task]:
    """
    Mark a task as complete and if it's recurring, create the next occurrence.
    """
    task = db.get(Task, task_id)

    if not task or task.user_id != user_id:
        return None

    # Mark current task as complete
    task.completed = True
    db.add(task)

    # Publish task completed event asynchronously
    # Run in a background task to avoid event loop issues
    import threading
    def publish_completed_event():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Handle tags appropriately - if it's already a list, use as-is, otherwise parse from JSON string
            tags_value = task.tags
            if isinstance(tags_value, list):
                processed_tags = tags_value
            else:
                try:
                    processed_tags = json.loads(tags_value) if tags_value else []
                except json.JSONDecodeError:
                    processed_tags = []

            loop.run_until_complete(
                dapr_client.publish_task_event("task.completed", {
                    "taskId": str(task.id),
                    "userId": user_id,
                    "title": task.title,
                    "description": task.description,
                    "dueDate": task.due_date.isoformat() if task.due_date else None,
                    "priority": task.priority,
                    "tags": processed_tags,
                    "recurringInterval": task.recurring_interval
                })
            )
        finally:
            loop.close()

    # Run the event publishing in a separate thread
    event_thread = threading.Thread(target=publish_completed_event, daemon=True)
    event_thread.start()

    # If the task is recurring, create the next occurrence
    if task.recurring_interval:
        next_due_date = calculate_next_due_date(task.due_date, task.recurring_interval)

        # Create a new task with the same properties but for the next occurrence
        new_task = Task(
            title=task.title,
            description=task.description,
            completed=False,  # New occurrence is not completed yet
            due_date=next_due_date,
            priority=task.priority,
            tags=task.tags,  # Tags are stored as JSON string
            recurring_interval=task.recurring_interval,
            user_id=user_id
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        # Publish task created event for the new recurring task
        # Run in a background task to avoid event loop issues
        import threading
        def publish_new_task_event():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Handle tags appropriately - if it's already a list, use as-is, otherwise parse from JSON string
                tags_value = new_task.tags
                if isinstance(tags_value, list):
                    processed_tags = tags_value
                else:
                    try:
                        processed_tags = json.loads(tags_value) if tags_value else []
                    except json.JSONDecodeError:
                        processed_tags = []

                loop.run_until_complete(
                    dapr_client.publish_task_event("task.created", {
                        "taskId": str(new_task.id),
                        "userId": user_id,
                        "title": new_task.title,
                        "description": new_task.description,
                        "completed": new_task.completed,
                        "dueDate": new_task.due_date.isoformat() if new_task.due_date else None,
                        "priority": new_task.priority,
                        "tags": processed_tags,
                        "recurringInterval": new_task.recurring_interval
                    })
                )
            finally:
                loop.close()

        # Run the event publishing in a separate thread
        event_thread = threading.Thread(target=publish_new_task_event, daemon=True)
        event_thread.start()

        return new_task

    db.commit()
    return None


def calculate_next_due_date(current_due_date: Optional[datetime], interval: RecurringIntervalEnum) -> Optional[datetime]:
    """
    Calculate the next due date based on the current due date and recurrence interval.
    """
    if not current_due_date:
        return None
        
    if interval == RecurringIntervalEnum.daily:
        return current_due_date + timedelta(days=1)
    elif interval == RecurringIntervalEnum.weekly:
        return current_due_date + timedelta(weeks=1)
    elif interval == RecurringIntervalEnum.monthly:
        # Add approximately one month (30 days)
        return current_due_date + timedelta(days=30)
    elif interval == RecurringIntervalEnum.yearly:
        # Add one year (approximately 365 days)
        return current_due_date + timedelta(days=365)
    
    return None