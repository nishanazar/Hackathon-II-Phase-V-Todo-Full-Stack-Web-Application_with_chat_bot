# Helm Chart Contract: todo-app

**Feature**: 012-helm-charts-deployment
**Version**: 1.0

## Overview

This contract defines the structure, parameters, and behavior of the `todo-app` Helm chart. This chart deploys the frontend and backend components of the todo application to a Kubernetes cluster.

## Chart Metadata

- **Name**: todo-app
- **Version**: 0.1.0 (Chart version)
- **AppVersion**: 1.0.0 (Application version)
- **API Version**: v2
- **Type**: Application

## Configuration Parameters

### Frontend Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frontend.enabled` | Boolean | `true` | Enable frontend deployment |
| `frontend.image.repository` | String | `"todo-frontend"` | Frontend image repository |
| `frontend.image.tag` | String | `"latest"` | Frontend image tag |
| `frontend.image.pullPolicy` | String | `"IfNotPresent"` | Image pull policy |
| `frontend.service.type` | String | `"ClusterIP"` | Frontend service type |
| `frontend.service.port` | Integer | `3000` | Frontend service port |
| `frontend.resources` | Object | `{}` | Resource requests and limits |
| `frontend.replicaCount` | Integer | `1` | Number of frontend replicas |

### Backend Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend.enabled` | Boolean | `true` | Enable backend deployment |
| `backend.image.repository` | String | `"todo-backend"` | Backend image repository |
| `backend.image.tag` | String | `"latest"` | Backend image tag |
| `backend.image.pullPolicy` | String | `"IfNotPresent"` | Image pull policy |
| `backend.service.type` | String | `"ClusterIP"` | Backend service type |
| `backend.service.port` | Integer | `8000` | Backend service port |
| `backend.resources` | Object | `{}` | Resource requests and limits |
| `backend.replicaCount` | Integer | `1` | Number of backend replicas |

### Environment Variables

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `env.GEMINI_API_KEY` | String | Yes | Gemini API key |
| `env.DATABASE_URL` | String | Yes | Database connection URL |
| `env.BETTER_AUTH_SECRET` | String | Yes | Authentication secret |

## Expected Resources

When deployed, the chart will create the following Kubernetes resources:

### Deployments
- `{{ include "todo-app.fullname" . }}-frontend`: Frontend application deployment
- `{{ include "todo-app.fullname" . }}-backend`: Backend application deployment

### Services
- `{{ include "todo-app.fullname" . }}-frontend`: Frontend service exposing port 3000
- `{{ include "todo-app.fullname" . }}-backend`: Backend service exposing port 8000

## Expected Behavior

### Installation
1. The chart validates all required parameters are provided
2. Creates frontend and backend deployments with specified replica counts
3. Creates corresponding services to expose the deployments
4. Configures environment variables in the pods based on the `env` values

### Upgrades
1. Preserves existing data and configurations
2. Updates deployments with new image versions if specified
3. Adjusts replica counts if changed in values
4. Updates environment variables if changed in values

### Uninstallation
1. Removes all created resources (deployments, services)
2. Does not remove any persistent data (if any exists)

## Validation Rules

- At least one of `frontend.enabled` or `backend.enabled` must be true
- `frontend.service.port` must be a valid port number (1-65535)
- `backend.service.port` must be a valid port number (1-65535)
- `env.GEMINI_API_KEY`, `env.DATABASE_URL`, and `env.BETTER_AUTH_SECRET` must be provided

## Example Usage

### Basic Installation
```bash
helm install todo-app-release .
```

### Installation with Custom Values
```bash
helm install todo-app-release . \
  --set frontend.replicaCount=2 \
  --set backend.replicaCount=2 \
  --set env.GEMINI_API_KEY="your-key" \
  --set env.DATABASE_URL="your-db-url" \
  --set env.BETTER_AUTH_SECRET="your-secret"
```

### Installation from Values File
```bash
helm install todo-app-release . -f values.yaml
```