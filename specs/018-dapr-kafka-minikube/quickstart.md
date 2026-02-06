# Quickstart Guide: Dapr & Kafka Setup on Minikube

## Overview
This guide provides step-by-step instructions to set up Dapr and Kafka/Redpanda on Minikube for event-driven features. This infrastructure enables applications to use Dapr's pub/sub API for reliable messaging without direct Kafka client code.

## Prerequisites
- Minikube installed and running
- kubectl configured to connect to Minikube
- Helm 3.x installed
- Dapr CLI installed

## Step 1: Verify Prerequisites

First, ensure Minikube is running:

```bash
minikube status
```

If Minikube is not running, start it:

```bash
minikube start
```

Verify kubectl can connect to your cluster:

```bash
kubectl cluster-info
```

## Step 2: Install Dapr on Minikube

Initialize Dapr on your Kubernetes cluster:

```bash
dapr init -k
```

Verify Dapr is running:

```bash
kubectl get pods -n dapr-system
```

You should see pods like `dapr-operator`, `dapr-placement-server`, `dapr-sentry`, and `dapr-dashboard` running.

## Step 3: Deploy Redpanda (Kafka-compatible broker)

Add the Redpanda Helm repository:

```bash
helm repo add redpanda https://charts.redpanda.com
helm repo update
```

Install Redpanda to your Minikube cluster:

```bash
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --create-namespace \
  --set resources.memory.container.max=512Mi \
  --set resources.memory.container.min=512Mi \
  --set resources.cpu.container.max=500m \
  --set resources.cpu.container.min=250m \
  --set console.resources.memory.request=256Mi \
  --set console.resources.memory.limit=256Mi \
  --set console.resources.cpu.request=250m \
  --set console.resources.cpu.limit=250m
```

Wait for Redpanda to be ready:

```bash
kubectl wait --for=condition=ready pod --selector=app.kubernetes.io/name=redpanda --timeout=300s -n redpanda
```

## Step 4: Create Dapr Pub/Sub Component Configuration

Create a file named `kafka-pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  # Kafka broker connection setting
  - name: brokers
    value: "redpanda-0.redpanda.redpanda.svc.cluster.local:9093"
  - name: authType
    value: "none"
  - name: consumerGroup
    value: "task-event-group"
  - name: clientID
    value: "dapr-consumer"
  - name: disableAutoCommit
    value: "false"
  - name: maxMessageBytes
    value: 1048576
  - name: consumeRetryInterval
    value: 100ms
```

Apply the configuration to your cluster:

```bash
kubectl apply -f kafka-pubsub.yaml
```

## Step 5: Verify Setup

Check that the Dapr component is registered:

```bash
kubectl get components
```

You should see the `kafka-pubsub` component listed.

## Step 6: Test Pub/Sub Functionality

Create a simple test publisher to send a task event:

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: test-publisher
spec:
  containers:
  - name: publisher
    image: curlimages/curl
    command: 
    - sleep
    - "3600"
    resources:
      requests:
        memory: "64Mi"
        cpu: "25m"
      limits:
        memory: "128Mi"
        cpu: "50m"
  restartPolicy: Never
EOF
```

Wait for the pod to be ready:

```bash
kubectl wait --for=condition=ready pod test-publisher
```

Publish a test task event:

```bash
kubectl exec test-publisher -- curl -X POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "event-1",
    "eventType": "task.created",
    "userId": "user-123",
    "taskId": "task-456",
    "timestamp": "2026-01-29T10:00:00Z",
    "payload": {
      "title": "Test task",
      "description": "This is a test task event"
    }
  }'
```

Clean up the test publisher:

```bash
kubectl delete pod test-publisher
```

## Step 7: Update Applications to Use Dapr Pub/Sub

To use Dapr pub/sub in your applications, add the Dapr sidecar annotation to your deployments:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-app
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "your-app-id"
        dapr.io/app-port: "8000"  # Port your app listens on
        dapr.io/components-path: "/dapr-components"
    spec:
      containers:
      - name: app
        image: your-app-image
```

To publish events from your application, make HTTP requests to Dapr:

```bash
curl -X POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "event-1",
    "eventType": "task.created",
    "userId": "user-123",
    "taskId": "task-456",
    "timestamp": "2026-01-29T10:00:00Z",
    "payload": {
      "title": "Test task",
      "description": "This is a test task event"
    }
  }'
```

## Troubleshooting

### Dapr Sidecar Issues
If Dapr sidecars are not starting, check the Dapr system pods:

```bash
kubectl get pods -n dapr-system
```

### Redpanda Connection Issues
If applications can't connect to Redpanda, verify the service is running:

```bash
kubectl get svc -n redpanda
```

### Component Status
Check the status of your Dapr components:

```bash
kubectl describe components
```

Look for any error messages in the status conditions.

## Next Steps

1. Integrate Dapr pub/sub into your application services
2. Implement event subscribers that listen to task-events
3. Set up monitoring for your pub/sub system
4. Scale your Redpanda cluster as needed