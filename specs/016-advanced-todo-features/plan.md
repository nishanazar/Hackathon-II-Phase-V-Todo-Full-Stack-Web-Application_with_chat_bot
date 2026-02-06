# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements advanced capabilities for the Todo AI Chatbot by extending the task model with due dates, priorities, tags, and recurring intervals. It includes recurring task logic that automatically generates the next occurrence when a task is completed, due date reminders using Dapr Jobs API or Kafka pub/sub, and enhanced search, filter, and sort functionality. The implementation follows event-driven architecture principles using Dapr and Kafka/Redpanda for all async communication, maintaining compatibility with existing Phase III functionality.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript (Next.js 16+)
**Primary Dependencies**: FastAPI, Next.js 16+ App Router, SQLModel, Neon PostgreSQL, Better Auth + JWT, Dapr SDK, Kafka/Redpanda
**Storage**: Neon PostgreSQL database accessed via SQLModel ORM
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (frontend + backend) deployed on Kubernetes
**Project Type**: Web application (frontend + backend)
**Performance Goals**:
- Users can create tasks with due dates, priorities, and tags in under 30 seconds
- Recurring tasks automatically generate next occurrence within 1 second of marking current task as complete
- Search functionality returns relevant results in under 1 second for datasets of up to 1000 tasks
**Constraints**:
- No breaking changes to existing Phase III functionality
- Must maintain stateless design principles
- All new features must integrate with existing authentication system (Better Auth + JWT)
- Use Dapr for all inter-service communication, pub/sub, and scheduling
- Use Kafka/Redpanda for all event streaming and async communication
**Scale/Scope**: Designed to handle up to 1000 tasks per user with efficient filtering and sorting

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Agentic Dev Stack: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- [x] Cloud-Native First: Design for scalability, loose coupling, observability, and portability
- [x] Event-Driven Architecture: Use Kafka/Redpanda for all async communication
- [x] Dapr Everywhere: All inter-service communication, state, pub/sub, secrets, and scheduling via Dapr sidecars
- [x] AI-Assisted Ops: Use kubectl-ai, Kagent, and Claude Code for Kubernetes, Helm, and infra tasks
- [x] Zero to Minimal Cost: Prefer Oracle Always Free OKE, Redpanda Cloud free tier, Azure/GCP free credits
- [x] Demo-Ready: Final output must be a live cloud URL + GitHub repo with CI/CD pipeline
- [x] Judges Focus: Show advanced features, event-driven design, Dapr abstraction, AI-assisted deployment, and monitoring
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation
- [x] Dapr integration for all service communication, state management, pub/sub, and secrets
- [x] Kafka/Redpanda for all event streaming and async communication
- [x] Containerized deployment with Docker and orchestrated via Kubernetes
- [x] CI/CD pipeline via GitHub Actions
- [x] Monitoring with Prometheus + Grafana or cloud-native solutions

## Project Structure

### Documentation (this feature)

```text
specs/016-advanced-todo-features/
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
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── task_model.py          # Extended task model with due_date, priority, tags, recurring_interval
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py        # Task CRUD operations with new features
│   │   ├── recurring_service.py   # Logic for recurring tasks
│   │   ├── reminder_service.py    # Reminder scheduling and delivery
│   │   └── search_service.py      # Search, filter, sort functionality
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependency injection
│   │   ├── auth.py                # Authentication middleware
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── task_router.py     # Task endpoints with new features
│   ├── dapr/
│   │   ├── __init__.py
│   │   ├── dapr_client.py         # Dapr integration
│   │   └── pubsub.py              # Pub/Sub components
│   └── main.py                    # Application entry point
└── tests/
    ├── unit/
    │   ├── test_task_model.py
    │   ├── test_recurring_service.py
    │   └── test_reminder_service.py
    └── integration/
        ├── test_task_endpoints.py
        └── test_search_endpoints.py

frontend/
├── src/
│   ├── components/
│   │   ├── TaskForm.tsx           # Updated form with due date, priority, tags inputs
│   │   ├── TaskList.tsx           # Task list with filtering, sorting
│   │   ├── TaskCard.tsx           # Individual task display
│   │   ├── DatePicker.tsx         # Date picker component
│   │   ├── PrioritySelector.tsx   # Priority selection component
│   │   └── TagInput.tsx           # Tag input component
│   ├── pages/
│   │   ├── index.tsx              # Main dashboard
│   │   └── tasks/
│   │       └── [id].tsx           # Individual task view
│   ├── services/
│   │   ├── api.ts                 # API client
│   │   └── auth.ts                # Authentication utilities
│   ├── hooks/
│   │   ├── useTasks.ts            # Task management hook
│   │   └── useFilters.ts          # Filtering and sorting hook
│   └── types/
│       └── task.ts                # Task type definitions
└── tests/
    ├── __mocks__/
    ├── unit/
    │   ├── TaskForm.test.tsx
    │   └── TaskList.test.tsx
    └── integration/
        └── pages/
            └── index.test.tsx

dapr/
├── components/
│   ├── pubsub.yaml                # Kafka/Redpanda pub/sub configuration
│   └── statestore.yaml            # State store configuration
└── config.yaml                    # Dapr configuration

kafka/
├── topics/
│   ├── task-events.yaml           # Task events topic configuration
│   └── reminders.yaml             # Reminders topic configuration
└── docker-compose.kafka.yml       # Kafka development setup
```

**Structure Decision**: Web application with separate frontend and backend components, following the existing monorepo structure. The feature extends the existing task model and API with new fields and functionality while maintaining backward compatibility.

## Phase 0: Outline & Research

Research completed in `research.md`. All technical unknowns have been resolved:

- Recurring logic implementation decided (Dapr Jobs API)
- Priority levels defined (1-5 scale)
- Tags implementation confirmed (array of strings)
- Search/Filter/Sort approach finalized (backend API with query params)
- Reminder system architecture selected (Dapr + Kafka pub/sub)

## Phase 1: Design & Contracts

Design artifacts completed:

- Data model documented in `data-model.md`
- API contracts created in `/contracts/` directory
- Quickstart guide created in `quickstart.md`
- Agent context updated

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
