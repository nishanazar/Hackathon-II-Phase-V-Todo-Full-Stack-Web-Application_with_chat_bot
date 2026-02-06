# Tasks: Gemini AI Agent with OpenAI Agents SDK for Phase III Todo AI Chatbot

## Overview
This document outlines the implementation tasks for the Gemini AI Agent with OpenAI Agents SDK for Phase III Todo AI Chatbot feature. The implementation follows the spec-driven development approach with tasks organized by user story priority.

## Implementation Strategy
- **MVP Scope**: Focus on User Story 1 (core AI task assistant functionality)
- **Incremental Delivery**: Complete each user story as an independently testable increment
- **Parallel Execution**: Identified tasks that can be executed in parallel are marked with [P]

## Dependencies
- User Story 1 (P1) must be completed before User Story 2 (P2) and User Story 3 (P3)
- Foundational tasks must be completed before any user story tasks

## Parallel Execution Examples
- Tasks T006-T010 can be executed in parallel as they involve creating different components
- Tasks T015-T020 can be executed in parallel as they involve different aspects of the agent

---

## Phase 1: Setup

- [X] T001 Create project structure per implementation plan in backend/src/agents/
- [X] T002 Add OpenAI Agents SDK and related dependencies to backend/requirements.txt
- [X] T003 Update environment variables in backend/.env.example with GEMINI_API_KEY

---

## Phase 2: Foundational

- [X] T004 Create base AI configuration model in backend/src/models/ai_config.py
- [X] T005 [P] Create ChatSession model in backend/src/models/chat_session.py
- [X] T006 [P] Create ChatMessage model in backend/src/models/chat_message.py
- [X] T007 [P] Create AIConfig model in backend/src/models/ai_config.py
- [X] T008 [P] Create database service for ChatSession in backend/src/services/chat_session_service.py
- [X] T009 [P] Create database service for ChatMessage in backend/src/services/chat_message_service.py
- [X] T010 [P] Create database service for AIConfig in backend/src/services/ai_config_service.py
- [X] T011 Implement utility functions for handling JWT in backend/src/utils/auth_utils.py
- [X] T012 Create constants for the AI agent in backend/src/constants/ai_constants.py

---

## Phase 3: User Story 1 - Interact with AI Task Assistant (Priority: P1)

**Story Goal**: Enable users to interact with an AI-powered chatbot that can help manage tasks through natural language commands.

**Independent Test**: Can be fully tested by sending task-related commands to the chat endpoint and verifying the AI agent responds appropriately and performs the requested task operations.

### Implementation Tasks

- [X] T013 [US1] Create the main AI agent module in backend/src/agents/todo_agent.py
- [X] T014 [P] [US1] Configure AsyncOpenAI with Gemini endpoint in backend/src/agents/todo_agent.py
- [X] T015 [P] [US1] Define OpenAIChatCompletionsModel for gemini-1.5-flash in backend/src/agents/todo_agent.py
- [X] T016 [P] [US1] Create Agent with strict task-only system prompt in backend/src/agents/todo_agent.py
- [X] T017 [P] [US1] Implement logic to load conversation history from DB in backend/src/agents/todo_agent.py
- [X] T018 [P] [US1] Implement logic to run agent with user message in backend/src/agents/todo_agent.py
- [X] T019 [P] [US1] Implement logic to handle MCP tool calls in backend/src/agents/todo_agent.py
- [X] T020 [P] [US1] Implement logic to enforce task-only rule with fixed reply in backend/src/agents/todo_agent.py
- [X] T021 [US1] Update the chat endpoint to integrate the AI agent in backend/src/api/chat_endpoint.py
- [ ] T022 [US1] Test the agent with "Add task buy milk" command to verify task creation
- [ ] T023 [US1] Test the agent with "Show tasks" command to verify task listing
- [ ] T024 [US1] Ensure the agent properly creates and returns tasks

---

## Phase 4: User Story 2 - Receive Restricted Responses (Priority: P2)

**Story Goal**: Ensure the AI agent only responds to task-related queries and rejects unrelated requests.

**Independent Test**: Can be tested by sending non-task-related queries to the AI agent and verifying it responds with the restricted message.

### Implementation Tasks

- [X] T025 [US2] Enhance the system prompt to strictly enforce task-only responses in backend/src/agents/todo_agent.py
- [X] T026 [US2] Implement detection logic for non-task-related queries in backend/src/agents/todo_agent.py
- [X] T027 [US2] Ensure the agent responds with fixed message "Sorry, I only help with your tasks..." for unrelated queries in backend/src/agents/todo_agent.py
- [X] T028 [US2] Test the agent with "Hello how are you" command to verify fixed reply
- [X] T029 [US2] Test the agent with various non-task queries to ensure consistent behavior

---

## Phase 5: User Story 3 - Use MCP Tools for Task Operations (Priority: P3)

**Story Goal**: Ensure the AI agent utilizes all 5 MCP tools for task management operations.

**Independent Test**: Can be tested by triggering various task operations and verifying the appropriate MCP tools are called.

### Implementation Tasks

- [X] T030 [US3] Attach add_task MCP tool to the agent in backend/src/agents/todo_agent.py
- [X] T031 [US3] Attach list_tasks MCP tool to the agent in backend/src/agents/todo_agent.py
- [X] T032 [US3] Attach update_task MCP tool to the agent in backend/src/agents/todo_agent.py
- [X] T033 [US3] Attach delete_task MCP tool to the agent in backend/src/agents/todo_agent.py
- [X] T034 [US3] Attach complete_task MCP tool to the agent in backend/src/agents/todo_agent.py
- [X] T035 [US3] Test that add_task tool is invoked when user requests to add a task
- [X] T036 [US3] Test that list_tasks tool is invoked when user requests to list tasks
- [X] T037 [US3] Test that update_task tool is invoked when user requests to update a task
- [X] T038 [US3] Test that delete_task tool is invoked when user requests to delete a task
- [X] T039 [US3] Test that complete_task tool is invoked when user requests to complete a task

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T040 Add error handling for invalid GEMINI_API_KEY in backend/src/agents/todo_agent.py
- [ ] T041 Implement rate limiting for the Gemini API in backend/src/middleware/rate_limit.py
- [X] T042 Add logging for AI agent interactions in backend/src/utils/logger.py
- [X] T043 Create comprehensive tests for the AI agent functionality in backend/tests/agents/test_todo_agent.py
- [X] T044 Update documentation for the new AI agent feature in backend/docs/ai_agent.md
- [ ] T045 Perform integration testing of the complete AI agent workflow
- [ ] T046 Optimize performance of the AI agent for faster response times
- [ ] T047 Conduct security review of the AI agent implementation