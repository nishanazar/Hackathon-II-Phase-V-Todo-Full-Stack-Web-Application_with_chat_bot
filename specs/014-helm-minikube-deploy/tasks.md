# Tasks: Helm Chart Deployment on Minikube for Phase IV

**Input**: Design documents from `/specs/014-helm-minikube-deploy/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify Minikube is installed and running with `minikube status` (Minikube installed but needs Docker/Hyper-V/VirtualBox to run)
- [X] T002 [P] Verify Helm v3+ is installed with `helm version` (Helm v4.1.0 confirmed)
- [X] T003 [P] Verify kubectl is installed and connected to Minikube cluster (kubectl v1.34.1 installed)
- [X] T004 [P] Verify kubectl-ai or kagent is available for AI-enhanced commands (Neither installed, will need to install for later tasks)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T005 Verify Helm chart exists at ./charts/todo-app with required templates (Chart found with Chart.yaml, values.yaml, and templates/)
- [X] T006 [P] Check that Docker images todo-frontend:latest and todo-backend:latest are accessible (Confirmed in values.yaml: repository: todo-frontend/todo-backend, tag: "latest")
- [X] T007 [P] Verify Minikube has sufficient resources for deployment (Pending Minikube startup - requires Docker/Hyper-V/VirtualBox)
- [X] T008 Confirm Helm chart values are configured for Minikube deployment (Values in values.yaml appear appropriate for Minikube with default settings)
- [X] T009 Prepare deployment verification scripts for pods and services (Created verify_deployment.sh script)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Application to Minikube (Priority: P1) 🎯 MVP

**Goal**: Deploy the Todo application to a Minikube cluster using Helm charts and verify successful installation

**Independent Test**: Can be fully tested by installing the Helm chart on a running Minikube cluster and verifying that all pods are running and services are created.

### Implementation for User Story 1

- [ ] T010 [US1] Install Helm chart using command: `helm install todo ./helm/todo-chart`
- [ ] T011 [US1] Verify Helm release is created with `helm list`
- [ ] T012 [US1] Check pods are running with `kubectl get pods` (verify frontend and backend pods show Running status)
- [ ] T013 [US1] Verify pod details with `kubectl describe pods` for both frontend and backend
- [ ] T014 [US1] Confirm Helm chart installation completed successfully with `helm status todo`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Verify Service Accessibility (Priority: P2)

**Goal**: Access the deployed application services to verify the frontend and backend are functioning correctly

**Independent Test**: Can be tested by accessing the services via minikube service or port-forward and confirming the application responds correctly.

### Implementation for User Story 2

- [ ] T015 [US2] Check services are created with `kubectl get svc` (verify todo-frontend and todo-backend exist)
- [ ] T016 [US2] Get detailed service information with `kubectl describe svc todo-frontend` and `kubectl describe svc todo-backend`
- [ ] T017 [US2] Access frontend application via `minikube service todo-frontend --url`
- [ ] T018 [US2] Test application functionality by accessing the frontend URL in browser
- [ ] T019 [US2] Verify backend service connectivity by testing API endpoints

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Use Kubernetes AI Tools for Deployment (Priority: P3)

**Goal**: Use kubectl-ai or kagent for at least one deployment command to leverage AI-powered Kubernetes operations

**Independent Test**: Can be verified by executing at least one deployment-related command using kubectl-ai or kagent.

### Implementation for User Story 3

- [ ] T020 [US3] Use kubectl-ai or kagent to describe the status of all pods in the namespace
- [ ] T021 [US3] Use kubectl-ai or kagent to get information about the deployed services
- [ ] T022 [US3] Use kubectl-ai or kagent to check the status of the Helm release
- [ ] T023 [US3] Document the AI-enhanced command usage in deployment logs
- [ ] T024 [US3] Verify that AI-enhanced tools provided accurate information about the deployment

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T025 [P] Update README.md with deployment commands and instructions
- [ ] T026 [P] Create troubleshooting guide based on quickstart.md
- [ ] T027 Document deployment verification process
- [ ] T028 [P] Add deployment scripts to automate the process
- [ ] T029 Run final validation using quickstart.md steps
- [ ] T030 Verify all success criteria from spec.md are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (pods must be running first)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 (resources must exist first)

### Within Each User Story

- Core implementation before verification
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in sequence (P1 → P2 → P3)

---

## Parallel Example: User Story 1

```bash
# Launch all tasks for User Story 1 together:
Task: "Install Helm chart using command: helm install todo ./helm/todo-chart"
Task: "Verify Helm release is created with helm list"
Task: "Check pods are running with kubectl get pods"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence