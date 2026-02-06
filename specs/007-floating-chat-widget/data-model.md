# Data Model: Floating AI Chat Widget

## Entities

### Chat Session
- **Fields**:
  - id: string (unique identifier for the session)
  - userId: string (authenticated user ID from JWT)
  - createdAt: Date (timestamp when session started)
  - isActive: boolean (whether the session is currently open)
  
- **Relationships**:
  - Belongs to one User (via userId)

- **Validation rules**:
  - userId must match authenticated user from JWT
  - createdAt must be in the past
  - id must be unique

### Chat Message
- **Fields**:
  - id: string (unique identifier for the message)
  - sessionId: string (reference to Chat Session)
  - sender: 'user' | 'ai' (who sent the message)
  - content: string (the message content)
  - timestamp: Date (when the message was sent)
  - status: 'sent' | 'delivered' | 'error' (delivery status)

- **Relationships**:
  - Belongs to one Chat Session (via sessionId)
  - Associated with User (via session's userId)

- **Validation rules**:
  - content must not be empty
  - sender must be either 'user' or 'ai'
  - timestamp must be in the past
  - status must be one of the allowed values

### Floating Chat Widget Configuration
- **Fields**:
  - isVisible: boolean (whether the widget is visible to the user)
  - position: { x: number, y: number } (coordinates for widget placement)
  - theme: 'light' | 'dark' | 'auto' (UI theme setting)
  - isExpanded: boolean (whether the chat panel is open)

- **Relationships**:
  - Associated with one User (for personalization)

- **Validation rules**:
  - position coordinates must be positive numbers
  - theme must be one of the allowed values
  - isVisible must be a boolean

## State Transitions

### Chat Widget State Machine
- **Initial State**: Hidden (isVisible = false)
- **Transition 1**: User authenticates → Visible (isVisible = true)
- **Transition 2**: User clicks floating icon → Expanded (isExpanded = true)
- **Transition 3**: User closes chat panel → Collapsed (isExpanded = false)
- **Transition 4**: User logs out → Hidden (isVisible = false)

### Message Status Transitions
- **Initial State**: Pending
- **Transition 1**: Message sent to server → Sent
- **Transition 2**: Server confirms receipt → Delivered
- **Transition 3**: Server reports error → Error