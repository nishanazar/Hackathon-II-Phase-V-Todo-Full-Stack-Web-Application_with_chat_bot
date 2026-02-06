# Quickstart Guide: AI-Assisted Kubernetes Operations with kubectl-ai & Kagent

## Prerequisites

- Running Minikube cluster with Helm-deployed application
- kubectl configured to connect to the cluster
- kubectl-ai and Kagent installed (see installation steps below)

## Installation

1. Install kubectl-ai:
   ```bash
   # Follow official installation instructions for your OS
   # For example, on Linux/macOS:
   curl -sL https://aka.ms/kubectl-ai/install.sh | bash
   ```

2. Install Kagent:
   ```bash
   # Follow official installation instructions for your OS
   # For example, on Linux/macOS:
   curl -sL https://aka.ms/kagent/install.sh | bash
   ```

## AI-Assisted Operations

### 1. Scaling Operations with kubectl-ai

Scale the frontend deployment to 2 replicas:
```bash
kubectl ai "scale deployment todo-frontend to 2 replicas"
```

Scale the backend deployment to 3 replicas:
```bash
kubectl ai "scale deployment todo-backend to 3 replicas"
```

### 2. Cluster Analysis with Kagent

Analyze cluster health:
```bash
kagent "analyze cluster health"
```

Check for pod failures:
```bash
kagent "check for pod failures in the default namespace"
```

### 3. Verification

Verify scaling operations:
```bash
kubectl get deployments
```

Verify all pods are running:
```bash
kubectl get pods
```

Check application accessibility:
```bash
minikube service todo-frontend --url
```

## Logging Operations

To document AI-assisted operations, you can redirect output to log files:
```bash
kubectl ai "scale deployment todo-frontend to 2 replicas" | tee -a ai_operations.log
kagent "analyze cluster health" | tee -a ai_operations.log
```

## Troubleshooting

- If kubectl-ai or Kagent commands fail, verify they are properly installed:
  ```bash
  kubectl ai version
  kagent version
  ```

- If scaling operations don't complete, check resource availability:
  ```bash
  kubectl top nodes
  kubectl describe nodes
  ```

- If the application becomes inaccessible after operations, check service endpoints:
  ```bash
  kubectl get svc
  kubectl describe svc todo-frontend
  ```