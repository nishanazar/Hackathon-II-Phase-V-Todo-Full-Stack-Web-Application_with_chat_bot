# Feature Specification: Dapr & Kafka Setup on Minikube

**Feature Branch**: `018-dapr-kafka-minikube`
**Created**: 2026-01-29
**Status**: Draft
**Input**: User description: "Dapr & Kafka Setup on Minikube for Phase V Target audience: Hackathon judges & agentic developers Focus: Install and configure Dapr on Minikube and set up Kafka/Redpanda Pub/Sub component for event-driven features Success criteria: - Dapr initialized on Minikube (dapr init -k) - Kafka/Redpanda Pub/Sub component deployed (kafka-pubsub or redpanda-pubsub) - Dapr sidecars running in pods (kubectl get pods -n dapr-system) - Test Pub/Sub: publish task-event and consume it - App uses Dapr for Pub/Sub (no direct Kafka client code) - No breaking changes to Phase V Step 1 features - Local Minikube cluster used Constraints: - Use Dapr CLI and Helm for installation - Prefer Redpanda (Kafka-compatible, simpler) or Strimzi for self-hosted Kafka - Reference Phase V documentation (Dapr architecture, Kafka use cases) - Implement via Dapr Agent only Not building: - Cloud deployment (next steps) - Full Dapr features (Jobs, Secrets, State — later) - Advanced monitoring (Phase V later)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dapr & Kafka Infrastructure Setup (Priority: P1)

As a hackathon judge or agentic developer, I want to have Dapr and Kafka/Redpanda properly set up on Minikube so that I can test event-driven features of the application.

**Why this priority**: This is foundational infrastructure that enables all event-driven features of the application.

**Independent Test**: Can be fully tested by verifying Dapr is initialized on Minikube and Kafka/Redpanda is running, delivering core infrastructure value.

**Acceptance Scenarios**:

1. **Given** a fresh Minikube cluster, **When** Dapr is initialized with `dapr init -k`, **Then** Dapr sidecars are available in the cluster
2. **Given** Dapr is running on Minikube, **When** Kafka/Redpanda Pub/Sub component is deployed, **Then** messaging infrastructure is available for applications

---

### User Story 2 - Event Publishing and Consumption (Priority: P2)

As an agentic developer, I want to publish and consume events through Dapr's pub/sub API so that I can implement event-driven features without direct Kafka client code.

**Why this priority**: This validates that the infrastructure is properly connected and functional for application use.

**Independent Test**: Can be tested by publishing a sample event and verifying it can be consumed, demonstrating end-to-end functionality.

**Acceptance Scenarios**:

1. **Given** Dapr and Kafka/Redpanda are running on Minikube, **When** a task-event is published via Dapr pub/sub API, **Then** the event is successfully delivered and can be consumed
2. **Given** a consumer application is subscribed to task-events, **When** events are published, **Then** the consumer receives and processes them correctly

---

### User Story 3 - Application Integration with Dapr (Priority: P3)

As an application developer, I want to use Dapr for pub/sub communication so that I can decouple services and implement event-driven architecture without complex Kafka client code.

**Why this priority**: This ensures the infrastructure serves its intended purpose of simplifying application development.

**Independent Test**: Can be validated by integrating a simple application with Dapr pub/sub and confirming it works without direct Kafka dependencies.

**Acceptance Scenarios**:

1. **Given** an application component, **When** it uses Dapr pub/sub APIs, **Then** it can publish and subscribe to events without direct Kafka client code
2. **Given** existing Phase V features, **When** Dapr & Kafka setup is deployed, **Then** no breaking changes occur to existing functionality

---

### Edge Cases

- What happens when Kafka/Redpanda components fail or become unavailable?
- How does the system handle high-volume event publishing that might overwhelm the messaging system?
- What occurs if Dapr sidecars fail to initialize or become unresponsive?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST initialize Dapr on Minikube using `dapr init -k` command
- **FR-002**: System MUST deploy Kafka/Redpanda Pub/Sub component using Dapr component configuration
- **FR-003**: System MUST verify Dapr sidecars are running in pods with `kubectl get pods -n dapr-system`
- **FR-004**: System MUST enable publishing and consuming of task-events through Dapr pub/sub API
- **FR-005**: System MUST ensure applications use Dapr for pub/sub without direct Kafka client code
- **FR-006**: System MUST maintain compatibility with existing Phase V Step 1 features
- **FR-007**: System MUST use Dapr CLI and Helm for installation and configuration
- **FR-008**: System MUST prefer Redpanda (Kafka-compatible, simpler) or Strimzi for self-hosted Kafka
- **FR-009**: System MUST run on local Minikube cluster as specified in constraints

### Key Entities *(include if feature involves data)*

- **[Dapr Sidecar]**: Service mesh component that handles communication, state, and pub/sub for applications
- **[Kafka/Redpanda Broker]**: Messaging system that handles pub/sub event distribution
- **[Pub/Sub Component]**: Dapr component that abstracts the underlying messaging infrastructure
- **[Task Event]**: Application-specific event representing task-related activities that flow through the system

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dapr is successfully initialized on Minikube with all required sidecars running (verifiable with `kubectl get pods -n dapr-system`)
- **SC-002**: Kafka/Redpanda Pub/Sub component is deployed and operational (confirmable through Dapr component status)
- **SC-003**: At least one task-event can be published and consumed successfully through Dapr pub/sub API
- **SC-004**: Applications can use Dapr for pub/sub without including direct Kafka client dependencies
- **SC-005**: All existing Phase V Step 1 features continue to function without breaking changes after Dapr & Kafka setup