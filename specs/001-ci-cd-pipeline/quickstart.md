# Quickstart Guide: CI/CD Pipeline Setup with GitHub Actions

## Overview
This guide explains how to set up and use the CI/CD pipeline for the Todo AI Chatbot application. The pipeline automates the build, push, and deployment process to a cloud Kubernetes cluster.

## Prerequisites
- GitHub repository with the Todo AI Chatbot code
- Access to a cloud Kubernetes cluster (OKE/AKS/GKE)
- Helm charts for the application
- Dockerfiles for frontend and backend services

## Setting Up Secrets in GitHub

Before the pipeline can work, you need to configure the following secrets in your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to Settings > Secrets and variables > Actions
3. Add the following secrets:

- `KUBECONFIG`: The Kubernetes configuration file content for accessing your cluster
- `REGISTRY_TOKEN`: Access token for GitHub Container Registry (ghcr.io)

## GitHub Actions Workflow

The pipeline is defined in `.github/workflows/deploy.yaml` and performs the following steps:

1. **Checkout**: Gets the latest code from the repository
2. **Login to Registry**: Authenticates with GitHub Container Registry
3. **Build and Push Images**: Builds Docker images for frontend and backend and pushes them to ghcr.io
4. **Set up Helm**: Installs Helm on the runner
5. **Deploy with Helm**: Executes Helm upgrade to deploy the application to the Kubernetes cluster
6. **Verify Deployment**: Checks that all pods are running successfully
7. **Send Notifications**: Sends success/failure notifications

## Triggering the Pipeline

The pipeline is automatically triggered when:
- Code is pushed to the `main` branch (production deployment)
- A pull request is opened or updated (testing deployment)

## Manual Trigger (Optional)

You can also manually trigger the pipeline:
1. Go to the "Actions" tab in your GitHub repository
2. Select the "Deploy to Kubernetes" workflow
3. Click "Run workflow" and select the branch

## Verifying Deployment

After the pipeline runs, you can verify the deployment by:
1. Checking the pipeline logs for success status
2. Using `kubectl get pods` to verify all pods are running
3. Accessing the application via the exposed URL

## Troubleshooting

If the pipeline fails:
1. Check the GitHub Actions logs for error details
2. Verify that all secrets are correctly configured
3. Ensure the Kubernetes cluster is accessible
4. Confirm that Helm charts are valid and properly configured

## Updating the Pipeline

To modify the pipeline:
1. Edit the `.github/workflows/deploy.yaml` file
2. Commit and push changes to the repository
3. The updated pipeline will be used for the next run