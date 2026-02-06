# Implementation Plan: Full Integration & Testing for Phase III Todo AI Chatbot

**Branch**: `011-full-integration-testing` | **Date**: 2026-01-19 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/011-full-integration-testing/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of full integration and testing for the Phase III Todo AI Chatbot. This involves integrating all components (ChatKit UI, chat endpoint, DB, MCP tools, Gemini AI agent) into a fully working, end-to-end chatbot and performing thorough testing. The solution ensures end-to-end flow works reliably, conversation history persists across server restarts, all 5 basic task features work via natural language, user isolation is 100% enforced, errors are handled gracefully, and the README is updated with run instructions.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11, JavaScript/TypeScript, Next.js 16+
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, Better Auth, OpenAI SDK, ChatKit, MCP Tools, Gemini AI
**Storage**: PostgreSQL (Neon) with SQLModel ORM
**Testing**: pytest, Jest, integration testing frameworks
**Target Platform**: Linux server (containerized environment)
**Project Type**: Web application (full-stack with Next.js frontend and FastAPI backend)
**Performance Goals**: <5s response time for AI agent interactions, 95% uptime during testing
**Constraints**: Must integrate with existing MCP tools, maintain statelessness (DB handles state), no changes to Phase II functionality
**Scale/Scope**: Support multiple concurrent users with proper JWT authentication and user isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven: All work starts and ends with /specs/
- [x] No manual coding: Only AI agents (Qwen CLI) edit code
- [x] Strict user isolation via JWT + DB filtering
- [x] Stateless JWT auth with shared BETTER_AUTH_SECRET
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation

## Project Structure

### Documentation (this feature)

```text
specs/011-full-integration-testing/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── chat-api-contract.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
The implementation will extend the existing web application structure:

```text
backend/
├── src/
│   ├── agents/
│   │   └── todo_agent.py      # AI agent implementation
│   ├── models/
│   │   ├── ai_config.py       # AI configuration model
│   │   ├── chat_session.py    # Chat session model
│   │   └── chat_message.py    # Chat message model
│   ├── services/
│   │   ├── ai_config_service.py      # AI config service
│   │   ├── chat_session_service.py   # Chat session service
│   │   └── chat_message_service.py   # Chat message service
│   ├── api/
│   │   └── chat_endpoint.py   # Updated chat endpoint with agent integration
│   └── utils/
│       ├── auth_utils.py      # Authentication utilities
│       └── logger.py          # Logging utilities
└── tests/
    └── agents/
        └── test_todo_agent.py # Tests for the AI agent

frontend/
├── src/
│   └── components/
│       └── ChatKit/           # ChatKit UI component
└── tests/
```

**Structure Decision**: The feature extends the existing web application structure by integrating the AI agent functionality into the existing chat endpoint and updating the UI to work with the agent. This maintains compatibility with the existing architecture while adding the new AI capabilities.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
