# Data Model: Minikube Setup & Helm Deployment for Phase IV

**Feature**: 013-minikube-helm-deployment

## Kubernetes Resources

### Minikube Cluster Configuration
- **Driver**: Docker (selected for best compatibility and performance)
- **CPUs**: 2 (minimum recommended for running both frontend and backend)
- **Memory**: 4096MB (4GB, sufficient for both services and Kubernetes overhead)
- **Disk Size**: 20GB (adequate for container images and persistent data)
- **Network**: Default Docker bridge network

### Namespace
- **Name**: default (can be overridden if needed)
- **Purpose**: Contains all deployed resources for the Todo Chatbot application

### Helm Release
- **Name**: todo-chatbot (identifies the deployed application)
- **Chart**: charts/todo-app (path to the Helm chart)
- **Version**: Latest (uses the most recent chart version)
- **Values**: Custom values file for Minikube-specific configuration

### Frontend Deployment
- **Name**: todo-chatbot-frontend
- **Replicas**: 1 (appropriate for local development)
- **Container Image**: todo-frontend:latest
- **Ports**: 
  - ContainerPort: 3000
  - Protocol: TCP
- **Environment Variables**:
  - NEXT_PUBLIC_API_BASE_URL: http://todo-chatbot-backend:8000
  - GEMINI_API_KEY: (from values)
  - DATABASE_URL: (from values)
  - BETTER_AUTH_SECRET: (from values)

### Backend Deployment
- **Name**: todo-chatbot-backend
- **Replicas**: 1 (appropriate for local development)
- **Container Image**: todo-backend:latest
- **Ports**:
  - ContainerPort: 8000
  - Protocol: TCP
- **Environment Variables**:
  - GEMINI_API_KEY: (from values)
  - DATABASE_URL: (from values)
  - BETTER_AUTH_SECRET: (from values)

### Frontend Service
- **Name**: todo-chatbot-frontend
- **Type**: ClusterIP (internal access within cluster)
- **Ports**:
  - Port: 3000
  - TargetPort: 3000
  - Protocol: TCP
  - Name: http

### Backend Service
- **Name**: todo-chatbot-backend
- **Type**: ClusterIP (internal access within cluster)
- **Ports**:
  - Port: 8000
  - TargetPort: 8000
  - Protocol: TCP
  - Name: http

## Configuration Values

### Image Configuration
- **frontend.image.repository**: todo-frontend
- **frontend.image.tag**: latest
- **frontend.image.pullPolicy**: IfNotPresent (important for local development)

- **backend.image.repository**: todo-backend
- **backend.image.tag**: latest
- **backend.image.pullPolicy**: IfNotPresent (important for local development)

### Service Configuration
- **frontend.service.type**: ClusterIP
- **frontend.service.port**: 3000

- **backend.service.type**: ClusterIP
- **backend.service.port**: 8000

### Environment Variables
- **env.GEMINI_API_KEY**: (to be provided by user)
- **env.DATABASE_URL**: (to be provided by user)
- **env.BETTER_AUTH_SECRET**: (to be provided by user)

## Deployment Process

### Pre-deployment Steps
1. Start Minikube cluster with Docker driver
2. Load Docker images into Minikube (if not using remote registry)
3. Verify kubectl is configured to communicate with Minikube

### Deployment Steps
1. Add Helm repository (if using remote chart) or use local chart
2. Install Helm release with custom values
3. Wait for deployments to become ready
4. Verify services are created and accessible

### Post-deployment Steps
1. Test frontend and backend connectivity
2. Verify application functionality
3. Document access methods for users