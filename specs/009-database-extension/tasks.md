# Tasks: MCP Server & Tools Implementation for Phase III

**Feature**: MCP Server & Tools Implementation for Phase III
**Branch**: `009-database-extension`
**Spec**: `/specs/009-database-extension/spec.md`
**Plan**: `/specs/009-database-extension/plan.md`

## Implementation Strategy

Build an MCP (Model Context Protocol) server in FastAPI that provides 5 standardized tools for AI agents to interact with the database. The implementation will use SQLModel for database operations with proper user isolation via JWT authentication. Each user story will be implemented as a complete, independently testable increment.

## Dependencies

User stories should be implemented in priority order (US1 → US2 → US3). US1 is foundational and required for other stories. US3 (secure data isolation) is validation-focused and can be tested after US1 and US2 implementations.

## Parallel Execution Examples

Within each user story phase, the following tasks can be executed in parallel:
- Model creation tasks (Conversation and Message models)
- Service layer tasks (once models are defined)
- Multiple tool implementations (once models and services are available)

## Phase 1: Setup

Initial project setup and dependency installation.

- [X] T001 Add mcp-sdk-python dependency to pyproject.toml
- [X] T002 Create backend/mcp_server.py file with basic server structure
- [X] T003 Create backend/services/mcp_tools.py file for tool implementations
- [X] T004 Create backend/routes/mcp.py file for route definitions (if needed)

## Phase 2: Foundational Components

Core components needed for all user stories.

- [X] T005 Create Conversation model in backend/models/conversation.py using SQLModel
- [X] T006 Create Message model in backend/models/message.py using SQLModel
- [X] T007 Implement database session management in backend/database.py
- [X] T008 Create base authentication utility in backend/utils/auth.py to validate JWT and extract user_id

## Phase 3: User Story 1 - Store Chat Conversation Data (Priority: P1)

As an authenticated user, I want my chat conversations to be stored in the database so that I can continue conversations across sessions and devices.

**Independent Test**: Can be fully tested by initiating a chat conversation, verifying that messages are stored in the Message table, and that conversation metadata is stored in the Conversation table.

- [X] T009 [US1] Implement create_conversation tool in backend/services/mcp_tools.py
- [X] T010 [US1] Implement add_message tool in backend/services/mcp_tools.py
- [X] T011 [US1] Register create_conversation and add_message tools with MCP server in backend/mcp_server.py
- [X] T012 [US1] Test storing new conversation and message in database

## Phase 4: User Story 2 - Retrieve Chat History (Priority: P2)

As an authenticated user, I want to retrieve my chat history so that I can continue conversations where I left off.

**Independent Test**: Can be tested by retrieving conversation history from the database and verifying that all messages for a specific conversation are returned in chronological order.

- [X] T013 [US2] Implement get_conversation_history tool in backend/services/mcp_tools.py
- [X] T014 [US2] Implement list_user_conversations tool in backend/services/mcp_tools.py
- [X] T015 [US2] Register get_conversation_history and list_user_conversations tools with MCP server in backend/mcp_server.py
- [X] T016 [US2] Test retrieving conversation history and user's conversations

## Phase 5: User Story 3 - Secure Data Isolation (Priority: P3)

As a system administrator, I want to ensure that users can only access their own conversations so that data privacy is maintained.

**Independent Test**: Can be tested by attempting to access another user's conversations and verifying that access is denied.

- [X] T017 [US3] Enhance all tools to validate user_id from JWT matches user_id in request parameters
- [X] T018 [US3] Implement update_message tool in backend/services/mcp_tools.py with user validation
- [X] T019 [US3] Register update_message tool with MCP server in backend/mcp_server.py
- [X] T020 [US3] Test that users can only access their own data and not others'

## Phase 6: Integration and Mounting

Integrate the MCP server with the main FastAPI application.

- [X] T021 Mount MCP server at /mcp in backend/main.py
- [X] T022 Update backend/main.py to handle JWT authentication for MCP endpoints
- [X] T023 Test end-to-end functionality of all 5 MCP tools

## Phase 7: Polish & Cross-Cutting Concerns

Final touches and cross-cutting concerns.

- [X] T024 Add proper error handling and logging to all MCP tools
- [X] T025 Add input validation to all MCP tools according to API contract
- [X] T026 Write comprehensive tests for all MCP tools
- [X] T027 Update documentation with usage examples
- [X] T028 Perform security review of JWT validation implementation