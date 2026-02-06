# Quickstart Guide: Dapr & Kafka Setup on Cloud Cluster for Phase V

## Prerequisites
- Access to a cloud Kubernetes cluster (Oracle OKE preferred)
- Dapr CLI installed locally
- kubectl configured to connect to the cloud cluster
- Helm 3.x installed locally
- Access to Redpanda Cloud account (or Kafka cluster details)

## Step 1: Verify Cluster Connection
```bash
kubectl cluster-info
kubectl get nodes
```

## Step 2: Install Dapr on the Cloud Cluster
```bash
# Initialize Dapr on the Kubernetes cluster
dapr init -k

# Verify Dapr control plane is running
dapr status -k
```

## Step 3: Configure Kafka/Redpanda Connection
If using Redpanda Cloud:
1. Log into your Redpanda Cloud Console
2. Get the connection details (brokers, SASL credentials)
3. Store these securely (we'll use Dapr secrets later)

If using self-hosted Kafka with Strimzi:
1. Deploy Kafka cluster using Strimzi operators
2. Get the service endpoint details

## Step 4: Create Dapr Component Configuration
Create a file named `task-pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "your-redpanda-brokers-list"  # Replace with actual brokers
  - name: consumerGroup
    value: "task-group"
  - name: clientID
    value: "dapr-producer-consumer"
  - name: authRequired
    value: "true"
  - name: saslUsername
    value: "your-sasl-username"  # Replace with actual username
  - name: saslPassword
    value: "your-sasl-password"  # Replace with actual password
  - name: maxMessageBytes
    value: 1048576
  - name: version
    value: 2.1.1
```

## Step 5: Apply Dapr Component
```bash
kubectl apply -f task-pubsub.yaml
```

## Step 6: Update Application Deployments
Add Dapr annotations to your application deployments:

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
        dapr.io/app-port: "8000"  # Replace with your app port
        dapr.io/config: "dapr-config"
    spec:
      containers:
      - name: your-app
        image: your-image:tag
```

## Step 7: Test Event Publishing
Use the Dapr API to publish a test event:

```bash
curl -X POST http://localhost:3500/v1.0/publish/task-pubsub/task-events \
  -H "Content-Type: application/json" \
  -d '{
    "eventType": "task.created",
    "taskId": "12345",
    "userId": "user123",
    "timestamp": "2026-01-31T10:00:00Z",
    "payload": {
      "title": "Test Task",
      "description": "A test task for verification",
      "status": "pending",
      "priority": "medium",
      "createdAt": "2026-01-31T10:00:00Z",
      "updatedAt": "2026-01-31T10:00:00Z"
    }
  }'
```

## Step 8: Verify Sidecar Injection
```bash
kubectl get pods
# You should see 2 containers in each pod (your app + daprd)
```

## Troubleshooting
- If Dapr isn't initializing, check cluster RBAC permissions
- If events aren't publishing, verify Kafka/Redpanda connection details
- Use `dapr logs -k` to view Dapr sidecar logs
- Use `kubectl describe pod <pod-name>` to troubleshoot pod issues