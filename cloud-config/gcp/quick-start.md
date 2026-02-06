# Quick Start: Deploy to Google Cloud Platform

This guide will walk you through deploying your Todo application to Google Kubernetes Engine (GKE) in just a few steps.

## Prerequisites

1. **Google Cloud Account**: Sign up at https://console.cloud.google.com/
2. **Google Cloud SDK**: Install from https://cloud.google.com/sdk/docs/install
3. **Dapr CLI**: Install from https://docs.dapr.io/getting-started/install-dapr-cli/
4. **Helm 3.x**: Install from https://helm.sh/docs/intro/install/
5. **Docker**: Install from https://docs.docker.com/get-docker/

## Step-by-Step Deployment

### 1. Clone and Navigate to Your Project

```bash
git clone <your-repo-url>
cd hackthon_2_complete_step/phase_5
```

### 2. Authenticate with Google Cloud

```bash
gcloud auth login
gcloud config set project <your-project-id>
```

### 3. Enable Required Services

```bash
gcloud services enable container.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 4. Create GKE Cluster

```bash
gcloud container clusters create todo-app-cluster \
    --zone=us-central1 \
    --num-nodes=3 \
    --machine-type=e2-medium \
    --disk-size=100GB \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=5
```

### 5. Get Cluster Credentials

```bash
gcloud container clusters get-credentials todo-app-cluster --zone=us-central1
```

### 6. Install Dapr on Your Cluster

```bash
dapr init -k
dapr status -k
```

### 7. Build and Push Docker Images

```bash
gcloud builds submit --tag gcr.io/<your-project-id>/todo-frontend ./frontend
gcloud builds submit --tag gcr.io/<your-project-id>/todo-backend ./backend
```

### 8. Update Helm Values

Update the `charts/todo-app/values.yaml` file to use your GCP images:

```yaml
frontend:
  image:
    repository: gcr.io/<your-project-id>/todo-frontend
    tag: "latest"

backend:
  image:
    repository: gcr.io/<your-project-id>/todo-backend
    tag: "latest"
```

### 9. Deploy Using Helm

```bash
helm upgrade --install todo-app ./charts/todo-app --namespace default --create-namespace
```

### 10. Verify Deployment

```bash
kubectl get pods
kubectl get services
dapr status -k
```

## Access Your Application

To access your deployed application:

```bash
kubectl port-forward svc/todo-frontend 3000:3000
```

Then visit http://localhost:3000 in your browser.

## Clean Up (Optional)

To avoid charges when you're done testing:

```bash
gcloud container clusters delete todo-app-cluster --zone=us-central1
```

## Troubleshooting

- If you encounter permission errors, make sure your Google Cloud account has the necessary roles assigned
- If pods are not starting, check their status with `kubectl describe pod <pod-name>`
- For Dapr-related issues, use `dapr logs -k` to view Dapr logs
- Verify your Docker images were pushed correctly with `gcloud container images list`

## Next Steps

1. Set up a CI/CD pipeline using GitHub Actions
2. Configure custom domain and SSL certificate
3. Set up monitoring and logging
4. Configure horizontal pod autoscaling based on metrics