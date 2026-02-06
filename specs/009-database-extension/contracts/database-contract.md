# API Contract: Database Extension for Chat History

## Overview
This document defines the database schema and access patterns for the chat history functionality in the Todo AI Chatbot application.

## Database Schema

### Conversation Table
- **Purpose**: Stores metadata for each conversation between a user and the AI assistant
- **Fields**:
  - `id`: SERIAL PRIMARY KEY (auto-incrementing integer)
  - `user_id`: VARCHAR(255) NOT NULL, INDEX (foreign key to users table)
  - `created_at`: TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  - `updated_at`: TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

### Message Table
- **Purpose**: Stores individual messages within conversations
- **Fields**:
  - `id`: SERIAL PRIMARY KEY (auto-incrementing integer)
  - `user_id`: VARCHAR(255) NOT NULL, INDEX (foreign key to users table)
  - `conversation_id`: INTEGER NOT NULL, INDEX (foreign key to conversations table)
  - `role`: VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant'))
  - `content`: TEXT NOT NULL
  - `created_at`: TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

### Relationships
- Foreign Key: `messages.conversation_id` → `conversations.id`
- Foreign Key: `messages.user_id` → `users.id`
- Foreign Key: `conversations.user_id` → `users.id`

### Indexes
- `idx_messages_conversation_id`: ON messages(conversation_id) for fast history retrieval
- `idx_messages_user_id`: ON messages(user_id) for user isolation
- `idx_conversations_user_id`: ON conversations(user_id) for user queries

## Access Patterns

### Reading Conversation History
```sql
SELECT * FROM messages 
WHERE conversation_id = $1 AND user_id = $2 
ORDER BY created_at ASC;
```
- **Purpose**: Retrieve all messages for a specific conversation belonging to a specific user
- **Parameters**: 
  - `$1`: conversation_id
  - `$2`: user_id (from JWT token)
- **Security**: User isolation enforced by user_id check

### Creating New Conversation
```sql
INSERT INTO conversations (user_id, created_at, updated_at) 
VALUES ($1, NOW(), NOW()) 
RETURNING id;
```
- **Purpose**: Create a new conversation for a user
- **Parameters**: 
  - `$1`: user_id (from JWT token)

### Storing New Message
```sql
INSERT INTO messages (user_id, conversation_id, role, content, created_at) 
VALUES ($1, $2, $3, $4, NOW());
```
- **Purpose**: Store a new message in a conversation
- **Parameters**: 
  - `$1`: user_id (from JWT token)
  - `$2`: conversation_id
  - `$3`: role ('user' or 'assistant')
  - `$4`: message content

### Updating Conversation Timestamp
```sql
UPDATE conversations 
SET updated_at = NOW() 
WHERE id = $1 AND user_id = $2;
```
- **Purpose**: Update the conversation's last activity timestamp
- **Parameters**: 
  - `$1`: conversation_id
  - `$2`: user_id (from JWT token)

## Security Requirements

### User Isolation
- All database queries must include a user_id filter
- Users can only access conversations and messages that belong to them
- The user_id in the JWT token must match the user_id in the database record

### Data Validation
- Role field must be either 'user' or 'assistant'
- Content field must not be empty
- Conversation and user IDs must exist in their respective tables
- All timestamps are stored in UTC

## Performance Requirements

### Query Performance
- Message history retrieval should complete in under 200ms for conversations with up to 1000 messages
- New message insertion should complete in under 100ms
- New conversation creation should complete in under 50ms

### Indexing Strategy
- Indexes on conversation_id and user_id fields for fast lookups
- Composite indexes may be added for complex queries if needed
- Regular monitoring of slow queries to optimize as needed

## Migration Requirements

### Schema Changes
- Add conversations and messages tables to existing database
- Maintain backward compatibility with existing task table
- No changes to existing data or tables
- Foreign key constraints to maintain referential integrity

### Rollback Plan
- Migration scripts must include rollback functionality
- Data integrity must be preserved during rollback
- Existing application functionality must remain unaffected during migration