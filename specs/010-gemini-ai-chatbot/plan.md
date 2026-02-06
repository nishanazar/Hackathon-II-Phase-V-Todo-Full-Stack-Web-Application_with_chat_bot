# Implementation Plan: Gemini AI Agent with OpenAI Agents SDK for Phase III Todo AI Chatbot

**Branch**: `010-gemini-ai-chatbot` | **Date**: 2026-01-19 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/010-gemini-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Gemini AI Agent using OpenAI Agents SDK for Phase III Todo AI Chatbot. The agent will be configured with a Gemini hack using the OpenAI-compatible endpoint, feature a strict system prompt that only responds to task-related queries, integrate with all 5 MCP tools, and be integrated into the existing chat endpoint. The solution will use gemini-1.5-flash model and maintain statelessness with database handling state persistence.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11
**Primary Dependencies**: OpenAI Agents SDK, FastAPI, SQLModel, Better Auth, async-openai, python-dotenv
**Storage**: PostgreSQL (Neon) with SQLModel ORM
**Testing**: pytest
**Target Platform**: Linux server (containerized environment)
**Project Type**: Web application (backend service for AI agent integration)
**Performance Goals**: <5s response time for AI agent queries, 95% accuracy in task management operations
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
specs/010-gemini-ai-chatbot/
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
│   │   └── todo_agent.py      # New AI agent implementation
│   ├── models/
│   ├── services/
│   └── api/
│       └── chat_endpoint.py   # Updated chat endpoint with agent integration
└── tests/

frontend/                    # Unchanged from existing structure
```

**Structure Decision**: The feature extends the existing web application structure by adding a new AI agent module in the backend and updating the chat endpoint to integrate with the agent. This maintains compatibility with the existing architecture while adding the new AI capabilities.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
