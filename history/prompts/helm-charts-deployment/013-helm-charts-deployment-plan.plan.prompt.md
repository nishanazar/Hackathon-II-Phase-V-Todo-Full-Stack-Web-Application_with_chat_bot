---
id: 013
title: helm-charts-deployment-plan
stage: plan
date_iso: 2026-01-25
surface: agent
model: Qwen
feature: helm-charts-deployment
branch: 012-helm-charts-deployment
user: USER
command: sp.plan
labels: ["helm", "kubernetes", "deployment", "planning"]
links:
  spec: ../specs/012-helm-charts-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/012-helm-charts-deployment/plan.md
  - specs/012-helm-charts-deployment/research.md
  - specs/012-helm-charts-deployment/data-model.md
  - specs/012-helm-charts-deployment/quickstart.md
  - specs/012-helm-charts-deployment/contracts/helm-chart-contract.md
tests_yaml: []
prompt_text: |
  /sp.plan Helm Charts Creation for Phase IV
  Create: Helm chart(s) for frontend and backend deployment
  Decisions:
  - Single chart vs separate charts (single chart for simplicity)
  - Replica count: 1 (hackathon) vs 2+ (production-ready)
  - Service type: ClusterIP (local Minikube)
  Phases:
  1. Install Helm if not present
  2. Use kubectl-ai or kagent to generate initial chart
  3. Create Chart.yaml, values.yaml, templates/deployment.yaml, service.yaml
  4. Add env vars from values.yaml
  5. Test: helm lint, helm install --dry-run
  6. Update README with helm install command
response_text: |
  Created comprehensive implementation plan for Helm Charts deployment with the following artifacts:
  
  - Implementation Plan: specs/012-helm-charts-deployment/plan.md
  - Research: specs/012-helm-charts-deployment/research.md
  - Data Model: specs/012-helm-charts-deployment/data-model.md
  - Quickstart Guide: specs/012-helm-charts-deployment/quickstart.md
  - Contract: specs/012-helm-charts-deployment/contracts/helm-chart-contract.md
  
  The plan includes:
  - Single chart approach for simplicity
  - 1 replica for hackathon/demo environment
  - ClusterIP service type for local Minikube
  - Proper environment variable handling via values.yaml
  - Helm 3+ and Kubernetes v1.25+ compatibility
  - Complete data model for Helm chart structure
  - Quickstart guide for users
  - API contract for the Helm chart
outcome: |
  Successfully created the implementation plan for Helm charts deployment.
  All required artifacts have been generated according to the template structure.
  The plan addresses all requirements from the feature specification.
evaluation: |
  The implementation plan is complete and follows the template structure.
  All mandatory sections have been filled with appropriate content.
  The research, data model, quickstart guide, and contracts have been created.
  Constitution check has been performed and all requirements are met.
---

# Implementation Plan: Helm Charts for Phase IV Kubernetes Deployment

**Branch**: `012-helm-charts-deployment` | **Date**: 2026-01-25 | **Spec**: [link to spec.md](spec.md)
**Input**: Feature specification from `/specs/012-helm-charts-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create Helm charts to package and deploy the todo application frontend and backend on Minikube. The implementation will use a single chart with deployments and services for both frontend (port 3000) and backend (port 8000), passing required environment variables (GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET) through the chart values.

## Technical Context

**Language/Version**: Helm 3+, Kubernetes v1.25+ or later
**Primary Dependencies**: Helm CLI, Minikube, kubectl, kubectl-ai or kagent (for chart generation)
**Storage**: N/A (Configuration stored in Kubernetes ConfigMaps/Secrets)
**Testing**: Helm lint, Helm install --dry-run, Manual verification on Minikube
**Target Platform**: Local Kubernetes cluster (Minikube)
**Project Type**: Infrastructure-as-Code/Deployment
**Performance Goals**: Chart installs within 5 minutes on local Minikube cluster
**Constraints**: Must use existing Docker images (todo-frontend:latest, todo-backend:latest), no changes to Phase III code, environment variables must be configurable via values.yaml
**Scale/Scope**: Single cluster deployment for hackathon/demo purposes, single replica per service

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven: All work starts and ends with /specs/
- [x] No manual coding: Only AI agents (Qwen CLI) edit code
- [x] Strict user isolation via JWT + DB filtering (existing feature, not modified)
- [x] Stateless JWT auth with shared BETTER_AUTH_SECRET (existing feature, not modified)
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT (existing features, not modified)
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/ (existing structure maintained)
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation (existing feature, not modified)

## Project Structure

### Documentation (this feature)

```text
specs/012-helm-charts-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
charts/
└── todo-app/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── frontend-deployment.yaml
    │   ├── backend-deployment.yaml
    │   ├── frontend-service.yaml
    │   ├── backend-service.yaml
    │   └── NOTES.txt
    └── README.md
```

**Structure Decision**: Creating a new charts/ directory at the root level to house the Helm chart for the todo application. This follows common practice for storing Helm charts alongside the application code. The single chart approach simplifies deployment for the hackathon demo while maintaining separation from the existing frontend/backend code.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

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