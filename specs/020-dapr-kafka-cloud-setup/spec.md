# Feature Specification: Dapr & Kafka Setup on Cloud Cluster for Phase V

**Feature Branch**: `020-dapr-kafka-cloud-setup`
**Created**: 2026-01-31
**Status**: Draft
**Input**: User description: "Dapr & Kafka Setup on Cloud Cluster for Phase V Target audience: Hackathon judges & agentic developers Focus: Install and configure Dapr and Kafka/Redpanda Pub/Sub on the cloud Kubernetes cluster (OKE/AKS/GKE) Success criteria: - Dapr initialized on cloud cluster (dapr init -k) - Kafka/Redpanda Pub/Sub component deployed and healthy - Dapr sidecars running in app pods (kubectl get pods) - Test Pub/Sub: publish task-event from backend → consume/log in another service - App uses Dapr HTTP API for events (no direct Kafka client) - No breaking changes to Phase V Step 1/2/3 - Cloud cluster used (Oracle OKE preferred) Constraints: - Use Dapr CLI and Helm for installation - Prefer Redpanda Cloud (free serverless) or Strimzi for self-hosted Kafka - Reference Phase V documentation (Dapr architecture, Kafka use cases) - Implement manually or via AI-assisted tools (kubectl-ai/kagent)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cloud Infrastructure Setup (Priority: P1)

As a hackathon judge or agentic developer, I want to have Dapr and Kafka/Redpanda properly installed and configured on the cloud Kubernetes cluster so that I can leverage event-driven architecture for microservices communication.

**Why this priority**: This is foundational for all other functionality. Without properly configured messaging infrastructure, the application cannot function as intended.

**Independent Test**: Can be fully tested by verifying Dapr is initialized on the cloud cluster and Kafka/Redpanda is deployed and healthy.

**Acceptance Scenarios**:

1. **Given** a cloud Kubernetes cluster (preferably Oracle OKE), **When** Dapr is initialized using `dapr init -k`, **Then** Dapr control plane components are deployed and operational
2. **Given** Dapr is running on the cluster, **When** Kafka/Redpanda Pub/Sub component is deployed, **Then** the messaging system is healthy and accessible

---

### User Story 2 - Application Integration with Dapr (Priority: P2)

As a hackathon judge or agentic developer, I want the application to use Dapr HTTP API for events instead of direct Kafka clients so that I can have standardized service communication and reduced complexity.

**Why this priority**: This enables the application to leverage Dapr's abstractions for pub/sub, making the system more maintainable and portable.

**Independent Test**: Can be verified by checking that Dapr sidecars are running alongside application pods.

**Acceptance Scenarios**:

1. **Given** application pods are deployed, **When** Dapr is configured for the services, **Then** Dapr sidecars are running in app pods as verified by `kubectl get pods`
2. **Given** Dapr sidecars are present, **When** the application publishes events, **Then** it uses Dapr HTTP API instead of direct Kafka client

---

### User Story 3 - Event Flow Verification (Priority: P3)

As a hackathon judge or agentic developer, I want to verify that task-events can be published from the backend and consumed/logged in another service so that I can confirm the end-to-end event-driven functionality works correctly.

**Why this priority**: This validates that the entire event-driven architecture is functioning as expected.

**Independent Test**: Can be tested by publishing a sample task-event and verifying it's received by the consuming service.

**Acceptance Scenarios**:

1. **Given** Dapr and Kafka/Redpanda are configured, **When** backend service publishes a task-event, **Then** another service consumes and logs the event successfully

---

### Edge Cases

- What happens when the Kafka/Redpanda cluster becomes temporarily unavailable?
- How does the system handle message backlogs during high traffic periods?
- What occurs if Dapr sidecar fails to initialize in an application pod?
- How does the system handle authentication and authorization for pub/sub communications?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST install and configure Dapr on the cloud Kubernetes cluster (dapr init -k)
- **FR-002**: System MUST deploy and configure Kafka/Redpanda Pub/Sub component on the cluster
- **FR-003**: System MUST ensure Dapr sidecars are running in application pods
- **FR-004**: System MUST enable publishing of task-events from backend via Dapr HTTP API
- **FR-005**: System MUST enable consumption and logging of events in another service
- **FR-006**: System MUST use Dapr HTTP API for events (no direct Kafka client)
- **FR-007**: System MUST maintain compatibility with Phase V Steps 1/2/3 (no breaking changes)
- **FR-008**: System MUST prefer Oracle OKE as the cloud Kubernetes cluster
- **FR-009**: System MUST use Dapr CLI and Helm for installation
- **FR-010**: System MUST prefer Redpanda Cloud (free serverless) or Strimzi for self-hosted Kafka
- **FR-011**: System MAY leverage AI-assisted tools (kubectl-ai/kagent) for implementation
- **FR-012**: System MUST reference Phase V documentation for Dapr architecture and Kafka use cases

### Key Entities

- **[Dapr Control Plane]**: Components that manage service discovery, configuration, and distributed tracing
- **[Kafka/Redpanda Cluster]**: Messaging system for pub/sub event communication between services
- **[Application Pods]**: Containerized services that will have Dapr sidecars injected
- **[Task Events]**: Domain-specific events related to task management that will be published and consumed

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dapr is successfully initialized on the cloud cluster with all control plane components operational within 10 minutes
- **SC-002**: Kafka/Redpanda Pub/Sub component is deployed and reports healthy status within 15 minutes
- **SC-003**: At least 95% of application pods have Dapr sidecars running as verified by `kubectl get pods`
- **SC-004**: Task-event can be successfully published from backend service and consumed/logged in another service with 99% reliability
- **SC-005**: Application continues to function without breaking changes to Phase V Steps 1/2/3
- **SC-006**: All services communicate via Dapr HTTP API instead of direct Kafka clients (0 direct Kafka connections)
