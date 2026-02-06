from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from src.models.task_model import Task, TaskCreate, TaskUpdate, TaskResponse
from src.dapr.pubsub import task_events_pubsub
from src.services.recurring_service import RecurringService
from src.services.reminder_service import ReminderService
import json


class TaskService:
    """
    Service class for handling task-related business logic
    """

    def __init__(self, db: Session):
        self.db = db
        self.recurring_service = RecurringService()
        self.reminder_service = ReminderService(dapr_service=None)  # Will be set later
    
    def create_task(self, task_create: TaskCreate, user_id: str) -> Task:
        """
        Create a new task with the provided details
        """
        # Create the task with the user_id
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            due_date=task_create.due_date,
            priority=task_create.priority,
            parsed_tags=task_create.parsed_tags,
            recurring_interval=task_create.recurring_interval,
            user_id=user_id
        )

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        # Publish task created event
        task_event_data = {
            "task_id": str(db_task.id),
            "event_type": "created",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "title": db_task.title,
                "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                "priority": db_task.priority,
                "tags": db_task.parsed_tags,
                "recurring_interval": db_task.recurring_interval
            }
        }
        
        # Note: In a real implementation, we would await this async call
        # For now, we'll just define the event data
        print(f"Task created event would be published: {task_event_data}")

        # Schedule reminder if the task has a due date
        if db_task.due_date:
            reminder = self.reminder_service.schedule_reminder(db_task, self.db)
            if reminder:
                print(f"Scheduled reminder for task {db_task.id} at {reminder.scheduled_time}")

        return db_task
    
    def get_task(self, task_id: UUID, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for the given user
        """
        task = self.db.get(Task, task_id)
        
        if task and task.user_id == user_id:
            return task
        return None
    
    def get_tasks(self, user_id: str, completed: Optional[bool] = None, 
                  priority: Optional[int] = None, due_after: Optional[datetime] = None,
                  due_before: Optional[datetime] = None, tags: Optional[List[str]] = None) -> List[Task]:
        """
        Get all tasks for a user with optional filtering
        """
        query = select(Task).where(Task.user_id == user_id)
        
        if completed is not None:
            query = query.where(Task.completed == completed)
        
        if priority is not None:
            query = query.where(Task.priority == priority)
            
        if due_after is not None:
            query = query.where(Task.due_date >= due_after)
            
        if due_before is not None:
            query = query.where(Task.due_date <= due_before)
        
        # Filter by tags if provided
        if tags:
            for tag in tags:
                # This is a simplified tag filtering - in practice, you might need more sophisticated logic
                query = query.where(Task.tags.contains(tag))
        
        tasks = self.db.exec(query).all()
        return tasks
    
    def update_task(self, task_id: UUID, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update a specific task with the provided details
        """
        db_task = self.db.get(Task, task_id)

        if not db_task or db_task.user_id != user_id:
            return None

        # Update the task fields that were provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "parsed_tags":
                setattr(db_task, "parsed_tags", value)
            else:
                setattr(db_task, field, value)

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        # Publish task updated event
        task_event_data = {
            "task_id": str(db_task.id),
            "event_type": "updated",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "title": db_task.title,
                "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                "priority": db_task.priority,
                "tags": db_task.parsed_tags,
                "recurring_interval": db_task.recurring_interval,
                "completed": db_task.completed
            }
        }

        # Note: In a real implementation, we would await this async call
        print(f"Task updated event would be published: {task_event_data}")

        return db_task
    
    def delete_task(self, task_id: UUID, user_id: str) -> bool:
        """
        Delete a specific task
        """
        db_task = self.db.get(Task, task_id)
        
        if not db_task or db_task.user_id != user_id:
            return False
        
        self.db.delete(db_task)
        self.db.commit()
        
        return True
    
    async def complete_task(self, task_id: UUID, user_id: str) -> Optional[Task]:
        """
        Mark a task as completed
        """
        db_task = self.db.get(Task, task_id)

        if not db_task or db_task.user_id != user_id:
            return None

        db_task.completed = True
        db_task.updated_at = datetime.now()

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        # Publish task completed event
        task_event_data = {
            "task_id": str(db_task.id),
            "event_type": "completed",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "title": db_task.title,
                "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                "priority": db_task.priority,
                "tags": db_task.parsed_tags,
                "recurring_interval": db_task.recurring_interval
            }
        }

        # Note: In a real implementation, we would await this async call
        print(f"Task completed event would be published: {task_event_data}")

        # Handle recurring task logic if applicable
        if db_task.recurring_interval:
            next_occurrence = await self.recurring_service.handle_task_completion(db_task)
            if next_occurrence:
                # Add the new occurrence to the database
                self.db.add(next_occurrence)
                self.db.commit()
                self.db.refresh(next_occurrence)
                print(f"Created next occurrence of recurring task: {next_occurrence.id}")

        return db_task