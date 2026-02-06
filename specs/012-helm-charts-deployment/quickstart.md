# Quickstart: Helm Charts for Phase IV Kubernetes Deployment

**Feature**: 012-helm-charts-deployment

## Prerequisites

- Kubernetes cluster (tested with Minikube)
- Helm 3+
- Docker images: `todo-frontend:latest` and `todo-backend:latest` available in cluster
- kubectl configured to access the cluster

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to the charts directory
```bash
cd charts/todo-app
```

### 3. Install the chart with default values
```bash
helm install todo-app .
```

### 4. Install the chart with custom values
```bash
# Create a custom values file
cat << EOF > custom-values.yaml
frontend:
  replicaCount: 1
  service:
    port: 3000

backend:
  replicaCount: 1
  service:
    port: 8000

env:
  GEMINI_API_KEY: "your-gemini-api-key"
  DATABASE_URL: "your-database-url"
  BETTER_AUTH_SECRET: "your-auth-secret"
EOF

# Install with custom values
helm install todo-app . -f custom-values.yaml
```

## Verification

### Check the status of the release
```bash
helm status todo-app
```

### List the deployed resources
```bash
kubectl get pods,services,deployments
```

### Access the application
```bash
# Port forward to access the frontend
kubectl port-forward svc/todo-app-frontend 3000:3000

# Port forward to access the backend
kubectl port-forward svc/todo-app-backend 8000:8000
```

## Upgrading the Chart

### Update the chart with new values
```bash
helm upgrade todo-app . -f custom-values.yaml
```

### Upgrade to a new version of the chart
```bash
helm upgrade todo-app . --set frontend.image.tag=new-version --set backend.image.tag=new-version
```

## Uninstalling

### Uninstall the release
```bash
helm uninstall todo-app
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure the Docker images `todo-frontend:latest` and `todo-backend:latest` are available in your cluster. You may need to build and load them:
   ```bash
   minikube load image todo-frontend:latest
   minikube load image todo-backend:latest
   ```

2. **Environment variables not set**: If the application fails to start, check that required environment variables are set in your values file.

3. **Service ports not accessible**: Verify that the service ports match what the application expects.

### Useful Commands

- Check pod logs: `kubectl logs -l app.kubernetes.io/name=todo-app`
- Get detailed status: `helm status todo-app -o yaml`
- Dry run installation: `helm install todo-app . --dry-run --debug`
- Validate chart: `helm lint .`