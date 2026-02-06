from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from src.models.reminder_model import Reminder, ReminderCreate
from src.models.task_model import Task
from src.dapr.dapr_client import dapr_service
from sqlmodel import Session, select


class ReminderService:
    """
    Service class for handling reminder scheduling and delivery
    """
    
    def __init__(self, dapr_service):
        self.dapr_service = dapr_service
    
    def schedule_reminder(self, task: Task, db: Session) -> Optional[Reminder]:
        """
        Schedule a reminder for a task based on its due date
        """
        if not task.due_date:
            return None
            
        # Schedule reminder 24 hours before due date, or at least 1 hour before if due date is soon
        time_diff = task.due_date - datetime.now()
        if time_diff.total_seconds() > 0:
            if time_diff.total_seconds() > 24 * 3600:  # More than 24 hours
                reminder_time = task.due_date - timedelta(hours=24)
            elif time_diff.total_seconds() > 3600:  # More than 1 hour
                reminder_time = task.due_date - timedelta(hours=1)
            else:  # Less than 1 hour, set for 10 minutes before
                reminder_time = task.due_date - timedelta(minutes=10)
        else:
            # Task is already overdue, don't schedule a reminder
            return None
        
        # Create reminder
        reminder_create = ReminderCreate(
            task_id=task.id,
            scheduled_time=reminder_time,
            user_id=task.user_id
        )
        
        reminder = Reminder.from_orm(reminder_create) if hasattr(Reminder, 'from_orm') else Reminder(
            task_id=reminder_create.task_id,
            scheduled_time=reminder_create.scheduled_time,
            user_id=reminder_create.user_id
        )
        
        # In a real implementation, we would schedule this with Dapr
        # For now, we'll just save it to the database
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return reminder
    
    def get_upcoming_reminders(self, db: Session, from_time: datetime) -> list[Reminder]:
        """
        Get all reminders scheduled from a specific time onwards that haven't been sent yet
        """
        reminders = db.exec(
            select(Reminder)
            .where(Reminder.scheduled_time >= from_time)
            .where(Reminder.sent == False)
        ).all()
        
        return reminders
    
    def mark_as_sent(self, reminder_id: UUID, db: Session) -> bool:
        """
        Mark a reminder as sent
        """
        reminder = db.get(Reminder, reminder_id)
        if reminder:
            reminder.sent = True
            reminder.sent_time = datetime.now()
            db.add(reminder)
            db.commit()
            return True
        return False
    
    async def send_reminder_notification(self, reminder: Reminder, task: Task):
        """
        Send the actual reminder notification to the user
        """
        # In a real implementation, this would send an email, push notification, etc.
        # For now, we'll just log it
        
        print(f"Sending reminder to user {reminder.user_id} for task '{task.title}' due at {task.due_date}")
        
        # Publish reminder sent event
        reminder_event_data = {
            "reminder_id": str(reminder.id),
            "task_id": str(task.id),
            "user_id": reminder.user_id,
            "scheduled_time": reminder.scheduled_time.isoformat(),
            "sent_time": datetime.now().isoformat(),
            "task_title": task.title,
            "task_due_date": task.due_date.isoformat() if task.due_date else None
        }
        
        # In a real implementation, we would await this async call
        print(f"Reminder sent event would be published: {reminder_event_data}")