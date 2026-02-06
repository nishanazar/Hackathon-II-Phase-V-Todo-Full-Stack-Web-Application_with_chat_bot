# Feature Specification: Dapr & Kafka Setup on Minikube for Phase V

**Feature Branch**: `017-dapr-kafka-minikube-setup`
**Created**: 2026-01-29
**Status**: Draft
**Input**: User description: "Dapr & Kafka Setup on Minikube for Phase V Target audience: Hackathon judges & agentic developers Focus: Install and configure Dapr on Minikube and set up Kafka/Redpanda Pub/Sub component for event-driven features Success criteria: - Dapr initialized on Minikube (dapr init -k) - Kafka/Redpanda Pub/Sub component deployed (kafka-pubsub or redpanda-pubsub) - Dapr sidecars running in pods (kubectl get pods -n dapr-system) - Test Pub/Sub: publish task-event and consume it - App uses Dapr for Pub/Sub (no direct Kafka client code) - No breaking changes to Phase V Step 1 features - Local Minikube cluster used Constraints: - Use Dapr CLI and Helm for installation - Prefer Redpanda (Kafka-compatible, simpler) or Strimzi for self-hosted Kafka - Reference Phase V documentation (Dapr architecture, Kafka use cases) - Implement via Dapr Agent only Not building: - Cloud deployment (next steps) - Full Dapr features (Jobs, Secrets, State — later) - Advanced monitoring (Phase V later)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dapr Infrastructure Setup (Priority: P1)

As a developer working on the Phase V Todo AI Chatbot, I want Dapr to be properly installed and configured on Minikube so that I can leverage Dapr's building blocks for my application.

**Why this priority**: This is foundational infrastructure that all other Dapr features depend on. Without a properly configured Dapr runtime, none of the event-driven features can be implemented.

**Independent Test**: Can be fully tested by verifying Dapr control plane components are running in the dapr-system namespace and the Dapr CLI can communicate with the runtime.

**Acceptance Scenarios**:

1. **Given** Minikube cluster is running, **When** Dapr is initialized with `dapr init -k`, **Then** Dapr control plane pods are deployed and running in the dapr-system namespace.
2. **Given** Dapr is installed on Minikube, **When** I run `dapr status -k`, **Then** I see all Dapr control plane components reporting healthy status.

---

### User Story 2 - Kafka/Redpanda Pub/Sub Component Setup (Priority: P2)

As a developer, I want a Kafka or Redpanda Pub/Sub component configured in Dapr so that my application can use event-driven architecture patterns for task notifications and reminders.

**Why this priority**: This enables the core event-driven functionality needed for task notifications and other async communications in the Todo AI Chatbot application.

**Independent Test**: Can be tested by deploying the Kafka/Redpanda component to the cluster and verifying it's recognized by Dapr.

**Acceptance Scenarios**:

1. **Given** Dapr is running on Minikube, **When** Kafka/Redpanda Pub/Sub component is deployed, **Then** Dapr runtime recognizes the component and can establish connections to it.
2. **Given** Kafka/Redpanda component is configured, **When** I check Dapr component status, **Then** the pub/sub component shows as active and healthy.

---

### User Story 3 - Application Integration with Dapr Pub/Sub (Priority: P3)

As a user of the Todo AI Chatbot, I want task events to be published via Dapr Pub/Sub so that other services can react to task changes asynchronously.

**Why this priority**: This delivers the end-user value by enabling the event-driven features that were designed in previous phases, such as notifications and automated task processing.

**Independent Test**: Can be tested by publishing a test task event and verifying it can be consumed by a subscriber service.

**Acceptance Scenarios**:

1. **Given** Dapr Pub/Sub is configured with Kafka/Redpanda, **When** a task event is published through Dapr, **Then** the event is successfully delivered to subscribed services.
2. **Given** Task event is published, **When** I monitor the Kafka/Redpanda topic, **Then** I can see the event message was properly serialized and stored.

### Edge Cases

- What happens when the Kafka/Redpanda cluster is temporarily unavailable?
- How does the system handle Dapr sidecar failures in application pods?
- What occurs if there are network partitions between application pods and Dapr sidecars?
- How does the system handle high-volume event publishing that might overwhelm the Kafka cluster?
- What happens if the Minikube cluster runs out of resources during Dapr/Kafka operations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST install Dapr runtime on Minikube using `dapr init -k` command
- **FR-002**: System MUST deploy Kafka or Redpanda as the Pub/Sub component for Dapr
- **FR-003**: System MUST configure Dapr to use Kafka/Redpanda as a pub/sub component
- **FR-004**: System MUST verify Dapr sidecars are running in application pods
- **FR-005**: System MUST test Pub/Sub functionality by publishing and consuming task-events
- **FR-006**: System MUST ensure the application uses Dapr for Pub/Sub (no direct Kafka client code)
- **FR-007**: System MUST maintain compatibility with existing Phase V Step 1 features
- **FR-008**: System MUST use Dapr CLI and Helm for all installation and configuration tasks
- **FR-009**: System SHOULD prefer Redpanda over Kafka if both options are viable (due to simplicity)
- **FR-010**: System MUST use local Minikube cluster for the setup
- **FR-011**: System MUST document the Dapr and Kafka/Redpanda configuration for future reference
- **FR-012**: System MUST provide verification steps to confirm successful setup
- **FR-013**: System MUST not break existing functionality during the setup process

### Key Entities *(include if feature involves data)*

- **[Dapr Runtime]**: Distributed Application Runtime running on Minikube that provides building blocks for the application
- **[Kafka/Redpanda Cluster]**: Event streaming platform used as the underlying Pub/Sub component for Dapr
- **[Dapr Sidecar]**: Per-application proxy that provides Dapr functionality to the main application container
- **[Pub/Sub Component]**: Dapr component that enables asynchronous messaging between services
- **[Task Event]**: Event published to Kafka/Redpanda topics when task-related actions occur
- **[Application Pod]**: Kubernetes pod containing the main application container and Dapr sidecar

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
