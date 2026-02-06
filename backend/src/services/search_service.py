from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from src.models.task_model import Task


class SearchService:
    """
    Service class for handling search, filter, and sort functionality
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def search_tasks(self, user_id: str, query: str) -> List[Task]:
        """
        Search tasks by title, description, or tags
        """
        # Build the search query
        search_query = select(Task).where(Task.user_id == user_id)
        
        # Add search conditions for title and description
        if query:
            search_query = search_query.where(
                Task.title.ilike(f"%{query}%") | 
                Task.description.ilike(f"%{query}%")
            )
        
        # Execute and return results
        tasks = self.db.exec(search_query).all()
        return tasks
    
    def filter_tasks(self, 
                     user_id: str, 
                     completed: Optional[bool] = None,
                     priority: Optional[int] = None,
                     due_after: Optional[datetime] = None,
                     due_before: Optional[datetime] = None,
                     tags: Optional[List[str]] = None,
                     recurring: Optional[bool] = None) -> List[Task]:
        """
        Filter tasks by various criteria
        """
        # Build the base query
        filter_query = select(Task).where(Task.user_id == user_id)
        
        # Apply filters
        if completed is not None:
            filter_query = filter_query.where(Task.completed == completed)
        
        if priority is not None:
            filter_query = filter_query.where(Task.priority == priority)
        
        if due_after is not None:
            filter_query = filter_query.where(Task.due_date >= due_after)
        
        if due_before is not None:
            filter_query = filter_query.where(Task.due_date <= due_before)
        
        if tags:
            # Filter by tags - tasks that have any of the specified tags
            for tag in tags:
                filter_query = filter_query.where(Task.tags.contains(tag))
        
        if recurring is not None:
            if recurring:
                filter_query = filter_query.where(Task.recurring_interval.is_not(None))
            else:
                filter_query = filter_query.where(Task.recurring_interval.is_(None))
        
        # Execute and return results
        tasks = self.db.exec(filter_query).all()
        return tasks
    
    def sort_tasks(self, 
                   tasks: List[Task], 
                   sort_by: str = "created_at", 
                   sort_order: str = "asc") -> List[Task]:
        """
        Sort tasks by specified field and order
        """
        # Define a mapping for sort fields to actual model attributes
        sort_mapping = {
            "title": lambda t: t.title.lower(),
            "priority": lambda t: t.priority,
            "due_date": lambda t: t.due_date or datetime.min,
            "created_at": lambda t: t.created_at,
            "updated_at": lambda t: t.updated_at,
            "completed": lambda t: t.completed
        }
        
        if sort_by not in sort_mapping:
            sort_by = "created_at"  # Default sort field
        
        # Get the sort key function
        sort_key = sort_mapping[sort_by]
        
        # Sort the tasks
        sorted_tasks = sorted(tasks, key=sort_key, reverse=(sort_order.lower() == "desc"))
        
        return sorted_tasks
    
    def search_and_filter_tasks(self,
                                user_id: str,
                                query: Optional[str] = None,
                                completed: Optional[bool] = None,
                                priority: Optional[int] = None,
                                due_after: Optional[datetime] = None,
                                due_before: Optional[datetime] = None,
                                tags: Optional[List[str]] = None,
                                recurring: Optional[bool] = None,
                                sort_by: str = "created_at",
                                sort_order: str = "asc") -> List[Task]:
        """
        Combined search, filter, and sort functionality
        """
        # First, filter tasks
        filtered_tasks = self.filter_tasks(
            user_id=user_id,
            completed=completed,
            priority=priority,
            due_after=due_after,
            due_before=due_before,
            tags=tags,
            recurring=recurring
        )
        
        # Then, if a search query is provided, further filter the results
        if query:
            filtered_tasks = [
                task for task in filtered_tasks
                if query.lower() in task.title.lower() or 
                   (task.description and query.lower() in task.description.lower())
            ]
        
        # Finally, sort the results
        sorted_tasks = self.sort_tasks(filtered_tasks, sort_by, sort_order)
        
        return sorted_tasks