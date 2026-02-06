import asyncio
import os
import json
import re
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from .mcp_tools import add_task, list_tasks, update_task, delete_task, complete_task
from ..constants.ai_constants import (
    GEMINI_MODEL_NAME,
    GEMINI_BASE_URL,
    GEMINI_API_KEY_ENV,
    TASK_ONLY_SYSTEM_PROMPT,
    UNRELATED_QUERY_RESPONSE
)
from ..models.chat_message import ChatMessageCreate
from ..services.chat_message_service import create_chat_message, get_chat_messages_by_session
from ..services.chat_session_service import get_chat_session_by_id
from ..utils.logger import log_ai_interaction, log_error
from sqlmodel import Session
from settings import settings
import time
from functools import wraps


class TodoMasterAI:
    """
    AI agent for managing user tasks through natural language commands
    """

    def __init__(self):
        # Get API key from settings
        api_key = settings.gemini_api_key
        if not api_key:
            raise ValueError(f"{GEMINI_API_KEY_ENV} environment variable not set")

        # Configure AsyncOpenAI with Gemini endpoint
        self.client = AsyncOpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key
        )

        # Define the model
        self.model = GEMINI_MODEL_NAME

        # Define the system prompt
        self.system_prompt = TASK_ONLY_SYSTEM_PROMPT

        # Define the tools available to the agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "The description of the task"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "The new title of the task (optional)"},
                            "description": {"type": "string", "description": "The new description of the task (optional)"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to delete (optional if title is provided)"},
                            "title": {"type": "string", "description": "The title of the task to delete (optional if task_id is provided)"}
                        },
                        "required": []  # Neither parameter is required since one of them can be provided
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to complete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

        # Initialize cache for conversation history to reduce DB calls
        self.conversation_cache = {}
        # Cache for user tasks to reduce DB calls
        self.tasks_cache = {}
        # Cache TTL in seconds (5 minutes)
        self.cache_ttl = 300

    def _get_cache_key(self, session_id: str) -> str:
        """Generate a cache key for a session"""
        return f"conv_{session_id}"

    def _is_cache_valid(self, cached_item: dict) -> bool:
        """Check if cached item is still valid based on TTL"""
        if not cached_item or 'timestamp' not in cached_item:
            return False
        return time.time() - cached_item['timestamp'] < self.cache_ttl

    def _cache_conversation_history(self, session_id: str, history: list):
        """Cache conversation history"""
        cache_key = self._get_cache_key(session_id)
        self.conversation_cache[cache_key] = {
            'history': history,
            'timestamp': time.time()
        }

    def _get_cached_conversation_history(self, session_id: str) -> Optional[list]:
        """Get cached conversation history if valid"""
        cache_key = self._get_cache_key(session_id)
        cached_item = self.conversation_cache.get(cache_key)
        if self._is_cache_valid(cached_item):
            return cached_item['history']
        # Remove expired cache entry
        if cached_item:
            del self.conversation_cache[cache_key]
        return None

    def _get_tasks_cache_key(self, user_id: str) -> str:
        """Generate a cache key for user tasks"""
        return f"tasks_{user_id}"

    def _cache_user_tasks(self, user_id: str, tasks: list):
        """Cache user tasks"""
        cache_key = self._get_tasks_cache_key(user_id)
        self.tasks_cache[cache_key] = {
            'tasks': tasks,
            'timestamp': time.time()
        }

    def _get_cached_user_tasks(self, user_id: str) -> Optional[list]:
        """Get cached user tasks if valid"""
        cache_key = self._get_tasks_cache_key(user_id)
        cached_item = self.tasks_cache.get(cache_key)
        if self._is_cache_valid(cached_item):
            return cached_item['tasks']
        # Remove expired cache entry
        if cached_item:
            del self.tasks_cache[cache_key]
        return None

    async def process_message(self, user_message: str, user_id: str, session_id: Optional[str] = None, db_session: Session = None) -> Dict[str, Any]:
        """
        Process a user message and return the AI agent's response
        """

        # Quick response for simple greetings to improve response time
        normalized_message = user_message.strip().lower()
        if normalized_message in ["hello", "hi", "hey", "hello!", "hi!", "hey!", "greetings", "good morning", "good afternoon", "good evening"]:
            quick_response = f"Hello! I'm your AI assistant for managing tasks. You can ask me to add, list, update, or complete tasks."

            # Store the user message in the database
            if db_session and session_id:
                user_msg = ChatMessageCreate(
                    chat_session_id=session_id,
                    role="user",
                    content=user_message
                )
                create_chat_message(session=db_session, chat_message_create=user_msg)

                # Store the AI response in the database
                ai_msg = ChatMessageCreate(
                    chat_session_id=session_id,
                    role="assistant",
                    content=quick_response
                )
                create_chat_message(session=db_session, chat_message_create=ai_msg)

            # Log the interaction
            log_ai_interaction(user_id, user_message, quick_response, session_id)

            return {
                "response": quick_response,
                "session_id": session_id,
                "tool_calls": [],
                "task_created": None
            }

        # Check if the user wants to complete a task by title directly
        # Look for patterns like "task [title] is completed", "mark [title] as completed", etc.

        # Multiple patterns to match different ways users might request task completion
        completion_patterns = [
            r'(?:task |^|\b)(.*?)(?: is completed| has been completed| marked as completed| complete$)',
            r'(?:complete task |complete |mark as complete |finish )(.*?)(?:$| please| now)',
            r'(?:mark task |task )(.*?)(?: as completed| as done| done)',
            r'(?:finish task )(.*?)(?:$| please)'
        ]

        matched_task_title = None
        for pattern in completion_patterns:
            match = re.search(pattern, user_message.lower().strip())
            if match:
                matched_task_title = match.group(1).strip()
                break

        if matched_task_title:
            # Try to find and complete the task directly
            # Get user's tasks
            cached_tasks = self._get_cached_user_tasks(user_id)
            if not cached_tasks:
                # Fetch from DB if not cached
                result = await list_tasks(user_id, db_session=db_session)
                if result.get("success"):
                    cached_tasks = result.get("tasks", [])
                    # Cache the tasks
                    self._cache_user_tasks(user_id, cached_tasks)

            # Find the task by title (case-insensitive exact match first, then partial)
            target_task = None
            matched_task_title_lower = matched_task_title.lower()

            # First, try exact match
            for task in cached_tasks or []:
                if task.get("title", "").lower() == matched_task_title_lower:
                    target_task = task
                    break

            # If no exact match, try partial match
            if not target_task:
                for task in cached_tasks or []:
                    if matched_task_title_lower in task.get("title", "").lower():
                        target_task = task
                        break

            if target_task:
                # Complete the task directly
                result = await complete_task(user_id, task_id=target_task["id"], db_session=db_session)

                # Invalidate the tasks cache since we updated a task
                tasks_cache_key = self._get_tasks_cache_key(user_id)
                if tasks_cache_key in self.tasks_cache:
                    del self.tasks_cache[tasks_cache_key]

                # Prepare response
                if result.get("success"):
                    response = f"Task '{target_task['title']}' has been marked as completed."

                    # Store the user message in the database
                    if db_session and session_id:
                        user_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="user",
                            content=user_message
                        )
                        create_chat_message(session=db_session, chat_message_create=user_msg)

                        # Store the AI response in the database
                        ai_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="assistant",
                            content=response
                        )
                        create_chat_message(session=db_session, chat_message_create=ai_msg)

                    # Log the interaction
                    log_ai_interaction(user_id, user_message, response, session_id)

                    return {
                        "response": response,
                        "session_id": session_id,
                        "tool_calls": [],
                        "task_created": None
                    }
                else:
                    # If direct completion failed, fall back to normal processing
                    pass

        # Check if the user wants to update a task by title directly
        # Look for patterns like "update task [title] to [new title]", "change [title] to [new title]", etc.
        update_patterns = [
            r'(?:update task |update |change task |change )(.*?)(?: to | - )(.*?)(?:$| please)',
            r'(?:modify task |modify )(.*?)(?: to | - )(.*?)(?:$| please)',
            r'(?:rename task |rename )(.*?)(?: to | - )(.*?)(?:$| please)'
        ]

        matched_update_task_title = None
        matched_new_title = None
        for pattern in update_patterns:
            match = re.search(pattern, user_message.lower().strip())
            if match:
                matched_update_task_title = match.group(1).strip()
                matched_new_title = match.group(2).strip()
                break

        if matched_update_task_title and matched_new_title:
            # Try to find and update the task directly
            # Get user's tasks
            cached_tasks = self._get_cached_user_tasks(user_id)
            if not cached_tasks:
                # Fetch from DB if not cached
                result = await list_tasks(user_id, db_session=db_session)
                if result.get("success"):
                    cached_tasks = result.get("tasks", [])
                    # Cache the tasks
                    self._cache_user_tasks(user_id, cached_tasks)

            # Find the task by title (case-insensitive exact match first, then partial)
            target_task = None
            matched_task_title_lower = matched_update_task_title.lower()

            # First, try exact match
            for task in cached_tasks or []:
                if task.get("title", "").lower() == matched_task_title_lower:
                    target_task = task
                    break

            # If no exact match, try partial match
            if not target_task:
                for task in cached_tasks or []:
                    if matched_task_title_lower in task.get("title", "").lower():
                        target_task = task
                        break

            if target_task:
                # Update the task directly
                result = await update_task(
                    user_id,
                    task_id=target_task["id"],
                    title=matched_new_title,
                    db_session=db_session
                )

                # Invalidate the tasks cache since we updated a task
                tasks_cache_key = self._get_tasks_cache_key(user_id)
                if tasks_cache_key in self.tasks_cache:
                    del self.tasks_cache[tasks_cache_key]

                # Prepare response
                if result.get("success"):
                    response = f"Task '{target_task['title']}' has been updated to '{matched_new_title}'."

                    # Store the user message in the database
                    if db_session and session_id:
                        user_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="user",
                            content=user_message
                        )
                        create_chat_message(session=db_session, chat_message_create=user_msg)

                        # Store the AI response in the database
                        ai_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="assistant",
                            content=response
                        )
                        create_chat_message(session=db_session, chat_message_create=ai_msg)

                    # Log the interaction
                    log_ai_interaction(user_id, user_message, response, session_id)

                    return {
                        "response": response,
                        "session_id": session_id,
                        "tool_calls": [],
                        "task_created": None
                    }
                else:
                    # If direct update failed, fall back to normal processing
                    pass

        # Check if the user wants to update just the description of a task
        # Look for patterns like "update description of task [title] to [new desc]" or "change description of task [title] to [new desc]"
        desc_update_patterns = [
            r'(?:update description of task |change description of task |update task |change task )(.*?)(?: description to | description - | to description | - description )(.*?)(?:$| please)'
        ]

        matched_desc_task_title = None
        matched_new_description = None
        for pattern in desc_update_patterns:
            match = re.search(pattern, user_message.lower().strip())
            if match:
                matched_desc_task_title = match.group(1).strip()
                matched_new_description = match.group(2).strip()
                break

        if matched_desc_task_title and matched_new_description:
            # Try to find and update the task description directly
            # Get user's tasks
            cached_tasks = self._get_cached_user_tasks(user_id)
            if not cached_tasks:
                # Fetch from DB if not cached
                result = await list_tasks(user_id, db_session=db_session)
                if result.get("success"):
                    cached_tasks = result.get("tasks", [])
                    # Cache the tasks
                    self._cache_user_tasks(user_id, cached_tasks)

            # Find the task by title (case-insensitive exact match first, then partial)
            target_task = None
            matched_task_title_lower = matched_desc_task_title.lower()

            # First, try exact match
            for task in cached_tasks or []:
                if task.get("title", "").lower() == matched_task_title_lower:
                    target_task = task
                    break

            # If no exact match, try partial match
            if not target_task:
                for task in cached_tasks or []:
                    if matched_task_title_lower in task.get("title", "").lower():
                        target_task = task
                        break

            if target_task:
                # Update the task description directly
                result = await update_task(
                    user_id,
                    task_id=target_task["id"],
                    description=matched_new_description,
                    db_session=db_session
                )

                # Invalidate the tasks cache since we updated a task
                tasks_cache_key = self._get_tasks_cache_key(user_id)
                if tasks_cache_key in self.tasks_cache:
                    del self.tasks_cache[tasks_cache_key]

                # Prepare response
                if result.get("success"):
                    response = f"Task '{target_task['title']}' has been updated with new description '{matched_new_description}'."

                    # Store the user message in the database
                    if db_session and session_id:
                        user_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="user",
                            content=user_message
                        )
                        create_chat_message(session=db_session, chat_message_create=user_msg)

                        # Store the AI response in the database
                        ai_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="assistant",
                            content=response
                        )
                        create_chat_message(session=db_session, chat_message_create=ai_msg)

                    # Log the interaction
                    log_ai_interaction(user_id, user_message, response, session_id)

                    return {
                        "response": response,
                        "session_id": session_id,
                        "tool_calls": [],
                        "task_created": None
                    }
                else:
                    # If direct update failed, fall back to normal processing
                    pass

        # Check if the user wants to update a task with both title and description
        # Look for patterns like "update task [title] with title [new title] and description [new desc]"
        detailed_update_patterns = [
            r'(?:update task |change task )(.*?)(?: with title | and title )(.*?)(?: and description |, description | - description )(.*?)(?:$| please)',
            r'(?:update task |change task )(.*?)(?: to title )(.*?)(?: and description |, description | - description )(.*?)(?:$| please)'
        ]

        matched_detailed_task_title = None
        matched_new_task_title = None
        matched_new_description = None
        for pattern in detailed_update_patterns:
            match = re.search(pattern, user_message.lower().strip())
            if match:
                matched_detailed_task_title = match.group(1).strip()
                matched_new_task_title = match.group(2).strip()
                matched_new_description = match.group(3).strip()
                break

        if matched_detailed_task_title and matched_new_task_title and matched_new_description:
            # Try to find and update the task directly
            # Get user's tasks
            cached_tasks = self._get_cached_user_tasks(user_id)
            if not cached_tasks:
                # Fetch from DB if not cached
                result = await list_tasks(user_id, db_session=db_session)
                if result.get("success"):
                    cached_tasks = result.get("tasks", [])
                    # Cache the tasks
                    self._cache_user_tasks(user_id, cached_tasks)

            # Find the task by title (case-insensitive exact match first, then partial)
            target_task = None
            matched_task_title_lower = matched_detailed_task_title.lower()

            # First, try exact match
            for task in cached_tasks or []:
                if task.get("title", "").lower() == matched_task_title_lower:
                    target_task = task
                    break

            # If no exact match, try partial match
            if not target_task:
                for task in cached_tasks or []:
                    if matched_task_title_lower in task.get("title", "").lower():
                        target_task = task
                        break

            if target_task:
                # Update the task directly with both title and description
                result = await update_task(
                    user_id,
                    task_id=target_task["id"],
                    title=matched_new_task_title,
                    description=matched_new_description,
                    db_session=db_session
                )

                # Invalidate the tasks cache since we updated a task
                tasks_cache_key = self._get_tasks_cache_key(user_id)
                if tasks_cache_key in self.tasks_cache:
                    del self.tasks_cache[tasks_cache_key]

                # Prepare response
                if result.get("success"):
                    response = f"Task '{target_task['title']}' has been updated with new title '{matched_new_task_title}' and description '{matched_new_description}'."

                    # Store the user message in the database
                    if db_session and session_id:
                        user_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="user",
                            content=user_message
                        )
                        create_chat_message(session=db_session, chat_message_create=user_msg)

                        # Store the AI response in the database
                        ai_msg = ChatMessageCreate(
                            chat_session_id=session_id,
                            role="assistant",
                            content=response
                        )
                        create_chat_message(session=db_session, chat_message_create=ai_msg)

                    # Log the interaction
                    log_ai_interaction(user_id, user_message, response, session_id)

                    return {
                        "response": response,
                        "session_id": session_id,
                        "tool_calls": [],
                        "task_created": None
                    }
                else:
                    # If direct update failed, fall back to normal processing
                    pass

        # Log the incoming interaction
        log_ai_interaction(user_id, user_message, "Processing", session_id)

        # Prepare the messages for the AI
        messages = [{"role": "system", "content": self.system_prompt}]

        # Load conversation history from cache or DB if session_id is provided
        if session_id and db_session:
            # Try to get conversation history from cache first
            cached_history = self._get_cached_conversation_history(session_id)
            if cached_history:
                # Use cached history
                for msg in cached_history:
                    messages.append(msg)
            else:
                # Retrieve from DB and cache it
                chat_session = get_chat_session_by_id(session=db_session, chat_session_id=session_id)
                if chat_session:
                    # Retrieve chat messages for this session
                    chat_messages = get_chat_messages_by_session(session=db_session, chat_session_id=session_id)

                    # Add messages to the conversation history
                    history_for_cache = []
                    for msg in chat_messages:
                        role = "user" if msg.role == "user" else "assistant"
                        message_obj = {
                            "role": role,
                            "content": msg.content
                        }
                        messages.append(message_obj)
                        # Also store in cache format
                        history_for_cache.append(message_obj)

                    # Cache the conversation history
                    self._cache_conversation_history(session_id, history_for_cache)

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Call the AI model with tools
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # If the AI wants to call tools
            if tool_calls:
                # Execute the tool calls
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Call the appropriate tool
                    if function_name == "add_task":
                        result = await add_task(user_id, db_session=db_session, **function_args)
                        # Use simplified task info for display
                        if result.get("display_task"):
                            result_for_display = {"success": True, "task": result["display_task"]}
                        else:
                            result_for_display = result
                    elif function_name == "list_tasks":
                        # First check if we have cached tasks
                        cached_tasks = self._get_cached_user_tasks(user_id)
                        if cached_tasks:
                            result = {"success": True, "tasks": cached_tasks}
                            # Use cached display tasks if available
                            if any(isinstance(task, dict) and 'id' not in task for task in cached_tasks):
                                result_for_display = {"success": True, "display_tasks": cached_tasks}
                            else:
                                # Convert to display format
                                display_tasks = []
                                for task in cached_tasks:
                                    display_tasks.append({
                                        "title": task.get("title"),
                                        "description": task.get("description"),
                                        "completed": task.get("completed")
                                    })
                                result_for_display = {"success": True, "display_tasks": display_tasks}
                        else:
                            result = await list_tasks(user_id, db_session=db_session)
                            # Cache the tasks if successful
                            if result.get("success") and "tasks" in result:
                                self._cache_user_tasks(user_id, result["tasks"])
                            # Use simplified display tasks
                            result_for_display = {
                                "success": True,
                                "display_tasks": result.get("display_tasks", [])
                            }
                    elif function_name == "update_task":
                        result = await update_task(user_id, db_session=db_session, **function_args)
                        # Use simplified task info for display
                        if result.get("display_task"):
                            result_for_display = {"success": True, "task": result["display_task"]}
                        else:
                            result_for_display = result
                        # Invalidate the tasks cache since we updated a task
                        tasks_cache_key = self._get_tasks_cache_key(user_id)
                        if tasks_cache_key in self.tasks_cache:
                            del self.tasks_cache[tasks_cache_key]
                    elif function_name == "delete_task":
                        result = await delete_task(user_id, db_session=db_session, **function_args)
                        # Invalidate the tasks cache since we deleted a task
                        tasks_cache_key = self._get_tasks_cache_key(user_id)
                        if tasks_cache_key in self.tasks_cache:
                            del self.tasks_cache[tasks_cache_key]
                        result_for_display = result
                    elif function_name == "complete_task":
                        result = await complete_task(user_id, db_session=db_session, **function_args)
                        # Use simplified task info for display
                        if result.get("display_task"):
                            result_for_display = {"success": True, "task": result["display_task"]}
                        else:
                            result_for_display = result
                        # Invalidate the tasks cache since we updated a task
                        tasks_cache_key = self._get_tasks_cache_key(user_id)
                        if tasks_cache_key in self.tasks_cache:
                            del self.tasks_cache[tasks_cache_key]
                    else:
                        result = {"error": f"Unknown function: {function_name}"}
                        result_for_display = result

                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": json.dumps(result_for_display),  # Use json.dumps to ensure proper formatting
                        "name": function_name
                    })

                # Send the tool results back to the AI to get the final response
                # For Gemini API, we need to format the tool responses correctly
                for tr in tool_results:
                    # Format the content as a JSON object as required by Gemini
                    formatted_content = {
                        "result": tr["content"]
                    }
                    messages.append({
                        "role": "function",  # Using "function" instead of "tool" for Gemini
                        "name": tr["name"],
                        "content": json.dumps(formatted_content),  # Convert to JSON string
                        "tool_call_id": tr["tool_call_id"]
                    })

                # Only make a second API call if there are tool results to process
                if tool_results:
                    final_response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=messages
                    )

                    # Extract the final response content
                    ai_response = final_response.choices[0].message.content
                else:
                    # If no tool results, use the initial response
                    ai_response = response_message.content

                # Store the user message in the database
                if db_session and session_id:
                    user_msg = ChatMessageCreate(
                        chat_session_id=session_id,
                        role="user",
                        content=user_message
                    )
                    create_chat_message(session=db_session, chat_message_create=user_msg)

                    # Store the AI response in the database
                    ai_msg = ChatMessageCreate(
                        chat_session_id=session_id,
                        role="assistant",
                        content=ai_response
                    )
                    create_chat_message(session=db_session, chat_message_create=ai_msg)

                # Log the successful interaction
                log_ai_interaction(user_id, user_message, ai_response, session_id)

                return {
                    "response": ai_response,
                    "session_id": session_id,
                    "tool_calls": [{"name": tc.function.name, "arguments": tc.function.arguments} for tc in tool_calls],
                    "task_created": result.get("task") if result and "task" in result else None
                }
            else:
                # Check if the response is unrelated to tasks
                ai_response = response_message.content
                if self._is_unrelated_query(user_message):
                    ai_response = UNRELATED_QUERY_RESPONSE

                # Store the user message in the database
                if db_session and session_id:
                    user_msg = ChatMessageCreate(
                        chat_session_id=session_id,
                        role="user",
                        content=user_message
                    )
                    create_chat_message(session=db_session, chat_message_create=user_msg)

                    # Store the AI response in the database
                    ai_msg = ChatMessageCreate(
                        chat_session_id=session_id,
                        role="assistant",
                        content=ai_response
                    )
                    create_chat_message(session=db_session, chat_message_create=ai_msg)

                # Log the interaction
                log_ai_interaction(user_id, user_message, ai_response, session_id)

                return {
                    "response": ai_response,
                    "session_id": session_id,
                    "tool_calls": [],
                    "task_created": None
                }
        except Exception as e:
            # Log the error
            log_error(f"Error processing user message: {str(e)}", {"user_id": user_id, "session_id": session_id, "user_message": user_message}, exc_info=True)

            # Handle any errors
            error_response = f"Sorry, I encountered an error processing your request: {str(e)}"
            return {
                "response": error_response,
                "session_id": session_id,
                "tool_calls": [],
                "task_created": None
            }

    def _is_unrelated_query(self, user_message: str) -> bool:
        """
        Check if the user's query is unrelated to tasks
        This is a simple heuristic - in a real implementation,
        this would likely use more sophisticated NLP techniques
        """
        task_related_keywords = [
            "task", "add", "list", "show", "create", "update", "change",
            "delete", "remove", "complete", "finish", "done", "todo"
        ]

        message_lower = user_message.lower()
        has_task_keyword = any(keyword in message_lower for keyword in task_related_keywords)

        return not has_task_keyword