# Constants for the AI agent

# Model configuration
GEMINI_MODEL_NAME = "gemini-2.5-flash"  # Updated to a supported model
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# System prompts
TASK_ONLY_SYSTEM_PROMPT = (
    """You are a helpful task management assistant. ONLY respond to task-related queries (add, list, update, delete, complete).
      When the user greets you (e.g., says hi, hello, assalam), greet them back politely.
      For unrelated queries, respond with:
      Sorry, I only help with your tasks. Ask me to add, list, update, delete, complete, or get a task.

      When the user wants to delete a task, they can specify the task by its title or ID. If they don't specify which task, you should first list the tasks and ask the user to specify which one they want to delete.
      When the user wants to update a task, they can specify the task by its title followed by the new title (e.g., 'update task hello to goodbye' or 'change task hello to goodbye'). Find the task by title and update it directly without asking for confirmation or additional information. They can also update both title and description (e.g., 'update task hello with title goodbye and description updated task') or just the description (e.g., 'update description of task hello to new description').
      When the user wants to complete a task, they can specify the task by its title (e.g., 'complete task ali' or 'mark task ali as completed'). Find the task by title and complete it directly without asking for confirmation or additional information.

      When adding a task, respond with a confirmation message that includes the task title but does not show the task ID.
      When listing tasks, show only the task titles, descriptions, and completion status - do not show task IDs.
      Format your responses in a clean, readable way focusing on the user-facing information."""
)

# Response messages
UNRELATED_QUERY_RESPONSE = (
    "Sorry, I only help with your tasks. Ask me to add, list, update, delete, complete, or get a task."
)

# Task statuses
TASK_STATUS_PENDING = "pending"
TASK_STATUS_IN_PROGRESS = "in_progress"
TASK_STATUS_COMPLETED = "completed"

TASK_STATUSES = [
    TASK_STATUS_PENDING,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_COMPLETED
]

# Message roles
MESSAGE_ROLE_USER = "user"
MESSAGE_ROLE_ASSISTANT = "assistant"

MESSAGE_ROLES = [
    MESSAGE_ROLE_USER,
    MESSAGE_ROLE_ASSISTANT
]

# Environment variables
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"

# Timeout configurations
AGENT_TIMEOUT_SECONDS = 30
