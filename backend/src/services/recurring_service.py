from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from src.models.task_model import Task
from src.dapr.dapr_client import dapr_service
from src.dapr.pubsub import task_events_pubsub
import json


class RecurringService:
    """
    Service class for handling recurring task logic
    """
    
    def __init__(self):
        pass
    
    def calculate_next_occurrence(self, task: Task) -> Optional[datetime]:
        """
        Calculate the next occurrence date based on the recurring interval
        """
        if not task.recurring_interval or not task.due_date:
            return None
            
        current_due_date = task.due_date
        
        if task.recurring_interval == "daily":
            return current_due_date + timedelta(days=1)
        elif task.recurring_interval == "weekly":
            return current_due_date + timedelta(weeks=1)
        elif task.recurring_interval == "monthly":
            # For monthly, we add 1 month (approximately 30 days)
            # In a real implementation, we'd handle month-end dates properly
            return current_due_date + timedelta(days=30)
        elif task.recurring_interval == "yearly":
            return current_due_date + timedelta(days=365)
        else:
            return None
    
    def create_next_occurrence(self, original_task: Task) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task
        """
        next_due_date = self.calculate_next_occurrence(original_task)
        
        if not next_due_date:
            return None
        
        # Create a new task with the same properties as the original
        # but reset completion status and update due date
        new_task = Task(
            title=original_task.title,
            description=original_task.description,
            completed=False,  # Reset completion status
            due_date=next_due_date,
            priority=original_task.priority,
            parsed_tags=original_task.parsed_tags,
            recurring_interval=original_task.recurring_interval,  # Preserve recurrence
            user_id=original_task.user_id
        )
        
        # In a real implementation, we would save this to the database
        # For now, we'll just return the new task object
        return new_task
    
    async def handle_task_completion(self, completed_task: Task) -> Optional[Task]:
        """
        Handle the completion of a task, creating the next occurrence if it's recurring
        """
        # If the task is recurring, create the next occurrence
        if completed_task.recurring_interval:
            next_occurrence = self.create_next_occurrence(completed_task)
            
            if next_occurrence:
                # In a real implementation, we would save the new task to the database
                # For now, we'll simulate publishing an event for the new task creation
                
                task_event_data = {
                    "task_id": str(next_occurrence.id),
                    "event_type": "recurring_created",
                    "user_id": next_occurrence.user_id,
                    "timestamp": datetime.now().isoformat(),
                    "payload": {
                        "title": next_occurrence.title,
                        "due_date": next_occurrence.due_date.isoformat() if next_occurrence.due_date else None,
                        "priority": next_occurrence.priority,
                        "tags": next_occurrence.parsed_tags,
                        "recurring_interval": next_occurrence.recurring_interval
                    }
                }
                
                # Publish the recurring task created event
                await task_events_pubsub.publish_task_event("task-events", task_event_data)
                
                return next_occurrence
        
        return None