# Data Model: Advanced Features Implementation for Phase V Todo AI Chatbot

## Enhanced Task Entity

### Fields
- **id** (UUID/string): Unique identifier for the task
- **title** (string): Task title/name
- **description** (string, optional): Detailed description of the task
- **completed** (boolean): Whether the task is completed
- **created_at** (datetime): Timestamp when the task was created
- **updated_at** (datetime): Timestamp when the task was last updated
- **due_date** (datetime, optional): Deadline for the task completion
- **priority** (integer): Priority level from 1 (lowest) to 5 (highest)
- **tags** (array of strings): Array of tag strings associated with the task
- **recurring_interval** (string, optional): Interval for recurring tasks (daily, weekly, monthly, yearly)
- **user_id** (string): Foreign key linking to the user who owns the task

### Relationships
- **User**: Many-to-one relationship with User entity (one user can have many tasks)

### Validation Rules
- `title` is required and must be between 1-255 characters
- `priority` must be an integer between 1-5
- `tags` array must not exceed 10 tags
- `recurring_interval` must be one of: 'daily', 'weekly', 'monthly', 'yearly' if provided
- `due_date` must be a future date if provided
- `user_id` must reference an existing user

### State Transitions
- **Created**: When a new task is added to the system
- **Updated**: When any attribute of the task is modified
- **Completed**: When the task is marked as completed
- **Recurring**: When a recurring task generates a new occurrence
- **Deleted**: When the task is removed from the system

## Task Event Entity

### Fields
- **id** (UUID/string): Unique identifier for the event
- **task_id** (string): Reference to the associated task
- **event_type** (string): Type of event (created, updated, completed, recurring_created)
- **payload** (JSON): Event-specific data
- **timestamp** (datetime): When the event occurred
- **processed** (boolean): Whether the event has been processed by subscribers

### Validation Rules
- `event_type` must be one of: 'created', 'updated', 'completed', 'recurring_created'
- `task_id` must reference an existing task
- `payload` must be valid JSON

## Reminder Entity

### Fields
- **id** (UUID/string): Unique identifier for the reminder
- **task_id** (string): Reference to the associated task
- **scheduled_time** (datetime): When the reminder should be sent
- **sent** (boolean): Whether the reminder has been sent
- **sent_time** (datetime, optional): When the reminder was actually sent
- **user_id** (string): Reference to the user who owns the task

### Validation Rules
- `task_id` must reference an existing task
- `scheduled_time` must be in the future
- `user_id` must reference an existing user

## Indexes for Performance

### Task Table
- Index on `(user_id)` for efficient user-specific queries
- Index on `(due_date)` for efficient due date filtering
- Index on `(priority)` for efficient priority-based sorting
- Composite index on `(user_id, completed)` for efficient user task list queries
- Index on `(recurring_interval)` for efficient recurring task processing

### Task Event Table
- Index on `(task_id)` for efficient task event retrieval
- Index on `(event_type)` for efficient event type filtering
- Index on `(processed)` for efficient processing queue management

### Reminder Table
- Index on `(scheduled_time)` for efficient reminder scheduling
- Index on `(sent)` for efficient unsent reminder queries
- Index on `(user_id)` for efficient user-specific reminder queries