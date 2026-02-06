# Data Model: Dapr & Kafka Setup on Cloud Cluster for Phase V

## Dapr Components

### Pub/Sub Component (Kafka/Redpanda)
- **Component Type**: pubsub.kafka or pubsub.resiliency
- **Name**: task-pubsub (or kafka-pubsub)
- **Version**: v1
- **Metadata**:
  - brokers: List of Kafka/Redpanda broker addresses
  - consumerGroup: Consumer group identifier
  - clientID: Client identifier for Kafka/Redpanda
  - authRequired: Boolean indicating if authentication is required
  - saslUsername: SASL username (if auth enabled)
  - saslPassword: SASL password (if auth enabled)
  - maxMessageBytes: Maximum message size allowed
  - version: Kafka protocol version

### State Store Component
- **Component Type**: state.redis or state.postgresql
- **Name**: task-statestore
- **Version**: v1
- **Metadata**:
  - redisHost: Redis host address (if using Redis)
  - redisPassword: Redis password (if required)
  - connectionString: Connection string for PostgreSQL (if using PostgreSQL)

## Task Event Schema

### Task Event Message
- **eventType**: String identifying the type of task event (e.g., "task.created", "task.updated", "task.deleted")
- **taskId**: Unique identifier for the task
- **userId**: Identifier of the user associated with the task
- **timestamp**: ISO 8601 timestamp of the event
- **payload**: Object containing the actual task data
  - title: Task title
  - description: Task description
  - status: Current status of the task
  - priority: Priority level of the task
  - createdAt: Timestamp when task was created
  - updatedAt: Timestamp when task was last updated

## Dapr Sidecar Configuration

### Application Pod Annotations
- **dapr.io/enabled**: "true" to enable Dapr sidecar injection
- **dapr.io/app-id**: Unique identifier for the application
- **dapr.io/app-port**: Port on which the application is listening
- **dapr.io/config**: Name of the Dapr configuration to use
- **dapr.io/components-path**: Path to mount Dapr components (optional)

## Topic Configuration

### Kafka/Redpanda Topics
- **Topic Name**: task-events
- **Partitions**: Number of partitions (typically 3-6 for basic setup)
- **Replication Factor**: Number of replicas (typically 3 for production)
- **Retention Policy**: Time-based or size-based retention settings
- **Cleanup Policy**: Compact, delete, or both