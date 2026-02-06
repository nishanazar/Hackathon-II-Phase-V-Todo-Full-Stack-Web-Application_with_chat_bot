# Data Model: Helm Charts for Phase IV Kubernetes Deployment

**Feature**: 012-helm-charts-deployment

## Helm Chart Structure

### Chart Metadata (Chart.yaml)

- **name**: todo-app
- **version**: 0.1.0
- **apiVersion**: v2
- **description**: A Helm chart for deploying the todo application
- **type**: application
- **appVersion**: "1.0.0"

### Values Configuration (values.yaml)

#### Global Configuration
- **global.imageRegistry**: String (optional) - Global Docker registry
- **global.imagePullSecrets**: Array - Global image pull secrets
- **global.storageClass**: String (optional) - Global storage class

#### Frontend Configuration
- **frontend.enabled**: Boolean - Enable frontend deployment
- **frontend.image.repository**: String - Frontend image repository (default: "todo-frontend")
- **frontend.image.tag**: String - Frontend image tag (default: "latest")
- **frontend.image.pullPolicy**: String - Image pull policy (default: "IfNotPresent")
- **frontend.service.type**: String - Service type (default: "ClusterIP")
- **frontend.service.port**: Integer - Service port (default: 3000)
- **frontend.resources**: Object - Resource requests/limits
- **frontend.replicaCount**: Integer - Number of replicas (default: 1)

#### Backend Configuration
- **backend.enabled**: Boolean - Enable backend deployment
- **backend.image.repository**: String - Backend image repository (default: "todo-backend")
- **backend.image.tag**: String - Backend image tag (default: "latest")
- **backend.image.pullPolicy**: String - Image pull policy (default: "IfNotPresent")
- **backend.service.type**: String - Service type (default: "ClusterIP")
- **backend.service.port**: Integer - Service port (default: 8000)
- **backend.resources**: Object - Resource requests/limits
- **backend.replicaCount**: Integer - Number of replicas (default: 1)

#### Environment Variables
- **env.GEMINI_API_KEY**: String - Gemini API key
- **env.DATABASE_URL**: String - Database connection URL
- **env.BETTER_AUTH_SECRET**: String - Authentication secret

## Kubernetes Resources

### Frontend Deployment
- **kind**: Deployment
- **apiVersion**: apps/v1
- **metadata.name**: {{ include "todo-app.fullname" . }}-frontend
- **metadata.labels**: Standard Helm labels
- **spec.replicas**: Value from `frontend.replicaCount`
- **spec.selector.matchLabels**: Matching labels
- **spec.template.metadata.labels**: Pod labels
- **spec.template.spec.containers[]**:
  - **name**: frontend
  - **image**: Value from `frontend.image.repository:tag`
  - **ports[]**:
    - **containerPort**: 3000
    - **name**: http
  - **env[]**: Environment variables from values
  - **resources**: From `frontend.resources`
  - **livenessProbe**: HTTP probe on /health
  - **readinessProbe**: HTTP probe on /health

### Backend Deployment
- **kind**: Deployment
- **apiVersion**: apps/v1
- **metadata.name**: {{ include "todo-app.fullname" . }}-backend
- **metadata.labels**: Standard Helm labels
- **spec.replicas**: Value from `backend.replicaCount`
- **spec.selector.matchLabels**: Matching labels
- **spec.template.metadata.labels**: Pod labels
- **spec.template.spec.containers[]**:
  - **name**: backend
  - **image**: Value from `backend.image.repository:tag`
  - **ports[]**:
    - **containerPort**: 8000
    - **name**: http
  - **env[]**: Environment variables from values
  - **resources**: From `backend.resources`
  - **livenessProbe**: HTTP probe on /health
  - **readinessProbe**: HTTP probe on /health

### Frontend Service
- **kind**: Service
- **apiVersion**: v1
- **metadata.name**: {{ include "todo-app.fullname" . }}-frontend
- **metadata.labels**: Standard Helm labels
- **spec.type**: Value from `frontend.service.type`
- **spec.ports[]**:
  - **port**: Value from `frontend.service.port`
  - **targetPort**: 3000
  - **protocol**: TCP
  - **name**: http
- **spec.selector**: Matching pod labels

### Backend Service
- **kind**: Service
- **apiVersion**: v1
- **metadata.name**: {{ include "todo-app.fullname" . }}-backend
- **metadata.labels**: Standard Helm labels
- **spec.type**: Value from `backend.service.type`
- **spec.ports[]**:
  - **port**: Value from `backend.service.port`
  - **targetPort**: 8000
  - **protocol**: TCP
  - **name**: http
- **spec.selector**: Matching pod labels

## Template Files

### _helpers.tpl
- **todo-app.name**: Template for chart name
- **todo-app.fullname**: Template for release name + chart name
- **todo-app.chart**: Template for chart name + version
- **todo-app.labels**: Standard labels for resources
- **todo-app.matchLabels**: Selector labels for resources

### NOTES.txt
- Instructions for accessing the deployed application
- Information about required environment variables
- Commands for port forwarding if needed