# Research Summary: Dapr & Kafka Setup on Cloud Cluster for Phase V

## Decision: Kafka/Redpanda Provider Selection
**Rationale**: Need to choose between Redpanda Cloud (free serverless) and Strimzi for self-hosted Kafka based on the project's "Zero to Minimal Cost" principle and technical requirements.
**Alternatives considered**: 
- Redpanda Cloud: Free serverless tier, easy setup, maintained by provider
- Self-hosted Kafka with Strimzi: More control, runs on same cluster, potential resource overhead
**Decision**: Starting with Redpanda Cloud free tier to align with cost objectives, with migration path to self-hosted if needed.

## Decision: Cloud Provider Selection
**Rationale**: Choose among Oracle OKE (preferred), Azure AKS, or Google GKE based on the "Zero to Minimal Cost" principle and availability.
**Alternatives considered**:
- Oracle OKE: Always Free tier, good Dapr compatibility
- Azure AKS: $200 credit, good ecosystem
- GKE: $300 credit, strong Kubernetes heritage
**Decision**: Oracle OKE due to alignment with specification preference and free tier availability.

## Decision: Dapr Component Configuration
**Rationale**: Configure Dapr pub/sub component to connect to Kafka/Redpanda with appropriate settings for reliability and performance.
**Alternatives considered**:
- Using default settings vs. optimized settings for production
- Different Kafka/Redpanda connection parameters
**Decision**: Start with recommended settings for cloud Kafka/Redpanda, with monitoring to adjust as needed.

## Decision: Testing Approach
**Rationale**: Establish a method to verify that task-events can be published from the backend and consumed/logged in another service.
**Alternatives considered**:
- Unit testing vs. integration testing vs. end-to-end testing
- Mock services vs. real services for testing
**Decision**: Integration testing approach using real services to validate the complete event flow.

## Best Practices for Dapr on Kubernetes
- Use Dapr's sidecar injection via annotations in deployments
- Secure communication between Dapr and Kafka/Redpanda with appropriate authentication
- Monitor Dapr sidecar health and resource usage
- Use Dapr components for secret management rather than environment variables

## Best Practices for Kafka/Redpanda Integration
- Use appropriate partitioning strategy for task-events topic
- Implement proper error handling and retry mechanisms
- Monitor message lag and throughput
- Plan for schema evolution of task-events

## Potential Challenges
- Network connectivity between Dapr sidecars and cloud-based Kafka/Redpanda
- Ensuring no breaking changes to existing Phase V components
- Managing authentication and authorization between services
- Verifying 99% event delivery reliability requirement