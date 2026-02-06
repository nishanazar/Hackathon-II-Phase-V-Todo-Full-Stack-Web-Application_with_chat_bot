# Deploying Your Application to Google Cloud Platform

This guide will walk you through deploying your application to Google Cloud Platform using your newly created account.

## Step 1: Set Up Your Local Environment

1. Install Google Cloud SDK if you haven't already:
   - Download from: https://cloud.google.com/sdk/docs/install
   - Follow the installation instructions for your operating system

2. Authenticate with Google Cloud:
```bash
gcloud auth login
```

3. Set your project ID:
```bash
gcloud config set project YOUR_PROJECT_ID
```

## Step 2: Enable Required APIs

Enable the APIs needed for your deployment:
```bash
gcloud services enable container.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable run.googleapis.com
```

## Step 3: Create a GKE Cluster

Create a Kubernetes cluster to deploy your application:
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

## Step 4: Get Cluster Credentials

Configure kubectl to connect to your cluster:
```bash
gcloud container clusters get-credentials todo-app-cluster --zone=us-central1
```

## Step 5: Install Dapr

Install Dapr on your cluster:
```bash
dapr init -k
dapr status -k
```

## Step 6: Build and Push Docker Images

Build and push your application images to Google Container Registry:
```bash
# Build and push frontend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/todo-frontend ./frontend

# Build and push backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/todo-backend ./backend
```

## Step 7: Update Helm Values

Update the `charts/todo-app/values.yaml` file to use your GCP images:
```yaml
frontend:
  image:
    repository: gcr.io/YOUR_PROJECT_ID/todo-frontend
    tag: "latest"

backend:
  image:
    repository: gcr.io/YOUR_PROJECT_ID/todo-backend
    tag: "latest"
```

## Step 8: Deploy Using Helm

Deploy your application using the Helm chart:
```bash
helm upgrade --install todo-app ./charts/todo-app --namespace default --create-namespace
```

## Step 9: Verify Your Deployment

Check that your application is running:
```bash
kubectl get pods
kubectl get services
dapr status -k
```

## Step 10: Access Your Application

To access your deployed application, you'll need to expose it:
```bash
kubectl port-forward svc/todo-frontend 3000:3000
```

Then visit http://localhost:3000 in your browser.

## Setting Up CI/CD Pipeline

To automate deployments, set up the GitHub Actions workflow:

1. In your GitHub repository, navigate to Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `GCP_CREDENTIALS`: Your service account key
   - `GCP_PROJECT_ID`: Your Google Cloud Project ID
   - `GKE_CLUSTER_NAME`: Your cluster name (todo-app-cluster)
   - `GKE_ZONE`: Your zone (us-central1)

## Monitoring Costs

Keep an eye on your usage to stay within your free credits:
- Visit the Google Cloud Console Billing page regularly
- Set up billing alerts to notify you when you reach certain thresholds
- Remember to delete resources when not in use to minimize costs

## Troubleshooting

- If you encounter permission errors, ensure your account has the necessary roles assigned
- If pods are not starting, check their status with `kubectl describe pod <pod-name>`
- For Dapr-related issues, use `dapr logs -k` to view Dapr logs
- Verify your Docker images were pushed correctly with `gcloud container images list`

## Cleaning Up

To avoid unnecessary charges when you're done testing:
```bash
gcloud container clusters delete todo-app-cluster --zone=us-central1
```

This will remove the cluster and all associated resources.