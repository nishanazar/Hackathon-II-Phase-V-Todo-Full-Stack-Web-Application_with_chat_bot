# Implementation Plan: Minikube Setup & Helm Deployment for Phase IV

**Branch**: `013-minikube-helm-deployment` | **Date**: 2026-01-25 | **Spec**: [link to spec.md](spec.md)
**Input**: Feature specification from `/specs/013-minikube-helm-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Set up a local Kubernetes cluster using Minikube and deploy the Todo Chatbot application using the existing Helm chart. The implementation will configure kubectl to communicate with the Minikube cluster, install the Helm chart, and ensure the frontend (port 3000) and backend (port 8000) services are accessible. At least one operation will be performed using kubectl-ai or kagent tools as specified in the requirements.

## Technical Context

**Language/Version**: Bash/PowerShell scripting, Helm v3+, Kubernetes v1.25+
**Primary Dependencies**: Minikube, kubectl, Helm, kubectl-ai or kagent (for at least one operation)
**Storage**: N/A (Configuration stored in Kubernetes ConfigMaps/Secrets)
**Testing**: Manual verification using kubectl commands, Helm status checks, port-forwarding tests
**Target Platform**: Local development environment (Windows, macOS, or Linux)
**Project Type**: Infrastructure-as-Code/Deployment
**Performance Goals**: Minikube cluster starts within 5 minutes, Helm chart installs within 2 minutes
**Constraints**: Must use existing Docker images (todo-frontend:latest, todo-backend:latest), no changes to existing Helm chart, must use kubectl-ai or kagent for at least one operation
**Scale/Scope**: Single local cluster deployment for hackathon/demo purposes, single replica per service

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven: All work starts and ends with /specs/
- [x] No manual coding: Only AI agents (Qwen CLI) edit code
- [x] Strict user isolation via JWT + DB filtering (existing feature, not modified)
- [x] Stateless JWT auth with shared BETTER_AUTH_SECRET (existing feature, not modified)
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT (existing features, not modified)
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/ (existing structure maintained)
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation (existing feature, not modified)

## Post-Design Constitution Check

*Updated after Phase 1 design completion*

- [x] Spec-driven: All work starts and ends with /specs/ - Confirmed
- [x] No manual coding: Only AI agents (Qwen CLI) edit code - Confirmed
- [x] Strict user isolation via JWT + DB filtering (existing feature, not modified) - Confirmed
- [x] Stateless JWT auth with shared BETTER_AUTH_SECRET (existing feature, not modified) - Confirmed
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT (existing features, not modified) - Confirmed
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/ (existing structure maintained) - Confirmed
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation (existing feature, not modified) - Confirmed

*All constitution requirements continue to be met after the design phase.*

## Project Structure

### Documentation (this feature)

```text
specs/013-minikube-helm-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# No new source code required - leveraging existing Helm chart
# from charts/todo-app/
```

**Structure Decision**: No new source code structure is needed as this feature leverages the existing Helm chart from the previous feature (012-helm-charts-deployment). The implementation will focus on deployment and configuration of the existing chart to a Minikube cluster.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |