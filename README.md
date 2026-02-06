# Dapr & Kafka Setup on Cloud Cluster for Phase V

## Overview

This document outlines the setup for Dapr and Kafka/Redpanda Pub/Sub on the cloud Kubernetes cluster (Google GKE or Oracle OKE) to enable event-driven architecture for microservices communication.

## Prerequisites

- Google Cloud account with billing enabled
- Google Cloud SDK installed locally
- Dapr CLI installed locally
- kubectl configured to connect to the cloud cluster
- Helm 3.x installed locally
- Access to Redpanda Cloud account (or Kafka cluster details)
- Docker installed locally

## Setup Instructions

### 1. Google Cloud Setup

Before deploying to GKE, you need to set up your Google Cloud environment:

```bash
# Install Google Cloud SDK (if not already installed)
# Download from: https://cloud.google.com/sdk/docs/install

# Authenticate with Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required services
gcloud services enable container.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Verify Cloud Cluster Connection

```bash
kubectl cluster-info
kubectl get nodes
```

### 2. Install Dapr on the Cloud Cluster

```bash
# Initialize Dapr on the Kubernetes cluster
dapr init -k

# Verify Dapr control plane is running
dapr status -k
```

### 3. Configure Kafka/Redpanda Connection

If using Redpanda Cloud:
1. Log into your Redpanda Cloud Console
2. Get the connection details (brokers, SASL credentials)
3. Update the `dapr/components/pubsub.yaml` file with the correct connection details

If using self-hosted Kafka with Strimzi:
1. Deploy Kafka cluster using Strimzi operators
2. Get the service endpoint details

### 4. Apply Dapr Components

```bash
# Apply the pub/sub component
kubectl apply -f dapr/components/pubsub.yaml

# Apply the configuration
kubectl apply -f dapr/config/config.yaml
```

### 5. Deploy Application with Dapr Sidecars

For Google Cloud deployment, you can use the provided deployment script:

```bash
# Make the script executable
chmod +x deploy_to_gcp.sh

# Run the deployment script (update the PROJECT_ID variable inside the script first)
./deploy_to_gcp.sh
```

Alternatively, you can manually deploy using Helm after setting up your GKE cluster:

```bash
# Install or upgrade the application using Helm
helm upgrade --install todo-app charts/todo-app --namespace default --create-namespace
```

### 6. Verify Setup

```bash
# Verify Dapr system components
kubectl get pods -n dapr-system

# Verify application pods with Dapr sidecars
kubectl get pods

# Check for 2 containers in each application pod (your app + daprd)
kubectl describe pod <pod-name>
```

## Testing

### 1. Test Event Publishing

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

### 2. Run Backend Integration Test

```bash
# Navigate to the backend directory
cd backend

# Run the Dapr pub/sub test
python test_dapr_pubsub.py
```

## Architecture

- **Dapr Control Plane**: Manages service discovery, configuration, and distributed tracing
- **Kafka/Redpanda Cluster**: Messaging system for pub/sub event communication between services
- **Application Pods**: Containerized services with Dapr sidecars injected
- **Task Events**: Domain-specific events related to task management that will be published and consumed

## Troubleshooting

- If Dapr isn't initializing, check cluster RBAC permissions
- If events aren't publishing, verify Kafka/Redpanda connection details
- Use `dapr logs -k` to view Dapr sidecar logs
- Use `kubectl describe pod <pod-name>` to troubleshoot pod issues
- Check consumer service logs to verify events are being received

## Current Environment

- kubectl: Installed (v1.34.1)
- Helm: Installed (v4.1.0)
- OCI CLI: Not installed (needs manual installation on Windows)

## CI/CD Pipeline

This project includes a CI/CD pipeline using GitHub Actions that automatically builds, pushes, and deploys the application to the cloud Kubernetes cluster.

![Deploy to Google Kubernetes Engine](https://github.com/user/repo/actions/workflows/deploy-gke.yaml/badge.svg)

### Usage

The pipeline is automatically triggered when:
- Code is pushed to the `main` branch (production deployment)
- A pull request is opened or updated (testing deployment)

To manually trigger the pipeline:
1. Go to the "Actions" tab in your GitHub repository
2. Select the "Deploy to Google Kubernetes Engine" workflow
3. Click "Run workflow" and select the branch

### Required Secrets for GCP

To use the CI/CD pipeline with Google Cloud, you need to configure the following secrets in your GitHub repository:

1. **GCP_CREDENTIALS**: Service account key for authenticating with Google Cloud
   - Create a service account in Google Cloud Console with appropriate roles
   - Download the JSON key file
   - Navigate to Settings > Secrets and variables > Actions in your GitHub repository
   - Add a new secret named `GCP_CREDENTIALS`
   - Paste the entire content of the JSON key file

2. **GCP_PROJECT_ID**: Your Google Cloud Project ID
   - Find your Project ID in the Google Cloud Console
   - Add a new secret named `GCP_PROJECT_ID`
   - Paste your Project ID

3. **GKE_CLUSTER_NAME**: Name of your GKE cluster
   - Add a new secret named `GKE_CLUSTER_NAME`
   - Paste your cluster name (default: todo-app-cluster)

4. **GKE_ZONE**: Zone where your GKE cluster is located
   - Add a new secret named `GKE_ZONE`
   - Paste your zone (default: us-central1)

### Pipeline Workflow

The pipeline is defined in `.github/workflows/deploy.yaml` and performs the following steps:
1. Checks out the code
2. Builds Docker images for frontend and backend
3. Pushes images to GitHub Container Registry
4. Deploys the application to the Kubernetes cluster using Helm
5. Verifies the deployment by checking pod status
6. Sends notifications on success or failure

### Notification Setup

The pipeline includes notification functionality that sends alerts on deployment success or failure. To enable notifications:

1. **SLACK_WEBHOOK**: Add your Slack webhook URL as a GitHub secret named `SLACK_WEBHOOK`
   - Navigate to Settings > Secrets and variables > Actions in your GitHub repository
   - Add a new secret named `SLACK_WEBHOOK`
   - Paste your Slack webhook URL

Alternatively, you can customize the notification steps to use other services like Discord, Microsoft Teams, or email.

## Troubleshooting

If you encounter issues with the CI/CD pipeline, please refer to the [Troubleshooting Guide](TROUBLESHOOTING.md) for solutions to common problems.

## Next Steps

1. For Google Cloud deployment:
   - Create a Google Cloud account at https://console.cloud.google.com/
   - Install Google Cloud SDK from https://cloud.google.com/sdk/docs/install
   - Follow the quick start guide in `cloud-config/gcp/quick-start.md`
   - Set up a service account as described in `cloud-config/gcp/service-account-setup.md`

2. For Oracle OKE deployment:
   - Install OCI CLI manually by downloading from Oracle's website
   - Continue with cloud account setup and cluster creation

3. Follow the setup instructions above to configure Dapr and Kafka/Redpanda
4. Set up the required GitHub secrets for the CI/CD pipeline