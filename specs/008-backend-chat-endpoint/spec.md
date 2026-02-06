# Feature Specification: Backend Chat Endpoint

**Feature Branch**: `008-backend-chat-endpoint`
**Created**: 2026-01-17
**Status**: Draft
**Input**: User description: "Backend Chat Endpoint Implementation for Phase III Todo AI Chatbot Target audience: Hackathon judges evaluating stateless AI integration and developers using agentic workflow Focus: Implement the stateless chat API endpoint in FastAPI backend to handle user messages, manage conversation state in DB, and prepare for AI agent integration, without modifying existing Phase II backend code Success criteria: - New POST /api/{user_id}/chat endpoint implemented - Endpoint requires valid JWT token (using existing middleware) - If no conversation_id provided, create new Conversation in DB - Load conversation history from Message table - Store user message in DB with role "user" - Prepare placeholder response logic (e.g., echo message) for now — full AI agent in next step - Store assistant response in DB with role "assistant" - Return JSON: {conversation_id, response, tool_calls: []} - Stateless: No in-memory state; all persistence in Neon DB - No changes to existing Phase II API endpoints or code Constraints: - Use FastAPI, SQLModel, Neon PostgreSQL - Stateless design: DB load/save on every request - JWT verification with BETTER_AUTH_SECRET - Reference @specs/api/rest-endpoints.md, @specs/database/schema.md, @backend/QWEN.md - Implement via Backend Chat Endpoint Agent iterations only - Do NOT modify existing Phase II routes or models (add new if needed) Not building: - Full AI agent or MCP tools (next steps) - Frontend changes (ChatKit already done) - New DB models (assume Conversation/Message from previous DB extension; add if missing)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Initiate New Conversation (Priority: P1)

As an authenticated user, I want to start a new conversation with the AI assistant so that I can get help with my tasks.

**Why this priority**: This is the core functionality that enables users to interact with the AI assistant.

**Independent Test**: Can be fully tested by making a POST request to /api/{user_id}/chat without a conversation_id and verifying that a new conversation is created and returned.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT, **When** user sends a message without a conversation_id, **Then** a new conversation is created in the database and the response includes the new conversation_id
2. **Given** user has a valid JWT token, **When** user sends a message to the chat endpoint, **Then** the user's message is stored in the database with role "user"
3. **Given** user sent a message, **When** the endpoint processes the request, **Then** a placeholder response is generated and stored in the database with role "assistant"

---

### User Story 2 - Continue Existing Conversation (Priority: P2)

As an authenticated user, I want to continue an existing conversation with the AI assistant so that I can maintain context across multiple exchanges.

**Why this priority**: Allows users to have ongoing conversations with preserved context.

**Independent Test**: Can be tested by making a POST request to /api/{user_id}/chat with a valid conversation_id and verifying that the conversation history is loaded and extended.

**Acceptance Scenarios**:

1. **Given** user has an existing conversation, **When** user sends a message with conversation_id, **Then** the conversation history is loaded from the database and the new message is appended
2. **Given** user is continuing a conversation, **When** user sends a message, **Then** the response includes the same conversation_id
3. **Given** conversation exists in DB, **When** endpoint retrieves history, **Then** all previous messages are loaded correctly

---

### User Story 3 - Secure Access Control (Priority: P3)

As a system administrator, I want to ensure that users can only access their own conversations so that data privacy is maintained.

**Why this priority**: Critical for maintaining user data isolation and security.

**Independent Test**: Can be tested by attempting to access another user's conversation and verifying that access is denied.

**Acceptance Scenarios**:

1. **Given** user has valid JWT token, **When** user attempts to access another user's conversation, **Then** access is denied with appropriate error response
2. **Given** invalid JWT token, **When** user attempts to access any conversation, **Then** authentication failure is returned
3. **Given** expired JWT token, **When** user attempts to access conversation, **Then** authentication failure is returned

---

### Edge Cases

- What happens when the JWT token is malformed or invalid?
- How does the system handle database connection failures during conversation load/save?
- What occurs when a conversation_id is provided but doesn't exist in the database?
- How does the system handle extremely large messages that exceed size limits?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST follow spec-driven development (all work starts and ends with /specs/)
- **FR-002**: System MUST be implemented using only AI agents (Qwen CLI) - no manual coding
- **FR-003**: System MUST implement strict user isolation via JWT + DB filtering
- **FR-004**: System MUST use stateless JWT auth with shared BETTER_AUTH_SECRET
- **FR-005**: System MUST use the specified tech stack: FastAPI, SQLModel, Neon PostgreSQL
- **FR-006**: System MUST follow monorepo structure: .spec-kit/, specs/, frontend/, backend/
- **FR-007**: System MUST implement all API endpoints as /api/{user_id}/chat with JWT validation
- **FR-008**: System MUST ensure users can only access their own data (no cross-user access)
- **FR-009**: System MUST implement a new POST /api/{user_id}/chat endpoint
- **FR-010**: System MUST require valid JWT token for endpoint access using existing middleware
- **FR-011**: System MUST create a new Conversation in DB if no conversation_id provided
- **FR-012**: System MUST load conversation history from Message table when conversation_id provided
- **FR-013**: System MUST store user message in DB with role "user"
- **FR-014**: System MUST implement placeholder response logic (e.g., echo message) for initial implementation
- **FR-015**: System MUST store assistant response in DB with role "assistant"
- **FR-016**: System MUST return JSON response with format {conversation_id, response, tool_calls: []}
- **FR-017**: System MUST implement stateless design with all persistence in Neon DB (no in-memory state)
- **FR-018**: System MUST NOT modify existing Phase II API endpoints or code
- **FR-019**: System MUST verify JWT using BETTER_AUTH_SECRET
- **FR-020**: System MUST validate that user_id in URL path matches authenticated user

### Key Entities

- **[User]**: Represents an authenticated user with JWT-based access control who can initiate and participate in conversations
- **[Conversation]**: Represents a conversation thread between a user and the AI assistant, with unique identifier and metadata
- **[Message]**: Represents a message within a conversation, with content, role (user/assistant), timestamp, and association to a conversation
- **[JWT Token]**: Stateless authentication token with user identity and permissions used to secure chat communications

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: New POST /api/{user_id}/chat endpoint is successfully implemented and accessible
- **SC-002**: Endpoint properly validates JWT tokens and rejects unauthorized requests
- **SC-003**: Conversations are correctly created in the database when no conversation_id is provided
- **SC-004**: Conversation history is properly loaded from the database when conversation_id is provided
- **SC-005**: User messages are stored in the database with role "user" and timestamp
- **SC-006**: Assistant responses are stored in the database with role "assistant" and timestamp
- **SC-007**: API returns correctly formatted JSON response with conversation_id, response, and empty tool_calls array
- **SC-008**: All conversation state is persisted in Neon DB with no in-memory storage
- **SC-009**: No existing Phase II API endpoints or code are modified during implementation
- **SC-010**: Users can only access their own conversations, with proper access controls enforced