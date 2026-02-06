"""
MCP (Model Context Protocol) Tools Implementation
Implements the 5 required tools for the Todo AI Chatbot
"""
import logging
import sys
import os
from typing import Dict, List, Optional
from datetime import datetime
from sqlmodel import Session, select
from uuid import uuid4

# Add the backend directory to the Python path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, backend_dir)

from models import Conversation, Message
from db import engine
from utils.auth import verify_user_access

# Set up logging
logger = logging.getLogger(__name__)


def create_conversation(user_id: str) -> Dict:
    """
    Creates a new conversation record in the database.

    Args:
        user_id (str): The ID of the user creating the conversation

    Returns:
        Dict: Contains conversation_id and created_at
    """
    logger.info(f"Creating conversation for user: {user_id}")
    try:
        with Session(engine) as session:
            # Verify user access
            if not verify_user_access(user_id):
                logger.warning(f"Invalid user access for user_id: {user_id}")
                raise Exception("invalid_user_id")

            # Create new conversation
            conversation = Conversation(
                id=str(uuid4()),
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            logger.info(f"Successfully created conversation: {conversation.id}")
            return {
                "conversation_id": conversation.id,
                "created_at": conversation.created_at.isoformat()
            }
    except Exception as e:
        logger.error(f"Failed to create conversation for user {user_id}: {str(e)}")
        raise Exception(f"Failed to create conversation: {str(e)}")


def add_message(conversation_id: str, user_id: str, role: str, content: str) -> Dict:
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
    logger.info(f"Adding message to conversation {conversation_id} for user {user_id}")
    try:
        with Session(engine) as session:
            # Verify user access
            if not verify_user_access(user_id):
                logger.warning(f"Invalid user access for user_id: {user_id}")
                raise Exception("invalid_user_id")

            # Validate role
            if role not in ["user", "assistant"]:
                logger.warning(f"Invalid role '{role}' for user {user_id}")
                raise Exception("invalid_role")

            # Validate content
            if not content.strip():
                logger.warning(f"Empty content provided by user {user_id}")
                raise Exception("empty_content")

            # Verify conversation exists and belongs to user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                logger.warning(f"Conversation {conversation_id} not found or doesn't belong to user {user_id}")
                raise Exception("conversation_not_found")

            # Create new message
            message = Message(
                id=str(uuid4()),
                user_id=user_id,
                conversation_id=conversation_id,
                role=role,
                content=content,
                created_at=datetime.utcnow()
            )

            session.add(message)
            session.commit()
            session.refresh(message)

            # Update conversation's updated_at
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()

            logger.info(f"Successfully added message {message.id} to conversation {conversation_id}")
            return {
                "message_id": message.id,
                "created_at": message.created_at.isoformat()
            }
    except Exception as e:
        logger.error(f"Failed to add message to conversation {conversation_id} for user {user_id}: {str(e)}")
        raise Exception(f"Failed to add message: {str(e)}")


def get_conversation_history(conversation_id: str, user_id: str) -> Dict:
    """
    Retrieves all messages in a conversation.

    Args:
        conversation_id (str): The ID of the conversation to retrieve
        user_id (str): The ID of the user requesting the history

    Returns:
        Dict: Contains messages array and conversation_info
    """
    logger.info(f"Retrieving conversation history for conversation {conversation_id} and user {user_id}")
    try:
        with Session(engine) as session:
            # Verify user access
            if not verify_user_access(user_id):
                logger.warning(f"Invalid user access for user_id: {user_id}")
                raise Exception("invalid_user_id")

            # Verify conversation exists and belongs to user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                logger.warning(f"Conversation {conversation_id} not found or doesn't belong to user {user_id}")
                raise Exception("conversation_not_found")

            # Get all messages for this conversation
            messages_query = select(Message).where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            ).order_by(Message.created_at)

            messages = session.exec(messages_query).all()

            # Format messages
            formatted_messages = [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat()
                }
                for msg in messages
            ]

            # Format conversation info
            conversation_info = {
                "id": conversation.id,
                "user_id": conversation.user_id,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat()
            }

            logger.info(f"Successfully retrieved {len(formatted_messages)} messages from conversation {conversation_id}")
            return {
                "messages": formatted_messages,
                "conversation_info": conversation_info
            }
    except Exception as e:
        logger.error(f"Failed to get conversation history for conversation {conversation_id} and user {user_id}: {str(e)}")
        raise Exception(f"Failed to get conversation history: {str(e)}")


def list_user_conversations(user_id: str, limit: int = 20, offset: int = 0) -> Dict:
    """
    Lists all conversations belonging to a user.

    Args:
        user_id (str): The ID of the user whose conversations to list
        limit (int): Maximum number of conversations to return (default: 20)
        offset (int): Number of conversations to skip (default: 0)

    Returns:
        Dict: Contains conversations array and total_count
    """
    logger.info(f"Listing conversations for user {user_id} with limit {limit} and offset {offset}")
    try:
        with Session(engine) as session:
            # Verify user access
            if not verify_user_access(user_id):
                logger.warning(f"Invalid user access for user_id: {user_id}")
                raise Exception("invalid_user_id")

            # Count total conversations for user
            count_query = select(Conversation).where(Conversation.user_id == user_id)
            total_count = len(session.exec(count_query).all())

            # Get conversations with limit and offset
            conversations_query = select(Conversation).where(
                Conversation.user_id == user_id
            ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)

            conversations = session.exec(conversations_query).all()

            # Format conversations
            formatted_conversations = [
                {
                    "id": conv.id,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ]

            logger.info(f"Successfully retrieved {len(formatted_conversations)} conversations for user {user_id}")
            return {
                "conversations": formatted_conversations,
                "total_count": total_count
            }
    except Exception as e:
        logger.error(f"Failed to list conversations for user {user_id}: {str(e)}")
        raise Exception(f"Failed to list user conversations: {str(e)}")


def update_message(message_id: str, user_id: str, content: str) -> Dict:
    """
    Updates the content of an existing message.

    Args:
        message_id (str): The ID of the message to update
        user_id (str): The ID of the user requesting the update
        content (str): The new content for the message

    Returns:
        Dict: Contains updated_at
    """
    logger.info(f"Updating message {message_id} for user {user_id}")
    try:
        with Session(engine) as session:
            # Verify user access
            if not verify_user_access(user_id):
                logger.warning(f"Invalid user access for user_id: {user_id}")
                raise Exception("invalid_user_id")

            # Validate content
            if not content.strip():
                logger.warning(f"Empty content provided by user {user_id} for message {message_id}")
                raise Exception("empty_content")

            # Get the message and verify it belongs to the user
            message = session.get(Message, message_id)
            if not message or message.user_id != user_id:
                logger.warning(f"Message {message_id} not found or doesn't belong to user {user_id}")
                raise Exception("message_not_found")

            # Update the message content
            message.content = content
            session.add(message)
            session.commit()

            logger.info(f"Successfully updated message {message_id}")
            return {
                "updated_at": message.updated_at.isoformat()
            }
    except Exception as e:
        logger.error(f"Failed to update message {message_id} for user {user_id}: {str(e)}")
        raise Exception(f"Failed to update message: {str(e)}")