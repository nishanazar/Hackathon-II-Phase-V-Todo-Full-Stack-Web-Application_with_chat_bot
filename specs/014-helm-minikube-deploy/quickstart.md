# Quickstart Guide: Helm Chart Deployment on Minikube for Phase IV

## Prerequisites

- Minikube installed and running
- Helm installed
- kubectl installed
- kubectl-ai or kagent (optional, for AI-enhanced commands)

## Setup

1. Ensure Minikube is running:
   ```bash
   minikube status
   ```
   
2. If not running, start Minikube:
   ```bash
   minikube start
   ```

## Deployment Steps

1. Navigate to the project root directory where the helm chart is located

2. Install the Helm chart using the specified command:
   ```bash
   helm install todo ./helm/todo-chart
   ```

3. Verify the pods are running:
   ```bash
   kubectl get pods
   ```
   You should see pods for both frontend and backend in "Running" status.

4. Verify the services are created:
   ```bash
   kubectl get svc
   ```
   You should see services named todo-frontend and todo-backend.

5. Access the frontend application:
   ```bash
   minikube service todo-frontend --url
   ```
   This will provide the URL to access the frontend application.

## Using AI-Enhanced Kubernetes Tools

As required by the specification, use kubectl-ai or kagent for at least one deployment command. For example:

```bash
kubectl-ai "describe the status of all pods in the default namespace"
```

Or:

```bash
kagent "show me the services created by the todo release"
```

## Verification

1. Confirm all pods are running:
   ```bash
   kubectl get pods -l app=todo-frontend
   kubectl get pods -l app=todo-backend
   ```

2. Confirm services are accessible:
   ```bash
   kubectl get svc todo-frontend
   kubectl get svc todo-backend
   ```

3. Access the application via the URL provided by:
   ```bash
   minikube service todo-frontend --url
   ```

## Troubleshooting

- If pods are not starting, check the logs:
  ```bash
  kubectl logs -l app=todo-frontend
  kubectl logs -l app=todo-backend
  ```

- If services are not accessible, verify they were created correctly:
  ```bash
  kubectl describe svc todo-frontend
  kubectl describe svc todo-backend
  ```

- If Helm installation fails, check the chart:
  ```bash
  helm lint ./helm/todo-chart
  ```