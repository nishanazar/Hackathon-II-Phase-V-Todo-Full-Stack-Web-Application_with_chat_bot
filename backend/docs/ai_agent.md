# AI Agent Documentation

## Overview
The TodoMasterAI is an intelligent task management assistant that allows users to interact with the task management system using natural language. The agent is built using the OpenAI Agents SDK and configured to work with Google's Gemini model through an OpenAI-compatible endpoint.

## Features
- Natural language processing for task management commands
- Integration with all 5 MCP tools (add, list, update, delete, complete tasks)
- Strict task-only responses to maintain focus
- Conversation history management
- Secure user isolation with JWT authentication

## Supported Commands
The AI agent understands various natural language commands for task management:

### Adding Tasks
- "Add a task to buy groceries"
- "Create a task for calling mom"
- "I need to schedule a meeting"

### Listing Tasks
- "Show my tasks"
- "What do I have to do?"
- "List all my tasks"

### Updating Tasks
- "Update task 'buy groceries' to 'buy organic groceries'"
- "Change the description of task X"

### Deleting Tasks
- "Delete the task to call mom"
- "Remove task X"

### Completing Tasks
- "Complete the task to buy groceries"
- "Mark task X as done"
- "Finish task Y"

## Architecture
The AI agent consists of several components:

### TodoMasterAI Class
Located in `backend/src/agents/todo_agent.py`, this class manages the interaction with the Gemini model and handles tool calls.

### MCP Tools Integration
The agent is connected to the following MCP tools:
- `add_task`: Creates new tasks
- `list_tasks`: Retrieves existing tasks
- `update_task`: Modifies existing tasks
- `delete_task`: Removes tasks
- `complete_task`: Marks tasks as completed

### Database Integration
The agent works with the following models:
- `ChatSession`: Manages conversation contexts
- `ChatMessage`: Stores individual messages in conversations
- `AIConfig`: Stores configuration for the AI agent

## Configuration
The agent is configured using environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `GEMINI_MODEL_NAME`: The model to use (default: gemini-1.5-flash)
- `GEMINI_BASE_URL`: The API endpoint (default: https://generativelanguage.googleapis.com/v1beta/openai/)

## Security
- All user data is isolated using JWT authentication
- Users can only access their own tasks and conversations
- API keys are securely stored in environment variables
- Conversation history is tied to specific user accounts

## Error Handling
The agent gracefully handles various error conditions:
- Invalid API keys
- Network connectivity issues
- Malformed user requests
- Unauthorized access attempts

## Logging
All AI interactions are logged for monitoring and debugging purposes. Logs include:
- User ID (without exposing user identity)
- Timestamp of interaction
- User message (with PII considerations)
- AI response
- Session ID (when applicable)

## Limitations
- The agent only responds to task-related queries
- Complex multi-step requests may require clarification
- Natural language understanding depends on the underlying AI model's capabilities