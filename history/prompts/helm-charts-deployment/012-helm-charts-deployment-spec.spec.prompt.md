---
id: 012
title: helm-charts-deployment-spec
stage: spec
date_iso: 2026-01-25
surface: agent
model: Qwen
feature: helm-charts-deployment
branch: 012-helm-charts-deployment
user: USER
command: sp.specify
labels: ["helm", "kubernetes", "deployment", "specification"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/012-helm-charts-deployment/spec.md
  - specs/012-helm-charts-deployment/checklists/requirements.md
tests_yaml: []
prompt_text: |
  Helm Charts Creation for Phase IV Local Kubernetes Deployment Target audience: Hackathon judges & agentic developers Focus: Create Helm charts to package and deploy frontend and backend Docker images on Minikube Success criteria: - Helm chart created for todo app (single chart or separate for frontend/backend) - Chart includes Deployment, Service for frontend (port 3000) and backend (port 8000) - Env vars passed (GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET) - Uses kubectl-ai or kagent to generate chart templates - Chart installs on Minikube without errors - No changes to Docker images or Phase III code Constraints: - Use Helm 3+ - Reference Phase IV requirements - Prefer kubectl-ai/kagent for generation - Same images (todo-frontend:latest, todo-backend:latest) - Implement via Helm Agent only
response_text: |
  Created feature specification for Helm Charts deployment with the following details:
  
  - Feature: Helm Charts for Phase IV Kubernetes Deployment
  - Branch: 012-helm-charts-deployment
  - User Stories: 
    1. Deploy Application on Kubernetes (P1)
    2. Configure Environment Variables (P2)
    3. Single Chart Deployment (P3)
  - Functional Requirements: 15 requirements defined
  - Success Criteria: 4 measurable outcomes
  - Checklists: Requirements checklist created
outcome: |
  Successfully created the feature specification for Helm charts deployment.
  The specification includes user stories, functional requirements, and success criteria
  for deploying the todo application on Kubernetes using Helm charts.
evaluation: |
  The specification is complete and follows the template structure.
  All mandatory sections have been filled with appropriate content.
  The requirements are testable and success criteria are measurable.
---

# Feature Specification: Helm Charts for Phase IV Kubernetes Deployment

**Feature Branch**: `012-helm-charts-deployment`
**Created**: 2026-01-25
**Status**: Draft
**Input**: User description: "Helm Charts Creation for Phase IV Local Kubernetes Deployment Target audience: Hackathon judges & agentic developers Focus: Create Helm charts to package and deploy frontend and backend Docker images on Minikube Success criteria: - Helm chart created for todo app (single chart or separate for frontend/backend) - Chart includes Deployment, Service for frontend (port 3000) and backend (port 8000) - Env vars passed (GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET) - Uses kubectl-ai or kagent to generate chart templates - Chart installs on Minikube without errors - No changes to Docker images or Phase III code Constraints: - Use Helm 3+ - Reference Phase IV requirements - Prefer kubectl-ai/kagent for generation - Same images (todo-frontend:latest, todo-backend:latest) - Implement via Helm Agent only"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Application on Kubernetes (Priority: P1)

As a hackathon judge or agentic developer, I want to deploy the todo application on a local Kubernetes cluster using Helm charts so that I can run the application in a production-like environment.

**Why this priority**: This is the core functionality that enables the application to run on Kubernetes, which is the primary goal of Phase IV.

**Independent Test**: Can be fully tested by installing the Helm chart on Minikube and verifying that both frontend and backend services are accessible and functioning properly.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** I install the Helm chart with appropriate values, **Then** the frontend service is available on port 3000 and the backend service is available on port 8000
2. **Given** the application is deployed via Helm chart, **When** I access the frontend, **Then** I can interact with the todo application normally

---

### User Story 2 - Configure Environment Variables (Priority: P2)

As a developer, I want to pass environment variables (GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET) through the Helm chart so that the application can connect to external services securely.

**Why this priority**: Essential for the application to function properly with required external services and authentication.

**Independent Test**: Can be tested by verifying that the environment variables are correctly set in the deployed pods and the application can access these values.

**Acceptance Scenarios**:

1. **Given** the Helm chart is configured with environment variables, **When** the pods are deployed, **Then** the environment variables are available in the containers
2. **Given** the application requires GEMINI_API_KEY, **When** the variable is passed via Helm, **Then** the backend can access Gemini services

---

### User Story 3 - Single Chart Deployment (Priority: P3)

As a DevOps engineer, I want a single Helm chart that deploys both frontend and backend services so that I can manage the entire application lifecycle with one deployment unit.

**Why this priority**: Simplifies deployment and management of the application, reducing operational complexity.

**Independent Test**: Can be tested by installing the single chart and verifying that both frontend and backend components are deployed and communicating correctly.

**Acceptance Scenarios**:

1. **Given** a single Helm chart for the todo app, **When** I run helm install, **Then** both frontend and backend deployments and services are created
2. **Given** the single chart is deployed, **When** I upgrade the chart with new image tags, **Then** both frontend and backend deployments are updated

---

### Edge Cases

- What happens when the Minikube cluster doesn't have sufficient resources to run the application?
- How does the system handle incorrect environment variable values during installation?
- What occurs if the Docker images (todo-frontend:latest, todo-backend:latest) are not available in the cluster?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST follow spec-driven development (all work starts and ends with /specs/)
- **FR-002**: System MUST be implemented using only AI agents (Qwen CLI) - no manual coding
- **FR-003**: System MUST implement strict user isolation via JWT + DB filtering
- **FR-004**: System MUST use stateless JWT auth with shared BETTER_AUTH_SECRET
- **FR-005**: System MUST use the specified tech stack: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- **FR-006**: System MUST follow monorepo structure: .spec-kit/, specs/, frontend/, backend/
- **FR-007**: System MUST implement all API endpoints as /api/{user_id}/tasks/* with JWT validation
- **FR-008**: System MUST ensure users can only access their own data (no cross-user access)
- **FR-009**: Helm chart MUST be compatible with Helm 3+
- **FR-010**: Helm chart MUST deploy frontend service on port 3000 and backend service on port 8000
- **FR-011**: Helm chart MUST accept environment variables (GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET) as parameters
- **FR-012**: Helm chart MUST use Docker images todo-frontend:latest and todo-backend:latest
- **FR-013**: Helm chart MUST install successfully on Minikube without errors
- **FR-014**: Helm chart generation SHOULD use kubectl-ai or kagent tools when possible
- **FR-015**: No changes MUST be made to existing Docker images or Phase III code during Helm chart creation

### Key Entities *(include if feature involves data)*

- **[Helm Chart]**: Package containing Kubernetes manifests for deploying the todo application
- **[Deployment]**: Kubernetes resource defining how many replicas of the application to run
- **[Service]**: Kubernetes resource exposing the application on a specific port
- **[Environment Variables]**: Configuration values passed to the application at runtime

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Helm chart successfully installs on Minikube with zero errors during deployment
- **SC-002**: Both frontend (port 3000) and backend (port 8000) services are accessible after Helm installation
- **SC-003**: All required environment variables (GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET) are properly configured in the deployed pods
- **SC-004**: Application functions correctly in the Kubernetes environment with the same capabilities as the non-Kubernetes deployment