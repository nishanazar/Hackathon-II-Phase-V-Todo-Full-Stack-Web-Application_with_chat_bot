# Research: Dapr & Kafka Setup on Minikube

## Overview
This research document addresses the unknowns and decisions required for implementing Dapr & Kafka Setup on Minikube as specified in the feature requirements.

## Decision Points

### 1. Kafka Implementation Choice
**Decision**: Use Redpanda instead of Apache Kafka
**Rationale**: Redpanda is Kafka-API compatible but simpler to deploy and manage, aligning with the constraint "Prefer Redpanda (Kafka-compatible, simpler) or Strimzi for self-hosted Kafka". Redpanda requires fewer resources and has a simpler configuration compared to a full Kafka/Zookeeper setup.
**Alternatives considered**: 
- Apache Kafka with Zookeeper (more complex, requires more resources)
- Strimzi operator (Kubernetes-native, but more complex than Redpanda)
- Confluent OSS (similar complexity to Apache Kafka)

### 2. Dapr Pub/Sub Component Configuration
**Decision**: Create a Dapr component configuration for Redpanda/Kafka
**Rationale**: Dapr provides a pub/sub building block that abstracts the underlying message broker. Creating a proper component configuration allows applications to use Dapr's pub/sub API without direct Kafka client code, satisfying FR-005.
**Configuration details**:
- Component type: `pubsub.kafka` (works with both Kafka and Redpanda)
- Broker address: Internal Kubernetes service address
- Topics: task-events (as specified in user stories)

### 3. Deployment Strategy
**Decision**: Deploy Redpanda via Helm chart, Dapr via CLI
**Rationale**: 
- Dapr provides `dapr init -k` command specifically for Kubernetes deployment, meeting FR-001
- Redpanda offers official Helm charts that simplify deployment and configuration
- Both approaches align with FR-007 (using Dapr CLI and Helm)

### 4. Testing Approach
**Decision**: Create a simple publisher and subscriber to validate pub/sub functionality
**Rationale**: To satisfy FR-004 (enable publishing and consuming of task-events) and SC-003 (task-event can be published and consumed successfully), we need to implement a basic test that publishes a task-event and verifies it can be consumed.
**Implementation approach**:
- Use Dapr's HTTP API to publish events
- Create a simple subscriber service that logs received events
- Verify end-to-end functionality

### 5. Integration with Existing Services
**Decision**: Update existing services with Dapr annotations for pub/sub
**Rationale**: To ensure applications can use Dapr for pub/sub without direct Kafka client code (FR-005), existing services need to be updated with Dapr sidecar annotations and configured to use Dapr's pub/sub API.
**Approach**:
- Add Dapr annotations to existing deployments
- Update application code to use Dapr pub/sub endpoints instead of direct Kafka clients
- Maintain backward compatibility during transition

## Best Practices Applied

### Dapr Deployment
- Use official Dapr Helm chart for production deployments
- For development/minikube, `dapr init -k` is sufficient
- Enable tracing and monitoring from the start
- Follow Dapr security best practices (mTLS enabled by default)

### Kafka/Redpanda Deployment
- Use official Redpanda Helm chart
- Configure appropriate resource limits for Minikube environment
- Set up proper persistence if needed
- Configure topic replication appropriately for single-node setup

### Pub/Sub Patterns
- Use topic-based pub/sub for loose coupling
- Implement proper error handling and retry mechanisms
- Follow Dapr pub/sub API best practices
- Design topic naming conventions (e.g., task-events)

## Technology Stack
- Dapr (Distributed Application Runtime)
- Redpanda (Kafka-compatible event streaming platform)
- Minikube (local Kubernetes cluster)
- Helm (package manager for Kubernetes)
- kubectl (Kubernetes command-line tool)

## Architecture Considerations
- Event-driven architecture with loose coupling between services
- Asynchronous communication patterns
- Scalability considerations for pub/sub
- Fault tolerance and resilience patterns
- Monitoring and observability for event flows