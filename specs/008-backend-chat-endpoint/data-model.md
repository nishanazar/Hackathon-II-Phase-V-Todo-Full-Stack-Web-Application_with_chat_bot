# Data Model: Backend Chat Endpoint

## Entities

### Conversation
- **Fields**:
  - id: int (primary key, auto-increment)
  - user_id: str (foreign key to User, required)
  - title: Optional[str] (optional title for the conversation)
  - created_at: datetime (timestamp when conversation was created)
  - updated_at: datetime (timestamp when conversation was last updated)

- **Relationships**:
  - Belongs to one User (via user_id)
  - Has many Messages (via conversation_id)

- **Validation rules**:
  - user_id must match an existing user
  - created_at must be in the past
  - updated_at must be >= created_at
  - title, if provided, must be between 1-200 characters

### Message
- **Fields**:
  - id: int (primary key, auto-increment)
  - conversation_id: int (foreign key to Conversation, required)
  - user_id: str (foreign key to User, required)
  - role: str (either 'user' or 'assistant', required)
  - content: str (message content, required)
  - created_at: datetime (timestamp when message was created)

- **Relationships**:
  - Belongs to one Conversation (via conversation_id)
  - Belongs to one User (via user_id)

- **Validation rules**:
  - conversation_id must match an existing conversation
  - user_id must match an existing user
  - role must be either 'user' or 'assistant'
  - content must not be empty
  - created_at must be in the past

## State Transitions

### Conversation State Management
- **Initial State**: New conversation created when no conversation_id provided
- **Transition 1**: User sends message → Message added to conversation
- **Transition 2**: AI responds → Assistant message added to conversation
- **Transition 3**: Conversation updated → updated_at timestamp refreshed

### Message State Flow
- **Initial State**: User message received
- **Transition 1**: Message validated and saved to DB
- **Transition 2**: AI processes message and generates response
- **Transition 3**: Assistant response saved to DB
- **Transition 4**: Response returned to client

## Database Schema

```sql
-- Conversation table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Message table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexes for performance
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
```

## API Request/Response Models

### Request Models
- **ChatRequest**:
  - message: str (the user's message content)
  - conversation_id: Optional[int] (ID of existing conversation, if continuing)

### Response Models
- **ChatResponse**:
  - conversation_id: int (ID of the conversation)
  - response: str (the AI's response)
  - tool_calls: List[Dict] (empty list for now, for future AI agent integration)