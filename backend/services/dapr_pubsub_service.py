import httpx
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from settings import settings

# Dapr pub/sub service to handle publishing events via Dapr
class DaprPubSubService:
    def __init__(self):
        # Dapr sidecar runs on localhost:3500 by default
        self.dapr_url = f"http://localhost:3500"
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def publish_event(self, pubsub_name: str, topic_name: str, data: Dict[str, Any]) -> bool:
        """
        Publish an event to a Dapr pub/sub component
        
        Args:
            pubsub_name: Name of the pub/sub component (e.g., "task-pubsub")
            topic_name: Name of the topic to publish to (e.g., "task-events")
            data: Event data to publish
            
        Returns:
            bool: True if published successfully, False otherwise
        """
        try:
            url = f"{self.dapr_url}/v1.0/publish/{pubsub_name}/{topic_name}"
            
            # Send the event data to Dapr
            response = await self.http_client.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            # Check if the request was successful
            if response.status_code == 204:
                return True
            else:
                print(f"Failed to publish event: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error publishing event: {str(e)}")
            return False

    async def close(self):
        """Close the HTTP client"""
        await self.http_client.aclose()

# Global instance of the Dapr pub/sub service
dapr_pubsub_service = DaprPubSubService()


# Task event schema
class TaskEvent(BaseModel):
    eventType: str
    taskId: str
    userId: str
    timestamp: str
    payload: Dict[str, Any]


async def publish_task_event(event_type: str, task_data: Dict[str, Any], user_id: str) -> bool:
    """
    Helper function to publish a task-related event
    
    Args:
        event_type: Type of event (e.g., "task.created", "task.updated", "task.deleted")
        task_data: Task data to include in the event
        user_id: ID of the user associated with the task
        
    Returns:
        bool: True if published successfully, False otherwise
    """
    from datetime import datetime
    import uuid
    
    # Create the event object
    event = TaskEvent(
        eventType=event_type,
        taskId=str(task_data.get('id', str(uuid.uuid4()))),
        userId=user_id,
        timestamp=datetime.utcnow().isoformat() + "Z",
        payload=task_data
    )
    
    # Publish the event via Dapr
    success = await dapr_pubsub_service.publish_event(
        pubsub_name="task-pubsub",  # This matches the component name in pubsub.yaml
        topic_name="task-events",   # This is the topic name
        data=event.dict()
    )
    
    return success