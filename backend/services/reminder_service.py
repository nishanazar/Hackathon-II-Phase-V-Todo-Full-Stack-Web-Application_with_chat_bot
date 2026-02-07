from sqlmodel import Session, select
from models import Task
from datetime import datetime, timedelta
from typing import List
import asyncio
import threading
from queue import Queue
import time


class ReminderService:
    """
    Service for handling task reminders using Dapr pub/sub or scheduled jobs.
    This implementation includes a basic scheduler for demonstration purposes.
    """
    
    def __init__(self):
        self.reminder_queue = Queue()
        self.running = False
        self.scheduler_thread = None
    
    def start_scheduler(self):
        """Start the reminder scheduler in a separate thread."""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the reminder scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
    
    def _scheduler_loop(self):
        """Main loop for checking and sending reminders."""
        while self.running:
            # Check for tasks that need reminders
            self._check_for_reminders()
            
            # Sleep for 60 seconds before next check
            time.sleep(60)
    
    def _check_for_reminders(self):
        """Check for tasks that need reminders and send them."""
        # This is a simplified implementation
        # In a real application, this would connect to Dapr or a job scheduler
        print("Checking for reminders...")
    
    def schedule_reminder(self, task_id: str, reminder_time: datetime, user_id: str):
        """Schedule a reminder for a specific task."""
        # In a real implementation, this would use Dapr Jobs API or Kafka pub/sub
        print(f"Scheduled reminder for task {task_id} at {reminder_time} for user {user_id}")
        
        # Add to internal queue for processing
        reminder_data = {
            'task_id': task_id,
            'reminder_time': reminder_time,
            'user_id': user_id
        }
        self.reminder_queue.put(reminder_data)
    
    def get_upcoming_reminders(self, db: Session, user_id: str, hours_ahead: int = 24) -> List[Task]:
        """Get tasks that have due dates within the specified hours ahead."""
        cutoff_time = datetime.now() + timedelta(hours=hours_ahead)
        
        query = select(Task).where(
            (Task.user_id == user_id) & 
            (Task.due_date.is_not(None)) & 
            (Task.due_date <= cutoff_time) & 
            (Task.completed == False)
        ).order_by(Task.due_date.asc())
        
        upcoming_tasks = db.exec(query).all()
        return upcoming_tasks


# Global instance of the reminder service
reminder_service = ReminderService()