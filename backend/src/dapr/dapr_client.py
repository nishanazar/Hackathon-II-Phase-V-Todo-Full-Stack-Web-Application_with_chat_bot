"""
Dapr Client for integration with Dapr sidecar
"""
import asyncio
from dapr.aio.clients import DaprClient
from typing import Dict, Any, Optional
import os


class DaprService:
    """
    Singleton class to manage Dapr client connections
    """
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DaprService, cls).__new__(cls)
        return cls._instance
    
    @property
    def client(self) -> DaprClient:
        if self._client is None:
            # Initialize the Dapr client
            # In production, Dapr handles the connection automatically
            self._client = DaprClient()
        return self._client
    
    async def publish_event(self, pubsub_name: str, topic_name: str, data: Dict[str, Any]) -> None:
        """
        Publish an event to a Dapr pub/sub topic
        """
        async with self.client as client:
            await client.publish_event(
                pubsub_name=pubsub_name,
                topic_name=topic_name,
                data=data,
                data_content_type='application/json',
            )
    
    async def invoke_method(self, app_id: str, method: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invoke a method on another Dapr-enabled service
        """
        async with self.client as client:
            response = await client.invoke_method(
                app_id=app_id,
                method_name=method,
                data=data,
            )
            return response
        
    async def save_state(self, store_name: str, key: str, value: Any) -> None:
        """
        Save state using Dapr state management
        """
        async with self.client as client:
            await client.save_state(store_name, key, value)
            
    async def get_state(self, store_name: str, key: str) -> Any:
        """
        Get state using Dapr state management
        """
        async with self.client as client:
            response = await client.get_state(store_name, key)
            return response.data
            
    async def delete_state(self, store_name: str, key: str) -> None:
        """
        Delete state using Dapr state management
        """
        async with self.client as client:
            await client.delete_state(store_name, key)


# Global instance
dapr_service = DaprService()