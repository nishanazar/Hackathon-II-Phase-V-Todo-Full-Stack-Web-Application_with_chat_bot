# Implementation Plan: Helm Chart Deployment on Minikube for Phase IV

**Branch**: `014-helm-minikube-deploy` | **Date**: 2026-01-26 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/014-helm-minikube-deploy/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy the Todo application to a Minikube cluster using Helm charts as specified in the feature requirements. The deployment will use the existing Helm chart (todo-chart) with the command `helm install todo ./helm/todo-chart`, verify that all pods are running, confirm services are created, and ensure the application is accessible. At least one command will use kubectl-ai or kagent as required by the specification.

## Technical Context

**Language/Version**: N/A (Infrastructure as Code)
**Primary Dependencies**: Helm v3+, Minikube, kubectl, kubectl-ai/kagent (for AI-enhanced commands)
**Storage**: N/A (Deployment infrastructure)
**Testing**: Manual verification of deployment status
**Target Platform**: Minikube (local Kubernetes cluster)
**Project Type**: Infrastructure deployment
**Performance Goals**: Helm chart installs successfully, pods reach Running state within 5 minutes
**Constraints**: Use existing Docker images (todo-frontend:latest, todo-backend:latest), use kubectl-ai or kagent for at least one command
**Scale/Scope**: Single deployment to local Minikube cluster

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven: All work starts and ends with /specs/
- [x] No manual coding: Only AI agents (Qwen CLI) edit code
- [N/A] Strict user isolation via JWT + DB filtering
- [N/A] Stateless JWT auth with shared BETTER_AUTH_SECRET
- [N/A] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/
- [N/A] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation

## Project Structure

### Documentation (this feature)

```text
specs/014-helm-minikube-deploy/
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
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

helm/
└── todo-chart/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── deployment-frontend.yaml
    │   ├── deployment-backend.yaml
    │   ├── service-frontend.yaml
    │   ├── service-backend.yaml
    │   └── ...
    └── ...
```

**Structure Decision**: Using the existing web application structure with backend and frontend components, deploying via Helm charts to Kubernetes. The Helm chart contains the necessary Kubernetes manifests for both frontend and backend deployments and services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [N/A] | [N/A] |