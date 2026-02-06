# Implementation Plan: Floating AI Chat Widget

**Branch**: `007-floating-chat-widget` | **Date**: 2026-01-17 | **Spec**: [001-floating-chat-widget/spec.md](../001-floating-chat-widget/spec.md)
**Input**: Feature specification from `/specs/007-floating-chat-widget/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a floating AI chat widget using OpenAI ChatKit that appears in the bottom-right corner of all pages for authenticated users. The widget allows users to access AI help without navigating away from the current page, without modifying any existing Phase II code or UI. The solution uses the existing authentication system (Better Auth + JWT) to ensure secure communication and proper user isolation.

## Technical Context

**Language/Version**: TypeScript/JavaScript for frontend, Python 3.11 for backend
**Primary Dependencies**: Next.js 16+ App Router, OpenAI ChatKit JS Agent (@openai/chatkit-jsagent), Better Auth, Tailwind CSS
**Storage**: N/A (client-side component with backend API communication)
**Testing**: Jest, React Testing Library (for frontend components)
**Target Platform**: Web application (cross-platform browser support)
**Project Type**: Web application (frontend component integration)
**Performance Goals**: Sub-200ms chat panel load time, responsive UI without affecting main page performance
**Constraints**: Must not modify any existing application code, UI, pages, components, or logic; widget must be responsive and support dark mode
**Scale/Scope**: Available to all authenticated users across the entire application

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
specs/007-floating-chat-widget/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   └── FloatingChat/
│   │       ├── FloatingChatProvider.tsx    # Global provider for the chat widget
│   │       ├── FloatingChatWidget.tsx      # The main floating chat component
│   │       └── FloatingChatIcon.tsx        # The floating icon button
│   └── app/
│       └── layout.tsx                      # Wrapper to mount the chat globally
└── tests/
    └── components/
        └── FloatingChat/
            └── FloatingChatWidget.test.tsx # Tests for the chat widget
```

**Structure Decision**: Web application structure selected as this is a frontend component integration. The floating chat widget will be implemented as a set of React components in the frontend directory, with a global provider mounted at the application root level to ensure the widget appears on all pages without modifying existing code.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None) | (Not applicable) | (Not applicable) |
