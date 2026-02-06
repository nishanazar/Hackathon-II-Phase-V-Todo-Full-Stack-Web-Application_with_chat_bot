import asyncio
import json
from datetime import datetime
from uuid import uuid4

from services.dapr_pubsub_service import publish_task_event

async def test_dapr_pubsub():
    """
    Test script to verify Dapr pub/sub functionality
    """
    print("Testing Dapr pub/sub functionality...")
    
    # Sample task data
    task_data = {
        "id": str(uuid4()),
        "title": "Test Task for Dapr Pub/Sub",
        "description": "This is a test task to verify Dapr pub/sub functionality",
        "completed": False,
        "user_id": "test-user-123",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    # Test publishing a task.created event
    print("Publishing task.created event...")
    success = await publish_task_event("task.created", task_data, "test-user-123")
    if success:
        print("✓ Successfully published task.created event")
    else:
        print("✗ Failed to publish task.created event")
    
    # Test publishing a task.updated event
    print("\nPublishing task.updated event...")
    task_data["completed"] = True
    task_data["updated_at"] = datetime.utcnow().isoformat()
    success = await publish_task_event("task.updated", task_data, "test-user-123")
    if success:
        print("✓ Successfully published task.updated event")
    else:
        print("✗ Failed to publish task.updated event")
    
    # Test publishing a task.deleted event
    print("\nPublishing task.deleted event...")
    success = await publish_task_event("task.deleted", task_data, "test-user-123")
    if success:
        print("✓ Successfully published task.deleted event")
    else:
        print("✗ Failed to publish task.deleted event")
    
    print("\nTest completed. Check the consumer service logs to verify events were received.")

if __name__ == "__main__":
    asyncio.run(test_dapr_pubsub())