# Quickstart: Minikube Setup & Helm Deployment for Phase IV

**Feature**: 013-minikube-helm-deployment

## Prerequisites

- Docker installed and running
- kubectl installed
- Helm 3+ installed
- Minikube installed

## Installation

### 1. Start Minikube Cluster

```bash
# Start Minikube with Docker driver and appropriate resources
minikube start --driver=docker --cpus=2 --memory=4096mb

# Verify kubectl is configured to talk to Minikube
kubectl config current-context
# Should show minikube as the current context
```

### 2. Load Docker Images (if using local images)

```bash
# If you have local images, load them into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 3. Deploy the Application

```bash
# Navigate to the charts directory
cd charts/todo-app

# Install the Helm chart with a release name
helm install todo-chatbot . \\
  --set env.GEMINI_API_KEY="your-gemini-api-key" \\
  --set env.DATABASE_URL="your-database-url" \\
  --set env.BETTER_AUTH_SECRET="your-auth-secret"
```

### 4. Verify the Deployment

```bash
# Check that pods are running
kubectl get pods

# Check that services are created
kubectl get services

# Check the status of the Helm release
helm status todo-chatbot
```

## Accessing the Application

### Option 1: Using Port Forwarding

```bash
# Forward frontend port
kubectl port-forward svc/todo-chatbot-frontend 3000:3000

# In another terminal, forward backend port
kubectl port-forward svc/todo-chatbot-backend 8000:8000
```

### Option 2: Using Minikube Service

```bash
# Get the URL for the frontend service
minikube service todo-chatbot-frontend --url

# Get the URL for the backend service
minikube service todo-chatbot-backend --url
```

## Using kubectl-ai/kagent

As required by the specification, at least one operation should be performed using kubectl-ai or kagent:

```bash
# Example of using kubectl-ai to get deployment information
kubectl ai describe "deployment todo-chatbot-frontend"

# Or to scale the deployment
kubectl ai patch deployment todo-chatbot-frontend -p '{"spec":{"replicas":2}}'
```

## Troubleshooting

### Common Issues

1. **Images not found**: If getting ImagePullBackOff errors, ensure images are loaded into Minikube:
   ```bash
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   ```

2. **Insufficient resources**: If pods are stuck in Pending state, ensure Minikube has enough resources:
   ```bash
   minikube delete
   minikube start --driver=docker --cpus=2 --memory=4096mb
   ```

3. **Service not accessible**: If services aren't accessible, verify they were created correctly:
   ```bash
   kubectl get services
   minikube service list
   ```

### Useful Commands

- Check pod logs: `kubectl logs -l app.kubernetes.io/instance=todo-chatbot`
- Get detailed status: `helm status todo-chatbot -o yaml`
- List Helm releases: `helm list`
- Uninstall the release: `helm uninstall todo-chatbot`