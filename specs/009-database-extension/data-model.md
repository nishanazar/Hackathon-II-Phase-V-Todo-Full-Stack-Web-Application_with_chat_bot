# Data Model: MCP Server & Tools Implementation for Phase III

## Overview
This document defines the data models for the MCP (Model Context Protocol) server implementation, including the database tables for conversations and messages as specified in the feature requirements.

## Entity Models

### Conversation Model
Represents a conversation thread between a user and the AI assistant.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the conversation
- `user_id` (String, Indexed): ID of the user who owns this conversation (for user isolation)
- `created_at` (DateTime): Timestamp when the conversation was created
- `updated_at` (DateTime): Timestamp when the conversation was last updated

**Validation Rules**:
- `user_id` must match the authenticated user's ID from JWT
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on any modification

**Relationships**:
- One-to-many with Message model (one conversation can have many messages)

### Message Model
Represents a message within a conversation, either from the user or the AI assistant.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the message
- `user_id` (String, Indexed): ID of the user who owns this message (for user isolation)
- `conversation_id` (UUID, Foreign Key, Indexed): References the conversation this message belongs to
- `role` (String): Role of the message sender ("user" or "assistant")
- `content` (Text): The actual content of the message
- `created_at` (DateTime): Timestamp when the message was created

**Validation Rules**:
- `user_id` must match the authenticated user's ID from JWT
- `conversation_id` must reference an existing conversation owned by the same user
- `role` must be either "user" or "assistant"
- `content` cannot be empty

**Relationships**:
- Many-to-one with Conversation model (many messages belong to one conversation)

### MCP Tool Execution Model (New)
Represents the execution of MCP tools, tracking tool usage and results.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the tool execution
- `user_id` (String, Indexed): ID of the user who triggered the tool execution
- `tool_name` (String): Name of the tool that was executed
- `input_params` (JSON): Parameters passed to the tool
- `result` (JSON): Result returned by the tool
- `created_at` (DateTime): Timestamp when the tool was executed
- `conversation_id` (UUID, Optional): References the conversation context if applicable

**Validation Rules**:
- `user_id` must match the authenticated user's ID from JWT
- `tool_name` must be one of the registered MCP tools
- `input_params` must conform to the tool's expected schema

## Database Schema

```sql
-- Conversation table
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for fast queries
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);

-- Message table
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for fast queries
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- MCP Tool Executions table
CREATE TABLE mcp_tool_executions (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    tool_name VARCHAR(255) NOT NULL,
    input_params JSONB,
    result JSONB,
    conversation_id UUID REFERENCES conversations(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for fast queries
CREATE INDEX idx_mcp_tool_executions_user_id ON mcp_tool_executions(user_id);
CREATE INDEX idx_mcp_tool_executions_tool_name ON mcp_tool_executions(tool_name);
CREATE INDEX idx_mcp_tool_executions_conversation_id ON mcp_tool_executions(conversation_id);
```

## State Transitions

### Conversation State Transitions
- Created: When a new conversation is initiated
- Active: When messages are being exchanged
- Archived: When the conversation is concluded (future enhancement)

### Message State Transitions
- Pending: When a message is being processed (for assistant messages)
- Completed: When a message has been fully processed and stored
- Error: When there was an issue processing the message (for assistant messages)

## Access Control Rules

1. All queries must filter by `user_id` to ensure users can only access their own data
2. Before any database operation, verify that the `user_id` in the JWT matches the `user_id` in the query
3. Foreign key constraints ensure referential integrity between conversations and messages