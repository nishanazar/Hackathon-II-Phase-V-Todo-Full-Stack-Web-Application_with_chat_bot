# Todo App Helm Chart

This Helm chart deploys the Todo application, which consists of a frontend (Next.js) and backend (FastAPI) service.

## Prerequisites

- Kubernetes 1.25+
- Helm 3+

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
helm install my-release .
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.enabled` | Enable frontend deployment | `true` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `IfNotPresent` |
| `frontend.service.type` | Frontend service type | `ClusterIP` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.replicaCount` | Number of frontend replicas | `1` |

### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.enabled` | Enable backend deployment | `true` |
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.image.pullPolicy` | Backend image pull policy | `IfNotPresent` |
| `backend.service.type` | Backend service type | `ClusterIP` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.replicaCount` | Number of backend replicas | `1` |

### Environment Variables

| Parameter | Description | Default |
|-----------|-------------|---------|
| `env.GEMINI_API_KEY` | Gemini API key | `""` |
| `env.DATABASE_URL` | Database connection URL | `""` |
| `env.BETTER_AUTH_SECRET` | Authentication secret | `""` |

## Customizing the Installation

You can customize the installation by creating a `values.yaml` file and overriding the default values:

```yaml
frontend:
  replicaCount: 2
  service:
    port: 3000

backend:
  replicaCount: 2
  service:
    port: 8000

env:
  GEMINI_API_KEY: "your-gemini-api-key"
  DATABASE_URL: "your-database-url"
  BETTER_AUTH_SECRET: "your-auth-secret"
```

Then install using:

```bash
helm install my-release . -f values.yaml
```

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm delete my-release
```