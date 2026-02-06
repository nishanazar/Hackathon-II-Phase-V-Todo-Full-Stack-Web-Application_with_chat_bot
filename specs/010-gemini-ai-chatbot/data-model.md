# Data Model: Gemini AI Agent with OpenAI Agents SDK for Phase III Todo AI Chatbot

## Overview
This document defines the data structures and relationships for the Gemini AI Agent with OpenAI Agents SDK for Phase III Todo AI Chatbot feature.

## Entities

### User
Represents an authenticated user with JWT-based access control
- **Fields:**
  - id: UUID (Primary Key)
  - email: String (Unique, Indexed)
  - name: String
  - created_at: DateTime
  - updated_at: DateTime
- **Relationships:**
  - Has many Tasks
  - Has many ChatSessions

### Task
Represents a task entity with user ownership and CRUD operations
- **Fields:**
  - id: UUID (Primary Key)
  - title: String
  - description: Text (Optional)
  - status: Enum (pending, in_progress, completed)
  - user_id: UUID (Foreign Key to User)
  - created_at: DateTime
  - updated_at: DateTime
  - completed_at: DateTime (Optional)
- **Relationships:**
  - Belongs to User
  - Belongs to ChatSession (Optional)

### ChatSession
Conversational context between user and AI agent
- **Fields:**
  - id: UUID (Primary Key)
  - user_id: UUID (Foreign Key to User)
  - title: String (Generated from first message or default)
  - created_at: DateTime
  - updated_at: DateTime
- **Relationships:**
  - Belongs to User
  - Has many ChatMessages

### ChatMessage
Individual message in a chat session
- **Fields:**
  - id: UUID (Primary Key)
  - chat_session_id: UUID (Foreign Key to ChatSession)
  - role: Enum (user, assistant)
  - content: Text
  - created_at: DateTime
  - task_id: UUID (Foreign Key to Task, Optional)
- **Relationships:**
  - Belongs to ChatSession
  - Belongs to Task (Optional)

### AIConfig
Configuration for the AI agent
- **Fields:**
  - id: UUID (Primary Key)
  - model_name: String (Default: "gemini-1.5-flash")
  - temperature: Float (Default: 0.7)
  - max_tokens: Integer (Default: 1000)
  - system_prompt: Text
  - created_at: DateTime
  - updated_at: DateTime
- **Relationships:**
  - None

## Validation Rules
- User email must be unique and valid
- Task title must not be empty
- Task status must be one of the defined enum values
- ChatMessage role must be either 'user' or 'assistant'
- All timestamps are in UTC

## State Transitions
- Task: pending → in_progress → completed
- ChatSession: active (until user closes or inactivity timeout)