from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import UUID

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: UUID
    response: str
    tool_calls: List[Dict] = []
    task_created: Optional[Dict] = None


ChatResponse.model_rebuild()