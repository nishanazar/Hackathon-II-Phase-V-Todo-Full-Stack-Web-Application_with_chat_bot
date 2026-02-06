"""
MCP tools for task management operations
These functions interact with the database to manage tasks
"""

from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from models import Task
from uuid import UUID
import uuid


async def add_task(user_id: str, title: str, description: Optional[str] = None, db_session: Session = None) -> Dict[str, Any]:
    """
    Add a new task for the user
    """
    if not db_session:
        return {"success": False, "error": "Database session required"}

    # Create the task with the user_id
    db_task = Task(
        title=title,
        description=description,
        completed=False,  # Initially not completed
        user_id=user_id
    )

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    # Convert to dict for return
    task_dict = {
        "id": str(db_task.id),  # Still include ID for internal operations
        "user_id": db_task.user_id,
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed,
        "created_at": db_task.created_at.isoformat()
    }

    # Return simplified version for user display
    simplified_task = {
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed
    }

    return {"success": True, "task": task_dict, "display_task": simplified_task}


async def list_tasks(user_id: str, db_session: Session = None) -> Dict[str, Any]:
    """
    List all tasks for the user
    """
    if not db_session:
        return {"success": False, "error": "Database session required"}

    # Query tasks for the user
    query = select(Task).where(Task.user_id == user_id)
    tasks = db_session.exec(query).all()

    # Convert to list of dicts
    tasks_list = []
    simplified_tasks_list = []
    for task in tasks:
        task_dict = {
            "id": str(task.id),
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
        tasks_list.append(task_dict)

        # Create simplified version for user display
        simplified_task = {
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
        simplified_tasks_list.append(simplified_task)

    return {"success": True, "tasks": tasks_list, "display_tasks": simplified_tasks_list}


async def update_task(user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None, db_session: Session = None) -> Dict[str, Any]:
    """
    Update an existing task for the user
    """
    if not db_session:
        return {"success": False, "error": "Database session required"}

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        return {"success": False, "error": f"Invalid task ID: {task_id}"}

    # Get the task from the database
    db_task = db_session.get(Task, uuid_task_id)

    if not db_task:
        return {"success": False, "error": f"Task {task_id} not found"}

    # Ensure the task belongs to the authenticated user
    if db_task.user_id != user_id:
        return {"success": False, "error": "Access denied. Task does not belong to user"}

    # Update the task fields if provided
    if title is not None:
        db_task.title = title
    if description is not None:
        db_task.description = description

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    # Convert to dict for return
    task_dict = {
        "id": str(db_task.id),
        "user_id": db_task.user_id,
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed,
        "updated_at": db_task.updated_at.isoformat()
    }

    # Return simplified version for user display
    simplified_task = {
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed
    }

    return {"success": True, "task": task_dict, "display_task": simplified_task}


async def delete_task(user_id: str, task_id: str = None, title: str = None, db_session: Session = None) -> Dict[str, Any]:
    """
    Delete a task for the user by ID or title
    """
    if not db_session:
        return {"success": False, "error": "Database session required"}

    task = None

    # If task_id is provided, try to delete by ID
    if task_id:
        # Convert task_id string to UUID
        try:
            uuid_task_id = UUID(task_id)
        except ValueError:
            return {"success": False, "error": f"Invalid task ID: {task_id}"}

        # Get the task from the database by ID
        task = db_session.get(Task, uuid_task_id)
    elif title:
        # Find task by title
        query = select(Task).where(Task.user_id == user_id).where(Task.title == title)
        task = db_session.exec(query).first()
    else:
        return {"success": False, "error": "Either task_id or title must be provided"}

    if not task:
        if task_id:
            return {"success": False, "error": f"Task with ID {task_id} not found"}
        else:
            return {"success": False, "error": f"Task with title '{title}' not found"}

    # Ensure the task belongs to the authenticated user
    if task.user_id != user_id:
        return {"success": False, "error": "Access denied. Task does not belong to user"}

    # Delete the task
    db_session.delete(task)
    db_session.commit()

    task_identifier = task_id if task_id else f"title '{title}'"
    return {"success": True, "message": f"Task {task_identifier} deleted"}


async def complete_task(user_id: str, task_id: str, db_session: Session = None) -> Dict[str, Any]:
    """
    Mark a task as completed for the user
    """
    if not db_session:
        return {"success": False, "error": "Database session required"}

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        return {"success": False, "error": f"Invalid task ID: {task_id}"}

    # Get the task from the database
    db_task = db_session.get(Task, uuid_task_id)

    if not db_task:
        return {"success": False, "error": f"Task {task_id} not found"}

    # Ensure the task belongs to the authenticated user
    if db_task.user_id != user_id:
        return {"success": False, "error": "Access denied. Task does not belong to user"}

    # Mark the task as completed
    db_task.completed = True
    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    # Convert to dict for return
    task_dict = {
        "id": str(db_task.id),
        "user_id": db_task.user_id,
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed,
        "updated_at": db_task.updated_at.isoformat()
    }

    # Return simplified version for user display
    simplified_task = {
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed
    }

    return {"success": True, "task": task_dict, "display_task": simplified_task}