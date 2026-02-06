# Dapr Pub/Sub Contract for Task Events

## Overview
This contract defines the interface for publishing and subscribing to task-related events using Dapr's pub/sub building block with Kafka/Redpanda as the underlying message broker.

## Publish Endpoint
### POST /v1.0/publish/{pubsubname}/{topic}

Publish a task event to the specified topic.

#### Path Parameters
- `pubsubname` (string, required): Name of the pub/sub component (e.g., "task-pubsub")
- `topic` (string, required): Name of the topic to publish to (e.g., "task-events")

#### Request Body
```json
{
  "eventType": "task.created",
  "taskId": "12345",
  "userId": "user123",
  "timestamp": "2026-01-31T10:00:00Z",
  "payload": {
    "title": "Sample Task",
    "description": "A sample task for demonstration",
    "status": "pending",
    "priority": "medium",
    "createdAt": "2026-01-31T10:00:00Z",
    "updatedAt": "2026-01-31T10:00:00Z"
  }
}
```

#### Headers
- `Content-Type`: application/json
- `dapr-app-id`: (optional) ID of the calling application

#### Response
- Status Code: 204 (No Content) on successful publication
- Status Code: 400 (Bad Request) if the payload is invalid
- Status Code: 500 (Internal Server Error) if publication fails

## Subscribe Endpoint
### GET /v1.0/subscriptions/{pubsubname}

Retrieve subscription information for the specified pub/sub component.

#### Path Parameters
- `pubsubname` (string, required): Name of the pub/sub component (e.g., "task-pubsub")

#### Response
```json
{
  "pubsubname": "task-pubsub",
  "topic": "task-events",
  "route": "/tasks/events"
}
```

## Subscription Handler
### POST /tasks/events

Handler endpoint that receives task events from the pub/sub component.

#### Request Body
Same format as the publish request body.

#### Response
- Status Code: 200 (OK) to acknowledge successful processing
- Status Code: 500 (Internal Server Error) to trigger retry

## Error Handling
- Network timeouts will result in retries according to Dapr's built-in retry mechanism
- Invalid payloads should return 400 status codes
- Processing errors should return 500 status codes to trigger retries