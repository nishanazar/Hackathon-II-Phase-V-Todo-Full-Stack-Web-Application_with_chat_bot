import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.agents.todo_agent import TodoMasterAI
from src.constants.ai_constants import UNRELATED_QUERY_RESPONSE


@pytest.fixture
def mock_todo_agent():
    """Create a mock TodoMasterAI instance for testing"""
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'fake-api-key'}):
        agent = TodoMasterAI()
        # Mock the client to avoid actual API calls
        agent.client = AsyncMock()
        return agent


@pytest.mark.asyncio
async def test_process_message_with_task_command(mock_todo_agent):
    """Test processing a message that should trigger a task command"""
    # Mock the API response
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_tool_calls = MagicMock()
    
    # Simulate a tool call to add_task
    mock_function = MagicMock()
    mock_function.name = "add_task"
    mock_function.arguments = '{"title": "Buy milk", "description": "Get whole milk"}'
    
    mock_tool_call = MagicMock()
    mock_tool_call.function = mock_function
    mock_tool_call.id = "call_123"
    
    mock_tool_calls.__iter__ = lambda x: iter([mock_tool_call])
    mock_message.tool_calls = [mock_tool_call]
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    mock_final_response = MagicMock()
    mock_final_choice = MagicMock()
    mock_final_message = MagicMock()
    mock_final_message.content = "I've added the task 'Buy milk' for you."
    mock_final_choice.message = mock_final_message
    mock_final_response.choices = [mock_final_choice]
    
    # Set up the mock to return the initial response first, then the final response
    mock_todo_agent.client.chat.completions.create = AsyncMock(side_effect=[mock_response, mock_final_response])
    
    # Mock the add_task function
    with patch('src.agents.todo_agent.add_task', return_value={"success": True, "task": {"id": "task_123", "title": "Buy milk"}}):
        result = await mock_todo_agent.process_message(
            user_message="Add a task to buy milk",
            user_id="user_123",
            session_id="session_123",
            db_session=MagicMock()
        )
        
        assert result["response"] == "I've added the task 'Buy milk' for you."
        assert result["tool_calls"][0]["name"] == "add_task"


@pytest.mark.asyncio
async def test_process_message_with_unrelated_query(mock_todo_agent):
    """Test processing a message that is unrelated to tasks"""
    # Mock the API response without tool calls
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.tool_calls = None
    mock_message.content = "This is a generic response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    mock_todo_agent.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    result = await mock_todo_agent.process_message(
        user_message="What's the weather like today?",
        user_id="user_123",
        session_id="session_123",
        db_session=MagicMock()
    )
    
    # The agent should recognize this as an unrelated query and respond with the fixed message
    assert result["response"] == UNRELATED_QUERY_RESPONSE


@pytest.mark.asyncio
async def test_process_message_with_list_command(mock_todo_agent):
    """Test processing a message that should trigger a list command"""
    # Mock the API response
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_tool_call = MagicMock()
    mock_function = MagicMock()
    
    mock_function.name = "list_tasks"
    mock_function.arguments = '{}'
    mock_tool_call.function = mock_function
    mock_tool_call.id = "call_456"
    
    mock_message.tool_calls = [mock_tool_call]
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    mock_final_response = MagicMock()
    mock_final_choice = MagicMock()
    mock_final_message = MagicMock()
    mock_final_message.content = "Here are your tasks: Buy milk, Walk the dog"
    mock_final_choice.message = mock_final_message
    mock_final_response.choices = [mock_final_choice]
    
    # Set up the mock to return the initial response first, then the final response
    mock_todo_agent.client.chat.completions.create = AsyncMock(side_effect=[mock_response, mock_final_response])
    
    # Mock the list_tasks function
    with patch('src.agents.todo_agent.list_tasks', return_value={"success": True, "tasks": [{"id": "task_1", "title": "Buy milk"}, {"id": "task_2", "title": "Walk the dog"}]}):
        result = await mock_todo_agent.process_message(
            user_message="Show me my tasks",
            user_id="user_123",
            session_id="session_123",
            db_session=MagicMock()
        )
        
        assert result["response"] == "Here are your tasks: Buy milk, Walk the dog"
        assert result["tool_calls"][0]["name"] == "list_tasks"


@pytest.mark.asyncio
async def test_init_without_api_key():
    """Test initializing the agent without an API key"""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable not set"):
            TodoMasterAI()


@pytest.mark.asyncio
async def test_process_message_error_handling(mock_todo_agent):
    """Test error handling in process_message"""
    # Force an exception in the API call
    mock_todo_agent.client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
    
    result = await mock_todo_agent.process_message(
        user_message="Test message",
        user_id="user_123",
        session_id="session_123",
        db_session=MagicMock()
    )
    
    assert "error processing your request" in result["response"]
    assert result["tool_calls"] == []
    assert result["task_created"] is None