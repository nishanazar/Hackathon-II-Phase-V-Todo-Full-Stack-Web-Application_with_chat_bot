"""
MCP (Model Context Protocol) Server Implementation
"""
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server to None by default to avoid import errors
mcp_server = None
mcp_available = False

# Try to initialize MCP server only if the module is available
try:
    import mcp
    from mcp.server import Server
    from mcp.shared.exceptions import McpError

    # Initialize the MCP server
    mcp_server = Server("todo-chat-mcp")

    # Import the MCP tools
    from services.mcp_tools import (
        create_conversation,
        add_message,
        get_conversation_history,
        list_user_conversations,
        update_message
    )

    mcp_available = True
except ImportError:
    # Handle the case where MCP is not available
    logger.warning("MCP library not available. Server will start without MCP functionality.")
    mcp_server = None
    mcp_available = False

# Register the tools with the MCP server
# Note: The exact registration method depends on the MCP server implementation
# This is a placeholder - you may need to adjust based on the actual API

# Define the tools
def tool_create_conversation(user_id: str):
    """
    Creates a new conversation record in the database.

    Args:
        user_id (str): The ID of the user creating the conversation

    Returns:
        Dict: Contains conversation_id and created_at
    """
    from services.mcp_tools import create_conversation
    return create_conversation(user_id)


def tool_add_message(conversation_id: str, user_id: str, role: str, content: str):
    """
    Adds a message to an existing conversation.

    Args:
        conversation_id (str): The ID of the conversation to add the message to
        user_id (str): The ID of the user adding the message
        role (str): Either "user" or "assistant"
        content (str): The content of the message

    Returns:
        Dict: Contains message_id and created_at
    """
    from services.mcp_tools import add_message
    return add_message(conversation_id, user_id, role, content)


def tool_get_conversation_history(conversation_id: str, user_id: str):
    """
    Retrieves all messages in a conversation.

    Args:
        conversation_id (str): The ID of the conversation to retrieve
        user_id (str): The ID of the user requesting the history

    Returns:
        Dict: Contains messages array and conversation_info
    """
    from services.mcp_tools import get_conversation_history
    return get_conversation_history(conversation_id, user_id)


def tool_list_user_conversations(user_id: str, limit: int = 20, offset: int = 0):
    """
    Lists all conversations belonging to a user.

    Args:
        user_id (str): The ID of the user whose conversations to list
        limit (int): Maximum number of conversations to return (default: 20)
        offset (int): Number of conversations to skip (default: 0)

    Returns:
        Dict: Contains conversations array and total_count
    """
    from services.mcp_tools import list_user_conversations
    return list_user_conversations(user_id, limit, offset)


def tool_update_message(message_id: str, user_id: str, content: str):
    """
    Updates the content of an existing message.

    Args:
        message_id (str): The ID of the message to update
        user_id (str): The ID of the user requesting the update
        content (str): The new content for the message

    Returns:
        Dict: Contains updated_at
    """
    from services.mcp_tools import update_message
    return update_message(message_id, user_id, content)

# Conditionally register tools if MCP is available
if mcp_available:
    try:
        # Register the tools with the MCP server
        mcp_server.register_tool("create_conversation")(tool_create_conversation)
        mcp_server.register_tool("add_message")(tool_add_message)
        mcp_server.register_tool("get_conversation_history")(tool_get_conversation_history)
        mcp_server.register_tool("list_user_conversations")(tool_list_user_conversations)
        mcp_server.register_tool("update_message")(tool_update_message)

        logger.info("MCP tools registered successfully.")
    except Exception as e:
        logger.error(f"Failed to register MCP tools: {str(e)}")
        logger.warning("Server will start without MCP tools.")
else:
    logger.warning("MCP is not available. Server will start without MCP functionality.")