# Deployment Contract: Minikube Setup & Helm Deployment

**Feature**: 013-minikube-helm-deployment
**Version**: 1.0

## Overview

This contract defines the expected behavior and configuration of the Todo Chatbot application when deployed on a Minikube cluster using Helm charts. It specifies the required resources, configurations, and operational characteristics.

## Prerequisites

### System Requirements
- Docker daemon running
- kubectl installed (v1.20+)
- Helm 3+ installed
- Minikube installed (v1.20+)

### Resource Requirements
- Minimum 4GB RAM allocated to Minikube
- Minimum 2 CPU cores allocated to Minikube
- Sufficient disk space for Docker images and Kubernetes components

## Expected Resources

When deployed, the Helm chart will create the following Kubernetes resources:

### Deployments
- `todo-chatbot-frontend`: Frontend application deployment
- `todo-chatbot-backend`: Backend application deployment

### Services
- `todo-chatbot-frontend`: Frontend service exposing port 3000
- `todo-chatbot-backend`: Backend service exposing port 8000

### Configuration
- Environment variables configured via Helm values
- Proper resource requests and limits (if specified in values)

## Configuration Parameters

### Required Parameters
- `env.GEMINI_API_KEY`: Gemini API key for AI functionality
- `env.DATABASE_URL`: Database connection URL
- `env.BETTER_AUTH_SECRET`: Authentication secret

### Optional Parameters
- `frontend.replicaCount`: Number of frontend replicas (default: 1)
- `backend.replicaCount`: Number of backend replicas (default: 1)
- `frontend.service.port`: Frontend service port (default: 3000)
- `backend.service.port`: Backend service port (default: 8000)

## Expected Behavior

### Installation
1. The Helm chart installs without errors
2. Both frontend and backend deployments reach the desired replica count
3. Services are created and assigned ClusterIP addresses
4. Pods become Ready after initial startup

### Runtime Behavior
1. Frontend application is accessible via the frontend service
2. Backend application is accessible via the backend service
3. Frontend can communicate with backend using internal service DNS
4. Environment variables are properly injected into containers

### Health Checks
1. Liveness and readiness probes pass after initial startup
2. Applications log to standard output for Kubernetes log collection
3. Applications handle graceful shutdown on SIGTERM

## Validation Rules

- Minikube cluster must be running before installation
- Required environment variables must be provided
- Docker images (todo-frontend:latest, todo-backend:latest) must be available
- At least one operation must be performed using kubectl-ai or kagent

## Success Criteria

### Installation Criteria
- [ ] Helm install command completes successfully
- [ ] Both deployments show READY status (e.g., 1/1)
- [ ] Both services are created and assigned ClusterIP
- [ ] All pods are in Running state

### Operational Criteria
- [ ] Frontend service is accessible on port 3000
- [ ] Backend service is accessible on port 8000
- [ ] At least one kubectl-ai or kagent command is executed successfully
- [ ] Application functions as expected in the Kubernetes environment

## Example Usage

### Basic Installation
```bash
helm install todo-chatbot charts/todo-app \\
  --set env.GEMINI_API_KEY="your-key" \\
  --set env.DATABASE_URL="your-db-url" \\
  --set env.BETTER_AUTH_SECRET="your-secret"
```

### Verification Commands
```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check deployment status
helm status todo-chatbot

# Verify kubectl-ai usage
kubectl ai get "pod with label app.kubernetes.io/instance=todo-chatbot"
```

### Access Methods
```bash
# Port forward for local access
kubectl port-forward svc/todo-chatbot-frontend 3000:3000
kubectl port-forward svc/todo-chatbot-backend 8000:8000

# Or get minikube service URLs
minikube service todo-chatbot-frontend --url
minikube service todo-chatbot-backend --url
```