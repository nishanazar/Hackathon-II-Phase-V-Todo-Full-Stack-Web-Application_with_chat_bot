# Implementation Plan: MCP Server & Tools Implementation for Phase III

**Branch**: `009-database-extension` | **Date**: 2026-01-18 | **Spec**: [link]
**Input**: Feature specification from `/specs/009-database-extension/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of MCP (Model Context Protocol) server in FastAPI with 5 tool definitions, database integration, and stateless execution. The MCP server will be mounted at /mcp and will provide standardized tools for the AI agents to interact with the system. The implementation will use SQLModel for database operations with proper user isolation via JWT authentication.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT, mcp-sdk-python
**Storage**: Neon PostgreSQL database (same as existing application)
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Web application backend service
**Performance Goals**: <200ms p95 for tool execution, support 1000+ concurrent users
**Constraints**: Must follow existing JWT auth patterns, integrate with existing database schema, maintain user isolation
**Scale/Scope**: Support multiple concurrent AI agents using MCP tools, handle high volume of tool calls

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven: All work starts and ends with /specs/
- [x] No manual coding: Only AI agents (Qwen CLI) edit code
- [x] Strict user isolation via JWT + DB filtering
- [x] Stateless JWT auth with shared BETTER_AUTH_SECRET
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation (ADAPTED: MCP endpoints will follow /mcp/* pattern but still enforce JWT validation)

## Project Structure

### Documentation (this feature)

```text
specs/009-database-extension/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── mcp_server.py        # New MCP server implementation
├── routes/
│   └── mcp.py          # MCP route definitions
├── models/
│   ├── __init__.py
│   ├── conversation.py # Conversation model
│   └── message.py      # Message model
├── services/
│   ├── __init__.py
│   └── mcp_tools.py    # MCP tool implementations
└── main.py             # Main FastAPI app with MCP mount

pyproject.toml          # Updated with mcp-sdk-python dependency
```

**Structure Decision**: Web application backend service following the existing monorepo structure with new MCP-specific files integrated into the backend directory.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| API endpoint pattern | MCP protocol requires /mcp/* endpoints | Standardizing on MCP protocol for model context exchange |
