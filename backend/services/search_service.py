from sqlmodel import Session, select
from models import Task
from typing import List, Optional
from datetime import datetime
import json


def search_tasks(
    db: Session,
    user_id: str,
    search_query: Optional[str] = None,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    tags_filter: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "asc"
) -> List[Task]:
    """
    Search tasks with multiple criteria including text search, filters, and sorting.
    """
    query = select(Task).where(Task.user_id == user_id)

    # Apply text search if provided
    if search_query:
        # Search in title and description
        query = query.where(
            (Task.title.ilike(f"%{search_query}%")) |
            (Task.description.ilike(f"%{search_query}%"))
        )

    # Apply status filter if specified
    if status_filter == "pending":
        query = query.where(Task.completed == False)
    elif status_filter == "completed":
        query = query.where(Task.completed == True)

    # Apply priority filter if specified
    if priority_filter:
        query = query.where(Task.priority == priority_filter)

    # Apply due date range filter if specified
    if due_date_from:
        query = query.where(Task.due_date >= due_date_from)
    if due_date_to:
        query = query.where(Task.due_date <= due_date_to)

    # Apply tags filter if specified
    if tags_filter:
        tag_list = tags_filter.split(',')
        for tag in tag_list:
            # Since tags are stored as JSON strings, we need to search within the JSON
            query = query.where(Task.tags.like(f'%{tag.strip()}%'))

    # Apply sorting
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
    elif sort_by == "title":
        if sort_order == "desc":
            query = query.order_by(Task.title.desc())
        else:
            query = query.order_by(Task.title.asc())

    tasks = db.exec(query).all()
    return tasks