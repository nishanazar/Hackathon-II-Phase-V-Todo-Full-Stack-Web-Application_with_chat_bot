import asyncio
from typing import Dict, Any
import json

try:
    import dapr.aio.clients as dapr_clients
    DAPR_AVAILABLE = True
except ImportError:
    DAPR_AVAILABLE = False
    print("Dapr SDK not available. Install with 'pip install dapr'")

class DaprClient:
    """
    Client for interacting with Dapr runtime for pub/sub functionality.
    """
    
    def __init__(self):
        self.client = None
        if DAPR_AVAILABLE:
            self.client = dapr_clients.DaprClient()
        else:
            print("Dapr client not initialized - Dapr SDK not available")
    
    async def publish_task_event(self, event_type: str, task_data: Dict[str, Any]):
        """
        Publish a task event to the task-pubsub component.
        """
        if not self.client:
            print("Dapr client not available, skipping event publishing")
            return
        
        # Prepare the event payload
        event_payload = {
            "eventType": event_type,
            "timestamp": asyncio.get_event_loop().time(),
            "payload": task_data
        }
        
        try:
            # Publish the event to the task-pubsub component
            await self.client.publish_event(
                pubsub_name="task-pubsub",
                topic_name="task-events",
                data=json.dumps(event_payload),
                data_content_type="application/json"
            )
            print(f"Published {event_type} event for task {task_data.get('id', 'unknown')}")
        except Exception as e:
            print(f"Error publishing event: {str(e)}")
    
    async def close(self):
        """
        Close the Dapr client connection.
        """
        if self.client:
            await self.client.close()

# Global instance of the Dapr client
dapr_client = DaprClient()