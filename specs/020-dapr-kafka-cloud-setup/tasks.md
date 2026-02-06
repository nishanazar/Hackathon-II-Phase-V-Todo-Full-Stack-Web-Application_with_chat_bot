---

description: "Task list for Dapr & Kafka Setup on Cloud Cluster for Phase V"
---

# Tasks: Dapr & Kafka Setup on Cloud Cluster for Phase V

**Input**: Design documents from `/specs/020-dapr-kafka-cloud-setup/`
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

- [ ] T001 Verify cloud Kubernetes cluster access (Oracle OKE preferred) and kubectl configuration
- [ ] T002 [P] Install Dapr CLI locally if not present
- [X] T003 [P] Install Helm 3.x locally if not present
- [ ] T004 [P] Create Redpanda Cloud account and set up free serverless cluster
- [X] T005 [P] Create necessary directories: dapr/components/, dapr/config/, charts/todo-app/templates/
- [ ] T006 [P] Verify kubectl connection to cloud cluster with `kubectl cluster-info`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Initialize Dapr on the cloud Kubernetes cluster with `dapr init -k`
- [ ] T008 [P] Verify Dapr control plane is running with `dapr status -k`
- [ ] T009 [P] Create Kafka/Redpanda topics: task-events, reminders, task-updates
- [X] T010 [P] Create Dapr pub/sub component configuration file: dapr/components/pubsub.yaml
- [ ] T011 Apply the Dapr pub/sub component to the cluster with `kubectl apply -f dapr/components/pubsub.yaml`
- [X] T012 [P] Create Dapr configuration file: dapr/config/config.yaml for tracing and other settings
- [X] T013 [P] Update Helm chart templates to include Dapr annotations in deployments
- [ ] T014 [P] Verify Dapr components are healthy with `kubectl get pods -n dapr-system`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Cloud Infrastructure Setup (Priority: P1) 🎯 MVP

**Goal**: Install and configure Dapr and Kafka/Redpanda Pub/Sub on the cloud Kubernetes cluster to enable event-driven architecture

**Independent Test**: Can be fully tested by verifying Dapr is initialized on the cloud cluster and Kafka/Redpanda is deployed and healthy

### Implementation for User Story 1

- [ ] T015 [US1] Verify Dapr control plane components are operational within 10 minutes (SC-001)
- [ ] T016 [US1] Verify Kafka/Redpanda Pub/Sub component is deployed and reports healthy status within 15 minutes (SC-002)
- [ ] T017 [US1] Test Dapr pub/sub functionality by publishing a test message to task-events topic
- [ ] T018 [US1] Document Dapr initialization and component commands for cloud deployment in README.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Application Integration with Dapr (Priority: P2)

**Goal**: Enable the application to use Dapr HTTP API for events instead of direct Kafka clients, with Dapr sidecars running in application pods

**Independent Test**: Can be verified by checking that Dapr sidecars are running alongside application pods

### Implementation for User Story 2

- [X] T019 [US2] Update backend deployment to include Dapr sidecar injection annotations
- [X] T020 [US2] Modify backend code to use Dapr pub/sub API instead of direct Kafka client
- [ ] T021 [US2] Verify Dapr sidecars are running in app pods with `kubectl get pods` (SC-003)
- [ ] T022 [US2] Confirm application uses Dapr HTTP API for events (no direct Kafka client) (FR-006)
- [ ] T023 [US2] Test that application can publish events via Dapr to task-events topic

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Event Flow Verification (Priority: P3)

**Goal**: Verify that task-events can be published from the backend and consumed/logged in another service, ensuring end-to-end event-driven functionality

**Independent Test**: Can be tested by publishing a sample task-event and verifying it's received by the consuming service

### Implementation for User Story 3

- [X] T024 [US3] Implement backend endpoint to publish task-events via Dapr pub/sub API
- [X] T025 [US3] Create or update consumer service to receive and log task-events from Dapr
- [ ] T026 [US3] Test end-to-end event flow: publish task-event from backend → consume/log in consumer service
- [ ] T027 [US3] Verify 99% reliability in task-event delivery (SC-004)
- [ ] T028 [US3] Document the event flow verification process and test results

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T029 [P] Update documentation in README.md with cloud Dapr commands and setup instructions
- [ ] T030 Verify no breaking changes to Phase V Steps 1/2/3 (SC-005)
- [ ] T031 [P] Create monitoring dashboard for Dapr and Kafka/Redpanda health
- [ ] T032 Run quickstart.md validation to ensure all steps work correctly
- [ ] T033 Verify all services communicate via Dapr HTTP API instead of direct Kafka clients (SC-006)
- [ ] T034 [P] Update CI/CD pipeline to include Dapr component deployment

## Phase Advanced: Advanced Features Implementation

**Purpose**: Implement advanced features for the Dapr & Kafka Setup

- [ ] T035 [P] Implement Dapr state management component for persistent storage
- [ ] T036 [P] Set up Dapr secrets management component for secure credential handling
- [ ] T037 [P] Configure Dapr service invocation for inter-service communication
- [ ] T038 [P] Implement monitoring and alerting for Dapr and Kafka/Redpanda with Prometheus and Grafana
- [ ] T039 [P] Finalize cloud deployment with proper resource limits and scaling
- [ ] T040 [P] Prepare demo environment with live URL and verify all functionality

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (Dapr infrastructure)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 (Dapr infrastructure and app integration)

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start (though US2 depends on US1 completion, US3 depends on US1 and US2)
- Different user stories can be worked on in parallel by different team members where dependencies allow

---

## Parallel Example: User Story 2

```bash
# Launch all tasks for User Story 2 together (where possible):
Task: "Update backend deployment to include Dapr sidecar injection annotations"
Task: "Modify backend code to use Dapr pub/sub API instead of direct Kafka client"
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
   - Developer B: User Story 2 (after US1 completion)
   - Developer C: User Story 3 (after US1 and US2 completion)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence