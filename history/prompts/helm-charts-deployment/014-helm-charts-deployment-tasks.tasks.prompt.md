---
id: 014
title: helm-charts-deployment-tasks
stage: tasks
date_iso: 2026-01-25
surface: agent
model: Qwen
feature: helm-charts-deployment
branch: 012-helm-charts-deployment
user: USER
command: sp.tasks
labels: ["helm", "kubernetes", "deployment", "tasks"]
links:
  spec: ../specs/012-helm-charts-deployment/spec.md
  plan: ../specs/012-helm-charts-deployment/plan.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/012-helm-charts-deployment/tasks.md
tests_yaml: []
prompt_text: |
  /sp.tasks Helm Charts Creation for Phase IV
  Create: Helm chart(s) for frontend and backend deployment
  Decisions:
  - Single chart vs separate charts (single chart for simplicity)
  - Replica count: 1 (hackathon) vs 2+ (production-ready)
  - Service type: ClusterIP (local Minikube)
  Phases:
  1. Install Helm (if not installed)
  2. Use kubectl-ai or kagent to generate initial chart
  3. Create Chart.yaml, values.yaml, templates/deployment.yaml, service.yaml
  4. Add env vars from values.yaml
  5. Test: helm lint, helm install --dry-run
  6. Update README with helm install command
response_text: |
  Created comprehensive task breakdown for Helm Charts deployment with the following structure:
  
  - Phase 1: Setup (5 tasks)
  - Phase 2: Foundational Tasks (9 tasks)
  - Phase 3: User Story 1 - Deploy Application on Kubernetes (11 tasks)
  - Phase 4: User Story 2 - Configure Environment Variables (11 tasks)
  - Phase 5: User Story 3 - Single Chart Deployment (10 tasks)
  - Phase 6: Polish & Cross-Cutting Concerns (7 tasks)
  
  Total: 53 tasks organized by user story priority
  Tasks follow proper format with checkboxes, IDs, story labels, and file paths
  Dependencies and parallel execution opportunities identified
  MVP scope defined as User Story 1
outcome: |
  Successfully created the task breakdown for Helm charts deployment.
  All tasks follow the required checklist format and are organized by user story priority.
  The tasks are specific enough to be executed by an LLM without additional context.
evaluation: |
  The task breakdown is complete and follows the template structure.
  All tasks follow the required checklist format with proper IDs, story labels, and file paths.
  Dependencies between user stories are clearly identified.
  Parallel execution opportunities are noted where appropriate.
---
# Implementation Tasks: Helm Charts for Phase IV Kubernetes Deployment

**Feature**: 012-helm-charts-deployment | **Date**: 2026-01-25

## Implementation Strategy

This implementation will follow an MVP-first approach, delivering the core functionality in the first user story, then enhancing with additional features in subsequent stories. Each user story is designed to be independently testable and deliverable.

**MVP Scope**: User Story 1 (Deploy Application on Kubernetes) with basic Helm chart creation and deployment.

## Dependencies

- User Story 1 (P1) must be completed before US2 and US3 can begin
- US2 (P2) and US3 (P3) can be developed in parallel after US1 completion

## Parallel Execution Examples

- Once US1 foundation is established, US2 (environment variables) and US3 (single chart enhancements) can be worked on in parallel
- Templates for frontend and backend can be developed in parallel after foundational chart structure is created

---

## Phase 1: Setup

### Goal
Prepare the development environment and initialize the Helm chart structure.

- [ ] T001 Create charts/ directory at project root
- [ ] T002 Initialize todo-app Helm chart using `helm create` command
- [ ] T003 [P] Install Helm CLI if not already installed
- [ ] T004 [P] Install kubectl-ai or kagent tools as specified in requirements
- [ ] T005 Verify Minikube is available and running

---

## Phase 2: Foundational Tasks

### Goal
Establish the core Helm chart structure with basic configuration that will support all user stories.

- [ ] T006 Update Chart.yaml with proper name, version, and description for todo-app
- [ ] T007 Create initial values.yaml with frontend and backend configurations
- [ ] T008 [P] Create templates/_helpers.tpl with standard Helm helper functions
- [ ] T009 [P] Create templates/NOTES.txt with post-installation instructions
- [ ] T010 Create basic frontend deployment template in templates/frontend-deployment.yaml
- [ ] T011 Create basic backend deployment template in templates/backend-deployment.yaml
- [ ] T012 Create basic frontend service template in templates/frontend-service.yaml
- [ ] T013 Create basic backend service template in templates/backend-service.yaml
- [ ] T014 Verify basic chart structure with `helm lint`

---

## Phase 3: User Story 1 - Deploy Application on Kubernetes (Priority: P1)

### Goal
Enable deployment of the todo application on a local Kubernetes cluster using Helm charts.

### Independent Test Criteria
Can be fully tested by installing the Helm chart on Minikube and verifying that both frontend and backend services are accessible and functioning properly.

- [ ] T015 [US1] Configure frontend deployment to use todo-frontend:latest image
- [ ] T016 [US1] Configure backend deployment to use todo-backend:latest image
- [ ] T017 [US1] Set frontend service to expose port 3000 as specified in requirements
- [ ] T018 [US1] Set backend service to expose port 8000 as specified in requirements
- [ ] T019 [US1] Set replica count to 1 for both frontend and backend deployments
- [ ] T020 [US1] Add proper labels and selectors to connect deployments with services
- [ ] T021 [US1] Test basic functionality with `helm install todo-app . --dry-run`
- [ ] T022 [US1] Deploy chart to Minikube and verify services are created
- [ ] T023 [US1] Verify frontend service is accessible on port 3000
- [ ] T024 [US1] Verify backend service is accessible on port 8000
- [ ] T025 [US1] Validate that application functions normally after deployment

---

## Phase 4: User Story 2 - Configure Environment Variables (Priority: P2)

### Goal
Pass environment variables (GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET) through the Helm chart to connect to external services securely.

### Independent Test Criteria
Can be tested by verifying that the environment variables are correctly set in the deployed pods and the application can access these values.

- [ ] T026 [US2] Add environment variable definitions to values.yaml
- [ ] T027 [US2] Update frontend deployment template to include environment variables
- [ ] T028 [US2] Update backend deployment template to include environment variables
- [ ] T029 [US2] Add GEMINI_API_KEY as environment variable in backend deployment
- [ ] T030 [US2] Add DATABASE_URL as environment variable in backend deployment
- [ ] T031 [US2] Add BETTER_AUTH_SECRET as environment variable in backend deployment
- [ ] T032 [US2] Test environment variable configuration with `helm install --dry-run`
- [ ] T033 [US2] Deploy chart with environment variables and verify they're set in pods
- [ ] T034 [US2] Verify application can access Gemini services using the API key
- [ ] T035 [US2] Validate that all required environment variables are properly configured in deployed pods

---

## Phase 5: User Story 3 - Single Chart Deployment (Priority: P3)

### Goal
Ensure the Helm chart properly deploys both frontend and backend services as a unified unit with proper configuration.

### Independent Test Criteria
Can be tested by installing the single chart and verifying that both frontend and backend components are deployed and communicating correctly.

- [ ] T036 [US3] Enhance Chart.yaml with proper dependencies and metadata
- [ ] T037 [US3] Add conditional enabling of frontend and backend in values.yaml
- [ ] T038 [US3] Update deployment templates to respect enabled/disabled flags
- [ ] T039 [US3] Add resource requests and limits to deployment templates
- [ ] T040 [US3] Add health checks (liveness and readiness probes) to deployments
- [ ] T041 [US3] Test complete single-chart deployment with all components
- [ ] T042 [US3] Verify both frontend and backend deployments are created with single install
- [ ] T043 [US3] Test upgrading the chart with new image tags
- [ ] T044 [US3] Verify both frontend and backend deployments update during upgrade
- [ ] T045 [US3] Document the single-chart deployment process in README.md

---

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with documentation, testing, and final validation.

- [ ] T046 Create comprehensive README.md for the Helm chart
- [ ] T047 Add troubleshooting section to quickstart guide
- [ ] T048 Perform final validation: `helm lint`, `helm install --dry-run`
- [ ] T049 Deploy complete chart to fresh Minikube instance for final test
- [ ] T050 Verify all success criteria from feature specification are met
- [ ] T051 Clean up any temporary files or test configurations
- [ ] T052 Update project documentation with Helm deployment instructions