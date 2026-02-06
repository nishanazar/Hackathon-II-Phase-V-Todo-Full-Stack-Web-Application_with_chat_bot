from fastapi import FastAPI, BackgroundTasks, Request
import logging
import json
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task Event Consumer", version="1.0.0")

@app.post("/tasks/events")
async def handle_task_event(request: Request):
    """
    Handle incoming task events from Dapr pub/sub
    """
    try:
        # Get the raw body to access Dapr metadata
        body = await request.body()
        event_data = json.loads(body.decode())
        
        # Log the received event
        logger.info(f"Received task event: {event_data}")
        
        # Extract event information
        event_type = event_data.get("eventType", "unknown")
        task_id = event_data.get("taskId", "unknown")
        user_id = event_data.get("userId", "unknown")
        timestamp = event_data.get("timestamp", "unknown")
        payload = event_data.get("payload", {})
        
        # Log specific details based on event type
        if event_type == "task.created":
            logger.info(f"Task created: ID={task_id}, User={user_id}, Title='{payload.get('title', 'N/A')}'")
        elif event_type == "task.updated":
            logger.info(f"Task updated: ID={task_id}, User={user_id}, Title='{payload.get('title', 'N/A')}'")
        elif event_type == "task.deleted":
            logger.info(f"Task deleted: ID={task_id}, User={user_id}")
        else:
            logger.info(f"Unknown event type: {event_type}")
        
        # Process the event based on type
        if event_type == "task.created":
            # Handle task creation event
            await handle_task_created(payload)
        elif event_type == "task.updated":
            # Handle task update event
            await handle_task_updated(payload)
        elif event_type == "task.deleted":
            # Handle task deletion event
            await handle_task_deleted(payload)
        else:
            logger.warning(f"Unknown event type received: {event_type}")
        
        # Return success response to acknowledge the event
        return {"status": "success", "message": "Event processed successfully"}
        
    except Exception as e:
        logger.error(f"Error processing task event: {str(e)}")
        # Return error response to trigger Dapr retry mechanism
        return {"status": "error", "message": str(e)}, 500


async def handle_task_created(task_data: Dict[str, Any]):
    """
    Handle task creation event
    """
    logger.info(f"Processing task creation: {task_data.get('title', 'N/A')}")


async def handle_task_updated(task_data: Dict[str, Any]):
    """
    Handle task update event
    """
    logger.info(f"Processing task update: {task_data.get('title', 'N/A')}")


async def handle_task_deleted(task_data: Dict[str, Any]):
    """
    Handle task deletion event
    """
    logger.info(f"Processing task deletion: {task_data.get('title', 'N/A')}")


@app.get("/")
def read_root():
    return {"message": "Task Event Consumer Service"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}